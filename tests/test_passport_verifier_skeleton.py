"""Tests for the passport verifier structural skeleton.

These cases pin the first fail-closed verifier boundary: the envelope must be a
mapping, contain a passport mapping, and contain a non-empty proofs sequence.

A structurally valid envelope still does not grant `ALLOW`; the current research
verifier reaches the explicit signature-not-implemented boundary and remains
denied for the minimal example.
"""

import json
from pathlib import Path
from typing import Any

import aaid
import aaid.passport_verifier as passport_verifier_module
from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"

ENVELOPE_IS_MAPPING_CHECK = "envelope_is_mapping"
PASSPORT_PRESENT_CHECK = "passport_present"
PASSPORT_IS_MAPPING_CHECK = "passport_is_mapping"
PROOFS_PRESENT_CHECK = "proofs_present"
PROOFS_IS_SEQUENCE_CHECK = "proofs_is_sequence"
PROOFS_NON_EMPTY_CHECK = "proofs_non_empty"
SIGNATURE_CHECK = "signature_verification_not_implemented"

STRUCTURAL_CHECK_NAMES = (
    ENVELOPE_IS_MAPPING_CHECK,
    PASSPORT_PRESENT_CHECK,
    PASSPORT_IS_MAPPING_CHECK,
    PROOFS_PRESENT_CHECK,
    PROOFS_IS_SEQUENCE_CHECK,
    PROOFS_NON_EMPTY_CHECK,
)

FORBIDDEN_MODULE_ATTRIBUTES = (
    "hashlib",
    "hmac",
    "hash_passport_payload",
    "canonicalize_passport_payload",
)

FORBIDDEN_PUBLIC_CALLABLE_SUBSTRINGS = ("sign", "hash", "crypto")


def load_example_envelope() -> dict[str, Any]:
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def find_check(
    result: VerificationResult,
    name: str,
) -> VerificationCheck | None:
    for check in result.checks:
        if check.name == name:
            return check
    return None


def verify_with_trusted_context(envelope: Any) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def assert_denied(result: VerificationResult) -> None:
    assert result.valid is False
    assert result.decision == DENY


def assert_check_passed(result: VerificationResult, name: str) -> None:
    check = find_check(result, name)

    assert check is not None
    assert check.passed is True


def assert_check_failed(result: VerificationResult, name: str) -> None:
    check = find_check(result, name)

    assert check is not None
    assert check.passed is False


def test_non_mapping_envelope_is_denied() -> None:
    result = verify_passport_envelope(["passport", "proofs"])

    assert_denied(result)
    assert_check_failed(result, ENVELOPE_IS_MAPPING_CHECK)


def test_missing_passport_is_denied() -> None:
    result = verify_passport_envelope({"proofs": [{"proof_id": "x"}]})

    assert_denied(result)
    assert_check_passed(result, ENVELOPE_IS_MAPPING_CHECK)
    assert_check_failed(result, PASSPORT_PRESENT_CHECK)


def test_non_mapping_passport_is_denied() -> None:
    result = verify_passport_envelope(
        {"passport": "not-a-mapping", "proofs": [{"proof_id": "x"}]}
    )

    assert_denied(result)
    assert_check_passed(result, PASSPORT_PRESENT_CHECK)
    assert_check_failed(result, PASSPORT_IS_MAPPING_CHECK)


def test_missing_proofs_is_denied() -> None:
    result = verify_passport_envelope({"passport": {"subject": "demo"}})

    assert_denied(result)
    assert_check_passed(result, PASSPORT_IS_MAPPING_CHECK)
    assert_check_failed(result, PROOFS_PRESENT_CHECK)


def test_string_proofs_is_rejected() -> None:
    result = verify_passport_envelope(
        {"passport": {"subject": "demo"}, "proofs": "signature"}
    )

    assert_denied(result)
    assert_check_passed(result, PROOFS_PRESENT_CHECK)
    assert_check_failed(result, PROOFS_IS_SEQUENCE_CHECK)


def test_bytes_proofs_is_rejected() -> None:
    result = verify_passport_envelope(
        {"passport": {"subject": "demo"}, "proofs": b"signature"}
    )

    assert_denied(result)
    assert_check_failed(result, PROOFS_IS_SEQUENCE_CHECK)


def test_empty_proofs_is_rejected() -> None:
    result = verify_passport_envelope(
        {"passport": {"subject": "demo"}, "proofs": []}
    )

    assert_denied(result)
    assert_check_passed(result, PROOFS_IS_SEQUENCE_CHECK)
    assert_check_failed(result, PROOFS_NON_EMPTY_CHECK)


def test_minimal_example_is_denied_due_to_signature_not_implemented() -> None:
    result = verify_with_trusted_context(load_example_envelope())

    assert_denied(result)

    for name in STRUCTURAL_CHECK_NAMES:
        assert_check_passed(result, name)

    assert_check_failed(result, SIGNATURE_CHECK)
    assert "signature" in result.reason.lower()


def test_checks_are_verification_check_instances() -> None:
    result = verify_passport_envelope(load_example_envelope())

    assert len(result.checks) >= 1
    assert all(isinstance(check, VerificationCheck) for check in result.checks)


def test_checks_stored_as_tuple() -> None:
    result = verify_passport_envelope(load_example_envelope())

    assert isinstance(result.checks, tuple)


def test_skeleton_never_returns_allow() -> None:
    cases = [
        load_example_envelope(),
        {},
        {"passport": {"subject": "demo"}},
        {"proofs": [{"proof_id": "x"}]},
        {"passport": "x", "proofs": [{"proof_id": "x"}]},
        {"passport": {"subject": "demo"}, "proofs": []},
        {"passport": {"subject": "demo"}, "proofs": "x"},
        {"passport": {"subject": "demo"}, "proofs": b"x"},
        [],
        "x",
        42,
        None,
    ]

    # Reach the deeper signature boundary for the valid, trusted example so this
    # sweep is not limited to early structural checks.
    reached = verify_with_trusted_context(load_example_envelope())

    assert find_check(reached, SIGNATURE_CHECK) is not None

    for case in cases:
        result = verify_with_trusted_context(case)

        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW, f"unexpected ALLOW for {case!r}"
        assert_denied(result)


def test_verify_passport_envelope_exported_from_package() -> None:
    from aaid import verify_passport_envelope as exported

    assert "verify_passport_envelope" in aaid.__all__
    assert exported is verify_passport_envelope


def test_skeleton_introduces_no_crypto_or_signing() -> None:
    for name in FORBIDDEN_MODULE_ATTRIBUTES:
        assert not hasattr(passport_verifier_module, name)

    for name in dir(passport_verifier_module):
        if name.startswith("_"):
            continue

        attribute = getattr(passport_verifier_module, name)

        if callable(attribute):
            lowered = name.lower()
            assert not any(
                substring in lowered
                for substring in FORBIDDEN_PUBLIC_CALLABLE_SUBSTRINGS
            ), (
                f"{name} suggests public signing, crypto, or hash behavior, "
                "which this verifier boundary must not expose"
            )
