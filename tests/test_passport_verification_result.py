import dataclasses
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import aaid.verification as ver
from aaid.verification import (
    ALLOW,
    DENY,
    REQUIRE_HUMAN_APPROVAL,
    VerificationCheck,
    VerificationResult,
)


def test_passed_result_is_valid():
    result = VerificationResult.passed("schema and payload hash recorded")
    assert result.valid is True


def test_failed_result_is_invalid():
    result = VerificationResult.failed("payload hash mismatch")
    assert result.valid is False


def test_failed_defaults_decision_to_deny():
    result = VerificationResult.failed("payload hash mismatch")
    assert result.decision == DENY


def test_passed_result_decision_is_allow():
    result = VerificationResult.passed("all recorded checks passed")
    assert result.decision == ALLOW


def test_checks_stored_as_tuple_when_list_passed():
    checks = [VerificationCheck(name="schema", passed=True, reason="valid")]
    result = VerificationResult(
        valid=True, decision=ALLOW, reason="ok", checks=checks
    )
    assert isinstance(result.checks, tuple)
    assert result.checks[0].name == "schema"


def test_checks_stored_as_tuple_when_generator_passed():
    checks = (
        VerificationCheck(name=f"check_{i}", passed=True, reason="ok")
        for i in range(3)
    )
    result = VerificationResult.passed("ok", checks=checks)
    assert isinstance(result.checks, tuple)
    assert len(result.checks) == 3


def test_result_is_frozen():
    result = VerificationResult.failed("denied")
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.valid = True


def test_check_is_frozen():
    check = VerificationCheck(name="schema", passed=True, reason="valid")
    with pytest.raises(dataclasses.FrozenInstanceError):
        check.passed = False


def test_reason_preserved_verbatim():
    reason = "  payload_hash mismatch: expected 'abc', got 'def'.  "
    assert VerificationResult.passed(reason).reason == reason
    assert VerificationResult.failed(reason).reason == reason


def test_failing_check_makes_passed_result_invalid():
    failing = VerificationCheck(
        name="payload_hash", passed=False, reason="hash mismatch"
    )
    result = VerificationResult.passed("recorded", checks=[failing])
    assert result.valid is False
    assert result.decision == DENY


def test_module_exposes_no_signature_or_crypto_callable():
    forbidden_prefixes = (
        "verify",
        "sign",
        "validate_signature",
        "check_signature",
    )
    for name in dir(ver):
        if name.startswith("_"):
            continue
        attr = getattr(ver, name)
        if callable(attr):
            lowered = name.lower()
            assert not any(lowered.startswith(p) for p in forbidden_prefixes), (
                f"{name} suggests signature/crypto verification, which this "
                "data model must not implement"
            )
    assert not hasattr(ver, "hashlib")
    assert not hasattr(ver, "hmac")


def test_signature_not_verified_is_recorded_as_data_only():
    check = VerificationCheck(
        name="signature_verification_not_implemented",
        passed=False,
        reason="signature verification is out of scope for this data model",
    )
    result = VerificationResult.passed("structural", checks=[check])
    assert result.valid is False
    assert result.decision == DENY
    assert result.checks[0].name == "signature_verification_not_implemented"


def test_exports_available_from_package():
    from aaid import (
        ALLOW,
        DENY,
        REQUIRE_HUMAN_APPROVAL,
        REQUIRE_HUMAN_REVIEW,
        VerificationCheck,
        VerificationResult,
    )

    import aaid

    exported = (
        "VerificationCheck",
        "VerificationResult",
        "ALLOW",
        "DENY",
        "REQUIRE_HUMAN_APPROVAL",
        "REQUIRE_HUMAN_REVIEW",
    )
    for name in exported:
        assert name in aaid.__all__


def test_unknown_decision_is_rejected():
    with pytest.raises(ValueError):
        VerificationResult(valid=False, decision="MAYBE", reason="bad decision")


def test_failed_accepts_require_human_approval_decision():
    result = VerificationResult.failed(
        "human approval required", decision=REQUIRE_HUMAN_APPROVAL
    )
    assert result.valid is False
    assert result.decision == REQUIRE_HUMAN_APPROVAL
