"""Structural-only local verifier for the agent passport envelope.

This module provides a single entry point, :func:`verify_passport_envelope`,
that checks the structural shape of an envelope-like object and records the
outcome in a :class:`~aaid.verification.VerificationResult`.

After the structural checks pass, the envelope is validated against the
committed JSON Schema and the outcome is recorded as a ``schema_valid`` check.
This is schema validation only: it does not verify the payload hash, does not
verify signatures or proofs, does not perform any cryptography, and does not
evaluate policy. Because signature verification does not exist yet, a
structurally and schema acceptable envelope still fails closed to ``DENY``;
this verifier can never return ``ALLOW``. Each check is recorded as a named,
immutable check so the decision can be explained and audited.
"""

import json
from collections.abc import Mapping, Sequence
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import best_match

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
    failing ``schema_valid`` check. If it passes, the result records
    ``schema_valid`` as passed and then records
    ``signature_verification_not_implemented`` as failed. Signature
    verification is out of scope here, so a schema-valid envelope still fails
    closed to ``DENY`` and never returns ``ALLOW``.
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

    checks.append(
        VerificationCheck(
            name="signature_verification_not_implemented",
            passed=False,
            reason=(
                "structure is acceptable but signature verification is not "
                "implemented, so the envelope cannot be allowed"
            ),
        )
    )
    return VerificationResult.failed(
        "structure is acceptable but signature verification is not "
        "implemented",
        checks=checks,
    )
