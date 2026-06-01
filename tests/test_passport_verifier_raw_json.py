import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.verification import VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"


def load_text():
    return EXAMPLE_PATH.read_text(encoding="utf-8")


def load_envelope():
    return json.loads(load_text())


def check_named(result, name):
    for check in result.checks:
        if check.name == name:
            return check
    return None


def test_verify_passport_json_importable_from_module():
    import aaid.passport_verifier as module

    assert module.verify_passport_json is verify_passport_json


def test_verify_passport_json_exported_from_package():
    import aaid

    assert "verify_passport_json" in aaid.__all__
    assert aaid.verify_passport_json is verify_passport_json


def test_valid_raw_json_reaches_existing_verifier_path():
    result = verify_passport_json(load_text())

    assert result.decision == DENY
    assert result.valid is False
    assert check_named(result, "raw_json_parsed").passed is True
    assert check_named(result, "schema_valid").passed is True
    assert check_named(result, "payload_hash_valid").passed is True
    signature = check_named(result, "signature_verification_not_implemented")
    assert signature is not None
    assert signature.passed is False


def test_raw_json_parsed_check_is_first_on_success():
    result = verify_passport_json(load_text())

    assert result.checks[0].name == "raw_json_parsed"
    assert result.checks[0].passed is True
    assert result.checks[1].name == "envelope_is_mapping"


def test_malformed_json_fails_raw_json_parsed():
    result = verify_passport_json('{"passport": }')

    assert result.decision == DENY
    assert result.valid is False
    raw = check_named(result, "raw_json_parsed")
    assert raw is not None
    assert raw.passed is False


def test_duplicate_top_level_key_fails_raw_json_parsed():
    result = verify_passport_json('{"passport": {}, "passport": {}, "proofs": []}')

    assert result.decision == DENY
    assert check_named(result, "raw_json_parsed").passed is False


def test_duplicate_nested_passport_key_fails_raw_json_parsed():
    result = verify_passport_json(
        '{"passport": {"agent_id": "good", "agent_id": "bad"}, "proofs": []}'
    )

    assert result.decision == DENY
    assert check_named(result, "raw_json_parsed").passed is False


def test_duplicate_proof_key_fails_raw_json_parsed():
    result = verify_passport_json(
        '{"passport": {}, "proofs": [{"kid": "good", "kid": "bad"}]}'
    )

    assert result.decision == DENY
    assert check_named(result, "raw_json_parsed").passed is False


def test_parse_failures_do_not_include_schema_valid():
    cases = [
        '{"passport": }',
        '{"passport": {}, "passport": {}, "proofs": []}',
        '{"passport": {"agent_id": "good", "agent_id": "bad"}, "proofs": []}',
        '{"passport": {}, "proofs": [{"kid": "good", "kid": "bad"}]}',
    ]

    for text in cases:
        result = verify_passport_json(text)
        assert check_named(result, "raw_json_parsed").passed is False
        assert check_named(result, "schema_valid") is None


def test_raw_json_verifier_never_returns_allow():
    cases = [
        load_text(),
        '{"passport": }',
        '{"passport": {}, "passport": {}, "proofs": []}',
        "[]",
        "null",
        "42",
    ]

    for text in cases:
        result = verify_passport_json(text)
        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.decision == DENY
        assert result.valid is False


def test_parsed_object_verifier_remains_available_and_unchanged():
    direct = verify_passport_envelope(load_envelope())
    raw = verify_passport_json(load_text())

    assert direct.checks[0].name == "envelope_is_mapping"
    assert check_named(direct, "raw_json_parsed") is None
    assert raw.checks[0].name == "raw_json_parsed"
    assert raw.checks[1:] == direct.checks
    assert raw.reason == direct.reason
    assert raw.decision == direct.decision
