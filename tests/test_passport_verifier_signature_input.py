import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import aaid.passport_verifier as passport_verifier_module
from _support import TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.canonicalization import (
    canonicalize_passport_payload,
    hash_passport_payload,
)
from aaid.verification import VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PV_SOURCE_PATH = SRC / "aaid" / "passport_verifier.py"

KEY_CHECK = "verification_key_selected"
INPUT_CHECK = "signature_input_prepared"
ALG_CHECK = "signature_algorithm_supported"
SIGNATURE_CHECK = "signature_verification_not_implemented"
PAYLOAD_CHECK = "payload_hash_valid"


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
    proof = envelope["proofs"][0]
    proof["payload_hash"] = hash_passport_payload(
        envelope["passport"], proof["hash_alg"]
    )
    return envelope


def envelope_with_unsupported_alg(alg="ML-DSA-87"):
    # Key selection requires key alg == proof alg, so set both to the same
    # unsupported (but schema-valid) algorithm. Changing the passport key alg
    # changes the payload, so the payload hash must be recomputed.
    envelope = load_envelope()
    envelope["passport"]["public_keys"][0]["alg"] = alg
    envelope["proofs"][0]["alg"] = alg
    return rehash(envelope)


def envelope_with_changed_signature():
    envelope = load_envelope()
    original = envelope["proofs"][0]["signature_b64u"]
    envelope["proofs"][0]["signature_b64u"] = original[:-1] + (
        "k" if original[-1] != "k" else "j"
    )
    return envelope


def envelope_with_second_proof():
    envelope = load_envelope()
    second = copy.deepcopy(envelope["proofs"][0])
    second["proof_id"] = "urn:aaid:proof:second-input-test-proof"
    envelope["proofs"].append(second)
    return envelope


# 1. Minimal example reaches signature_input_prepared passed=True.
def test_minimal_example_reaches_signature_input_prepared_passed():
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS)
    assert check_named(result, KEY_CHECK).passed is True
    input_check = check_named(result, INPUT_CHECK)
    assert input_check is not None
    assert input_check.passed is True


# 2. signature_input_prepared sits between key selection and algorithm support.
def test_signature_input_prepared_between_key_selected_and_algorithm():
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS)
    key_index = check_index(result, KEY_CHECK)
    input_index = check_index(result, INPUT_CHECK)
    alg_index = check_index(result, ALG_CHECK)
    assert key_index != -1
    assert input_index != -1
    assert alg_index != -1
    assert key_index < input_index < alg_index


# 3. signature_algorithm_supported sits between input prep and signature step.
def test_signature_algorithm_supported_between_input_and_signature():
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS)
    input_index = check_index(result, INPUT_CHECK)
    alg_index = check_index(result, ALG_CHECK)
    signature_index = check_index(result, SIGNATURE_CHECK)
    assert input_index != -1
    assert alg_index != -1
    assert signature_index != -1
    assert input_index < alg_index < signature_index


# 4. The prepared signature input is the canonical passport payload UTF-8 bytes.
def test_prepare_signature_input_returns_canonical_utf8_bytes():
    passport = load_envelope()["passport"]
    check, data = passport_verifier_module._prepare_signature_input(passport)
    assert check.name == INPUT_CHECK
    assert check.passed is True
    assert isinstance(data, bytes)
    assert data == canonicalize_passport_payload(passport)
    assert data.decode("utf-8")  # valid, non-empty UTF-8
    # detached proof material is excluded from the signing input
    assert b'"proofs"' not in data
    assert b"signature_b64u" not in data


# 5. Changing proof.signature_b64u does not change the prepared signature input.
def test_changed_signature_does_not_change_prepared_input():
    base_passport = load_envelope()["passport"]
    changed_passport = envelope_with_changed_signature()["passport"]
    _, base_input = passport_verifier_module._prepare_signature_input(
        base_passport
    )
    _, changed_input = passport_verifier_module._prepare_signature_input(
        changed_passport
    )
    assert base_input == changed_input


# 6. Adding a second proof does not change the prepared signature input.
def test_second_proof_does_not_change_prepared_input():
    base_passport = load_envelope()["passport"]
    second_proof_passport = envelope_with_second_proof()["passport"]
    _, base_input = passport_verifier_module._prepare_signature_input(
        base_passport
    )
    _, second_input = passport_verifier_module._prepare_signature_input(
        second_proof_passport
    )
    assert base_input == second_input


# 7. Unsupported selected key alg fails signature_algorithm_supported, DENY.
def test_unsupported_key_alg_fails_closed():
    result = verify_passport_envelope(
        envelope_with_unsupported_alg(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS
    )
    assert check_named(result, KEY_CHECK).passed is True
    assert check_named(result, INPUT_CHECK).passed is True
    alg_check = check_named(result, ALG_CHECK)
    assert alg_check is not None
    assert alg_check.passed is False
    assert result.decision == DENY
    assert result.valid is False
    assert check_named(result, SIGNATURE_CHECK) is None


# 8. Unsupported algorithm failure short-circuits before the signature step.
def test_unsupported_algorithm_short_circuits_before_signature():
    result = verify_passport_envelope(
        envelope_with_unsupported_alg(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS
    )
    assert check_named(result, ALG_CHECK).passed is False
    assert check_named(result, SIGNATURE_CHECK) is None


# 9. Key-selection failure short-circuits before signature_input_prepared.
def test_key_selection_failure_short_circuits_before_signature_input():
    envelope = load_envelope()
    envelope["proofs"][0]["kid"] = "urn:aaid:key:no-such-key-input-0001"
    result = verify_passport_envelope(envelope, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS)
    assert check_named(result, KEY_CHECK).passed is False
    assert check_named(result, INPUT_CHECK) is None
    assert check_named(result, ALG_CHECK) is None


# 10. payload_hash failure short-circuits before signature_input_prepared.
def test_payload_hash_failure_short_circuits_before_signature_input():
    envelope = load_envelope()
    envelope["proofs"][0]["payload_hash"] = "0" * 64
    result = verify_passport_envelope(envelope, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS)
    assert check_named(result, PAYLOAD_CHECK).passed is False
    assert check_named(result, INPUT_CHECK) is None


# 11. schema failure short-circuits before signature_input_prepared.
def test_schema_failure_short_circuits_before_signature_input():
    envelope = load_envelope()
    envelope["proofs"][0]["unexpected_field"] = "x"
    result = verify_passport_envelope(envelope)
    assert check_named(result, "schema_valid").passed is False
    assert check_named(result, INPUT_CHECK) is None


# 12. structural failure short-circuits before signature_input_prepared.
def test_structural_failure_short_circuits_before_signature_input():
    result = verify_passport_envelope(["passport", "proofs"])
    assert check_named(result, "envelope_is_mapping").passed is False
    assert check_named(result, INPUT_CHECK) is None


# 13. No input reaches ALLOW through the signature-input step.
def test_signature_input_step_never_returns_allow():
    cases = [
        load_envelope(),
        envelope_with_unsupported_alg(),
        envelope_with_changed_signature(),
        envelope_with_second_proof(),
        {"passport": {"subject": "demo"}, "proofs": [{"proof_id": "x"}]},
        {"passport": {"subject": "demo"}, "proofs": []},
        {},
        None,
    ]
    # Reach the named step for the valid, trusted example so this sweep actually
    # exercises signature_input_prepared rather than stopping at issuer_trusted.
    reached = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS
    )
    assert check_named(reached, INPUT_CHECK) is not None

    for case in cases:
        result = verify_passport_envelope(
            case, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS
        )
        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.valid is False


# 14. Signature verification is still not implemented.
def test_signature_verification_still_not_implemented():
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS)
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
