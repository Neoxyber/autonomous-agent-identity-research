"""Canonical payload verifier-boundary tests.

These tests record current verifier behavior around canonical payload
preparation, raw JSON parity, signature-input reuse, and fail-closed
canonicalization errors.

They do not adopt an external canonicalizer, add real signature verification, or
make the passport verifier return `ALLOW`. More tests and research are still
needed around canonicalization and signature-verification boundaries.
"""

import json
from pathlib import Path
from typing import Any

import aaid.passport_verifier as passport_verifier_module
from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.canonicalization import canonicalize_passport_payload
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PASSPORT_VERIFIER_SOURCE_PATH = ROOT / "src" / "aaid" / "passport_verifier.py"

RAW_JSON_CHECK = "raw_json_parsed"
PROOF_CHECK = "proof_selected"
PREPARED_CHECK = "canonical_payload_prepared"
PAYLOAD_CHECK = "payload_hash_valid"
KEY_CHECK = "verification_key_selected"
KEY_VALIDITY_CHECK = "verification_key_valid_for_proof"
CANONICALIZATION_SCHEME_CHECK = "signature_canonicalization_supported"
INPUT_CHECK = "signature_input_prepared"
ALGORITHM_CHECK = "signature_algorithm_supported"
SIGNATURE_CHECK = "signature_verification_not_implemented"

LATER_CHECKS_AFTER_CANONICAL_PAYLOAD_FAILURE = (
    PAYLOAD_CHECK,
    KEY_CHECK,
    KEY_VALIDITY_CHECK,
    CANONICALIZATION_SCHEME_CHECK,
    INPUT_CHECK,
    ALGORITHM_CHECK,
    SIGNATURE_CHECK,
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
    "rfc8785",
    "jcs",
)


def load_example_envelope() -> dict[str, Any]:
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_example_text() -> str:
    return EXAMPLE_PATH.read_text(encoding="utf-8")


def load_example_passport() -> dict[str, Any]:
    return load_example_envelope()["passport"]


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


def verify_envelope(envelope: dict[str, Any]) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


class _FakeCanonicalizerError(Exception):
    """A candidate-canonicalizer-style error, defined without importing REF-014."""


def _raise_value_error(_passport: dict[str, Any]) -> bytes:
    raise ValueError("simulated canonicalization failure")


def _raise_candidate_error(_passport: dict[str, Any]) -> bytes:
    raise _FakeCanonicalizerError("simulated candidate-canonicalizer failure")


def test_minimal_example_records_canonical_payload_prepared_passed() -> None:
    result = verify_envelope(load_example_envelope())

    prepared = find_check(result, PREPARED_CHECK)
    assert prepared is not None
    assert prepared.passed is True

    signature = find_check(result, SIGNATURE_CHECK)
    assert signature is not None
    assert signature.passed is False

    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False


def test_canonical_payload_prepared_ordering() -> None:
    result = verify_envelope(load_example_envelope())

    proof_index = check_index(result, PROOF_CHECK)
    prepared_index = check_index(result, PREPARED_CHECK)
    payload_index = check_index(result, PAYLOAD_CHECK)
    input_index = check_index(result, INPUT_CHECK)

    assert -1 not in (proof_index, prepared_index, payload_index, input_index)
    assert proof_index < prepared_index < payload_index
    assert prepared_index < input_index


def test_canonicalization_value_error_fails_closed(monkeypatch: Any) -> None:
    monkeypatch.setattr(
        passport_verifier_module.canonicalization,
        "canonicalize_passport_payload",
        _raise_value_error,
    )

    result = verify_envelope(load_example_envelope())

    assert isinstance(result, VerificationResult)

    prepared = find_check(result, PREPARED_CHECK)
    assert prepared is not None
    assert prepared.passed is False

    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False

    for name in LATER_CHECKS_AFTER_CANONICAL_PAYLOAD_FAILURE:
        assert find_check(result, name) is None, (
            f"{name} must not run after canonical payload preparation fails"
        )


def test_candidate_canonicalizer_error_fails_closed(monkeypatch: Any) -> None:
    monkeypatch.setattr(
        passport_verifier_module.canonicalization,
        "canonicalize_passport_payload",
        _raise_candidate_error,
    )

    result = verify_envelope(load_example_envelope())

    assert isinstance(result, VerificationResult)

    prepared = find_check(result, PREPARED_CHECK)
    assert prepared is not None
    assert prepared.passed is False

    assert result.decision == DENY
    assert result.valid is False
    assert find_check(result, PAYLOAD_CHECK) is None
    assert find_check(result, SIGNATURE_CHECK) is None


def test_raw_json_parity_includes_canonical_payload_prepared() -> None:
    direct = verify_envelope(load_example_envelope())
    raw = verify_passport_json(
        load_example_text(),
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )

    assert raw.checks[0].name == RAW_JSON_CHECK
    assert raw.checks[1:] == direct.checks
    assert raw.reason == direct.reason
    assert raw.decision == direct.decision

    prepared = find_check(raw, PREPARED_CHECK)
    assert prepared is not None
    assert prepared.passed is True


def test_raw_json_canonicalization_failure_fails_closed(monkeypatch: Any) -> None:
    monkeypatch.setattr(
        passport_verifier_module.canonicalization,
        "canonicalize_passport_payload",
        _raise_value_error,
    )

    result = verify_passport_json(
        load_example_text(),
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )

    assert isinstance(result, VerificationResult)

    raw_json_parsed = find_check(result, RAW_JSON_CHECK)
    assert raw_json_parsed is not None
    assert raw_json_parsed.passed is True

    prepared = find_check(result, PREPARED_CHECK)
    assert prepared is not None
    assert prepared.passed is False

    assert find_check(result, PAYLOAD_CHECK) is None
    assert result.decision == DENY
    assert result.valid is False


def test_prepare_signature_input_default_path_canonicalizes() -> None:
    passport = load_example_passport()

    check, data = passport_verifier_module._prepare_signature_input(passport)

    assert check.name == INPUT_CHECK
    assert check.passed is True
    assert data == canonicalize_passport_payload(passport)


def test_prepare_signature_input_reuses_provided_bytes() -> None:
    passport = load_example_passport()
    sentinel = b"sentinel-canonical-bytes"

    check, data = passport_verifier_module._prepare_signature_input(
        passport,
        canonical_payload=sentinel,
    )

    assert check.name == INPUT_CHECK
    assert check.passed is True
    assert data == sentinel


def test_canonical_payload_step_never_returns_allow(monkeypatch: Any) -> None:
    reached = verify_envelope(load_example_envelope())
    assert find_check(reached, PREPARED_CHECK) is not None

    monkeypatch.setattr(
        passport_verifier_module.canonicalization,
        "canonicalize_passport_payload",
        _raise_value_error,
    )

    result = verify_envelope(load_example_envelope())

    assert isinstance(result, VerificationResult)
    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False


def test_no_forbidden_imports_after_canonical_payload() -> None:
    for name in FORBIDDEN_VERIFIER_IMPORTS:
        top_level_name = name.split(".")[0]
        assert not hasattr(passport_verifier_module, top_level_name), (
            f"verifier must not import {name}"
        )

    source = PASSPORT_VERIFIER_SOURCE_PATH.read_text(encoding="utf-8")
    for name in FORBIDDEN_VERIFIER_IMPORTS:
        assert f"import {name}" not in source
        assert f"from {name}" not in source
