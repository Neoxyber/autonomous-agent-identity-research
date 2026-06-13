"""Tests for the signature input verifier boundary.

These cases keep the prepared signature input bound to the canonical passport
payload bytes while keeping detached proof and signature material outside the
signed payload.

A prepared signature input does not grant `ALLOW`. More research and testing are
needed before real signature verification can be added.
"""

import copy
import json
from pathlib import Path
from typing import Any

import aaid.passport_verifier as passport_verifier_module
from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.canonicalization import (
    canonicalize_passport_payload,
    hash_passport_payload,
)
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PASSPORT_VERIFIER_SOURCE_PATH = ROOT / "src" / "aaid" / "passport_verifier.py"

KEY_SELECTED_CHECK = "verification_key_selected"
SIGNATURE_INPUT_CHECK = "signature_input_prepared"
ALGORITHM_SUPPORTED_CHECK = "signature_algorithm_supported"
SIGNATURE_CHECK = "signature_verification_not_implemented"
PAYLOAD_HASH_CHECK = "payload_hash_valid"
SCHEMA_CHECK = "schema_valid"
ENVELOPE_IS_MAPPING_CHECK = "envelope_is_mapping"

FORBIDDEN_CRYPTO_OR_NETWORK_IMPORTS = (
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


def find_check_index(result: VerificationResult, name: str) -> int:
    for index, check in enumerate(result.checks):
        if check.name == name:
            return index
    return -1


def verify_with_trusted_context(envelope: Any) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def assert_check_passed(result: VerificationResult, name: str) -> None:
    check = find_check(result, name)

    assert check is not None
    assert check.passed is True


def assert_check_failed(result: VerificationResult, name: str) -> None:
    check = find_check(result, name)

    assert check is not None
    assert check.passed is False


def prepare_signature_input(
    passport: dict[str, Any],
) -> tuple[VerificationCheck, bytes | None]:
    return passport_verifier_module._prepare_signature_input(passport)


def rehash_envelope(envelope: dict[str, Any]) -> dict[str, Any]:
    proof = envelope["proofs"][0]
    proof["payload_hash"] = hash_passport_payload(
        envelope["passport"],
        proof["hash_alg"],
    )
    return envelope


def make_envelope_with_unsupported_algorithm(
    algorithm: str = "ML-DSA-87",
) -> dict[str, Any]:
    # Key selection requires key alg == proof alg, so set both to the same
    # unsupported but schema-valid algorithm. Changing the passport key alg
    # changes the payload, so the payload hash must be recomputed.
    envelope = load_example_envelope()
    envelope["passport"]["public_keys"][0]["alg"] = algorithm
    envelope["proofs"][0]["alg"] = algorithm
    return rehash_envelope(envelope)


def make_envelope_with_changed_signature() -> dict[str, Any]:
    envelope = load_example_envelope()
    original = envelope["proofs"][0]["signature_b64u"]
    replacement = "k" if original[-1] != "k" else "j"

    envelope["proofs"][0]["signature_b64u"] = original[:-1] + replacement

    return envelope


def make_envelope_with_second_proof() -> dict[str, Any]:
    envelope = load_example_envelope()
    second = copy.deepcopy(envelope["proofs"][0])

    second["proof_id"] = "urn:aaid:proof:second-input-test-proof"
    envelope["proofs"].append(second)

    return envelope


def test_minimal_example_reaches_signature_input_prepared_passed() -> None:
    result = verify_with_trusted_context(load_example_envelope())
    input_check = find_check(result, SIGNATURE_INPUT_CHECK)

    assert_check_passed(result, KEY_SELECTED_CHECK)

    assert input_check is not None
    assert input_check.passed is True


def test_signature_input_prepared_between_key_selected_and_algorithm() -> None:
    result = verify_with_trusted_context(load_example_envelope())

    key_index = find_check_index(result, KEY_SELECTED_CHECK)
    input_index = find_check_index(result, SIGNATURE_INPUT_CHECK)
    algorithm_index = find_check_index(result, ALGORITHM_SUPPORTED_CHECK)

    assert key_index != -1
    assert input_index != -1
    assert algorithm_index != -1
    assert key_index < input_index < algorithm_index


def test_signature_algorithm_supported_between_input_and_signature() -> None:
    result = verify_with_trusted_context(load_example_envelope())

    input_index = find_check_index(result, SIGNATURE_INPUT_CHECK)
    algorithm_index = find_check_index(result, ALGORITHM_SUPPORTED_CHECK)
    signature_index = find_check_index(result, SIGNATURE_CHECK)

    assert input_index != -1
    assert algorithm_index != -1
    assert signature_index != -1
    assert input_index < algorithm_index < signature_index


def test_prepare_signature_input_returns_canonical_utf8_bytes() -> None:
    passport = load_example_envelope()["passport"]
    check, data = prepare_signature_input(passport)

    assert check.name == SIGNATURE_INPUT_CHECK
    assert check.passed is True
    assert isinstance(data, bytes)
    assert data == canonicalize_passport_payload(passport)
    assert data.decode("utf-8")

    # Detached proof material is excluded from the signing input.
    assert b'"proofs"' not in data
    assert b"signature_b64u" not in data


def test_changed_signature_does_not_change_prepared_input() -> None:
    base_passport = load_example_envelope()["passport"]
    changed_passport = make_envelope_with_changed_signature()["passport"]

    _, base_input = prepare_signature_input(base_passport)
    _, changed_input = prepare_signature_input(changed_passport)

    assert base_input == changed_input


def test_second_proof_does_not_change_prepared_input() -> None:
    base_passport = load_example_envelope()["passport"]
    second_proof_passport = make_envelope_with_second_proof()["passport"]

    _, base_input = prepare_signature_input(base_passport)
    _, second_input = prepare_signature_input(second_proof_passport)

    assert base_input == second_input


def test_unsupported_key_alg_fails_closed() -> None:
    result = verify_with_trusted_context(make_envelope_with_unsupported_algorithm())
    algorithm_check = find_check(result, ALGORITHM_SUPPORTED_CHECK)

    assert_check_passed(result, KEY_SELECTED_CHECK)
    assert_check_passed(result, SIGNATURE_INPUT_CHECK)

    assert algorithm_check is not None
    assert algorithm_check.passed is False

    assert find_check(result, SIGNATURE_CHECK) is None
    assert result.decision == DENY
    assert result.valid is False


def test_unsupported_algorithm_short_circuits_before_signature() -> None:
    result = verify_with_trusted_context(make_envelope_with_unsupported_algorithm())

    assert_check_failed(result, ALGORITHM_SUPPORTED_CHECK)
    assert find_check(result, SIGNATURE_CHECK) is None


def test_key_selection_failure_short_circuits_before_signature_input() -> None:
    envelope = load_example_envelope()
    envelope["proofs"][0]["kid"] = "urn:aaid:key:no-such-key-input-0001"

    result = verify_with_trusted_context(envelope)

    assert_check_failed(result, KEY_SELECTED_CHECK)
    assert find_check(result, SIGNATURE_INPUT_CHECK) is None
    assert find_check(result, ALGORITHM_SUPPORTED_CHECK) is None


def test_payload_hash_failure_short_circuits_before_signature_input() -> None:
    envelope = load_example_envelope()
    envelope["proofs"][0]["payload_hash"] = "0" * 64

    result = verify_with_trusted_context(envelope)

    assert_check_failed(result, PAYLOAD_HASH_CHECK)
    assert find_check(result, SIGNATURE_INPUT_CHECK) is None


def test_schema_failure_short_circuits_before_signature_input() -> None:
    envelope = load_example_envelope()
    envelope["proofs"][0]["unexpected_field"] = "x"

    result = verify_passport_envelope(envelope)

    assert_check_failed(result, SCHEMA_CHECK)
    assert find_check(result, SIGNATURE_INPUT_CHECK) is None


def test_structural_failure_short_circuits_before_signature_input() -> None:
    result = verify_passport_envelope(["passport", "proofs"])

    assert_check_failed(result, ENVELOPE_IS_MAPPING_CHECK)
    assert find_check(result, SIGNATURE_INPUT_CHECK) is None


def test_signature_input_step_never_returns_allow() -> None:
    cases = [
        load_example_envelope(),
        make_envelope_with_unsupported_algorithm(),
        make_envelope_with_changed_signature(),
        make_envelope_with_second_proof(),
        {"passport": {"subject": "demo"}, "proofs": [{"proof_id": "x"}]},
        {"passport": {"subject": "demo"}, "proofs": []},
        {},
        None,
    ]

    # Reach the named step for the valid, trusted example so this sweep actually
    # exercises signature_input_prepared rather than stopping at issuer_trusted.
    reached = verify_with_trusted_context(load_example_envelope())

    assert find_check(reached, SIGNATURE_INPUT_CHECK) is not None

    for case in cases:
        result = verify_with_trusted_context(case)

        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.valid is False


def test_signature_verification_still_not_implemented() -> None:
    result = verify_with_trusted_context(load_example_envelope())

    assert_check_failed(result, SIGNATURE_CHECK)


def test_passport_verifier_imports_no_crypto_or_network_modules() -> None:
    for module_name in FORBIDDEN_CRYPTO_OR_NETWORK_IMPORTS:
        assert not hasattr(passport_verifier_module, module_name), (
            f"passport_verifier must not import {module_name}"
        )

    source = PASSPORT_VERIFIER_SOURCE_PATH.read_text(encoding="utf-8")

    for module_name in FORBIDDEN_CRYPTO_OR_NETWORK_IMPORTS:
        assert f"import {module_name}" not in source
        assert f"from {module_name}" not in source
