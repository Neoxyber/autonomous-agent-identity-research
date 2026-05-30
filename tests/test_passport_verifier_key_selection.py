import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import aaid.passport_verifier as passport_verifier_module
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.canonicalization import hash_passport_payload
from aaid.verification import VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PV_SOURCE_PATH = SRC / "aaid" / "passport_verifier.py"

KEY_CHECK = "verification_key_selected"
PAYLOAD_CHECK = "payload_hash_valid"
SIGNATURE_CHECK = "signature_verification_not_implemented"


def load_envelope():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def check_named(result, name):
    for check in result.checks:
        if check.name == name:
            return check
    return None


def check_index(result, name):
    for index, check in enumerate(result.checks):
        if check.name == name:
            return index
    return -1


def rehash(envelope):
    # Any change to the passport changes its canonical payload hash, so the
    # selected proof's recorded payload_hash must be recomputed for the
    # envelope to still pass payload_hash_valid and reach key selection.
    proof = envelope["proofs"][0]
    proof["payload_hash"] = hash_passport_payload(
        envelope["passport"], proof["hash_alg"]
    )
    return envelope


def envelope_with_key_field(field, value):
    envelope = load_envelope()
    envelope["passport"]["public_keys"][0][field] = value
    return rehash(envelope)


def envelope_with_proof_field(field, value):
    # Proof-only change: the payload hash is computed over the passport, so it
    # stays valid without rehashing.
    envelope = load_envelope()
    envelope["proofs"][0][field] = value
    return envelope


def envelope_with_duplicate_key_kid():
    envelope = load_envelope()
    keys = envelope["passport"]["public_keys"]
    proof_kid = envelope["proofs"][0]["kid"]
    duplicate = copy.deepcopy(keys[0])
    duplicate["kid"] = proof_kid
    duplicate["created_at"] = "2026-05-30T00:00:00Z"
    keys.append(duplicate)
    return rehash(envelope)


# 1. Minimal example reaches verification_key_selected passed=True.
def test_minimal_example_reaches_verification_key_selected_passed():
    result = verify_passport_envelope(load_envelope())
    assert check_named(result, PAYLOAD_CHECK).passed is True
    key_check = check_named(result, KEY_CHECK)
    assert key_check is not None
    assert key_check.passed is True


# 2. verification_key_selected sits between payload_hash_valid and signature.
def test_verification_key_selected_between_payload_hash_and_signature():
    result = verify_passport_envelope(load_envelope())
    payload_index = check_index(result, PAYLOAD_CHECK)
    key_index = check_index(result, KEY_CHECK)
    signature_index = check_index(result, SIGNATURE_CHECK)
    assert payload_index != -1
    assert key_index != -1
    assert signature_index != -1
    assert payload_index < key_index < signature_index


# 3. Missing public key for the selected proof kid fails closed.
def test_missing_public_key_for_proof_kid_fails_closed():
    envelope = envelope_with_proof_field("kid", "urn:aaid:key:no-such-key-0001")
    result = verify_passport_envelope(envelope)
    key_check = check_named(result, KEY_CHECK)
    assert key_check is not None
    assert key_check.passed is False
    assert result.decision == DENY
    assert result.valid is False
    assert check_named(result, SIGNATURE_CHECK) is None


# 4. Duplicate public key kid fails closed.
def test_duplicate_public_key_kid_fails_closed():
    result = verify_passport_envelope(envelope_with_duplicate_key_kid())
    # Confirm the fixture reached key selection (schema + payload hash passed).
    assert check_named(result, PAYLOAD_CHECK).passed is True
    key_check = check_named(result, KEY_CHECK)
    assert key_check is not None
    assert key_check.passed is False
    assert result.decision == DENY
    assert check_named(result, SIGNATURE_CHECK) is None


# 5. proof.alg mismatch with the selected public key alg fails closed.
def test_proof_alg_mismatch_with_key_fails_closed():
    result = verify_passport_envelope(envelope_with_proof_field("alg", "ML-DSA-87"))
    assert check_named(result, PAYLOAD_CHECK).passed is True
    key_check = check_named(result, KEY_CHECK)
    assert key_check is not None
    assert key_check.passed is False
    assert result.decision == DENY
    assert check_named(result, SIGNATURE_CHECK) is None


# 6. Selected public key status retired fails closed.
def test_retired_key_status_fails_closed():
    result = verify_passport_envelope(
        envelope_with_key_field("status", "retired")
    )
    assert check_named(result, PAYLOAD_CHECK).passed is True
    key_check = check_named(result, KEY_CHECK)
    assert key_check is not None
    assert key_check.passed is False
    assert result.decision == DENY
    assert check_named(result, SIGNATURE_CHECK) is None


# 7. Selected public key status compromised fails closed.
def test_compromised_key_status_fails_closed():
    result = verify_passport_envelope(
        envelope_with_key_field("status", "compromised")
    )
    assert check_named(result, PAYLOAD_CHECK).passed is True
    key_check = check_named(result, KEY_CHECK)
    assert key_check is not None
    assert key_check.passed is False
    assert result.decision == DENY
    assert check_named(result, SIGNATURE_CHECK) is None


# 8. Accepted key purposes sig, verify, hybrid-sig all pass key selection.
def test_accepted_key_purposes_pass_key_selection():
    for purpose in ("sig", "verify", "hybrid-sig"):
        result = verify_passport_envelope(
            envelope_with_key_field("purpose", purpose)
        )
        assert check_named(result, PAYLOAD_CHECK).passed is True, purpose
        key_check = check_named(result, KEY_CHECK)
        assert key_check is not None, purpose
        assert key_check.passed is True, purpose


# 9. Key-selection failure short-circuits before signature verification.
def test_key_selection_failure_short_circuits_before_signature():
    envelope = envelope_with_proof_field("kid", "urn:aaid:key:no-such-key-0002")
    result = verify_passport_envelope(envelope)
    assert check_named(result, KEY_CHECK).passed is False
    assert check_named(result, SIGNATURE_CHECK) is None


# 10. payload_hash failure short-circuits before verification_key_selected.
def test_payload_hash_failure_short_circuits_before_key_selection():
    envelope = load_envelope()
    envelope["proofs"][0]["payload_hash"] = "0" * 64
    result = verify_passport_envelope(envelope)
    assert check_named(result, PAYLOAD_CHECK).passed is False
    assert check_named(result, KEY_CHECK) is None
    assert check_named(result, SIGNATURE_CHECK) is None


# 11. schema failure short-circuits before verification_key_selected.
def test_schema_failure_short_circuits_before_key_selection():
    envelope = load_envelope()
    envelope["proofs"][0]["unexpected_field"] = "x"
    result = verify_passport_envelope(envelope)
    assert check_named(result, "schema_valid").passed is False
    assert check_named(result, KEY_CHECK) is None


# 12. structural failure short-circuits before verification_key_selected.
def test_structural_failure_short_circuits_before_key_selection():
    result = verify_passport_envelope(["passport", "proofs"])
    assert check_named(result, "envelope_is_mapping").passed is False
    assert check_named(result, KEY_CHECK) is None


# 13. No input reaches ALLOW through the key-selection step.
def test_key_selection_step_never_returns_allow():
    cases = [
        load_envelope(),
        envelope_with_proof_field("kid", "urn:aaid:key:no-such-key-0003"),
        envelope_with_duplicate_key_kid(),
        envelope_with_proof_field("alg", "ML-DSA-87"),
        envelope_with_key_field("status", "retired"),
        envelope_with_key_field("status", "compromised"),
        envelope_with_key_field("purpose", "verify"),
        envelope_with_key_field("purpose", "hybrid-sig"),
    ]
    for case in cases:
        result = verify_passport_envelope(case)
        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.valid is False


# 14. Signature verification is still not implemented.
def test_signature_verification_still_not_implemented():
    result = verify_passport_envelope(load_envelope())
    signature = check_named(result, SIGNATURE_CHECK)
    assert signature is not None
    assert signature.passed is False


# 15. passport_verifier.py imports no crypto or network modules.
def test_passport_verifier_imports_no_crypto_or_network_modules():
    forbidden = (
        "hashlib", "hmac", "base64", "ssl", "secrets", "cryptography",
        "pqcrypto", "oqs", "requests", "httpx", "socket", "urllib",
    )
    for module_name in forbidden:
        assert not hasattr(passport_verifier_module, module_name), (
            f"passport_verifier must not import {module_name}"
        )
    source = PV_SOURCE_PATH.read_text(encoding="utf-8")
    for module_name in forbidden:
        assert f"import {module_name}" not in source
        assert f"from {module_name}" not in source
