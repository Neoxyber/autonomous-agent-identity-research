import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = Path(__file__).resolve().parent

import pytest

from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.verification import VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"

ISSUER_CHECK = "issuer_trusted"
EXAMPLE_ISSUER = "urn:aaid:issuer:aixybertech-issuer"
OTHER_ISSUER = "urn:aaid:issuer:some-other-issuer"


def load_text():
    return EXAMPLE_PATH.read_text(encoding="utf-8")


def load_envelope():
    return json.loads(load_text())


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


# --- Trusted issuer: the check passes and the chain continues ---

def test_trusted_issuer_passes_and_reaches_proof_selected():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS
    )
    issuer = check_named(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is True
    assert "configured as trusted" in issuer.reason.lower()
    # The gate opens, so proof selection and later checks now run.
    assert check_named(result, "proof_selected").passed is True


def test_trusted_issuer_valid_now_still_denies_and_never_allows():
    # A trusted issuer must not open an ALLOW path: signature verification is
    # still not implemented, so the verifier fails closed.
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS
    )
    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False
    signature = check_named(result, "signature_verification_not_implemented")
    assert signature is not None
    assert signature.passed is False


@pytest.mark.parametrize(
    "trusted",
    [
        frozenset({EXAMPLE_ISSUER}),
        {EXAMPLE_ISSUER},
        [EXAMPLE_ISSUER],
        (EXAMPLE_ISSUER,),
    ],
)
def test_any_collection_form_carrying_the_issuer_passes(trusted):
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=trusted
    )
    assert check_named(result, ISSUER_CHECK).passed is True


# --- Not configured (default None): fail closed, short-circuit ---

def test_default_none_trust_fails_closed_and_short_circuits():
    # trusted_issuers defaults to None: issuer trust is not configured.
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW)
    issuer = check_named(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is False
    assert "no trusted issuers were provided" in issuer.reason.lower()
    assert result.decision == DENY
    assert result.valid is False
    # Time and lifecycle still pass; issuer trust is the failing gate.
    assert check_named(result, "passport_time_valid").passed is True
    assert check_named(result, "lifecycle_status_allows_verification").passed is True
    # The chain short-circuits before proof selection and everything after it.
    assert check_named(result, "proof_selected") is None
    assert check_named(result, "payload_hash_valid") is None
    assert check_named(result, "verification_key_selected") is None
    assert check_named(result, "signature_verification_not_implemented") is None


# --- Configured but issuer absent: fail closed ---

def test_empty_collection_fails_closed_not_trusted():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=frozenset()
    )
    issuer = check_named(result, ISSUER_CHECK)
    assert issuer.passed is False
    assert "not configured as trusted" in issuer.reason.lower()
    assert result.decision == DENY
    assert check_named(result, "proof_selected") is None


def test_unknown_issuer_fails_closed_not_trusted():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=frozenset({OTHER_ISSUER})
    )
    issuer = check_named(result, ISSUER_CHECK)
    assert issuer.passed is False
    assert "not configured as trusted" in issuer.reason.lower()
    assert result.decision == DENY
    assert check_named(result, "proof_selected") is None


# --- Misconfiguration guards: a string or a mapping must fail closed ---

def test_string_trust_config_fails_closed_even_if_it_contains_the_issuer():
    # The full issuer id passed as a bare string would, under a naive ``in``
    # test, match itself as a substring. The guard must reject strings so this
    # never opens the gate.
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=EXAMPLE_ISSUER
    )
    issuer = check_named(result, ISSUER_CHECK)
    assert issuer.passed is False
    assert "not a string" in issuer.reason.lower()
    assert result.decision == DENY
    assert check_named(result, "proof_selected") is None


def test_mapping_trust_config_fails_closed():
    # A mapping keyed by issuer id is registry-shaped and must fail closed
    # rather than membership-test on keys.
    result = verify_passport_envelope(
        load_envelope(),
        now=VALID_NOW,
        trusted_issuers={EXAMPLE_ISSUER: {"note": "demo"}},
    )
    issuer = check_named(result, ISSUER_CHECK)
    assert issuer.passed is False
    assert "not a mapping" in issuer.reason.lower()
    assert result.decision == DENY
    assert check_named(result, "proof_selected") is None


@pytest.mark.parametrize("bad", [123, 1.5, True])
def test_non_iterable_trust_config_fails_closed_without_raising(bad):
    # A non-collection trust configuration (for example an int, float, or bool)
    # must fail closed at issuer_trusted rather than raising a TypeError on the
    # membership test.
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=bad
    )
    issuer = check_named(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is False
    assert "collection of issuer identifiers" in issuer.reason.lower()
    assert result.decision == DENY
    assert result.valid is False
    assert check_named(result, "proof_selected") is None


# --- Ordering: after lifecycle, before proof selection ---

def test_issuer_trusted_runs_after_lifecycle_and_before_proof_selected():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS
    )
    schema_index = check_index(result, "schema_valid")
    time_index = check_index(result, "passport_time_valid")
    lifecycle_index = check_index(result, "lifecycle_status_allows_verification")
    issuer_index = check_index(result, ISSUER_CHECK)
    proof_index = check_index(result, "proof_selected")
    assert -1 not in (
        schema_index,
        time_index,
        lifecycle_index,
        issuer_index,
        proof_index,
    )
    assert schema_index < time_index < lifecycle_index < issuer_index < proof_index


# --- issuer trust runs only after lifecycle: earlier failures short-circuit ---

def test_lifecycle_failure_short_circuits_before_issuer_trusted():
    envelope = load_envelope()
    envelope["passport"]["lifecycle_status"] = "revoked"
    result = verify_passport_envelope(
        envelope, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS
    )
    assert check_named(result, "lifecycle_status_allows_verification").passed is False
    assert check_named(result, ISSUER_CHECK) is None
    assert result.decision == DENY


# --- Never ALLOW across every trust configuration ---

def test_issuer_trust_step_never_returns_allow():
    cases = [
        TRUSTED_ISSUERS,
        None,
        frozenset(),
        frozenset({OTHER_ISSUER}),
        EXAMPLE_ISSUER,  # string misconfiguration
        {EXAMPLE_ISSUER: {"note": "demo"}},  # mapping misconfiguration
        123,  # non-iterable misconfiguration
        1.5,  # non-iterable misconfiguration
        True,  # non-iterable misconfiguration
    ]
    for trusted in cases:
        result = verify_passport_envelope(
            load_envelope(), now=VALID_NOW, trusted_issuers=trusted
        )
        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW, f"unexpected ALLOW for {trusted!r}"
        assert result.decision == DENY
        assert result.valid is False


# --- Raw JSON entry point forwards the trust configuration ---

def test_verify_passport_json_forwards_trusted_issuers_pass():
    result = verify_passport_json(
        load_text(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS
    )
    assert check_named(result, "raw_json_parsed").passed is True
    assert check_named(result, ISSUER_CHECK).passed is True
    assert check_named(result, "proof_selected").passed is True
    assert result.decision == DENY


def test_verify_passport_json_without_trust_fails_issuer_trusted():
    result = verify_passport_json(load_text(), now=VALID_NOW)
    assert check_named(result, "raw_json_parsed").passed is True
    issuer = check_named(result, ISSUER_CHECK)
    assert issuer.passed is False
    assert "no trusted issuers were provided" in issuer.reason.lower()
    assert check_named(result, "proof_selected") is None
    assert result.decision == DENY


def test_verify_passport_json_wrong_issuer_fails_closed():
    result = verify_passport_json(
        load_text(), now=VALID_NOW, trusted_issuers=frozenset({OTHER_ISSUER})
    )
    assert check_named(result, ISSUER_CHECK).passed is False
    assert result.decision == DENY


def test_raw_and_direct_results_match_with_same_trust_config():
    direct = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS
    )
    raw = verify_passport_json(
        load_text(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS
    )
    assert raw.checks[0].name == "raw_json_parsed"
    assert raw.checks[1:] == direct.checks
    assert raw.reason == direct.reason
    assert raw.decision == direct.decision


# --- Guard: issuer trust must not introduce network or crypto imports ---

def test_no_forbidden_imports_after_issuer_trust():
    import aaid.passport_verifier as module

    forbidden = (
        "hashlib", "hmac", "base64", "ssl", "secrets", "cryptography",
        "pqcrypto", "oqs", "requests", "httpx", "socket", "urllib",
    )
    for name in forbidden:
        assert not hasattr(module, name)
    source = (SRC / "aaid" / "passport_verifier.py").read_text(encoding="utf-8")
    for name in forbidden:
        assert f"import {name}" not in source
        assert f"from {name}" not in source
