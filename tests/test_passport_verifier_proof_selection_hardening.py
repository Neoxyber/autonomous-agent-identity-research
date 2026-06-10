import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = Path(__file__).resolve().parent

from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.verification import VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PV_SOURCE_PATH = SRC / "aaid" / "passport_verifier.py"

COUNT_CHECK = "proof_count_allowed"
PROOF_CHECK = "proof_selected"
PAYLOAD_CHECK = "payload_hash_valid"
KEY_CHECK = "verification_key_selected"
KEY_VALIDITY_CHECK = "verification_key_valid_for_proof"
CANON_CHECK = "signature_canonicalization_supported"
INPUT_CHECK = "signature_input_prepared"
ALG_CHECK = "signature_algorithm_supported"
SIGNATURE_CHECK = "signature_verification_not_implemented"

SIGNATURE_STAGE_CHECKS = (
    PROOF_CHECK,
    PAYLOAD_CHECK,
    KEY_CHECK,
    KEY_VALIDITY_CHECK,
    CANON_CHECK,
    INPUT_CHECK,
    ALG_CHECK,
    SIGNATURE_CHECK,
)


def load_envelope():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_text():
    return EXAMPLE_PATH.read_text(encoding="utf-8")


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


def envelope_with_n_proofs(n):
    # Build an envelope whose proofs sequence has exactly n schema-valid proofs.
    # Each extra proof is a deep copy of the first with a distinct proof_id, so
    # the only meaningful difference from the minimal example is the proof count.
    envelope = load_envelope()
    first = envelope["proofs"][0]
    extras = []
    for index in range(1, n):
        extra = copy.deepcopy(first)
        extra["proof_id"] = f"urn:aaid:proof:extra-proof-{index}"
        extras.append(extra)
    envelope["proofs"] = [first, *extras]
    return envelope


def verify(envelope):
    return verify_passport_envelope(
        envelope, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


# --- single proof: passes the new check, still DENIES ---

def test_single_proof_example_passes_count_check_and_still_denies():
    result = verify(load_envelope())
    count = check_named(result, COUNT_CHECK)
    assert count is not None
    assert count.passed is True
    assert check_named(result, PROOF_CHECK).passed is True
    signature = check_named(result, SIGNATURE_CHECK)
    assert signature is not None
    assert signature.passed is False
    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False


# --- two proofs: fail closed at the new check, before any later step ---

def test_two_proof_envelope_fails_closed_at_count_check():
    result = verify(envelope_with_n_proofs(2))
    count = check_named(result, COUNT_CHECK)
    assert count is not None
    assert count.passed is False
    assert result.decision == DENY
    assert result.valid is False


def test_two_proof_envelope_does_not_record_proof_selected():
    result = verify(envelope_with_n_proofs(2))
    assert check_named(result, PROOF_CHECK) is None


def test_two_proof_envelope_does_not_record_payload_hash_valid():
    result = verify(envelope_with_n_proofs(2))
    assert check_named(result, PAYLOAD_CHECK) is None


def test_two_proof_envelope_does_not_record_verification_key_selected():
    result = verify(envelope_with_n_proofs(2))
    assert check_named(result, KEY_CHECK) is None


def test_two_proof_envelope_does_not_reach_signature_stage_checks():
    result = verify(envelope_with_n_proofs(2))
    for name in SIGNATURE_STAGE_CHECKS:
        assert check_named(result, name) is None, (
            f"{name} must not run for a multi-proof envelope"
        )


def test_three_proof_envelope_also_fails_closed():
    result = verify(envelope_with_n_proofs(3))
    assert check_named(result, COUNT_CHECK).passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


# --- ordering: after proofs_non_empty, before proof_selected ---

def test_count_check_runs_after_proofs_non_empty_and_before_proof_selected():
    result = verify(load_envelope())
    non_empty_index = check_index(result, "proofs_non_empty")
    count_index = check_index(result, COUNT_CHECK)
    proof_index = check_index(result, PROOF_CHECK)
    assert -1 not in (non_empty_index, count_index, proof_index)
    assert non_empty_index < count_index < proof_index


# --- existing structural proof checks still behave as before ---

def test_empty_proofs_still_fails_at_proofs_non_empty_not_count_check():
    result = verify_passport_envelope(
        {"passport": {"subject": "demo"}, "proofs": []}
    )
    non_empty = check_named(result, "proofs_non_empty")
    assert non_empty is not None
    assert non_empty.passed is False
    # The count check is never reached for an empty sequence.
    assert check_named(result, COUNT_CHECK) is None
    assert result.decision == DENY


def test_missing_proofs_still_fails_at_proofs_present_not_count_check():
    result = verify_passport_envelope({"passport": {"subject": "demo"}})
    present = check_named(result, "proofs_present")
    assert present is not None
    assert present.passed is False
    assert check_named(result, COUNT_CHECK) is None


def test_non_sequence_proofs_still_fails_at_proofs_is_sequence_not_count_check():
    result = verify_passport_envelope(
        {"passport": {"subject": "demo"}, "proofs": "not-a-sequence"}
    )
    is_sequence = check_named(result, "proofs_is_sequence")
    assert is_sequence is not None
    assert is_sequence.passed is False
    assert check_named(result, COUNT_CHECK) is None


# --- never-ALLOW invariant ---

def test_proof_count_step_never_returns_allow():
    cases = [
        load_envelope(),
        envelope_with_n_proofs(2),
        envelope_with_n_proofs(3),
        {"passport": {"subject": "demo"}, "proofs": []},
    ]
    # Reach the named step for the valid single-proof example so this sweep
    # actually exercises the count check.
    reached = verify(load_envelope())
    assert check_named(reached, COUNT_CHECK) is not None

    for case in cases:
        result = verify(case)
        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW, f"unexpected ALLOW for {case!r}"
        assert result.decision == DENY
        assert result.valid is False


# --- raw JSON parity for a valid single-proof envelope is unchanged ---

def test_raw_json_parity_includes_count_check():
    direct = verify(load_envelope())
    raw = verify_passport_json(
        load_text(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    assert raw.checks[0].name == "raw_json_parsed"
    assert raw.checks[1:] == direct.checks
    assert raw.reason == direct.reason
    assert raw.decision == direct.decision
    assert check_named(raw, COUNT_CHECK).passed is True


# --- guard: no network/crypto/dependency imports ---

def test_no_forbidden_imports_after_proof_count():
    import aaid.passport_verifier as module

    forbidden = (
        "requests", "httpx", "urllib", "socket", "http.client",
        "hashlib", "hmac", "base64", "ssl", "secrets", "cryptography",
        "pqcrypto", "oqs",
    )
    for name in forbidden:
        top = name.split(".")[0]
        assert not hasattr(module, top), f"verifier must not import {name}"
    source = PV_SOURCE_PATH.read_text(encoding="utf-8")
    for name in forbidden:
        assert f"import {name}" not in source
        assert f"from {name}" not in source
