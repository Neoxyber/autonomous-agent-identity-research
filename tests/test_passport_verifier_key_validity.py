"""Key-validity verifier-boundary tests.

These tests record current verifier behavior around selected key validity,
strict timestamp handling, optional key expiry, verification-method binding,
ordering, short-circuit behavior, raw JSON parity, and the never-ALLOW boundary.

They do not add real signature verification, cryptographic key validation, or
make the passport verifier return `ALLOW`. More tests and
research are still needed around key-validity and signature-verification
boundaries.
"""

import json
from pathlib import Path
from typing import Any

import pytest

import aaid.passport_verifier as passport_verifier_module
from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.canonicalization import hash_passport_payload
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PASSPORT_VERIFIER_SOURCE_PATH = ROOT / "src" / "aaid" / "passport_verifier.py"

RAW_JSON_CHECK = "raw_json_parsed"
KEY_CHECK = "verification_key_selected"
VALIDITY_CHECK = "verification_key_valid_for_proof"
INPUT_CHECK = "signature_input_prepared"
ALG_CHECK = "signature_algorithm_supported"
SIGNATURE_CHECK = "signature_verification_not_implemented"
PAYLOAD_CHECK = "payload_hash_valid"

KID = "urn:aaid:key:018fd7c2-8c44-72ff-91ab-2e81e9fd4422"
OTHER_KEY_AAID = "urn:aaid:key:00000000-0000-7000-8000-000000000000"

NON_STRICT_TIMESTAMPS = (
    pytest.param("2026-06-15T00:00:00+05:00", id="explicit-offset"),
    pytest.param("2026-06-15T00:00:00+00:00", id="utc-offset-not-z"),
    pytest.param("2026-06-15 00:00:00Z", id="space-separator"),
    pytest.param("2026-06-15T00:00:00.500Z", id="fractional-seconds"),
    pytest.param("2026-06-15T00:00:00z", id="lowercase-z"),
    pytest.param("2026-06-15T00:00:00Z ", id="trailing-whitespace"),
    pytest.param(" 2026-06-15T00:00:00Z", id="leading-whitespace"),
    pytest.param("2026-06-15", id="date-only"),
    pytest.param("", id="empty-string"),
    pytest.param("2026-13-01T00:00:00Z", id="invalid-month"),
    pytest.param("2026-06-15T24:00:00Z", id="invalid-hour"),
)

VERIFICATION_METHOD_MISMATCHES = (
    pytest.param(KID[:-4], id="prefix"),
    pytest.param(f"{KID}-extra", id="superstring"),
    pytest.param(KID.replace("018fd7c2", "018FD7C2"), id="case-variant"),
    pytest.param("key:018fd7c2-8c44-72ff-91ab-2e81e9fd4422", id="substring"),
)

FORBIDDEN_VERIFIER_IMPORTS = (
    "requests",
    "httpx",
    "urllib",
    "socket",
    "http.client",
    "hashlib",
    "hmac",
    "base64",
    "ssl",
    "secrets",
    "cryptography",
    "pqcrypto",
    "oqs",
)


def load_example_envelope() -> dict[str, Any]:
    return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))


def load_example_text() -> str:
    return EXAMPLE_PATH.read_text(encoding="utf-8")


def find_check(
    result: VerificationResult,
    name: str,
) -> VerificationCheck | None:
    for check in result.checks:
        if check.name == name:
            return check
    return None


def check_index(result: VerificationResult, name: str) -> int:
    for index, check in enumerate(result.checks):
        if check.name == name:
            return index
    return -1


def update_payload_hash(envelope: dict[str, Any]) -> dict[str, Any]:
    proof = envelope["proofs"][0]
    proof["payload_hash"] = hash_passport_payload(
        envelope["passport"],
        proof["hash_alg"],
    )
    return envelope


def envelope_with_key_fields(**fields: Any) -> dict[str, Any]:
    envelope = load_example_envelope()
    envelope["passport"]["public_keys"][0].update(fields)
    return update_payload_hash(envelope)


def envelope_without_key_field(field: str) -> dict[str, Any]:
    envelope = load_example_envelope()
    envelope["passport"]["public_keys"][0].pop(field, None)
    return update_payload_hash(envelope)


def envelope_with_proof_field(field: str, value: Any) -> dict[str, Any]:
    envelope = load_example_envelope()
    envelope["proofs"][0][field] = value
    return envelope


def verify_trusted_envelope(envelope: Any) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def make_key(**overrides: Any) -> dict[str, Any]:
    key = {
        "kid": KID,
        "kty": "ML-DSA",
        "alg": "ML-DSA-65",
        "purpose": "sig",
        "status": "active",
        "created_at": "2026-05-29T00:00:00Z",
    }
    key.update(overrides)
    return key


def make_proof(verification_method: str = KID) -> dict[str, str]:
    return {
        "verification_method": verification_method,
        "kid": KID,
        "alg": "ML-DSA-65",
    }


def run_key_validity_check(
    key: dict[str, Any],
    proof: dict[str, str],
) -> VerificationCheck:
    return passport_verifier_module._verification_key_valid_for_proof_check(
        key,
        proof,
        VALID_NOW,
    )


def test_minimal_example_passes_key_validity_and_still_denies() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    validity = find_check(result, VALIDITY_CHECK)
    signature = find_check(result, SIGNATURE_CHECK)

    assert validity is not None
    assert signature is not None
    assert validity.passed is True
    assert signature.passed is False

    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False


def test_missing_optional_not_after_passes() -> None:
    envelope = load_example_envelope()
    assert "not_after" not in envelope["passport"]["public_keys"][0]

    result = verify_trusted_envelope(envelope)

    validity = find_check(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is True


def test_created_at_after_now_fails_closed_before_signature_input() -> None:
    result = verify_trusted_envelope(
        envelope_with_key_fields(created_at="2026-06-20T00:00:00Z"),
    )

    validity = find_check(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is False

    assert find_check(result, INPUT_CHECK) is None
    assert find_check(result, SIGNATURE_CHECK) is None
    assert result.decision == DENY
    assert result.valid is False


def test_created_at_equal_now_passes() -> None:
    result = verify_trusted_envelope(
        envelope_with_key_fields(created_at="2026-06-15T00:00:00Z"),
    )

    validity = find_check(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is True


@pytest.mark.parametrize("bad_timestamp", NON_STRICT_TIMESTAMPS)
def test_malformed_created_at_fails_closed(bad_timestamp: str) -> None:
    result = verify_trusted_envelope(
        envelope_with_key_fields(created_at=bad_timestamp),
    )

    validity = find_check(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is False

    assert find_check(result, INPUT_CHECK) is None
    assert result.decision == DENY


def test_not_after_before_now_fails_closed() -> None:
    result = verify_trusted_envelope(
        envelope_with_key_fields(not_after="2026-06-10T00:00:00Z"),
    )

    validity = find_check(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is False

    assert find_check(result, INPUT_CHECK) is None
    assert result.decision == DENY


def test_not_after_equal_now_fails_closed() -> None:
    result = verify_trusted_envelope(
        envelope_with_key_fields(not_after="2026-06-15T00:00:00Z"),
    )

    validity = find_check(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is False
    assert result.decision == DENY


def test_not_after_after_now_passes() -> None:
    result = verify_trusted_envelope(
        envelope_with_key_fields(not_after="2026-06-20T00:00:00Z"),
    )

    validity = find_check(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is True


@pytest.mark.parametrize("bad_timestamp", NON_STRICT_TIMESTAMPS)
def test_malformed_not_after_fails_closed(bad_timestamp: str) -> None:
    result = verify_trusted_envelope(
        envelope_with_key_fields(not_after=bad_timestamp),
    )

    validity = find_check(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is False
    assert result.decision == DENY


def test_inverted_window_created_after_not_after_fails_closed() -> None:
    result = verify_trusted_envelope(
        envelope_with_key_fields(
            created_at="2026-06-14T00:00:00Z",
            not_after="2026-06-10T00:00:00Z",
        ),
    )

    validity = find_check(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is False
    assert result.decision == DENY


def test_verification_method_mismatch_fails_closed() -> None:
    result = verify_trusted_envelope(
        envelope_with_proof_field("verification_method", OTHER_KEY_AAID),
    )

    key_check = find_check(result, KEY_CHECK)
    validity = find_check(result, VALIDITY_CHECK)

    assert key_check is not None
    assert validity is not None
    assert key_check.passed is True
    assert validity.passed is False

    assert find_check(result, INPUT_CHECK) is None
    assert result.decision == DENY


def test_helper_exact_binding_passes() -> None:
    check = run_key_validity_check(make_key(), make_proof(KID))

    assert check.name == VALIDITY_CHECK
    assert check.passed is True


@pytest.mark.parametrize("verification_method", VERIFICATION_METHOD_MISMATCHES)
def test_helper_rejects_prefix_substring_superstring_and_case(
    verification_method: str,
) -> None:
    assert verification_method != KID

    check = run_key_validity_check(make_key(), make_proof(verification_method))

    assert check.name == VALIDITY_CHECK
    assert check.passed is False


def test_helper_missing_created_at_fails_closed() -> None:
    key = make_key()
    key.pop("created_at", None)

    check = run_key_validity_check(key, make_proof(KID))

    assert check.passed is False


def test_helper_missing_not_after_passes() -> None:
    check = run_key_validity_check(make_key(), make_proof(KID))

    assert check.passed is True


def test_validity_runs_after_key_selected_and_before_signature_input() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    key_index = check_index(result, KEY_CHECK)
    validity_index = check_index(result, VALIDITY_CHECK)
    input_index = check_index(result, INPUT_CHECK)

    assert -1 not in (key_index, validity_index, input_index)
    assert key_index < validity_index < input_index


def test_key_selection_failure_short_circuits_before_validity() -> None:
    result = verify_trusted_envelope(
        envelope_with_proof_field("kid", "urn:aaid:key:no-such-key-0001"),
    )

    key_check = find_check(result, KEY_CHECK)
    assert key_check is not None
    assert key_check.passed is False

    assert find_check(result, VALIDITY_CHECK) is None
    assert find_check(result, INPUT_CHECK) is None


def test_payload_hash_failure_short_circuits_before_validity() -> None:
    envelope = load_example_envelope()
    envelope["proofs"][0]["payload_hash"] = "0" * 64

    result = verify_trusted_envelope(envelope)

    payload = find_check(result, PAYLOAD_CHECK)
    assert payload is not None
    assert payload.passed is False
    assert find_check(result, VALIDITY_CHECK) is None


def test_key_validity_step_never_returns_allow() -> None:
    cases = [
        load_example_envelope(),
        envelope_with_key_fields(created_at="2026-06-20T00:00:00Z"),
        envelope_with_key_fields(not_after="2026-06-10T00:00:00Z"),
        envelope_with_key_fields(not_after="2026-06-15T00:00:00Z"),
        envelope_with_key_fields(created_at="2026-06-15T00:00:00Z"),
        envelope_with_key_fields(created_at="bad-timestamp"),
        envelope_with_proof_field("verification_method", OTHER_KEY_AAID),
    ]

    reached = verify_trusted_envelope(load_example_envelope())
    assert find_check(reached, VALIDITY_CHECK) is not None

    for envelope in cases:
        result = verify_trusted_envelope(envelope)

        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW, f"unexpected ALLOW for {envelope!r}"
        assert result.decision == DENY
        assert result.valid is False


def test_raw_json_parity_includes_key_validity() -> None:
    direct = verify_trusted_envelope(load_example_envelope())
    raw = verify_passport_json(
        load_example_text(),
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )

    validity = find_check(raw, VALIDITY_CHECK)

    assert raw.checks[0].name == RAW_JSON_CHECK
    assert raw.checks[1:] == direct.checks
    assert raw.reason == direct.reason
    assert raw.decision == direct.decision
    assert validity is not None
    assert validity.passed is True


def test_no_forbidden_imports_after_key_validity() -> None:
    for name in FORBIDDEN_VERIFIER_IMPORTS:
        top_level_name = name.split(".")[0]
        assert not hasattr(passport_verifier_module, top_level_name), (
            f"verifier must not import {name}"
        )

    source = PASSPORT_VERIFIER_SOURCE_PATH.read_text(encoding="utf-8")
    for name in FORBIDDEN_VERIFIER_IMPORTS:
        assert f"import {name}" not in source
        assert f"from {name}" not in source
