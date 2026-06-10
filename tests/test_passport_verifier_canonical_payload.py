import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = Path(__file__).resolve().parent

import aaid.passport_verifier as passport_verifier_module
from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.canonicalization import canonicalize_passport_payload
from aaid.verification import VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PV_SOURCE_PATH = SRC / "aaid" / "passport_verifier.py"

PROOF_CHECK = "proof_selected"
PREPARED_CHECK = "canonical_payload_prepared"
PAYLOAD_CHECK = "payload_hash_valid"
KEY_CHECK = "verification_key_selected"
INPUT_CHECK = "signature_input_prepared"
SIGNATURE_CHECK = "signature_verification_not_implemented"

LATER_CHECKS = (
    PAYLOAD_CHECK,
    KEY_CHECK,
    "verification_key_valid_for_proof",
    "signature_canonicalization_supported",
    INPUT_CHECK,
    "signature_algorithm_supported",
    SIGNATURE_CHECK,
)


def load_envelope():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_text():
    return EXAMPLE_PATH.read_text(encoding="utf-8")


def load_passport():
    return load_envelope()["passport"]


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


def verify(envelope):
    return verify_passport_envelope(
        envelope, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


class _FakeCanonicalizerError(Exception):
    """A candidate-canonicalizer-style error, defined without importing REF-014."""


def _raise_value_error(_passport):
    raise ValueError("simulated canonicalization failure")


def _raise_candidate_error(_passport):
    raise _FakeCanonicalizerError("simulated candidate-canonicalizer failure")


# --- happy path ---

def test_minimal_example_records_canonical_payload_prepared_passed():
    result = verify(load_envelope())
    prepared = check_named(result, PREPARED_CHECK)
    assert prepared is not None
    assert prepared.passed is True
    signature = check_named(result, SIGNATURE_CHECK)
    assert signature is not None
    assert signature.passed is False
    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False


# --- ordering ---

def test_canonical_payload_prepared_ordering():
    result = verify(load_envelope())
    proof_index = check_index(result, PROOF_CHECK)
    prepared_index = check_index(result, PREPARED_CHECK)
    payload_index = check_index(result, PAYLOAD_CHECK)
    input_index = check_index(result, INPUT_CHECK)
    assert -1 not in (proof_index, prepared_index, payload_index, input_index)
    assert proof_index < prepared_index < payload_index
    assert prepared_index < input_index


# --- canonicalization ValueError fails closed ---

def test_canonicalization_value_error_fails_closed(monkeypatch):
    monkeypatch.setattr(
        passport_verifier_module.canonicalization,
        "canonicalize_passport_payload",
        _raise_value_error,
    )
    result = verify(load_envelope())
    assert isinstance(result, VerificationResult)  # no exception escaped
    prepared = check_named(result, PREPARED_CHECK)
    assert prepared is not None
    assert prepared.passed is False
    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False
    for name in LATER_CHECKS:
        assert check_named(result, name) is None, (
            f"{name} must not run after canonical payload preparation fails"
        )


# --- candidate-style exception fails closed ---

def test_candidate_canonicalizer_error_fails_closed(monkeypatch):
    monkeypatch.setattr(
        passport_verifier_module.canonicalization,
        "canonicalize_passport_payload",
        _raise_candidate_error,
    )
    result = verify(load_envelope())
    assert isinstance(result, VerificationResult)  # no exception escaped
    prepared = check_named(result, PREPARED_CHECK)
    assert prepared is not None
    assert prepared.passed is False
    assert result.decision == DENY
    assert result.valid is False
    assert check_named(result, PAYLOAD_CHECK) is None
    assert check_named(result, SIGNATURE_CHECK) is None


# --- raw JSON parity ---

def test_raw_json_parity_includes_canonical_payload_prepared():
    direct = verify(load_envelope())
    raw = verify_passport_json(
        load_text(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    assert raw.checks[0].name == "raw_json_parsed"
    assert raw.checks[1:] == direct.checks
    assert raw.reason == direct.reason
    assert raw.decision == direct.decision
    assert check_named(raw, PREPARED_CHECK).passed is True


def test_raw_json_canonicalization_failure_fails_closed(monkeypatch):
    monkeypatch.setattr(
        passport_verifier_module.canonicalization,
        "canonicalize_passport_payload",
        _raise_value_error,
    )
    result = verify_passport_json(
        load_text(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    assert isinstance(result, VerificationResult)  # no exception escaped
    assert check_named(result, "raw_json_parsed").passed is True
    assert check_named(result, PREPARED_CHECK).passed is False
    assert check_named(result, PAYLOAD_CHECK) is None
    assert result.decision == DENY
    assert result.valid is False


# --- signature-input reuse ---

def test_prepare_signature_input_default_path_canonicalizes():
    passport = load_passport()
    check, data = passport_verifier_module._prepare_signature_input(passport)
    assert check.name == INPUT_CHECK
    assert check.passed is True
    assert data == canonicalize_passport_payload(passport)


def test_prepare_signature_input_reuses_provided_bytes():
    passport = load_passport()
    sentinel = b"sentinel-canonical-bytes"
    check, data = passport_verifier_module._prepare_signature_input(
        passport, canonical_payload=sentinel
    )
    assert check.name == INPUT_CHECK
    assert check.passed is True
    assert data == sentinel


# --- never-ALLOW invariant ---

def test_canonical_payload_step_never_returns_allow(monkeypatch):
    # Reach the named step for the valid example so this exercises the check.
    reached = verify(load_envelope())
    assert check_named(reached, PREPARED_CHECK) is not None

    monkeypatch.setattr(
        passport_verifier_module.canonicalization,
        "canonicalize_passport_payload",
        _raise_value_error,
    )
    result = verify(load_envelope())
    assert isinstance(result, VerificationResult)
    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False


# --- guard: no forbidden imports introduced ---

def test_no_forbidden_imports_after_canonical_payload():
    import aaid.passport_verifier as module

    forbidden = (
        "requests", "httpx", "urllib", "socket", "http.client",
        "hashlib", "hmac", "base64", "ssl", "secrets", "cryptography",
        "pqcrypto", "oqs", "rfc8785", "jcs",
    )
    for name in forbidden:
        top = name.split(".")[0]
        assert not hasattr(module, top), f"verifier must not import {name}"
    source = PV_SOURCE_PATH.read_text(encoding="utf-8")
    for name in forbidden:
        assert f"import {name}" not in source
        assert f"from {name}" not in source
