"""Key-selection verifier-boundary tests.

These tests record current verifier behavior around proof key selection,
proof/key mismatch, duplicate key identifiers, key status, key purpose,
ordering, short-circuit behavior, and the never-ALLOW boundary.

They do not add real signature verification, cryptographic key validation, or
make the passport verifier return `ALLOW`. More tests and
research are still needed around key-selection and signature-verification
boundaries.
"""

import copy
import json
from pathlib import Path
from typing import Any

import aaid.passport_verifier as passport_verifier_module
from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.canonicalization import hash_passport_payload
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PASSPORT_VERIFIER_SOURCE_PATH = ROOT / "src" / "aaid" / "passport_verifier.py"

SCHEMA_CHECK = "schema_valid"
ENVELOPE_MAPPING_CHECK = "envelope_is_mapping"
KEY_CHECK = "verification_key_selected"
PAYLOAD_CHECK = "payload_hash_valid"
SIGNATURE_CHECK = "signature_verification_not_implemented"

ACCEPTED_KEY_PURPOSES = ("sig", "verify", "hybrid-sig")

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
    return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))


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


def verify_trusted_envelope(envelope: Any) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def update_payload_hash(envelope: dict[str, Any]) -> dict[str, Any]:
    proof = envelope["proofs"][0]
    proof["payload_hash"] = hash_passport_payload(
        envelope["passport"],
        proof["hash_alg"],
    )
    return envelope


def envelope_with_key_field(field: str, value: Any) -> dict[str, Any]:
    envelope = load_example_envelope()
    envelope["passport"]["public_keys"][0][field] = value
    return update_payload_hash(envelope)


def envelope_with_proof_field(field: str, value: Any) -> dict[str, Any]:
    envelope = load_example_envelope()
    envelope["proofs"][0][field] = value
    return envelope


def envelope_with_duplicate_key_kid() -> dict[str, Any]:
    envelope = load_example_envelope()
    keys = envelope["passport"]["public_keys"]
    proof_kid = envelope["proofs"][0]["kid"]

    duplicate = copy.deepcopy(keys[0])
    duplicate["kid"] = proof_kid
    duplicate["created_at"] = "2026-05-30T00:00:00Z"
    keys.append(duplicate)

    return update_payload_hash(envelope)


def test_minimal_example_reaches_verification_key_selected_passed() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    payload = find_check(result, PAYLOAD_CHECK)
    key_check = find_check(result, KEY_CHECK)

    assert payload is not None
    assert key_check is not None
    assert payload.passed is True
    assert key_check.passed is True


def test_verification_key_selected_between_payload_hash_and_signature() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    payload_index = check_index(result, PAYLOAD_CHECK)
    key_index = check_index(result, KEY_CHECK)
    signature_index = check_index(result, SIGNATURE_CHECK)

    assert payload_index != -1
    assert key_index != -1
    assert signature_index != -1
    assert payload_index < key_index < signature_index


def test_missing_public_key_for_proof_kid_fails_closed() -> None:
    envelope = envelope_with_proof_field("kid", "urn:aaid:key:no-such-key-0001")

    result = verify_trusted_envelope(envelope)

    key_check = find_check(result, KEY_CHECK)
    assert key_check is not None
    assert key_check.passed is False

    assert result.decision == DENY
    assert result.valid is False
    assert find_check(result, SIGNATURE_CHECK) is None


def test_duplicate_public_key_kid_fails_closed() -> None:
    result = verify_trusted_envelope(envelope_with_duplicate_key_kid())

    payload = find_check(result, PAYLOAD_CHECK)
    key_check = find_check(result, KEY_CHECK)

    assert payload is not None
    assert key_check is not None
    assert payload.passed is True
    assert key_check.passed is False

    assert result.decision == DENY
    assert find_check(result, SIGNATURE_CHECK) is None


def test_proof_alg_mismatch_with_key_fails_closed() -> None:
    result = verify_trusted_envelope(
        envelope_with_proof_field("alg", "ML-DSA-87"),
    )

    payload = find_check(result, PAYLOAD_CHECK)
    key_check = find_check(result, KEY_CHECK)

    assert payload is not None
    assert key_check is not None
    assert payload.passed is True
    assert key_check.passed is False

    assert result.decision == DENY
    assert find_check(result, SIGNATURE_CHECK) is None


def test_retired_key_status_fails_closed() -> None:
    result = verify_trusted_envelope(envelope_with_key_field("status", "retired"))

    payload = find_check(result, PAYLOAD_CHECK)
    key_check = find_check(result, KEY_CHECK)

    assert payload is not None
    assert key_check is not None
    assert payload.passed is True
    assert key_check.passed is False

    assert result.decision == DENY
    assert find_check(result, SIGNATURE_CHECK) is None


def test_compromised_key_status_fails_closed() -> None:
    result = verify_trusted_envelope(
        envelope_with_key_field("status", "compromised"),
    )

    payload = find_check(result, PAYLOAD_CHECK)
    key_check = find_check(result, KEY_CHECK)

    assert payload is not None
    assert key_check is not None
    assert payload.passed is True
    assert key_check.passed is False

    assert result.decision == DENY
    assert find_check(result, SIGNATURE_CHECK) is None


def test_accepted_key_purposes_pass_key_selection() -> None:
    for purpose in ACCEPTED_KEY_PURPOSES:
        result = verify_trusted_envelope(envelope_with_key_field("purpose", purpose))

        payload = find_check(result, PAYLOAD_CHECK)
        key_check = find_check(result, KEY_CHECK)

        assert payload is not None, purpose
        assert key_check is not None, purpose
        assert payload.passed is True, purpose
        assert key_check.passed is True, purpose


def test_key_selection_failure_short_circuits_before_signature() -> None:
    envelope = envelope_with_proof_field("kid", "urn:aaid:key:no-such-key-0002")

    result = verify_trusted_envelope(envelope)

    key_check = find_check(result, KEY_CHECK)
    assert key_check is not None
    assert key_check.passed is False
    assert find_check(result, SIGNATURE_CHECK) is None


def test_payload_hash_failure_short_circuits_before_key_selection() -> None:
    envelope = load_example_envelope()
    envelope["proofs"][0]["payload_hash"] = "0" * 64

    result = verify_trusted_envelope(envelope)

    payload = find_check(result, PAYLOAD_CHECK)
    assert payload is not None
    assert payload.passed is False
    assert find_check(result, KEY_CHECK) is None
    assert find_check(result, SIGNATURE_CHECK) is None


def test_schema_failure_short_circuits_before_key_selection() -> None:
    envelope = load_example_envelope()
    envelope["proofs"][0]["unexpected_field"] = "x"

    result = verify_passport_envelope(envelope)

    schema = find_check(result, SCHEMA_CHECK)
    assert schema is not None
    assert schema.passed is False
    assert find_check(result, KEY_CHECK) is None


def test_structural_failure_short_circuits_before_key_selection() -> None:
    result = verify_passport_envelope(["passport", "proofs"])

    envelope_mapping = find_check(result, ENVELOPE_MAPPING_CHECK)
    assert envelope_mapping is not None
    assert envelope_mapping.passed is False
    assert find_check(result, KEY_CHECK) is None


def test_key_selection_step_never_returns_allow() -> None:
    cases = [
        load_example_envelope(),
        envelope_with_proof_field("kid", "urn:aaid:key:no-such-key-0003"),
        envelope_with_duplicate_key_kid(),
        envelope_with_proof_field("alg", "ML-DSA-87"),
        envelope_with_key_field("status", "retired"),
        envelope_with_key_field("status", "compromised"),
        envelope_with_key_field("purpose", "verify"),
        envelope_with_key_field("purpose", "hybrid-sig"),
    ]

    reached = verify_trusted_envelope(load_example_envelope())
    assert find_check(reached, KEY_CHECK) is not None

    for envelope in cases:
        result = verify_trusted_envelope(envelope)

        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.valid is False


def test_signature_verification_still_not_implemented() -> None:
    result = verify_trusted_envelope(load_example_envelope())

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
