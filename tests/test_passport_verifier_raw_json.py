"""Tests for the raw JSON verifier entry point.

These cases keep raw JSON parsing and duplicate-key rejection before schema
validation and before the parsed-object verifier path.

A parsed raw JSON envelope does not grant `ALLOW`. More research and testing are
needed to improve raw JSON verifier boundaries over time.
"""

import json
from pathlib import Path
from typing import Any

from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"

RAW_JSON_CHECK = "raw_json_parsed"
ENVELOPE_MAPPING_CHECK = "envelope_is_mapping"
SCHEMA_CHECK = "schema_valid"
PAYLOAD_CHECK = "payload_hash_valid"
SIGNATURE_CHECK = "signature_verification_not_implemented"

MALFORMED_JSON = '{"passport": }'
DUPLICATE_ENVELOPE_KEY_JSON = '{"passport": {}, "passport": {}, "proofs": []}'
DUPLICATE_PASSPORT_KEY_JSON = (
    '{"passport": {"agent_id": "good", "agent_id": "bad"}, "proofs": []}'
)
DUPLICATE_PROOF_KEY_JSON = (
    '{"passport": {}, "proofs": [{"kid": "good", "kid": "bad"}]}'
)

PARSE_FAILURE_CASES = (
    MALFORMED_JSON,
    DUPLICATE_ENVELOPE_KEY_JSON,
    DUPLICATE_PASSPORT_KEY_JSON,
    DUPLICATE_PROOF_KEY_JSON,
)

NON_ENVELOPE_JSON_CASES = (
    "[]",
    "null",
    "42",
)


def load_example_text() -> str:
    return EXAMPLE_PATH.read_text(encoding="utf-8")


def load_example_envelope() -> dict[str, Any]:
    return json.loads(load_example_text())


def find_check(
    result: VerificationResult,
    name: str,
) -> VerificationCheck | None:
    for check in result.checks:
        if check.name == name:
            return check
    return None


def verify_trusted_raw_json(raw_json: str) -> VerificationResult:
    return verify_passport_json(
        raw_json,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def verify_with_injected_now(envelope: dict[str, Any]) -> VerificationResult:
    return verify_passport_envelope(envelope, now=VALID_NOW)


def verify_raw_json_with_injected_now(raw_json: str) -> VerificationResult:
    return verify_passport_json(raw_json, now=VALID_NOW)


def assert_raw_json_parse_failed(result: VerificationResult) -> None:
    raw = find_check(result, RAW_JSON_CHECK)

    assert raw is not None
    assert raw.passed is False
    assert result.decision == DENY
    assert result.valid is False


def test_verify_passport_json_importable_from_module() -> None:
    import aaid.passport_verifier as module

    assert module.verify_passport_json is verify_passport_json


def test_verify_passport_json_exported_from_package() -> None:
    import aaid

    assert "verify_passport_json" in aaid.__all__
    assert aaid.verify_passport_json is verify_passport_json


def test_valid_raw_json_reaches_existing_verifier_path() -> None:
    result = verify_trusted_raw_json(load_example_text())

    raw = find_check(result, RAW_JSON_CHECK)
    schema = find_check(result, SCHEMA_CHECK)
    payload_hash = find_check(result, PAYLOAD_CHECK)
    signature = find_check(result, SIGNATURE_CHECK)

    assert raw is not None
    assert schema is not None
    assert payload_hash is not None
    assert signature is not None

    assert raw.passed is True
    assert schema.passed is True
    assert payload_hash.passed is True
    assert signature.passed is False

    assert result.decision == DENY
    assert result.valid is False


def test_raw_json_parsed_check_is_first_on_success() -> None:
    result = verify_raw_json_with_injected_now(load_example_text())

    assert result.checks[0].name == RAW_JSON_CHECK
    assert result.checks[0].passed is True
    assert result.checks[1].name == ENVELOPE_MAPPING_CHECK


def test_malformed_json_fails_raw_json_parsed() -> None:
    result = verify_passport_json(MALFORMED_JSON)

    assert_raw_json_parse_failed(result)


def test_duplicate_envelope_key_fails_raw_json_parsed() -> None:
    result = verify_passport_json(DUPLICATE_ENVELOPE_KEY_JSON)

    assert_raw_json_parse_failed(result)


def test_duplicate_passport_key_fails_raw_json_parsed() -> None:
    result = verify_passport_json(DUPLICATE_PASSPORT_KEY_JSON)

    assert_raw_json_parse_failed(result)


def test_duplicate_proof_key_fails_raw_json_parsed() -> None:
    result = verify_passport_json(DUPLICATE_PROOF_KEY_JSON)

    assert_raw_json_parse_failed(result)


def test_parse_failures_do_not_include_schema_valid() -> None:
    for raw_json in PARSE_FAILURE_CASES:
        result = verify_passport_json(raw_json)

        assert_raw_json_parse_failed(result)
        assert find_check(result, SCHEMA_CHECK) is None


def test_raw_json_verifier_never_returns_allow() -> None:
    cases = [
        load_example_text(),
        *PARSE_FAILURE_CASES,
        *NON_ENVELOPE_JSON_CASES,
    ]

    for raw_json in cases:
        result = verify_passport_json(raw_json)

        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.decision == DENY
        assert result.valid is False


def test_parsed_object_verifier_remains_available_and_unchanged() -> None:
    direct = verify_with_injected_now(load_example_envelope())
    raw = verify_raw_json_with_injected_now(load_example_text())

    assert direct.checks[0].name == ENVELOPE_MAPPING_CHECK
    assert find_check(direct, RAW_JSON_CHECK) is None

    assert raw.checks[0].name == RAW_JSON_CHECK
    assert raw.checks[1:] == direct.checks
    assert raw.reason == direct.reason
    assert raw.decision == direct.decision
