import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.canonicalization import hash_passport_payload

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


def test_minimal_example_reaches_payload_hash_valid_true():
    # The committed example stores the real canonical digest of its passport, so
    # the verifier recomputes it and records payload_hash_valid as passed.
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS)
    for name in STRUCTURAL_CHECK_NAMES:
        assert check_named(result, name).passed is True
    assert check_named(result, "schema_valid").passed is True
    payload_hash = check_named(result, "payload_hash_valid")
    assert payload_hash is not None
    assert payload_hash.passed is True


def test_minimal_example_denied_with_signature_not_implemented():
    # payload_hash passing does not allow the envelope: signature verification
    # is still not implemented, so the result fails closed to DENY.
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS)
    assert check_named(result, "payload_hash_valid").passed is True
    signature = check_named(result, "signature_verification_not_implemented")
    assert signature is not None
    assert signature.passed is False
    assert result.valid is False
    assert result.decision == DENY
    assert "signature" in result.reason.lower()


def test_tampering_passport_content_fails_payload_hash():
    # Changing the passport after issuance leaves the stored hash stale, so the
    # recomputed hash no longer matches and payload_hash_valid fails.
    envelope = load_envelope()
    tampered = copy.deepcopy(envelope)
    tampered["passport"]["subject"] = "A tampered subject"
    result = verify_passport_envelope(tampered, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS)
    payload_hash = check_named(result, "payload_hash_valid")
    assert payload_hash is not None
    assert payload_hash.passed is False
    assert result.valid is False
    assert result.decision == DENY


def test_tampering_proof_payload_hash_fails():
    # A different but schema-valid hex hash must not be trusted: the verifier
    # recomputes the hash and rejects the mismatch.
    envelope = load_envelope()
    tampered = copy.deepcopy(envelope)
    tampered["proofs"][0]["payload_hash"] = "b" * 64
    result = verify_passport_envelope(tampered, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS)
    payload_hash = check_named(result, "payload_hash_valid")
    assert payload_hash is not None
    assert payload_hash.passed is False
    assert result.valid is False
    assert result.decision == DENY


def test_unsupported_hash_alg_fails_closed():
    # An out-of-enum hash algorithm is rejected at schema validation before the
    # payload hash step runs, so the result is a clear DENY.
    envelope = load_envelope()
    tampered = copy.deepcopy(envelope)
    tampered["proofs"][0]["hash_alg"] = "SHA3-256"
    result = verify_passport_envelope(tampered)
    schema = check_named(result, "schema_valid")
    assert schema is not None
    assert schema.passed is False
    assert check_named(result, "payload_hash_valid") is None
    assert result.valid is False
    assert result.decision == DENY


def test_schema_invalid_input_does_not_run_payload_hash():
    # A schema violation short-circuits before the payload hash step.
    envelope = load_envelope()
    tampered = copy.deepcopy(envelope)
    tampered["passport"]["risk_class"] = "critical"
    result = verify_passport_envelope(tampered)
    schema = check_named(result, "schema_valid")
    assert schema is not None
    assert schema.passed is False
    assert check_named(result, "payload_hash_valid") is None
    assert result.valid is False
    assert result.decision == DENY


def test_malformed_structural_input_does_not_run_payload_hash():
    malformed_cases = [
        ["passport", "proofs"],
        {"proofs": [{"proof_id": "x"}]},
        {"passport": "not-a-mapping", "proofs": [{"proof_id": "x"}]},
        {"passport": {"subject": "demo"}},
        {"passport": {"subject": "demo"}, "proofs": []},
    ]
    for case in malformed_cases:
        result = verify_passport_envelope(case)
        assert check_named(result, "payload_hash_valid") is None, (
            f"payload_hash_valid must not run for structurally invalid {case!r}"
        )
        assert result.valid is False
        assert result.decision == DENY


def test_payload_hash_failure_short_circuits_before_signature_check():
    # A payload hash mismatch must stop before signature_verification_not_implemented.
    envelope = load_envelope()
    tampered = copy.deepcopy(envelope)
    tampered["proofs"][0]["payload_hash"] = "b" * 64
    result = verify_passport_envelope(tampered, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS)
    payload_hash = check_named(result, "payload_hash_valid")
    assert payload_hash is not None
    assert payload_hash.passed is False
    assert check_named(result, "signature_verification_not_implemented") is None


def test_payload_hash_step_never_returns_allow():
    envelope = load_envelope()
    wrong_hash = copy.deepcopy(envelope)
    wrong_hash["proofs"][0]["payload_hash"] = "b" * 64
    tampered_passport = copy.deepcopy(envelope)
    tampered_passport["passport"]["subject"] = "tampered"
    bad_alg = copy.deepcopy(envelope)
    bad_alg["proofs"][0]["hash_alg"] = "SHA3-256"
    malformed = {"passport": {"subject": "demo"}, "proofs": []}

    cases = [load_envelope(), wrong_hash, tampered_passport, bad_alg, malformed]
    # Reach the named step for the valid, trusted example so this sweep actually
    # exercises payload_hash_valid rather than stopping at issuer_trusted.
    reached = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS
    )
    assert check_named(reached, "payload_hash_valid") is not None

    for case in cases:
        result = verify_passport_envelope(
            case, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS
        )
        assert result.decision != ALLOW, f"unexpected ALLOW for {case!r}"
        assert result.decision == DENY
        assert result.valid is False


def test_no_signature_verification_in_this_step():
    # Changing the signature value while the payload hash stays correct must not
    # change the outcome: the signature is never actually verified here.
    envelope = load_envelope()
    tampered = copy.deepcopy(envelope)
    tampered["proofs"][0]["signature_b64u"] = "QW5vdGhlci1zaWduYXR1cmU"
    result = verify_passport_envelope(tampered, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS)
    assert check_named(result, "payload_hash_valid").passed is True
    signature = check_named(result, "signature_verification_not_implemented")
    assert signature is not None
    assert signature.passed is False
    assert result.decision == DENY
    assert "signature" in result.reason.lower()


def test_multi_proof_envelope_fails_closed_before_payload_hash():
    # Proof-selection hardening: a multi-proof envelope fails closed before the
    # payload-hash step, so payload_hash_valid is never recorded.
    envelope = load_envelope()
    tampered = copy.deepcopy(envelope)
    second = copy.deepcopy(tampered["proofs"][0])
    second["proof_id"] = "urn:aaid:proof:second-test-proof"
    second["payload_hash"] = "c" * 64
    tampered["proofs"].append(second)
    result = verify_passport_envelope(tampered, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS)
    assert check_named(result, "proof_count_allowed").passed is False
    assert check_named(result, "payload_hash_valid") is None
    assert result.decision == DENY
    assert result.valid is False


def test_multi_proof_fails_closed_even_with_correct_later_proof():
    # A correct later proof does not rescue a multi-proof envelope; it fails
    # closed at proof_count_allowed before payload-hash validation.
    envelope = load_envelope()
    tampered = copy.deepcopy(envelope)
    correct = hash_passport_payload(
        tampered["passport"], tampered["proofs"][0]["hash_alg"]
    )
    second = copy.deepcopy(tampered["proofs"][0])
    second["proof_id"] = "urn:aaid:proof:second-test-proof"
    second["payload_hash"] = correct
    tampered["proofs"].append(second)
    result = verify_passport_envelope(tampered, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS)
    assert check_named(result, "proof_count_allowed").passed is False
    assert check_named(result, "payload_hash_valid") is None
    assert result.decision == DENY


def test_hash_alg_length_mismatch_fails_payload_hash():
    # hash_alg and a too-short hash both pass the schema, but the verifier binds
    # them: a SHA-512 digest cannot equal a 64-character value.
    envelope = load_envelope()
    tampered = copy.deepcopy(envelope)
    tampered["proofs"][0]["hash_alg"] = "SHA-512"
    tampered["proofs"][0]["payload_hash"] = "a" * 64
    result = verify_passport_envelope(tampered, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS)
    schema = check_named(result, "schema_valid")
    assert schema is not None
    assert schema.passed is True
    payload_hash = check_named(result, "payload_hash_valid")
    assert payload_hash is not None
    assert payload_hash.passed is False
    assert result.decision == DENY
    assert check_named(result, "signature_verification_not_implemented") is None


def test_changing_a_proof_field_does_not_affect_payload_hash():
    # Proof metadata is detached and not part of the hashed payload, so changing
    # a non-hash proof field leaves payload_hash_valid passing.
    envelope = load_envelope()
    tampered = copy.deepcopy(envelope)
    tampered["proofs"][0]["signature_b64u"] = "QW5vdGhlci1zaWduYXR1cmU"
    result = verify_passport_envelope(tampered, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS)
    payload_hash = check_named(result, "payload_hash_valid")
    assert payload_hash is not None
    assert payload_hash.passed is True


def test_payload_hash_failure_reason_is_about_hash_not_signature():
    # The recorded failure must read as a payload hash mismatch, not a signature
    # check, so the decision stays explainable and auditable.
    envelope = load_envelope()
    tampered = copy.deepcopy(envelope)
    tampered["proofs"][0]["payload_hash"] = "b" * 64
    result = verify_passport_envelope(tampered, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS)
    payload_hash = check_named(result, "payload_hash_valid")
    assert payload_hash is not None
    assert payload_hash.passed is False
    assert payload_hash.name == "payload_hash_valid"
    assert payload_hash.reason
    assert "payload hash" in payload_hash.reason.lower()
    assert "signature" not in payload_hash.reason.lower()
    assert "payload hash" in result.reason.lower()
    assert "signature" not in result.reason.lower()
