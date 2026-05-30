import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.verification import VerificationCheck, VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"

STRUCTURAL_CHECK_NAMES = (
    "envelope_is_mapping",
    "passport_present",
    "passport_is_mapping",
    "proofs_present",
    "proofs_is_sequence",
    "proofs_non_empty",
)


def load_envelope():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def check_named(result, name):
    for check in result.checks:
        if check.name == name:
            return check
    return None


def test_non_mapping_envelope_is_denied():
    result = verify_passport_envelope(["passport", "proofs"])
    assert result.valid is False
    assert result.decision == DENY
    failed = check_named(result, "envelope_is_mapping")
    assert failed is not None
    assert failed.passed is False


def test_missing_passport_is_denied():
    result = verify_passport_envelope({"proofs": [{"proof_id": "x"}]})
    assert result.valid is False
    assert result.decision == DENY
    assert check_named(result, "envelope_is_mapping").passed is True
    failed = check_named(result, "passport_present")
    assert failed is not None
    assert failed.passed is False


def test_non_mapping_passport_is_denied():
    result = verify_passport_envelope(
        {"passport": "not-a-mapping", "proofs": [{"proof_id": "x"}]}
    )
    assert result.valid is False
    assert result.decision == DENY
    assert check_named(result, "passport_present").passed is True
    failed = check_named(result, "passport_is_mapping")
    assert failed is not None
    assert failed.passed is False


def test_missing_proofs_is_denied():
    result = verify_passport_envelope({"passport": {"subject": "demo"}})
    assert result.valid is False
    assert result.decision == DENY
    assert check_named(result, "passport_is_mapping").passed is True
    failed = check_named(result, "proofs_present")
    assert failed is not None
    assert failed.passed is False


def test_string_proofs_is_rejected():
    result = verify_passport_envelope(
        {"passport": {"subject": "demo"}, "proofs": "signature"}
    )
    assert result.valid is False
    assert result.decision == DENY
    assert check_named(result, "proofs_present").passed is True
    failed = check_named(result, "proofs_is_sequence")
    assert failed is not None
    assert failed.passed is False


def test_bytes_proofs_is_rejected():
    result = verify_passport_envelope(
        {"passport": {"subject": "demo"}, "proofs": b"signature"}
    )
    assert result.valid is False
    assert result.decision == DENY
    failed = check_named(result, "proofs_is_sequence")
    assert failed is not None
    assert failed.passed is False


def test_empty_proofs_is_rejected():
    result = verify_passport_envelope(
        {"passport": {"subject": "demo"}, "proofs": []}
    )
    assert result.valid is False
    assert result.decision == DENY
    assert check_named(result, "proofs_is_sequence").passed is True
    failed = check_named(result, "proofs_non_empty")
    assert failed is not None
    assert failed.passed is False


def test_minimal_example_is_denied_due_to_signature_not_implemented():
    result = verify_passport_envelope(load_envelope())
    assert result.valid is False
    assert result.decision == DENY
    for name in STRUCTURAL_CHECK_NAMES:
        check = check_named(result, name)
        assert check is not None, f"missing structural check {name}"
        assert check.passed is True, f"structural check {name} should pass"
    signature = check_named(result, "signature_verification_not_implemented")
    assert signature is not None
    assert signature.passed is False
    assert "signature" in result.reason.lower()


def test_checks_are_verification_check_instances():
    result = verify_passport_envelope(load_envelope())
    assert len(result.checks) >= 1
    assert all(isinstance(check, VerificationCheck) for check in result.checks)


def test_checks_stored_as_tuple():
    result = verify_passport_envelope(load_envelope())
    assert isinstance(result.checks, tuple)


def test_skeleton_never_returns_allow():
    cases = [
        load_envelope(),
        {},
        {"passport": {"subject": "demo"}},
        {"proofs": [{"proof_id": "x"}]},
        {"passport": "x", "proofs": [{"proof_id": "x"}]},
        {"passport": {"subject": "demo"}, "proofs": []},
        {"passport": {"subject": "demo"}, "proofs": "x"},
        {"passport": {"subject": "demo"}, "proofs": b"x"},
        [],
        "x",
        42,
        None,
    ]
    for case in cases:
        result = verify_passport_envelope(case)
        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW, f"unexpected ALLOW for {case!r}"
        assert result.decision == DENY
        assert result.valid is False


def test_verify_passport_envelope_exported_from_package():
    import aaid

    from aaid import verify_passport_envelope as exported

    assert "verify_passport_envelope" in aaid.__all__
    assert exported is verify_passport_envelope


def test_skeleton_introduces_no_crypto_or_signing():
    import aaid.passport_verifier as mod

    assert not hasattr(mod, "hashlib")
    assert not hasattr(mod, "hmac")
    assert not hasattr(mod, "hash_passport_payload")
    assert not hasattr(mod, "canonicalize_passport_payload")

    forbidden_substrings = ("sign", "hash", "crypto")
    for name in dir(mod):
        if name.startswith("_"):
            continue
        attr = getattr(mod, name)
        if callable(attr):
            lowered = name.lower()
            assert not any(s in lowered for s in forbidden_substrings), (
                f"{name} suggests signing/crypto/hash logic, which this "
                "structural-only verifier must not implement"
            )
