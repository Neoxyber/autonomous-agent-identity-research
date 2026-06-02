import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import aaid.passport_verifier as passport_verifier_module
from _support import TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.verification import VerificationCheck, VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PV_SOURCE_PATH = SRC / "aaid" / "passport_verifier.py"
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


def envelope_with_broken_payload_hash():
    envelope = load_envelope()
    envelope["proofs"][0]["payload_hash"] = "0" * 64
    return envelope


def envelope_with_changed_signature():
    # signature_b64u is base64url metadata in the proof, not part of the signed
    # payload, so a same-length, same-charset edit stays schema-valid and leaves
    # the payload hash valid.
    envelope = load_envelope()
    original = envelope["proofs"][0]["signature_b64u"]
    envelope["proofs"][0]["signature_b64u"] = original[:-1] + (
        "k" if original[-1] != "k" else "j"
    )
    return envelope


# 1. Valid envelope reaches the signature step.
def test_valid_envelope_reaches_signature_verification_not_implemented():
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS)
    assert check_named(result, "schema_valid").passed is True
    assert check_named(result, "proof_selected").passed is True
    assert check_named(result, "payload_hash_valid").passed is True
    assert check_named(result, SIGNATURE_CHECK) is not None


# 2. Signature check is recorded after payload_hash_valid.
def test_signature_check_recorded_after_payload_hash_valid():
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS)
    payload_index = check_index(result, "payload_hash_valid")
    signature_index = check_index(result, SIGNATURE_CHECK)
    assert payload_index != -1
    assert signature_index != -1
    assert payload_index < signature_index


# 3. Signature check is failed, not passed.
def test_signature_check_is_failed_not_passed():
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS)
    signature = check_named(result, SIGNATURE_CHECK)
    assert signature is not None
    assert signature.passed is False


# 4. Final result is invalid and DENY.
def test_valid_envelope_final_result_is_invalid_and_denied():
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS)
    assert result.valid is False
    assert result.decision == DENY


# 5. No input returns ALLOW.
def test_signature_abstraction_step_never_returns_allow():
    cases = [
        load_envelope(),
        envelope_with_broken_payload_hash(),
        envelope_with_changed_signature(),
        ["not", "a", "mapping"],
        {"passport": {"subject": "demo"}, "proofs": []},
        {"passport": {"subject": "demo"}, "proofs": [{"proof_id": "x"}]},
        {},
        None,
    ]
    # Reach the named step for the valid, trusted example so this sweep actually
    # exercises signature_verification_not_implemented rather than stopping at
    # issuer_trusted.
    reached = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS
    )
    assert check_named(reached, SIGNATURE_CHECK) is not None

    for case in cases:
        result = verify_passport_envelope(
            case, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS
        )
        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.valid is False


# 6. Payload hash failure short-circuits before signature verification.
def test_payload_hash_failure_short_circuits_before_signature():
    result = verify_passport_envelope(
        envelope_with_broken_payload_hash(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS
    )
    assert check_named(result, "payload_hash_valid").passed is False
    assert check_named(result, SIGNATURE_CHECK) is None
    assert result.decision == DENY


# 7. Schema failure short-circuits before signature verification.
def test_schema_failure_short_circuits_before_signature():
    envelope = load_envelope()
    # proof objects set additionalProperties: false, so an unknown key fails
    # schema validation while leaving the envelope structurally intact.
    envelope["proofs"][0]["unexpected_field"] = "x"
    result = verify_passport_envelope(envelope)
    assert check_named(result, "schema_valid").passed is False
    assert check_named(result, "proof_selected") is None
    assert check_named(result, "payload_hash_valid") is None
    assert check_named(result, SIGNATURE_CHECK) is None


# 8. Structural failure short-circuits before signature verification.
def test_structural_failure_short_circuits_before_signature():
    result = verify_passport_envelope(["passport", "proofs"])
    assert check_named(result, "envelope_is_mapping").passed is False
    assert check_named(result, "schema_valid") is None
    assert check_named(result, SIGNATURE_CHECK) is None


# 9. Changing signature_b64u does not make the verifier allow the envelope.
def test_changing_signature_b64u_does_not_allow():
    result = verify_passport_envelope(
        envelope_with_changed_signature(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS
    )
    assert result.decision == DENY
    assert result.valid is False
    assert check_named(result, "payload_hash_valid").passed is True
    signature = check_named(result, SIGNATURE_CHECK)
    assert signature is not None
    assert signature.passed is False


# 10. No public callable looks like real signing/signature verification beyond
#     the existing verify_passport_envelope API.
def test_no_public_signing_or_verification_callable_beyond_api():
    public_callables = [
        name
        for name in dir(passport_verifier_module)
        if not name.startswith("_")
        and callable(getattr(passport_verifier_module, name))
    ]
    for name in public_callables:
        assert "sign" not in name.lower(), (
            f"unexpected signing-like public callable: {name}"
        )
    verify_like = [n for n in public_callables if "verify" in n.lower()]
    assert verify_like == ["verify_passport_envelope", "verify_passport_json"]


# 11. passport_verifier.py imports no crypto or network modules.
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


# --- Focused RED: the new internal boundary (helper does not exist yet) ---

def test_signature_helper_exists_and_returns_failed_named_check():
    helper = (
        passport_verifier_module._signature_verification_not_implemented_check
    )
    envelope = load_envelope()
    check = helper(envelope["passport"], envelope["proofs"][0])
    assert isinstance(check, VerificationCheck)
    assert check.name == SIGNATURE_CHECK
    assert check.passed is False
    assert isinstance(check.reason, str) and check.reason.strip()


def test_signature_helper_fails_closed_regardless_of_arguments():
    helper = (
        passport_verifier_module._signature_verification_not_implemented_check
    )
    samples = [({"a": 1}, {"b": 2}), ({}, {}), (load_envelope()["passport"], {})]
    for passport, proof in samples:
        check = helper(passport, proof)
        assert check.name == SIGNATURE_CHECK
        assert check.passed is False
