"""Verification result data-model tests.

These tests record current behavior for `VerificationResult` and
`VerificationCheck`.

The model can record `ALLOW` as data. These tests do not make the passport
verifier return `ALLOW` and do not add signature or crypto verification. More
tests and research are still needed around the verifier/result boundary.
"""

import dataclasses

import pytest

import aaid
import aaid.verification as verification_module
from aaid.verification import (
    ALLOW,
    DENY,
    REQUIRE_HUMAN_APPROVAL,
    VerificationCheck,
    VerificationResult,
)

FORBIDDEN_CALLABLE_PREFIXES = (
    "verify",
    "sign",
    "validate_signature",
    "check_signature",
)

FORBIDDEN_IMPORTED_MODULES = (
    "hashlib",
    "hmac",
)

PACKAGE_EXPORTS = (
    "VerificationCheck",
    "VerificationResult",
    "ALLOW",
    "DENY",
    "REQUIRE_HUMAN_APPROVAL",
    "REQUIRE_HUMAN_REVIEW",
)


def test_passed_result_is_valid() -> None:
    result = VerificationResult.passed("schema and payload hash recorded")

    assert result.valid is True


def test_failed_result_is_invalid() -> None:
    result = VerificationResult.failed("payload hash mismatch")

    assert result.valid is False


def test_failed_defaults_decision_to_deny() -> None:
    result = VerificationResult.failed("payload hash mismatch")

    assert result.decision == DENY


def test_passed_result_records_allow_decision_data() -> None:
    result = VerificationResult.passed("all recorded checks passed")

    assert result.decision == ALLOW


def test_checks_stored_as_tuple_when_list_passed() -> None:
    checks = [VerificationCheck(name="schema", passed=True, reason="valid")]
    result = VerificationResult(valid=True, decision=ALLOW, reason="ok", checks=checks)

    assert isinstance(result.checks, tuple)
    assert result.checks[0].name == "schema"


def test_checks_stored_as_tuple_when_generator_passed() -> None:
    checks = (
        VerificationCheck(name=f"check_{index}", passed=True, reason="ok")
        for index in range(3)
    )
    result = VerificationResult.passed("ok", checks=checks)

    assert isinstance(result.checks, tuple)
    assert len(result.checks) == 3


def test_result_is_frozen() -> None:
    result = VerificationResult.failed("denied")

    with pytest.raises(dataclasses.FrozenInstanceError):
        result.valid = True


def test_check_is_frozen() -> None:
    check = VerificationCheck(name="schema", passed=True, reason="valid")

    with pytest.raises(dataclasses.FrozenInstanceError):
        check.passed = False


def test_reason_preserved_verbatim() -> None:
    reason = "  payload_hash mismatch: expected 'abc', got 'def'.  "

    assert VerificationResult.passed(reason).reason == reason
    assert VerificationResult.failed(reason).reason == reason


def test_failing_check_makes_passed_result_invalid() -> None:
    failing_check = VerificationCheck(
        name="payload_hash",
        passed=False,
        reason="hash mismatch",
    )
    result = VerificationResult.passed("recorded", checks=[failing_check])

    assert result.valid is False
    assert result.decision == DENY


def test_module_exposes_no_signature_or_crypto_callable() -> None:
    for name in dir(verification_module):
        if name.startswith("_"):
            continue

        attr = getattr(verification_module, name)
        if callable(attr):
            lowered = name.lower()
            assert not any(
                lowered.startswith(prefix) for prefix in FORBIDDEN_CALLABLE_PREFIXES
            ), (
                f"{name} suggests signature/crypto verification, which this "
                "data model does not implement"
            )

    for module_name in FORBIDDEN_IMPORTED_MODULES:
        assert not hasattr(verification_module, module_name)


def test_signature_not_verified_is_recorded_as_data_only() -> None:
    check = VerificationCheck(
        name="signature_verification_not_implemented",
        passed=False,
        reason="signature verification is out of scope for this data model",
    )
    result = VerificationResult.passed("structural", checks=[check])

    assert result.valid is False
    assert result.decision == DENY
    assert result.checks[0].name == "signature_verification_not_implemented"


def test_exports_available_from_package() -> None:
    from aaid import (
        ALLOW,
        DENY,
        REQUIRE_HUMAN_APPROVAL,
        REQUIRE_HUMAN_REVIEW,
        VerificationCheck,
        VerificationResult,
    )

    imported_exports = (
        VerificationCheck,
        VerificationResult,
        ALLOW,
        DENY,
        REQUIRE_HUMAN_APPROVAL,
        REQUIRE_HUMAN_REVIEW,
    )

    assert all(export is not None for export in imported_exports)
    for name in PACKAGE_EXPORTS:
        assert name in aaid.__all__


def test_unknown_decision_is_rejected() -> None:
    with pytest.raises(ValueError):
        VerificationResult(valid=False, decision="MAYBE", reason="bad decision")


def test_failed_accepts_require_human_approval_decision() -> None:
    result = VerificationResult.failed(
        "human approval required",
        decision=REQUIRE_HUMAN_APPROVAL,
    )

    assert result.valid is False
    assert result.decision == REQUIRE_HUMAN_APPROVAL
