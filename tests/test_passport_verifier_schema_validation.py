import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aaid import ALLOW, DENY, verify_passport_envelope

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"

STRUCTURAL_CHECK_NAMES = (
    "envelope_is_mapping",
    "passport_present",
    "passport_is_mapping",
    "proofs_present",
    "proofs_is_sequence",
    "proofs_non_empty",
)


def load_envelope():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def valid_envelope():
    """A fresh, schema-valid envelope.

    Each call re-parses the example file, so per-test mutations stay isolated.
    """
    return load_envelope()


def check_named(result, name):
    for check in result.checks:
        if check.name == name:
            return check
    return None


def test_minimal_example_passes_schema_valid_check():
    result = verify_passport_envelope(load_envelope())
    for name in STRUCTURAL_CHECK_NAMES:
        check = check_named(result, name)
        assert check is not None, f"missing structural check {name}"
        assert check.passed is True
    schema = check_named(result, "schema_valid")
    assert schema is not None
    assert schema.passed is True


def test_minimal_example_still_denied_for_unimplemented_signature():
    result = verify_passport_envelope(load_envelope())
    assert result.valid is False
    assert result.decision == DENY
    signature = check_named(result, "signature_verification_not_implemented")
    assert signature is not None
    assert signature.passed is False
    assert "signature" in result.reason.lower()


def test_structurally_valid_but_schema_invalid_records_schema_valid_false():
    envelope = {"passport": {"subject": "demo"}, "proofs": [{"proof_id": "x"}]}
    result = verify_passport_envelope(envelope)
    for name in STRUCTURAL_CHECK_NAMES:
        check = check_named(result, name)
        assert check is not None, f"missing structural check {name}"
        assert check.passed is True
    schema = check_named(result, "schema_valid")
    assert schema is not None
    assert schema.passed is False
    assert result.valid is False
    assert result.decision == DENY


def test_schema_failure_reason_is_clear_and_concise():
    envelope = {"passport": {"subject": "demo"}, "proofs": [{"proof_id": "x"}]}
    result = verify_passport_envelope(envelope)
    schema = check_named(result, "schema_valid")
    assert schema is not None
    reason = schema.reason
    assert "schema" in reason.lower()
    assert "$" in reason
    assert len(reason) < 200


def test_malformed_structural_inputs_do_not_run_schema_valid():
    malformed_cases = [
        ["passport", "proofs"],
        {"proofs": [{"proof_id": "x"}]},
        {"passport": "not-a-mapping", "proofs": [{"proof_id": "x"}]},
        {"passport": {"subject": "demo"}},
        {"passport": {"subject": "demo"}, "proofs": "signature"},
        {"passport": {"subject": "demo"}, "proofs": []},
    ]
    for case in malformed_cases:
        result = verify_passport_envelope(case)
        assert check_named(result, "schema_valid") is None, (
            f"schema_valid must not run for structurally invalid input {case!r}"
        )
        assert result.decision == DENY
        assert result.valid is False


def test_schema_validation_step_never_returns_allow():
    cases = [
        load_envelope(),
        {"passport": {"subject": "demo"}, "proofs": [{"proof_id": "x"}]},
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


def test_no_payload_hash_verification_in_this_step():
    import aaid.passport_verifier as mod

    assert not hasattr(mod, "hashlib")
    assert not hasattr(mod, "hmac")

    env = valid_envelope()
    # A different but still schema-valid hash value: the verifier must not
    # recompute or compare the payload hash, so schema validation still passes.
    env["proofs"][0]["payload_hash"] = "b" * 64
    result = verify_passport_envelope(env)
    schema = check_named(result, "schema_valid")
    assert schema is not None
    assert schema.passed is True
    signature = check_named(result, "signature_verification_not_implemented")
    assert signature is not None
    assert signature.passed is False
    assert result.decision == DENY


def test_no_signature_verification_in_this_step():
    env = valid_envelope()
    # A different but still schema-valid signature value: the verifier must not
    # verify the signature, so the deny reason stays "not implemented".
    env["proofs"][0]["signature_b64u"] = "AAAA"
    result = verify_passport_envelope(env)
    schema = check_named(result, "schema_valid")
    assert schema is not None
    assert schema.passed is True
    signature = check_named(result, "signature_verification_not_implemented")
    assert signature is not None
    assert signature.passed is False
    assert result.decision == DENY
    assert result.valid is False


def test_schema_failure_short_circuits_before_signature_check():
    envelope = {"passport": {"subject": "demo"}, "proofs": [{"proof_id": "x"}]}
    result = verify_passport_envelope(envelope)
    schema = check_named(result, "schema_valid")
    assert schema is not None
    assert schema.passed is False
    assert check_named(result, "signature_verification_not_implemented") is None


def test_specific_schema_violations_are_rejected():
    enum_env = valid_envelope()
    enum_env["passport"]["risk_class"] = "critical"
    enum_result = verify_passport_envelope(enum_env)
    for name in STRUCTURAL_CHECK_NAMES:
        assert check_named(enum_result, name).passed is True
    enum_schema = check_named(enum_result, "schema_valid")
    assert enum_schema is not None
    assert enum_schema.passed is False
    assert enum_result.decision == DENY

    extra_env = valid_envelope()
    extra_env["unexpected"] = "x"
    extra_result = verify_passport_envelope(extra_env)
    extra_schema = check_named(extra_result, "schema_valid")
    assert extra_schema is not None
    assert extra_schema.passed is False
    assert extra_result.decision == DENY
