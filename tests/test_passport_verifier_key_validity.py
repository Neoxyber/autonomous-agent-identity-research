import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = Path(__file__).resolve().parent

import pytest

import aaid.passport_verifier as passport_verifier_module
from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.canonicalization import hash_passport_payload
from aaid.verification import VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PV_SOURCE_PATH = SRC / "aaid" / "passport_verifier.py"

KEY_CHECK = "verification_key_selected"
VALIDITY_CHECK = "verification_key_valid_for_proof"
INPUT_CHECK = "signature_input_prepared"
ALG_CHECK = "signature_algorithm_supported"
SIGNATURE_CHECK = "signature_verification_not_implemented"
PAYLOAD_CHECK = "payload_hash_valid"

KID = "urn:aaid:key:018fd7c2-8c44-72ff-91ab-2e81e9fd4422"
OTHER_KEY_AAID = "urn:aaid:key:00000000-0000-7000-8000-000000000000"


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


def rehash(envelope):
    # Changing a public key field changes the canonical passport payload, so the
    # selected proof's recorded payload_hash must be recomputed for the envelope
    # to still pass payload_hash_valid and reach the key-validity check.
    proof = envelope["proofs"][0]
    proof["payload_hash"] = hash_passport_payload(
        envelope["passport"], proof["hash_alg"]
    )
    return envelope


def envelope_with_key_fields(**fields):
    envelope = load_envelope()
    envelope["passport"]["public_keys"][0].update(fields)
    return rehash(envelope)


def envelope_without_key_field(field):
    envelope = load_envelope()
    envelope["passport"]["public_keys"][0].pop(field, None)
    return rehash(envelope)


def envelope_with_proof_field(field, value):
    # Proof-only change: the payload hash is computed over the passport, so it
    # stays valid without rehashing.
    envelope = load_envelope()
    envelope["proofs"][0][field] = value
    return envelope


def verify(envelope):
    return verify_passport_envelope(
        envelope, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


# Non-strict timestamp strings that pass schema (format is not enforced) but the
# verifier's strict UTC parser must reject.
NON_STRICT_TIMESTAMPS = [
    "2026-06-15T00:00:00+05:00",  # explicit offset, not Z
    "2026-06-15T00:00:00+00:00",  # +00:00 is not the Z form
    "2026-06-15 00:00:00Z",       # space separator
    "2026-06-15T00:00:00.500Z",   # fractional seconds
    "2026-06-15T00:00:00z",       # lowercase z
    "2026-06-15T00:00:00Z ",      # trailing whitespace
    " 2026-06-15T00:00:00Z",      # leading whitespace
    "2026-06-15",                 # date only
    "",                           # empty string
    "2026-13-01T00:00:00Z",       # calendar-invalid month (matches shape)
    "2026-06-15T24:00:00Z",       # calendar-invalid hour (matches shape)
]


# --- happy path: minimal example passes the new check and still DENIES ---

def test_minimal_example_passes_key_validity_and_still_denies():
    result = verify(load_envelope())
    validity = check_named(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is True
    signature = check_named(result, SIGNATURE_CHECK)
    assert signature is not None
    assert signature.passed is False
    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False


def test_missing_optional_not_after_passes():
    # The minimal example key has no not_after; created_at <= now, so it passes.
    envelope = load_envelope()
    assert "not_after" not in envelope["passport"]["public_keys"][0]
    result = verify(envelope)
    assert check_named(result, VALIDITY_CHECK).passed is True


# --- created_at: required, inclusive lower bound ---

def test_created_at_after_now_fails_closed_before_signature_input():
    result = verify(envelope_with_key_fields(created_at="2026-06-20T00:00:00Z"))
    validity = check_named(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is False
    assert check_named(result, INPUT_CHECK) is None
    assert check_named(result, SIGNATURE_CHECK) is None
    assert result.decision == DENY
    assert result.valid is False


def test_created_at_equal_now_passes():
    result = verify(envelope_with_key_fields(created_at="2026-06-15T00:00:00Z"))
    validity = check_named(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is True


@pytest.mark.parametrize("bad", NON_STRICT_TIMESTAMPS)
def test_malformed_created_at_fails_closed(bad):
    result = verify(envelope_with_key_fields(created_at=bad))
    validity = check_named(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is False
    assert check_named(result, INPUT_CHECK) is None
    assert result.decision == DENY


# --- not_after: optional, exclusive upper bound ---

def test_not_after_before_now_fails_closed():
    result = verify(envelope_with_key_fields(not_after="2026-06-10T00:00:00Z"))
    validity = check_named(result, VALIDITY_CHECK)
    assert validity.passed is False
    assert check_named(result, INPUT_CHECK) is None
    assert result.decision == DENY


def test_not_after_equal_now_fails_closed():
    result = verify(envelope_with_key_fields(not_after="2026-06-15T00:00:00Z"))
    validity = check_named(result, VALIDITY_CHECK)
    assert validity.passed is False
    assert result.decision == DENY


def test_not_after_after_now_passes():
    result = verify(envelope_with_key_fields(not_after="2026-06-20T00:00:00Z"))
    validity = check_named(result, VALIDITY_CHECK)
    assert validity.passed is True


@pytest.mark.parametrize("bad", NON_STRICT_TIMESTAMPS)
def test_malformed_not_after_fails_closed(bad):
    result = verify(envelope_with_key_fields(not_after=bad))
    validity = check_named(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is False
    assert result.decision == DENY


def test_inverted_window_created_after_not_after_fails_closed():
    result = verify(
        envelope_with_key_fields(
            created_at="2026-06-14T00:00:00Z",
            not_after="2026-06-10T00:00:00Z",
        )
    )
    validity = check_named(result, VALIDITY_CHECK)
    assert validity.passed is False
    assert result.decision == DENY


# --- verification_method binding to the selected key kid ---

def test_verification_method_mismatch_fails_closed():
    # A different valid key aaid in verification_method must fail closed: the
    # proof must name the same key it is verified against.
    result = verify(envelope_with_proof_field("verification_method", OTHER_KEY_AAID))
    # Key selection still passes (kid is unchanged), so the new check is reached.
    assert check_named(result, KEY_CHECK).passed is True
    validity = check_named(result, VALIDITY_CHECK)
    assert validity is not None
    assert validity.passed is False
    assert check_named(result, INPUT_CHECK) is None
    assert result.decision == DENY


# --- direct helper coverage: exact equality, no normalization; missing field ---

def _key(**over):
    base = {
        "kid": KID,
        "kty": "ML-DSA",
        "alg": "ML-DSA-65",
        "purpose": "sig",
        "status": "active",
        "created_at": "2026-05-29T00:00:00Z",
    }
    base.update(over)
    return base


def _proof(verification_method=KID):
    return {"verification_method": verification_method, "kid": KID, "alg": "ML-DSA-65"}


def _validity(key, proof):
    return passport_verifier_module._verification_key_valid_for_proof_check(
        key, proof, VALID_NOW
    )


def test_helper_exact_binding_passes():
    check = _validity(_key(), _proof(KID))
    assert check.name == VALIDITY_CHECK
    assert check.passed is True


@pytest.mark.parametrize(
    "variant",
    [
        KID[:-4],                # prefix of the kid
        KID + "-extra",          # superstring of the kid
        KID.replace("018fd7c2", "018FD7C2"),  # case variant of the id segment
        "key:018fd7c2-8c44-72ff-91ab-2e81e9fd4422",  # substring of the kid
    ],
)
def test_helper_rejects_prefix_substring_superstring_and_case(variant):
    assert variant != KID
    check = _validity(_key(), _proof(variant))
    assert check.name == VALIDITY_CHECK
    assert check.passed is False


def test_helper_missing_created_at_fails_closed():
    key = _key()
    key.pop("created_at", None)
    check = _validity(key, _proof(KID))
    assert check.passed is False


def test_helper_missing_not_after_passes():
    # not_after is optional: absence must not fail the check.
    check = _validity(_key(), _proof(KID))
    assert check.passed is True


# --- ordering and short-circuit ---

def test_validity_runs_after_key_selected_and_before_signature_input():
    result = verify(load_envelope())
    key_index = check_index(result, KEY_CHECK)
    validity_index = check_index(result, VALIDITY_CHECK)
    input_index = check_index(result, INPUT_CHECK)
    assert -1 not in (key_index, validity_index, input_index)
    assert key_index < validity_index < input_index


def test_key_selection_failure_short_circuits_before_validity():
    # An unknown proof kid fails key selection before the new check runs.
    result = verify(envelope_with_proof_field("kid", "urn:aaid:key:no-such-key-0001"))
    assert check_named(result, KEY_CHECK).passed is False
    assert check_named(result, VALIDITY_CHECK) is None
    assert check_named(result, INPUT_CHECK) is None


def test_payload_hash_failure_short_circuits_before_validity():
    envelope = load_envelope()
    envelope["proofs"][0]["payload_hash"] = "0" * 64
    result = verify(envelope)
    assert check_named(result, PAYLOAD_CHECK).passed is False
    assert check_named(result, VALIDITY_CHECK) is None


# --- never-ALLOW invariant across key-validity outcomes ---

def test_key_validity_step_never_returns_allow():
    cases = [
        load_envelope(),
        envelope_with_key_fields(created_at="2026-06-20T00:00:00Z"),
        envelope_with_key_fields(not_after="2026-06-10T00:00:00Z"),
        envelope_with_key_fields(not_after="2026-06-15T00:00:00Z"),
        envelope_with_key_fields(created_at="2026-06-15T00:00:00Z"),
        envelope_with_key_fields(created_at="bad-timestamp"),
        envelope_with_proof_field("verification_method", OTHER_KEY_AAID),
    ]
    # Reach the named step for the valid example so this sweep actually exercises
    # the key-validity check.
    reached = verify(load_envelope())
    assert check_named(reached, VALIDITY_CHECK) is not None

    for case in cases:
        result = verify(case)
        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW, f"unexpected ALLOW for {case!r}"
        assert result.decision == DENY
        assert result.valid is False


# --- raw JSON parity is unchanged ---

def test_raw_json_parity_includes_key_validity():
    direct = verify(load_envelope())
    raw = verify_passport_json(
        load_text(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    assert raw.checks[0].name == "raw_json_parsed"
    assert raw.checks[1:] == direct.checks
    assert raw.reason == direct.reason
    assert raw.decision == direct.decision
    assert check_named(raw, VALIDITY_CHECK).passed is True


# --- guard: the key-validity path introduces no network/crypto imports ---

def test_no_forbidden_imports_after_key_validity():
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
