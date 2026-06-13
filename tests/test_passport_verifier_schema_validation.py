"""Tests for the schema validation verifier boundary.

These cases keep structural checks before schema validation and keep schema
failure before later signature-stage checks.

A schema-valid envelope still does not grant `ALLOW`. More research and testing
are needed to improve schema-validation boundaries over time.
"""

import json
from pathlib import Path
from typing import Any

from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"

STRUCTURAL_CHECK_NAMES = (
    "envelope_is_mapping",
    "passport_present",
    "passport_is_mapping",
    "proofs_present",
    "proofs_is_sequence",
    "proofs_non_empty",
)

SCHEMA_CHECK = "schema_valid"
SIGNATURE_CHECK = "signature_verification_not_implemented"


def load_example_envelope() -> dict[str, Any]:
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def make_valid_envelope() -> dict[str, Any]:
    """Return a fresh schema-valid envelope for isolated per-test mutation."""
    return load_example_envelope()


def make_schema_invalid_envelope() -> dict[str, Any]:
    return {"passport": {"subject": "demo"}, "proofs": [{"proof_id": "x"}]}


def malformed_structural_inputs() -> tuple[Any, ...]:
    return (
        ["passport", "proofs"],
        {"proofs": [{"proof_id": "x"}]},
        {"passport": "not-a-mapping", "proofs": [{"proof_id": "x"}]},
        {"passport": {"subject": "demo"}},
        {"passport": {"subject": "demo"}, "proofs": "signature"},
        {"passport": {"subject": "demo"}, "proofs": []},
    )


def find_check(
    result: VerificationResult,
    name: str,
) -> VerificationCheck | None:
    for check in result.checks:
        if check.name == name:
            return check
    return None


def verify_trusted_envelope(envelope: dict[str, Any]) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def assert_structural_checks_passed(result: VerificationResult) -> None:
    for name in STRUCTURAL_CHECK_NAMES:
        check = find_check(result, name)

        assert check is not None, f"missing structural check {name}"
        assert check.passed is True


def test_minimal_example_passes_schema_valid_check() -> None:
    result = verify_passport_envelope(load_example_envelope())

    assert_structural_checks_passed(result)

    schema = find_check(result, SCHEMA_CHECK)

    assert schema is not None
    assert schema.passed is True


def test_minimal_example_still_denied_for_unimplemented_signature() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    signature = find_check(result, SIGNATURE_CHECK)

    assert signature is not None
    assert signature.passed is False
    assert "signature" in result.reason.lower()
    assert result.decision == DENY
    assert result.valid is False


def test_structurally_valid_but_schema_invalid_records_schema_valid_false() -> None:
    result = verify_passport_envelope(make_schema_invalid_envelope())

    assert_structural_checks_passed(result)

    schema = find_check(result, SCHEMA_CHECK)

    assert schema is not None
    assert schema.passed is False
    assert result.decision == DENY
    assert result.valid is False


def test_schema_failure_reason_is_clear_and_concise() -> None:
    result = verify_passport_envelope(make_schema_invalid_envelope())
    schema = find_check(result, SCHEMA_CHECK)

    assert schema is not None

    reason = schema.reason

    assert "schema" in reason.lower()
    assert "$" in reason
    assert len(reason) < 200


def test_malformed_structural_inputs_do_not_run_schema_valid() -> None:
    for case in malformed_structural_inputs():
        result = verify_passport_envelope(case)

        assert find_check(result, SCHEMA_CHECK) is None
        assert result.decision == DENY
        assert result.valid is False


def test_schema_validation_step_never_returns_allow() -> None:
    cases = [
        load_example_envelope(),
        make_schema_invalid_envelope(),
        {},
        {"passport": {"subject": "demo"}},
        ["passport", "proofs"],
        {"passport": {"subject": "demo"}, "proofs": []},
        None,
        42,
        "x",
    ]

    for case in cases:
        result = verify_passport_envelope(case)

        assert result.decision != ALLOW, f"unexpected ALLOW for {case!r}"
        assert result.decision == DENY
        assert result.valid is False


def test_no_signature_verification_in_this_step() -> None:
    envelope = make_valid_envelope()

    # A different but still schema-valid signature value: the verifier must not
    # verify the signature, so the deny reason stays "not implemented".
    envelope["proofs"][0]["signature_b64u"] = "AAAA"

    result = verify_trusted_envelope(envelope)
    schema = find_check(result, SCHEMA_CHECK)
    signature = find_check(result, SIGNATURE_CHECK)

    assert schema is not None
    assert schema.passed is True

    assert signature is not None
    assert signature.passed is False

    assert result.decision == DENY
    assert result.valid is False


def test_schema_failure_short_circuits_before_signature_check() -> None:
    result = verify_passport_envelope(make_schema_invalid_envelope())
    schema = find_check(result, SCHEMA_CHECK)

    assert schema is not None
    assert schema.passed is False
    assert find_check(result, SIGNATURE_CHECK) is None


def test_specific_schema_violations_are_rejected() -> None:
    enum_envelope = make_valid_envelope()
    enum_envelope["passport"]["risk_class"] = "critical"

    enum_result = verify_passport_envelope(enum_envelope)
    enum_schema = find_check(enum_result, SCHEMA_CHECK)

    assert_structural_checks_passed(enum_result)

    assert enum_schema is not None
    assert enum_schema.passed is False
    assert enum_result.decision == DENY

    extra_envelope = make_valid_envelope()
    extra_envelope["unexpected"] = "x"

    extra_result = verify_passport_envelope(extra_envelope)
    extra_schema = find_check(extra_result, SCHEMA_CHECK)

    assert extra_schema is not None
    assert extra_schema.passed is False
    assert extra_result.decision == DENY
