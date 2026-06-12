"""Canonicalization-scheme verifier-boundary tests.

These tests record current verifier behavior around the
`signature_canonicalization_supported` check.

They do not adopt an external canonicalizer, add real signature verification, or
make the passport verifier return `ALLOW`. More tests and research are still
needed around canonicalization-scheme and signature-verification boundaries.
"""

import json
from pathlib import Path
from typing import Any

import pytest

import aaid.passport_verifier as passport_verifier_module
from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PASSPORT_VERIFIER_SOURCE_PATH = ROOT / "src" / "aaid" / "passport_verifier.py"

SCHEMA_CHECK = "schema_valid"
ENVELOPE_MAPPING_CHECK = "envelope_is_mapping"
KEY_CHECK = "verification_key_selected"
CANONICALIZATION_CHECK = "signature_canonicalization_supported"
INPUT_CHECK = "signature_input_prepared"
ALGORITHM_CHECK = "signature_algorithm_supported"
SIGNATURE_CHECK = "signature_verification_not_implemented"
PAYLOAD_CHECK = "payload_hash_valid"

EMPTY_ALLOWLIST = ()

FORBIDDEN_VERIFIER_IMPORTS = (
    "hashlib",
    "hmac",
    "base64",
    "ssl",
    "secrets",
    "cryptography",
    "pqcrypto",
    "oqs",
    "requests",
    "httpx",
    "socket",
    "urllib",
)


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


def check_index(result: VerificationResult, name: str) -> int:
    for index, check in enumerate(result.checks):
        if check.name == name:
            return index
    return -1


def verify_envelope(envelope: Any) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def force_unsupported_canonicalization(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        passport_verifier_module,
        "_SUPPORTED_SIGNATURE_CANONICALIZATIONS",
        EMPTY_ALLOWLIST,
    )


def test_minimal_example_reaches_canonicalization_supported_passed() -> None:
    result = verify_envelope(load_example_envelope())

    key = find_check(result, KEY_CHECK)
    assert key is not None
    assert key.passed is True

    canonicalization = find_check(result, CANONICALIZATION_CHECK)
    assert canonicalization is not None
    assert canonicalization.passed is True


def test_canonicalization_supported_between_key_selected_and_input() -> None:
    result = verify_envelope(load_example_envelope())

    key_index = check_index(result, KEY_CHECK)
    canonicalization_index = check_index(result, CANONICALIZATION_CHECK)
    input_index = check_index(result, INPUT_CHECK)

    assert key_index != -1
    assert canonicalization_index != -1
    assert input_index != -1
    assert key_index < canonicalization_index < input_index


def test_unsupported_canonicalization_value_fails_check_directly() -> None:
    check = passport_verifier_module._signature_canonicalization_supported_check(
        {"canonicalization": "some-unsupported-scheme"}
    )

    assert check.name == CANONICALIZATION_CHECK
    assert check.passed is False


def test_unsupported_canonicalization_returns_deny(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    force_unsupported_canonicalization(monkeypatch)

    result = verify_envelope(load_example_envelope())

    canonicalization = find_check(result, CANONICALIZATION_CHECK)
    assert canonicalization is not None
    assert canonicalization.passed is False

    assert result.decision == DENY
    assert result.valid is False


@pytest.mark.parametrize(
    "later_check",
    [
        pytest.param(INPUT_CHECK, id="before-signature-input"),
        pytest.param(ALGORITHM_CHECK, id="before-algorithm"),
        pytest.param(SIGNATURE_CHECK, id="before-signature"),
    ],
)
def test_unsupported_canonicalization_short_circuits_before_later_steps(
    monkeypatch: pytest.MonkeyPatch,
    later_check: str,
) -> None:
    force_unsupported_canonicalization(monkeypatch)

    result = verify_envelope(load_example_envelope())

    canonicalization = find_check(result, CANONICALIZATION_CHECK)
    assert canonicalization is not None
    assert canonicalization.passed is False
    assert find_check(result, later_check) is None


def test_key_selection_failure_short_circuits_before_canonicalization() -> None:
    envelope = load_example_envelope()
    envelope["proofs"][0]["kid"] = "urn:aaid:key:no-such-key-canon-0001"

    result = verify_envelope(envelope)

    key = find_check(result, KEY_CHECK)
    assert key is not None
    assert key.passed is False
    assert find_check(result, CANONICALIZATION_CHECK) is None


def test_payload_hash_failure_short_circuits_before_canonicalization() -> None:
    envelope = load_example_envelope()
    envelope["proofs"][0]["payload_hash"] = "0" * 64

    result = verify_envelope(envelope)

    payload = find_check(result, PAYLOAD_CHECK)
    assert payload is not None
    assert payload.passed is False
    assert find_check(result, CANONICALIZATION_CHECK) is None


def test_schema_failure_short_circuits_before_canonicalization() -> None:
    envelope = load_example_envelope()
    envelope["proofs"][0]["unexpected_field"] = "x"

    result = verify_passport_envelope(envelope)

    schema = find_check(result, SCHEMA_CHECK)
    assert schema is not None
    assert schema.passed is False
    assert find_check(result, CANONICALIZATION_CHECK) is None


def test_structural_failure_short_circuits_before_canonicalization() -> None:
    result = verify_passport_envelope(["passport", "proofs"])

    envelope_mapping = find_check(result, ENVELOPE_MAPPING_CHECK)
    assert envelope_mapping is not None
    assert envelope_mapping.passed is False
    assert find_check(result, CANONICALIZATION_CHECK) is None


def test_canonicalization_scheme_step_never_returns_allow() -> None:
    cases = [
        load_example_envelope(),
        {"passport": {"subject": "demo"}, "proofs": [{"proof_id": "x"}]},
        {"passport": {"subject": "demo"}, "proofs": []},
        {},
        None,
    ]

    reached = verify_envelope(load_example_envelope())
    assert find_check(reached, CANONICALIZATION_CHECK) is not None

    for case in cases:
        result = verify_envelope(case)

        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.valid is False


def test_signature_verification_still_not_implemented() -> None:
    result = verify_envelope(load_example_envelope())

    signature = find_check(result, SIGNATURE_CHECK)
    assert signature is not None
    assert signature.passed is False


def test_passport_verifier_imports_no_crypto_or_network_modules() -> None:
    for module_name in FORBIDDEN_VERIFIER_IMPORTS:
        assert not hasattr(passport_verifier_module, module_name), (
            f"passport_verifier must not import {module_name}"
        )

    source = PASSPORT_VERIFIER_SOURCE_PATH.read_text(encoding="utf-8")
    for module_name in FORBIDDEN_VERIFIER_IMPORTS:
        assert f"import {module_name}" not in source
        assert f"from {module_name}" not in source
