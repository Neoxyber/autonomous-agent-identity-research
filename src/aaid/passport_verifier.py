"""Structural-only local verifier for the agent passport envelope.

This module provides a single entry point, :func:`verify_passport_envelope`,
that checks the structural shape of an envelope-like object and records the
outcome in a :class:`~aaid.verification.VerificationResult`.

After the structural checks pass, the envelope is validated against the
committed JSON Schema and the outcome is recorded as a ``schema_valid`` check.
When schema validation passes, the verifier selects the proof to check and
records the choice as a ``proof_selected`` check; the first-version rule selects
the first proof only. It then recomputes the canonical payload hash over the
passport and compares it to the selected proof's recorded hash, recording the
outcome as a ``payload_hash_valid`` check. This step verifies
the payload hash only: it does not verify signatures or proofs, does not check
revocation or issuer trust, and does not evaluate policy. After the payload hash
matches, the verifier selects the public key referenced by the proof and
validates basic, non-cryptographic key metadata, recording the outcome as a
``verification_key_selected`` check; finding no single suitable key fails closed
to ``DENY`` before the signature step. Because signature
verification does not exist yet, a structurally valid, schema valid envelope
with a matching payload hash still fails closed to ``DENY``; this verifier can
never return ``ALLOW``. Each check is recorded as a named, immutable check so
the decision can be explained and audited.
"""

import json
from collections.abc import Mapping, Sequence
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import best_match

from aaid import canonicalization
from aaid.verification import VerificationCheck, VerificationResult

_SCHEMA_PATH = (
    Path(__file__).resolve().parents[2] / "specs" / "agent-passport.schema.json"
)


@lru_cache(maxsize=1)
def _envelope_validator() -> Draft202012Validator:
    """Load and cache the committed envelope schema validator.

    This validates the JSON shape of the envelope only. It does not recompute
    the payload hash, verify signatures, or check proofs.
    """
    with _SCHEMA_PATH.open(encoding="utf-8") as handle:
        schema = json.load(handle)
    return Draft202012Validator(schema)


def _select_proof(proofs: Sequence) -> Mapping:
    """Select which proof the verifier will check.

    First-version rule: select only the first proof. Selection is made
    explicit here so it can be tested and later replaced before real
    signature verification exists. Structural checks and schema validation
    have already guaranteed that proofs is a non-empty sequence of proof
    objects when this runs.
    """
    return proofs[0]


def _signature_verification_not_implemented_check(
    passport: Mapping, proof: Mapping
) -> VerificationCheck:
    """Produce the signature verification check for the selected proof.

    This is the internal boundary where real signature verification will later
    run. For now it performs no cryptographic work: it does not inspect keys,
    compute hashes, or verify any signature. It accepts the passport and the
    selected proof so the boundary is ready for a later implementation, and it
    always records a failed check so the verifier fails closed. The arguments
    are intentionally unused at this step.
    """
    del passport, proof
    return VerificationCheck(
        name="signature_verification_not_implemented",
        passed=False,
        reason=(
            "structure is acceptable but signature verification is not "
            "implemented, so the envelope cannot be allowed"
        ),
    )


_ACCEPTED_KEY_PURPOSES = ("sig", "verify", "hybrid-sig")


def _select_verification_key(
    passport: Mapping, proof: Mapping
) -> "tuple[VerificationCheck, Mapping | None]":
    """Select the public key referenced by the selected proof.

    This step inspects public-key metadata only. It finds the public key in
    ``passport["public_keys"]`` whose ``kid`` matches the selected proof's
    ``kid`` and confirms basic, non-cryptographic metadata: exactly one key
    matches, the key algorithm matches the proof algorithm, the key is active,
    and the key purpose is suitable for signature verification. It performs no
    cryptographic work and does not verify signatures, issuer trust, revocation,
    or policy.

    Returns a ``(check, key)`` pair. On success the check passes and ``key`` is
    the selected public key. On any failure the check fails and ``key`` is
    ``None`` so the verifier can fail closed. Structural checks and schema
    validation have already guaranteed that ``public_keys`` is a non-empty list
    of key objects and that the proof carries a ``kid`` and ``alg`` when this
    runs.
    """
    proof_kid = proof["kid"]
    matches = [
        key for key in passport["public_keys"] if key.get("kid") == proof_kid
    ]

    if not matches:
        return (
            VerificationCheck(
                name="verification_key_selected",
                passed=False,
                reason=(
                    "no public key matches the selected proof key identifier"
                ),
            ),
            None,
        )
    if len(matches) > 1:
        return (
            VerificationCheck(
                name="verification_key_selected",
                passed=False,
                reason=(
                    "more than one public key matches the selected proof key "
                    "identifier"
                ),
            ),
            None,
        )

    key = matches[0]
    if key.get("alg") != proof["alg"]:
        return (
            VerificationCheck(
                name="verification_key_selected",
                passed=False,
                reason=(
                    "selected public key algorithm does not match the proof "
                    "algorithm"
                ),
            ),
            None,
        )
    if key.get("status") != "active":
        return (
            VerificationCheck(
                name="verification_key_selected",
                passed=False,
                reason="selected public key is not active",
            ),
            None,
        )
    if key.get("purpose") not in _ACCEPTED_KEY_PURPOSES:
        return (
            VerificationCheck(
                name="verification_key_selected",
                passed=False,
                reason=(
                    "selected public key purpose is not suitable for signature "
                    "verification"
                ),
            ),
            None,
        )

    return (
        VerificationCheck(
            name="verification_key_selected",
            passed=True,
            reason=(
                "selected the public key referenced by the proof; key metadata "
                "is acceptable for signature verification"
            ),
        ),
        key,
    )


def verify_passport_envelope(envelope: object) -> VerificationResult:
    """Check the structure of a passport envelope and record the outcome.

    The checks run in order and stop at the first structural problem, because
    each check depends on the previous one holding. On the first failure the
    result records the checks that passed plus the failing check and fails
    closed to ``DENY``.

    A structurally acceptable envelope (a mapping with a mapping ``passport``
    and a non-empty, non-string ``proofs`` sequence) is then validated against
    the committed JSON Schema and the outcome is recorded as ``schema_valid``.
    If schema validation fails, the result fails closed to ``DENY`` with the
    failing ``schema_valid`` check. If it passes, the verifier selects the proof
    to check and records the choice as ``proof_selected``; the first-version
    rule selects the first proof only. It then recomputes the canonical payload
    hash over ``envelope["passport"]`` using the selected proof's recorded hash
    algorithm and compares it to that proof's ``payload_hash``; the outcome is
    recorded as ``payload_hash_valid``. The hash algorithm is taken from the
    schema-validated proof, so it is always a supported algorithm. A mismatch
    fails closed to ``DENY`` with the failing ``payload_hash_valid`` check and
    stops before the signature step. When the payload hash matches, the result
    records ``payload_hash_valid`` as passed and then selects the public key
    referenced by the proof, recording ``verification_key_selected``. If no
    single public key matches the proof's ``kid`` with a matching algorithm,
    active status, and suitable purpose, the result fails closed to ``DENY``
    before the signature step. Otherwise it records
    ``signature_verification_not_implemented`` as failed. Signature
    verification is out of scope here, so even a matching payload hash still
    fails closed to ``DENY`` and never returns ``ALLOW``.
    """
    checks: list[VerificationCheck] = []

    if not isinstance(envelope, Mapping):
        checks.append(
            VerificationCheck(
                name="envelope_is_mapping",
                passed=False,
                reason="envelope is not a mapping",
            )
        )
        return VerificationResult.failed(
            "envelope is not a mapping", checks=checks
        )
    checks.append(
        VerificationCheck(
            name="envelope_is_mapping",
            passed=True,
            reason="envelope is a mapping",
        )
    )

    if "passport" not in envelope:
        checks.append(
            VerificationCheck(
                name="passport_present",
                passed=False,
                reason="envelope is missing required key 'passport'",
            )
        )
        return VerificationResult.failed(
            "envelope is missing required key 'passport'", checks=checks
        )
    checks.append(
        VerificationCheck(
            name="passport_present",
            passed=True,
            reason="envelope has a 'passport' key",
        )
    )

    passport = envelope["passport"]
    if not isinstance(passport, Mapping):
        checks.append(
            VerificationCheck(
                name="passport_is_mapping",
                passed=False,
                reason="passport is not a mapping",
            )
        )
        return VerificationResult.failed(
            "passport is not a mapping", checks=checks
        )
    checks.append(
        VerificationCheck(
            name="passport_is_mapping",
            passed=True,
            reason="passport is a mapping",
        )
    )

    if "proofs" not in envelope:
        checks.append(
            VerificationCheck(
                name="proofs_present",
                passed=False,
                reason="envelope is missing required key 'proofs'",
            )
        )
        return VerificationResult.failed(
            "envelope is missing required key 'proofs'", checks=checks
        )
    checks.append(
        VerificationCheck(
            name="proofs_present",
            passed=True,
            reason="envelope has a 'proofs' key",
        )
    )

    proofs = envelope["proofs"]
    if not isinstance(proofs, Sequence) or isinstance(
        proofs, (str, bytes, bytearray)
    ):
        checks.append(
            VerificationCheck(
                name="proofs_is_sequence",
                passed=False,
                reason="proofs is not a sequence of proofs",
            )
        )
        return VerificationResult.failed(
            "proofs is not a sequence of proofs", checks=checks
        )
    checks.append(
        VerificationCheck(
            name="proofs_is_sequence",
            passed=True,
            reason="proofs is a sequence",
        )
    )

    if len(proofs) == 0:
        checks.append(
            VerificationCheck(
                name="proofs_non_empty",
                passed=False,
                reason="proofs must contain at least one proof",
            )
        )
        return VerificationResult.failed(
            "proofs must contain at least one proof", checks=checks
        )
    checks.append(
        VerificationCheck(
            name="proofs_non_empty",
            passed=True,
            reason="proofs contains at least one proof",
        )
    )

    error = best_match(_envelope_validator().iter_errors(envelope))
    if error is not None:
        checks.append(
            VerificationCheck(
                name="schema_valid",
                passed=False,
                reason=(
                    "envelope does not match the agent passport schema at "
                    f"{error.json_path}: {error.message}"
                ),
            )
        )
        return VerificationResult.failed(
            "envelope does not match the agent passport schema", checks=checks
        )
    checks.append(
        VerificationCheck(
            name="schema_valid",
            passed=True,
            reason="envelope matches the agent passport schema",
        )
    )

    proof = _select_proof(proofs)
    checks.append(
        VerificationCheck(
            name="proof_selected",
            passed=True,
            reason=(
                "selected the first proof; the first-version verifier "
                "verifies only the first proof"
            ),
        )
    )

    expected_payload_hash = proof["payload_hash"]
    computed_payload_hash = canonicalization.hash_passport_payload(
        passport, proof["hash_alg"]
    )
    if computed_payload_hash != expected_payload_hash:
        checks.append(
            VerificationCheck(
                name="payload_hash_valid",
                passed=False,
                reason=(
                    "payload hash does not match the canonical passport "
                    f"payload for {proof['hash_alg']}"
                ),
            )
        )
        return VerificationResult.failed(
            "payload hash does not match the canonical passport payload",
            checks=checks,
        )
    checks.append(
        VerificationCheck(
            name="payload_hash_valid",
            passed=True,
            reason="payload hash matches the canonical passport payload",
        )
    )

    # Key selection runs before signature verification. The selected key (the
    # second tuple element) will be consumed when real signature verification is
    # implemented; for now only the recorded check is needed to fail closed.
    key_check, _ = _select_verification_key(passport, proof)
    checks.append(key_check)
    if not key_check.passed:
        return VerificationResult.failed(key_check.reason, checks=checks)

    checks.append(
        _signature_verification_not_implemented_check(passport, proof)
    )
    return VerificationResult.failed(
        "structure is acceptable but signature verification is not "
        "implemented",
        checks=checks,
    )
