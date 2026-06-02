"""Structural-only local verifier for the agent passport envelope.

This module provides two verifier entry points. :func:`verify_passport_json`
is the raw JSON boundary for untrusted input and rejects duplicate object
member names before later verification steps. :func:`verify_passport_envelope`
checks the structural shape of an already parsed envelope-like object and
records the outcome in a :class:`~aaid.verification.VerificationResult`.

After the structural checks pass, the envelope is validated against the
committed JSON Schema and the outcome is recorded as a ``schema_valid`` check.
When schema validation passes, the verifier selects the proof to check and
records the choice as a ``proof_selected`` check; the first-version rule selects
the first proof only. It then recomputes the canonical payload hash over the
passport and compares it to the selected proof's recorded hash, recording the
outcome as a ``payload_hash_valid`` check. This step verifies
the payload hash only: it does not verify signatures or proofs and does not
evaluate policy. Issuer trust and caller-provided revocation status are checked
earlier as separate boundaries; the revocation boundary binds caller-supplied
in-memory status evidence to the passport and issuer and checks a freshness
window, but performs no network lookup, no registry lookup, no signed status
list parsing, and no cryptographic verification of the status. After the payload
hash
matches, the verifier selects the public key referenced by the proof and
validates basic, non-cryptographic key metadata, recording the outcome as a
``verification_key_selected`` check; finding no single suitable key fails closed
to ``DENY`` before the signature step. After the key is selected, the verifier
checks that the proof's declared canonicalization scheme is recognized,
recording ``signature_canonicalization_supported``, then
prepares the canonical passport payload bytes that a future signature verifier
will use, recording ``signature_input_prepared``, and checks that the selected
key's signed algorithm is supported, recording ``signature_algorithm_supported``;
an unsupported algorithm fails closed to ``DENY`` before the signature step.
Because signature
verification does not exist yet, a structurally valid, schema valid envelope
with a matching payload hash still fails closed to ``DENY``; this verifier can
never return ``ALLOW``. Each check is recorded as a named, immutable check so
the decision can be explained and audited.
"""

import json
import re
from collections.abc import Collection, Mapping, Sequence
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import best_match

from aaid import canonicalization
from aaid.json_parsing import parse_json_no_duplicate_keys
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


_UTC_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def _parse_strict_utc_timestamp(value: object) -> "datetime | None":
    """Parse a strict UTC RFC3339-style timestamp ending in ``Z``.

    This is intentionally stricter than :func:`datetime.fromisoformat`, which
    accepts numeric offsets, a space separator, fractional seconds, and a
    lowercase ``z``. Parsing runs in two mandatory stages and ``fromisoformat``
    is never used:

    1. ``value`` must be a string matching ``_UTC_TIMESTAMP_RE``
       (``YYYY-MM-DDTHH:MM:SSZ``). This rejects offsets, the space separator,
       fractional seconds, lowercase ``z``, date-only values, and surrounding
       whitespace.
    2. :func:`datetime.strptime` validates the calendar fields, rejecting values
       such as month 13 or hour 24 that still match the shape, and the result is
       made timezone-aware in UTC.

    Both stages are required; the regex alone would admit calendar-invalid
    values. Any failure returns ``None`` so callers fail closed.
    """
    if not isinstance(value, str) or _UTC_TIMESTAMP_RE.match(value) is None:
        return None
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None
    return parsed.replace(tzinfo=timezone.utc)


def _passport_time_valid_check(
    passport: Mapping, now: datetime
) -> VerificationCheck:
    """Check that ``now`` is within the passport validity window.

    ``now`` is an already-resolved, timezone-aware UTC instant. ``issued_at`` is
    inclusive and ``expires_at`` is exclusive. The check fails closed when either
    timestamp is not a strict UTC ``Z`` timestamp, when ``issued_at`` is after
    ``expires_at``, when ``now`` is before ``issued_at``, or when ``now`` is at or
    after ``expires_at``. It performs no cryptographic work.
    """
    issued_at = _parse_strict_utc_timestamp(passport.get("issued_at"))
    if issued_at is None:
        return VerificationCheck(
            name="passport_time_valid",
            passed=False,
            reason="issued_at is not a strict UTC timestamp ending in 'Z'",
        )
    expires_at = _parse_strict_utc_timestamp(passport.get("expires_at"))
    if expires_at is None:
        return VerificationCheck(
            name="passport_time_valid",
            passed=False,
            reason="expires_at is not a strict UTC timestamp ending in 'Z'",
        )
    if issued_at > expires_at:
        return VerificationCheck(
            name="passport_time_valid",
            passed=False,
            reason="passport issued_at is after expires_at",
        )
    if now < issued_at:
        return VerificationCheck(
            name="passport_time_valid",
            passed=False,
            reason="passport is not yet valid: current time is before issued_at",
        )
    if now >= expires_at:
        return VerificationCheck(
            name="passport_time_valid",
            passed=False,
            reason="passport has expired: current time is at or after expires_at",
        )
    return VerificationCheck(
        name="passport_time_valid",
        passed=True,
        reason=(
            "current time is within the passport validity window; issued_at is "
            "inclusive and expires_at is exclusive"
        ),
    )


_VERIFIABLE_LIFECYCLE_STATUS = "active"


def _lifecycle_status_allows_verification_check(
    passport: Mapping,
) -> VerificationCheck:
    """Check that the lifecycle status allows verification to continue.

    Only ``active`` continues; ``suspended``, ``revoked``, ``expired``,
    ``compromised``, and ``retired`` fail closed. Schema validation has already
    constrained the value to the lifecycle enum members. This validates the
    status value only: it does not check revocation references, issuer trust, or
    time windows, and it takes no ``now``. It performs no cryptographic work.
    """
    status = passport.get("lifecycle_status")
    if status == _VERIFIABLE_LIFECYCLE_STATUS:
        return VerificationCheck(
            name="lifecycle_status_allows_verification",
            passed=True,
            reason="lifecycle_status is 'active'; verification may continue",
        )
    return VerificationCheck(
        name="lifecycle_status_allows_verification",
        passed=False,
        reason=(
            "lifecycle_status does not allow verification; only 'active' "
            "continues"
        ),
    )


def _issuer_trusted_check(
    passport: Mapping, trusted_issuers: object
) -> VerificationCheck:
    """Check that the passport issuer is explicitly configured as trusted.

    Issuer trust is evaluated against caller-provided configuration only. This
    boundary uses no registry, performs no network lookup, and does not perform
    external issuer verification. ``trusted_issuers`` is a collection of issuer
    identifier strings (for example a ``set``, ``frozenset``, ``tuple``, or
    ``list``); the check passes only when ``passport["issuer_id"]`` is a member
    of that collection.

    It fails closed when issuer trust is not configured (``None``), when the
    configuration is a bare string, a mapping, or any other non-collection value
    rather than a collection of identifiers, and when the issuer is not
    explicitly configured as trusted (an empty collection trusts no issuer). It
    performs no cryptographic work and does not verify signatures, key
    possession, revocation, or an external issuer identity; a passing check does
    not by itself allow the passport.
    """
    if trusted_issuers is None:
        return VerificationCheck(
            name="issuer_trusted",
            passed=False,
            reason=(
                "issuer trust is not configured; no trusted issuers were "
                "provided"
            ),
        )
    if isinstance(trusted_issuers, (str, bytes, bytearray)):
        return VerificationCheck(
            name="issuer_trusted",
            passed=False,
            reason=(
                "trusted issuer configuration must be a collection of issuer "
                "identifiers, not a string"
            ),
        )
    if isinstance(trusted_issuers, Mapping):
        return VerificationCheck(
            name="issuer_trusted",
            passed=False,
            reason=(
                "trusted issuer configuration must be a collection of issuer "
                "identifiers, not a mapping"
            ),
        )
    # A non-collection value (for example an int, float, or bool) is not a usable
    # trust configuration. Require a Collection before the membership test so
    # such input fails closed instead of raising a TypeError on ``in``. Strings,
    # bytes, and mappings are collections but are rejected above.
    if not isinstance(trusted_issuers, Collection):
        return VerificationCheck(
            name="issuer_trusted",
            passed=False,
            reason=(
                "trusted issuer configuration must be a collection of issuer "
                "identifiers"
            ),
        )
    if passport.get("issuer_id") in trusted_issuers:
        return VerificationCheck(
            name="issuer_trusted",
            passed=True,
            reason="issuer_id is explicitly configured as trusted",
        )
    return VerificationCheck(
        name="issuer_trusted",
        passed=False,
        reason="issuer_id is not configured as trusted",
    )


def _revocation_status_checked_check(
    passport: Mapping,
    revocation_status: object,
    trusted_issuers: object,
) -> VerificationCheck:
    """Check that caller-provided revocation status is bound to this passport.

    Revocation status is supplied by the caller as in-memory evidence. This
    boundary performs no network lookup, no registry lookup, no signed status
    list parsing, and no cryptographic verification of the status; it only checks
    exact identity binding by string equality. The status must be a mapping that
    carries string ``status_reference``, ``passport_id``, and ``status_authority``
    fields, and each must match the passport exactly: ``status_reference`` equals
    ``passport["revocation"]["status_reference"]``, ``passport_id`` equals
    ``passport["passport_id"]``, and ``status_authority`` equals
    ``passport["issuer_id"]``. The ``status_authority`` must also be a member of
    the caller-provided ``trusted_issuers`` configuration. No normalization,
    prefix matching, substring matching, or case folding is performed, so
    matching only ``status_reference`` is not enough and status from a different
    issuer fails closed even if that issuer is otherwise trusted; this prevents
    cross-issuer status spoofing and snapshot substitution. It performs no
    cryptographic work and does not confirm the status was actually signed by the
    authority. Any missing, mistyped, or mismatched field fails closed.
    """
    if not isinstance(revocation_status, Mapping):
        return VerificationCheck(
            name="revocation_status_checked",
            passed=False,
            reason="revocation status evidence is missing or not a mapping",
        )

    status_reference = revocation_status.get("status_reference")
    status_passport_id = revocation_status.get("passport_id")
    status_authority = revocation_status.get("status_authority")
    if not (
        isinstance(status_reference, str)
        and isinstance(status_passport_id, str)
        and isinstance(status_authority, str)
    ):
        return VerificationCheck(
            name="revocation_status_checked",
            passed=False,
            reason=(
                "revocation status must carry string status_reference, "
                "passport_id, and status_authority fields"
            ),
        )

    revocation = passport.get("revocation")
    expected_status_reference = (
        revocation.get("status_reference")
        if isinstance(revocation, Mapping)
        else None
    )
    if status_reference != expected_status_reference:
        return VerificationCheck(
            name="revocation_status_checked",
            passed=False,
            reason=(
                "revocation status_reference does not match the passport "
                "revocation reference"
            ),
        )
    if status_passport_id != passport.get("passport_id"):
        return VerificationCheck(
            name="revocation_status_checked",
            passed=False,
            reason="revocation status passport_id does not match the passport",
        )
    if status_authority != passport.get("issuer_id"):
        return VerificationCheck(
            name="revocation_status_checked",
            passed=False,
            reason=(
                "revocation status_authority does not match the passport "
                "issuer_id"
            ),
        )

    # Defence in depth: the status authority must itself be a configured trusted
    # issuer. Issuer trust has already passed when this runs in the normal flow,
    # so this can only fail when the helper is exercised in isolation or the
    # trust configuration is malformed. The guard positively requires a
    # collection (excluding strings, bytes, and mappings) so a None, bare-string,
    # mapping, or non-iterable configuration fails closed rather than raising
    # before the membership test runs.
    trusted_is_collection = (
        isinstance(trusted_issuers, Collection)
        and not isinstance(trusted_issuers, (str, bytes, bytearray))
        and not isinstance(trusted_issuers, Mapping)
    )
    if not trusted_is_collection or status_authority not in trusted_issuers:
        return VerificationCheck(
            name="revocation_status_checked",
            passed=False,
            reason=(
                "revocation status_authority is not a configured trusted issuer"
            ),
        )

    return VerificationCheck(
        name="revocation_status_checked",
        passed=True,
        reason=(
            "revocation status is bound to this passport and its "
            "status_authority is configured as trusted"
        ),
    )


def _revocation_status_fresh_check(
    revocation_status: object, now: datetime
) -> VerificationCheck:
    """Check that caller-provided revocation status is fresh at ``now``.

    Freshness reuses the strict UTC ``Z`` timestamp parsing used for passport
    time validity and the already-resolved injected ``now``; the wall clock is
    not read again here. The status must carry ``produced_at`` and
    ``valid_until`` as strict UTC ``Z`` timestamps, and freshness holds only when
    ``produced_at <= now < valid_until`` (``produced_at`` inclusive,
    ``valid_until`` exclusive). Missing, malformed, non-strict, future-dated
    (``now`` before ``produced_at``), stale (``now`` at or after ``valid_until``),
    or inverted (``produced_at`` after ``valid_until``) windows fail closed. It
    performs no cryptographic work.
    """
    if not isinstance(revocation_status, Mapping):
        return VerificationCheck(
            name="revocation_status_fresh",
            passed=False,
            reason="revocation status evidence is missing or not a mapping",
        )
    produced_at = _parse_strict_utc_timestamp(
        revocation_status.get("produced_at")
    )
    if produced_at is None:
        return VerificationCheck(
            name="revocation_status_fresh",
            passed=False,
            reason="produced_at is not a strict UTC timestamp ending in 'Z'",
        )
    valid_until = _parse_strict_utc_timestamp(
        revocation_status.get("valid_until")
    )
    if valid_until is None:
        return VerificationCheck(
            name="revocation_status_fresh",
            passed=False,
            reason="valid_until is not a strict UTC timestamp ending in 'Z'",
        )
    if produced_at > valid_until:
        return VerificationCheck(
            name="revocation_status_fresh",
            passed=False,
            reason="revocation status produced_at is after valid_until",
        )
    if now < produced_at:
        return VerificationCheck(
            name="revocation_status_fresh",
            passed=False,
            reason=(
                "revocation status is not yet valid: current time is before "
                "produced_at"
            ),
        )
    if now >= valid_until:
        return VerificationCheck(
            name="revocation_status_fresh",
            passed=False,
            reason=(
                "revocation status is stale: current time is at or after "
                "valid_until"
            ),
        )
    return VerificationCheck(
        name="revocation_status_fresh",
        passed=True,
        reason=(
            "revocation status is fresh; produced_at is inclusive and "
            "valid_until is exclusive"
        ),
    )


_ACTIVE_REVOCATION_STATUS = "active"


def _passport_not_revoked_check(revocation_status: object) -> VerificationCheck:
    """Check that the caller-provided revocation status reports ``active``.

    This passes only when ``revocation_status["status"]`` is exactly the string
    ``active``. Every other value fails closed, including a missing field, a
    non-string value, an unknown or misspelled value, and the values ``revoked``,
    ``suspended``, ``expired``, ``compromised``, and ``retired``. It performs no
    cryptographic work and does not parse signed status lists.
    """
    if not isinstance(revocation_status, Mapping):
        return VerificationCheck(
            name="passport_not_revoked",
            passed=False,
            reason="revocation status evidence is missing or not a mapping",
        )
    if revocation_status.get("status") == _ACTIVE_REVOCATION_STATUS:
        return VerificationCheck(
            name="passport_not_revoked",
            passed=True,
            reason=(
                "revocation status is 'active' according to the provided "
                "status evidence"
            ),
        )
    return VerificationCheck(
        name="passport_not_revoked",
        passed=False,
        reason="revocation status is not 'active'; the passport fails closed",
    )


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


def _verification_key_valid_for_proof_check(
    key: Mapping, proof: Mapping, now: datetime
) -> VerificationCheck:
    """Check the selected public key's time validity and proof binding.

    This runs after the key is selected and before the signing input is prepared.
    It reuses the strict UTC ``Z`` timestamp parsing used for passport time
    validity and the already-resolved injected ``now``; the wall clock is not
    read again here. The key's required ``created_at`` is inclusive
    (``created_at <= now``) and its optional ``not_after`` is exclusive (when
    present, ``now < not_after``). Missing, malformed, non-strict, future-created
    (``now`` before ``created_at``), expired (``now`` at or after ``not_after``),
    or inverted (``created_at`` after ``not_after``) key validity windows fail
    closed. It also binds the proof to the selected key by exact string equality:
    ``proof["verification_method"]`` must equal the selected key's ``kid`` with no
    normalization, prefix, substring, or case folding. It performs no
    cryptographic work and does not verify signatures.
    """
    created_at = _parse_strict_utc_timestamp(key.get("created_at"))
    if created_at is None:
        return VerificationCheck(
            name="verification_key_valid_for_proof",
            passed=False,
            reason=(
                "selected public key created_at is not a strict UTC timestamp "
                "ending in 'Z'"
            ),
        )

    not_after = None
    raw_not_after = key.get("not_after")
    if raw_not_after is not None:
        not_after = _parse_strict_utc_timestamp(raw_not_after)
        if not_after is None:
            return VerificationCheck(
                name="verification_key_valid_for_proof",
                passed=False,
                reason=(
                    "selected public key not_after is not a strict UTC "
                    "timestamp ending in 'Z'"
                ),
            )
        if created_at > not_after:
            return VerificationCheck(
                name="verification_key_valid_for_proof",
                passed=False,
                reason="selected public key created_at is after not_after",
            )

    if now < created_at:
        return VerificationCheck(
            name="verification_key_valid_for_proof",
            passed=False,
            reason=(
                "selected public key is not yet valid: current time is before "
                "created_at"
            ),
        )
    if not_after is not None and now >= not_after:
        return VerificationCheck(
            name="verification_key_valid_for_proof",
            passed=False,
            reason=(
                "selected public key has expired: current time is at or after "
                "not_after"
            ),
        )

    if proof.get("verification_method") != key.get("kid"):
        return VerificationCheck(
            name="verification_key_valid_for_proof",
            passed=False,
            reason=(
                "proof verification_method does not match the selected public "
                "key kid"
            ),
        )

    return VerificationCheck(
        name="verification_key_valid_for_proof",
        passed=True,
        reason=(
            "selected public key is within its validity window and the proof "
            "verification_method matches the selected key kid"
        ),
    )


_SUPPORTED_SIGNATURE_CANONICALIZATIONS = ("json-canonicalization-scheme",)


def _signature_canonicalization_supported_check(
    proof: Mapping,
) -> VerificationCheck:
    """Check that the proof's declared canonicalization scheme is recognized.

    This validates declared canonicalization metadata only. It confirms that the
    proof's ``canonicalization`` value is recognized for this verifier stage so
    the signing input can later be prepared under a known scheme. It does not
    implement, replace, or fully validate canonicalization, and it makes no claim
    that the current canonicalization helper is a complete independent RFC 8785 /
    JSON Canonicalization Scheme implementation; full-JCS compliance is left to a
    later research and implementation step. An unrecognized scheme fails closed.
    """
    declared = proof.get("canonicalization")
    if declared in _SUPPORTED_SIGNATURE_CANONICALIZATIONS:
        return VerificationCheck(
            name="signature_canonicalization_supported",
            passed=True,
            reason=(
                f"selected proof canonicalization scheme {declared} is "
                "recognized for this verifier stage"
            ),
        )
    return VerificationCheck(
        name="signature_canonicalization_supported",
        passed=False,
        reason=(
            f"selected proof canonicalization scheme {declared!r} is not "
            "recognized for this verifier stage"
        ),
    )


_SUPPORTED_SIGNATURE_ALGORITHMS = ("ML-DSA-65",)


def _prepare_signature_input(
    passport: Mapping,
    canonical_payload: "bytes | None" = None,
) -> "tuple[VerificationCheck, bytes | None]":
    """Prepare the canonical passport payload bytes for signature verification.

    The future signature input is the canonical passport payload bytes only.
    These are the deterministic, UTF-8 encoded canonical JSON bytes of the
    ``passport`` object, produced by the shared canonicalization helper so the
    signing input matches the payload-hash input exactly. The input excludes the
    envelope wrapper, the ``proofs`` array, signature material, and any
    display-formatted JSON. This prepares input only: it performs no
    cryptographic work and does not verify signatures.

    When ``canonical_payload`` is provided (the bytes already prepared by the
    ``canonical_payload_prepared`` step), it is reused unchanged so the signing
    input is byte-identical to the prepared canonical payload. When it is
    ``None`` the bytes are produced from the shared canonicalization helper, so
    callers that pass only the passport keep the previous behavior.

    Returns a ``(check, signature_input)`` pair. The canonicalization helper
    already returns UTF-8 bytes, so ``signature_input`` is those canonical
    payload bytes.
    """
    if canonical_payload is None:
        canonical_payload = canonicalization.canonicalize_passport_payload(
            passport
        )
    return (
        VerificationCheck(
            name="signature_input_prepared",
            passed=True,
            reason=(
                "prepared the canonical passport payload bytes as the future "
                "signature input"
            ),
        ),
        canonical_payload,
    )


def _signature_algorithm_supported_check(key: Mapping) -> VerificationCheck:
    """Check that the selected public key's algorithm is supported.

    The decision uses the selected public key's signed ``alg`` metadata, not the
    detached proof algorithm; the key-selection step has already required the
    key algorithm to equal the proof algorithm. For this step the supported set
    is a narrow internal allowlist, so an unsupported algorithm fails closed and
    the verifier cannot proceed to signature verification. This performs no
    cryptographic work.
    """
    key_alg = key.get("alg")
    if key_alg in _SUPPORTED_SIGNATURE_ALGORITHMS:
        return VerificationCheck(
            name="signature_algorithm_supported",
            passed=True,
            reason=(
                f"selected public key algorithm {key_alg} is supported for "
                "signature verification"
            ),
        )
    return VerificationCheck(
        name="signature_algorithm_supported",
        passed=False,
        reason=(
            f"selected public key algorithm {key_alg!r} is not supported for "
            "signature verification"
        ),
    )



def verify_passport_json(
    text: str,
    *,
    now: "datetime | None" = None,
    trusted_issuers: object = None,
    revocation_status: object = None,
) -> VerificationResult:
    """Verify an untrusted raw JSON passport envelope.

    Raw JSON input is parsed with duplicate object member rejection before schema
    validation, canonicalization, payload-hash comparison, or signature input
    preparation. Malformed JSON and duplicate member names fail closed.

    ``now`` is the keyword-only effective verification time forwarded to
    :func:`verify_passport_envelope` for the expiration check; ``None`` uses the
    real wall-clock UTC time.

    ``trusted_issuers`` is the keyword-only issuer-trust configuration forwarded
    unchanged to :func:`verify_passport_envelope` after duplicate-key-safe
    parsing; ``None`` (the default) fails the issuer-trust check closed.

    ``revocation_status`` is the keyword-only caller-provided revocation status
    evidence forwarded unchanged to :func:`verify_passport_envelope` after
    duplicate-key-safe parsing; ``None`` (the default) fails the
    revocation-status check closed.
    """
    try:
        envelope = parse_json_no_duplicate_keys(text)
    except ValueError:
        check = VerificationCheck(
            name="raw_json_parsed",
            passed=False,
            reason=(
                "malformed JSON or duplicate object member names were rejected "
                "at the raw JSON boundary"
            ),
        )
        return VerificationResult.failed(
            "raw JSON could not be parsed safely",
            checks=[check],
        )

    raw_check = VerificationCheck(
        name="raw_json_parsed",
        passed=True,
        reason="raw JSON parsed with duplicate object member rejection",
    )
    result = verify_passport_envelope(
        envelope,
        now=now,
        trusted_issuers=trusted_issuers,
        revocation_status=revocation_status,
    )
    return VerificationResult(
        valid=result.valid,
        decision=result.decision,
        reason=result.reason,
        checks=(raw_check, *result.checks),
    )


def verify_passport_envelope(
    envelope: object,
    *,
    now: "datetime | None" = None,
    trusted_issuers: object = None,
    revocation_status: object = None,
) -> VerificationResult:
    """Check the structure of a passport envelope and record the outcome.

    The checks run in order and stop at the first structural problem, because
    each check depends on the previous one holding. On the first failure the
    result records the checks that passed plus the failing check and fails
    closed to ``DENY``.

    A structurally acceptable envelope (a mapping with a mapping ``passport``
    and a non-empty, non-string ``proofs`` sequence) is then validated against
    the committed JSON Schema and the outcome is recorded as ``schema_valid``.
    If schema validation fails, the result fails closed to ``DENY`` with the
    failing ``schema_valid`` check. When it passes, the verifier resolves the
    effective time (``now``; ``None`` uses the wall clock, a naive value is
    assumed UTC) and checks the passport validity window
    (``passport_time_valid``: ``issued_at`` inclusive, ``expires_at`` exclusive)
    and then that the lifecycle status is ``active``
    (``lifecycle_status_allows_verification``); either failing fails closed to
    ``DENY`` before the issuer-trust check. Otherwise the verifier checks that
    the passport issuer is explicitly configured as trusted against the
    caller-provided ``trusted_issuers`` configuration (``issuer_trusted``); this
    uses caller configuration only, with no registry or network lookup, and
    fails closed to ``DENY`` before proof selection when issuer trust is not
    configured or the issuer is not trusted. Otherwise the verifier evaluates
    caller-provided revocation status before proof selection. The status is
    in-memory evidence supplied by the caller; this boundary performs no network
    lookup, registry lookup, signed status list parsing, or cryptographic
    verification of the status. It records ``revocation_status_checked`` (the
    status must be a mapping bound to this passport by exact string equality on
    ``status_reference``, ``passport_id``, and ``status_authority``, with the
    authority also a trusted issuer), then ``revocation_status_fresh`` (strict
    UTC ``Z`` ``produced_at`` and ``valid_until`` with
    ``produced_at <= now < valid_until`` against the already-resolved ``now``),
    then ``passport_not_revoked`` (the status must be exactly ``active``); any of
    these failing fails closed to ``DENY`` before proof selection. Otherwise the
    verifier selects the
    proof to check and records the choice as ``proof_selected``; the
    first-version rule selects the first proof only. It then recomputes the
    canonical payload hash over ``envelope["passport"]`` using the selected
    proof's recorded hash
    algorithm and compares it to that proof's ``payload_hash``; the outcome is
    recorded as ``payload_hash_valid``. The hash algorithm is taken from the
    schema-validated proof, so it is always a supported algorithm. A mismatch
    fails closed to ``DENY`` with the failing ``payload_hash_valid`` check and
    stops before the signature step. When the payload hash matches, the result
    records ``payload_hash_valid`` as passed and then selects the public key
    referenced by the proof, recording ``verification_key_selected``. If no
    single public key matches the proof's ``kid`` with a matching algorithm,
    active status, and suitable purpose, the result fails closed to ``DENY``
    before the signature step. Otherwise the verifier checks that the proof's
    declared canonicalization scheme is recognized
    (``signature_canonicalization_supported``), then prepares the canonical
    passport payload bytes as the future signature input
    (``signature_input_prepared``) and checks that the selected key's signed
    algorithm is supported (``signature_algorithm_supported``); an unsupported
    algorithm fails closed to ``DENY`` before the signature step. Otherwise it
    records ``signature_verification_not_implemented`` as failed. Signature
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

    # Resolve the effective verification time exactly once. now=None uses the
    # real wall clock; a naive injected now is assumed to be UTC so every
    # comparison below is timezone-aware.
    now_dt = now if now is not None else datetime.now(timezone.utc)
    if now_dt.tzinfo is None:
        now_dt = now_dt.replace(tzinfo=timezone.utc)

    time_check = _passport_time_valid_check(passport, now_dt)
    checks.append(time_check)
    if not time_check.passed:
        return VerificationResult.failed(time_check.reason, checks=checks)

    lifecycle_check = _lifecycle_status_allows_verification_check(passport)
    checks.append(lifecycle_check)
    if not lifecycle_check.passed:
        return VerificationResult.failed(lifecycle_check.reason, checks=checks)

    # Issuer trust is decided before proof selection, payload-hash comparison,
    # key selection, and any future signature or revocation step: a later result
    # is only meaningful once the verifier knows the issuer is trusted under the
    # caller-provided configuration. This step uses caller configuration only.
    issuer_check = _issuer_trusted_check(passport, trusted_issuers)
    checks.append(issuer_check)
    if not issuer_check.passed:
        return VerificationResult.failed(issuer_check.reason, checks=checks)

    # Caller-provided revocation status is evaluated after issuer trust and
    # before proof selection. The status is in-memory evidence supplied by the
    # caller: this boundary performs no network lookup, registry lookup, signed
    # status list parsing, or cryptographic verification of the status. It binds
    # the status to this passport and issuer, checks freshness against the same
    # resolved now, and requires an active status. Each sub-step fails closed,
    # so an absent or unbound status denies before any later step runs.
    revocation_checked = _revocation_status_checked_check(
        passport, revocation_status, trusted_issuers
    )
    checks.append(revocation_checked)
    if not revocation_checked.passed:
        return VerificationResult.failed(
            revocation_checked.reason, checks=checks
        )

    revocation_fresh = _revocation_status_fresh_check(revocation_status, now_dt)
    checks.append(revocation_fresh)
    if not revocation_fresh.passed:
        return VerificationResult.failed(revocation_fresh.reason, checks=checks)

    not_revoked = _passport_not_revoked_check(revocation_status)
    checks.append(not_revoked)
    if not not_revoked.passed:
        return VerificationResult.failed(not_revoked.reason, checks=checks)

    # Proof-selection hardening: fail closed when more than one proof is present.
    # The first-version verifier selects the first proof only, which is
    # acceptable while it cannot return ALLOW, but proof ordering must not become
    # a trust model. Until a multi-proof, hybrid, or post-quantum selection
    # policy exists, a multi-proof envelope is not interpreted. Missing,
    # non-sequence, and empty proofs are already rejected by earlier structural
    # checks; this runs before proof selection and performs no cryptographic
    # work.
    if len(proofs) != 1:
        checks.append(
            VerificationCheck(
                name="proof_count_allowed",
                passed=False,
                reason=(
                    "exactly one proof is required; a multi-proof envelope "
                    "fails closed until a proof-selection policy exists"
                ),
            )
        )
        return VerificationResult.failed(
            "exactly one proof is required", checks=checks
        )
    checks.append(
        VerificationCheck(
            name="proof_count_allowed",
            passed=True,
            reason="exactly one proof is present",
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

    # Prepare the canonical passport payload bytes once, before the payload-hash
    # and signature-input steps reuse them. A canonicalization error (and any
    # future candidate-canonicalizer error) fails closed here as a recorded
    # check and a ``DENY`` result rather than escaping as an unhandled exception
    # in a verifier path that must return a ``VerificationResult``. The except is
    # deliberately scoped to this single canonicalization call.
    try:
        canonical_payload = canonicalization.canonicalize_passport_payload(
            passport
        )
    except Exception:
        checks.append(
            VerificationCheck(
                name="canonical_payload_prepared",
                passed=False,
                reason=(
                    "canonical payload bytes could not be prepared; "
                    "canonicalization failed closed"
                ),
            )
        )
        return VerificationResult.failed(
            "canonical payload bytes could not be prepared", checks=checks
        )
    checks.append(
        VerificationCheck(
            name="canonical_payload_prepared",
            passed=True,
            reason="prepared the canonical passport payload bytes",
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

    # Key selection runs before signature verification and yields the selected
    # public key, which the algorithm-support check below relies on.
    key_check, selected_key = _select_verification_key(passport, proof)
    checks.append(key_check)
    if not key_check.passed:
        return VerificationResult.failed(key_check.reason, checks=checks)

    # Validate the selected key's time validity and bind the proof to it before
    # preparing the signing input. This reuses the already-resolved now and
    # performs no cryptographic work.
    key_validity_check = _verification_key_valid_for_proof_check(
        selected_key, proof, now_dt
    )
    checks.append(key_validity_check)
    if not key_validity_check.passed:
        return VerificationResult.failed(
            key_validity_check.reason, checks=checks
        )

    # Validate the proof's declared canonicalization scheme before preparing the
    # signing input, so the input is prepared under a recognized scheme. This
    # validates declared metadata only; it does not canonicalize.
    canonicalization_check = _signature_canonicalization_supported_check(proof)
    checks.append(canonicalization_check)
    if not canonicalization_check.passed:
        return VerificationResult.failed(
            canonicalization_check.reason, checks=checks
        )

    # Reuse the canonical payload bytes prepared above as the future signature
    # input, so the signing input is byte-identical to the prepared payload. The
    # bytes are not consumed yet because real signature verification is not
    # implemented in this step.
    input_check, _ = _prepare_signature_input(passport, canonical_payload)
    checks.append(input_check)

    # The algorithm decision uses the selected key's signed metadata, not the
    # detached proof algorithm.
    algorithm_check = _signature_algorithm_supported_check(selected_key)
    checks.append(algorithm_check)
    if not algorithm_check.passed:
        return VerificationResult.failed(algorithm_check.reason, checks=checks)

    checks.append(
        _signature_verification_not_implemented_check(passport, proof)
    )
    return VerificationResult.failed(
        "structure is acceptable but signature verification is not "
        "implemented",
        checks=checks,
    )
