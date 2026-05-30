import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import aaid.passport_verifier as passport_verifier_module
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.verification import VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PV_SOURCE_PATH = SRC / "aaid" / "passport_verifier.py"

KEY_CHECK = "verification_key_selected"
CANON_CHECK = "signature_canonicalization_supported"
INPUT_CHECK = "signature_input_prepared"
ALG_CHECK = "signature_algorithm_supported"
SIGNATURE_CHECK = "signature_verification_not_implemented"
PAYLOAD_CHECK = "payload_hash_valid"

# The schema restricts proof.canonicalization to a single enum value, so an
# unsupported declared scheme cannot pass schema validation. To exercise the
# verifier's unsupported-canonicalization branch, narrow the private allowlist
# so the example's (schema-valid) scheme is treated as unrecognized.
EMPTY_ALLOWLIST = ()


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


def force_unsupported_canonicalization(monkeypatch):
    monkeypatch.setattr(
        passport_verifier_module,
        "_SUPPORTED_SIGNATURE_CANONICALIZATIONS",
        EMPTY_ALLOWLIST,
    )


# 1. Minimal example reaches signature_canonicalization_supported passed=True.
def test_minimal_example_reaches_canonicalization_supported_passed():
    result = verify_passport_envelope(load_envelope())
    assert check_named(result, KEY_CHECK).passed is True
    canon = check_named(result, CANON_CHECK)
    assert canon is not None
    assert canon.passed is True


# 2. signature_canonicalization_supported sits between key selection and input.
def test_canonicalization_supported_between_key_selected_and_input():
    result = verify_passport_envelope(load_envelope())
    key_index = check_index(result, KEY_CHECK)
    canon_index = check_index(result, CANON_CHECK)
    input_index = check_index(result, INPUT_CHECK)
    assert key_index != -1
    assert canon_index != -1
    assert input_index != -1
    assert key_index < canon_index < input_index


# 3a. The helper fails closed for an unrecognized declared scheme.
def test_unsupported_canonicalization_value_fails_check_directly():
    check = passport_verifier_module._signature_canonicalization_supported_check(
        {"canonicalization": "some-unsupported-scheme"}
    )
    assert check.name == CANON_CHECK
    assert check.passed is False


# 3b. An unsupported declared scheme makes the verifier fail closed to DENY.
def test_unsupported_canonicalization_returns_deny(monkeypatch):
    force_unsupported_canonicalization(monkeypatch)
    result = verify_passport_envelope(load_envelope())
    canon = check_named(result, CANON_CHECK)
    assert canon is not None
    assert canon.passed is False
    assert result.decision == DENY
    assert result.valid is False


# 4. Unsupported canonicalization short-circuits before signature_input_prepared.
def test_unsupported_canonicalization_short_circuits_before_input(monkeypatch):
    force_unsupported_canonicalization(monkeypatch)
    result = verify_passport_envelope(load_envelope())
    assert check_named(result, CANON_CHECK).passed is False
    assert check_named(result, INPUT_CHECK) is None


# 5. Unsupported canonicalization short-circuits before signature_algorithm_supported.
def test_unsupported_canonicalization_short_circuits_before_algorithm(monkeypatch):
    force_unsupported_canonicalization(monkeypatch)
    result = verify_passport_envelope(load_envelope())
    assert check_named(result, CANON_CHECK).passed is False
    assert check_named(result, ALG_CHECK) is None


# 6. Unsupported canonicalization short-circuits before the signature step.
def test_unsupported_canonicalization_short_circuits_before_signature(monkeypatch):
    force_unsupported_canonicalization(monkeypatch)
    result = verify_passport_envelope(load_envelope())
    assert check_named(result, CANON_CHECK).passed is False
    assert check_named(result, SIGNATURE_CHECK) is None


# 7. Key-selection failure short-circuits before canonicalization.
def test_key_selection_failure_short_circuits_before_canonicalization():
    envelope = load_envelope()
    envelope["proofs"][0]["kid"] = "urn:aaid:key:no-such-key-canon-0001"
    result = verify_passport_envelope(envelope)
    assert check_named(result, KEY_CHECK).passed is False
    assert check_named(result, CANON_CHECK) is None


# 8. payload_hash failure short-circuits before canonicalization.
def test_payload_hash_failure_short_circuits_before_canonicalization():
    envelope = load_envelope()
    envelope["proofs"][0]["payload_hash"] = "0" * 64
    result = verify_passport_envelope(envelope)
    assert check_named(result, PAYLOAD_CHECK).passed is False
    assert check_named(result, CANON_CHECK) is None


# 9. schema failure short-circuits before canonicalization.
def test_schema_failure_short_circuits_before_canonicalization():
    envelope = load_envelope()
    envelope["proofs"][0]["unexpected_field"] = "x"
    result = verify_passport_envelope(envelope)
    assert check_named(result, "schema_valid").passed is False
    assert check_named(result, CANON_CHECK) is None


# 10. structural failure short-circuits before canonicalization.
def test_structural_failure_short_circuits_before_canonicalization():
    result = verify_passport_envelope(["passport", "proofs"])
    assert check_named(result, "envelope_is_mapping").passed is False
    assert check_named(result, CANON_CHECK) is None


# 11. No input reaches ALLOW through the canonicalization-scheme step.
def test_canonicalization_scheme_step_never_returns_allow():
    cases = [
        load_envelope(),
        {"passport": {"subject": "demo"}, "proofs": [{"proof_id": "x"}]},
        {"passport": {"subject": "demo"}, "proofs": []},
        {},
        None,
    ]
    for case in cases:
        result = verify_passport_envelope(case)
        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.valid is False


# 12. Signature verification is still not implemented.
def test_signature_verification_still_not_implemented():
    result = verify_passport_envelope(load_envelope())
    signature = check_named(result, SIGNATURE_CHECK)
    assert signature is not None
    assert signature.passed is False


# 13. passport_verifier.py imports no crypto or network modules.
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
