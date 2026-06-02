import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(TESTS))

import pytest

import aaid.passport_verifier as passport_verifier_module
from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.verification import VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PV_SOURCE_PATH = SRC / "aaid" / "passport_verifier.py"

CHECKED = "revocation_status_checked"
FRESH = "revocation_status_fresh"
NOT_REVOKED = "passport_not_revoked"
ISSUER_CHECK = "issuer_trusted"
PROOF_CHECK = "proof_selected"
SIGNATURE_CHECK = "signature_verification_not_implemented"

EXAMPLE_ISSUER = "urn:aaid:issuer:aixybertech-issuer"
OTHER_ISSUER = "urn:aaid:issuer:some-other-issuer"
EXAMPLE_PASSPORT_ID = "urn:aaid:passport:018fd7c2-6f1e-7a4e-9b18-3d7a9d93c111"
EXAMPLE_STATUS_REFERENCE = "urn:aaid:revocation:018fd7c2-9d55-7a11-8a22-24b1e3f92310"


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


def status(**overrides):
    # A fresh, mutable copy of the good status so a test never mutates the
    # shared FRESH_STATUS constant. All values are flat strings.
    fresh = dict(FRESH_STATUS)
    fresh.update(overrides)
    return fresh


def status_without(key):
    fresh = dict(FRESH_STATUS)
    fresh.pop(key, None)
    return fresh


# Same strict-timestamp rejection set the passport-time check is exercised with.
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


# --- revocation_status_checked: identity binding ---

def test_minimal_example_with_fresh_status_reaches_checked_passed():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    checked = check_named(result, CHECKED)
    assert checked is not None
    assert checked.passed is True


def test_missing_status_fails_closed_before_proof_selected():
    # revocation_status defaults to None: the boundary fails closed before any
    # later check runs, so proof selection and the signature step never run.
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS
    )
    checked = check_named(result, CHECKED)
    assert checked is not None
    assert checked.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert check_named(result, SIGNATURE_CHECK) is None
    assert result.decision == DENY
    assert result.valid is False


@pytest.mark.parametrize(
    "bad", ["urn:aaid:revocation:not-a-mapping", b"bytes", 42, 0, 1.5, ["x"], True]
)
def test_non_mapping_status_fails_closed(bad):
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=bad,
    )
    checked = check_named(result, CHECKED)
    assert checked is not None
    assert checked.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


@pytest.mark.parametrize(
    "missing", ["status_reference", "passport_id", "status_authority"]
)
def test_missing_required_field_fails_closed(missing):
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status_without(missing),
    )
    checked = check_named(result, CHECKED)
    assert checked.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


@pytest.mark.parametrize(
    "field", ["status_reference", "passport_id", "status_authority"]
)
@pytest.mark.parametrize("value", [None, 123, ["x"], {"a": 1}, True])
def test_non_string_field_fails_closed(field, value):
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(**{field: value}),
    )
    checked = check_named(result, CHECKED)
    assert checked.passed is False
    assert result.decision == DENY


def test_status_reference_mismatch_fails_closed():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(status_reference="urn:aaid:revocation:other"),
    )
    checked = check_named(result, CHECKED)
    assert checked.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


def test_passport_id_mismatch_fails_closed():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(passport_id="urn:aaid:passport:other"),
    )
    checked = check_named(result, CHECKED)
    assert checked.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


def test_status_authority_mismatch_fails_closed():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(status_authority=OTHER_ISSUER),
    )
    checked = check_named(result, CHECKED)
    assert checked.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


def test_different_trusted_issuer_cannot_provide_status_for_this_passport():
    # The status authority is a different issuer that is itself trusted, but it
    # is not this passport's issuer. The status must still fail closed: trust in
    # an issuer does not let it vouch for another issuer's passport.
    trusted = frozenset({EXAMPLE_ISSUER, OTHER_ISSUER})
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=trusted,
        revocation_status=status(status_authority=OTHER_ISSUER),
    )
    checked = check_named(result, CHECKED)
    assert checked.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


def test_matching_status_reference_alone_is_not_enough():
    # The status_reference matches, but passport_id and status_authority do not.
    # Binding requires all three, so this fails closed.
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(
            passport_id="urn:aaid:passport:wrong",
            status_authority=OTHER_ISSUER,
        ),
    )
    checked = check_named(result, CHECKED)
    assert checked.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


# --- revocation_status_checked: direct helper coverage of the trust membership
# branch, which the full flow cannot reach because issuer_trusted already
# requires the issuer to be configured as trusted. ---

def _minimal_passport():
    return {
        "passport_id": EXAMPLE_PASSPORT_ID,
        "issuer_id": EXAMPLE_ISSUER,
        "revocation": {
            "method": "signed_status_reference",
            "status_reference": EXAMPLE_STATUS_REFERENCE,
        },
    }


def test_checked_helper_passes_when_bound_and_authority_trusted():
    check = passport_verifier_module._revocation_status_checked_check(
        _minimal_passport(), dict(FRESH_STATUS), frozenset({EXAMPLE_ISSUER})
    )
    assert check.name == CHECKED
    assert check.passed is True


def test_checked_helper_fails_when_authority_not_in_trusted_issuers():
    check = passport_verifier_module._revocation_status_checked_check(
        _minimal_passport(), dict(FRESH_STATUS), frozenset()
    )
    assert check.name == CHECKED
    assert check.passed is False


@pytest.mark.parametrize(
    "trusted",
    [None, EXAMPLE_ISSUER, {EXAMPLE_ISSUER: {"note": "demo"}}, 123, 1.5],
)
def test_checked_helper_fails_closed_for_misconfigured_trust(trusted):
    # A None, bare-string, mapping, or non-iterable trust configuration must fail
    # closed in the revocation boundary, never raise.
    check = passport_verifier_module._revocation_status_checked_check(
        _minimal_passport(), dict(FRESH_STATUS), trusted
    )
    assert check.name == CHECKED
    assert check.passed is False


def test_checked_helper_fails_closed_when_passport_revocation_malformed():
    # Defensive: even if the passport revocation block is not a mapping (schema
    # would reject this earlier), the helper must fail closed, not raise.
    passport = _minimal_passport()
    passport["revocation"] = "not-a-mapping"
    check = passport_verifier_module._revocation_status_checked_check(
        passport, dict(FRESH_STATUS), frozenset({EXAMPLE_ISSUER})
    )
    assert check.passed is False


# --- revocation_status_fresh: strict UTC freshness window ---

def test_fresh_status_reaches_revocation_status_fresh_passed():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    fresh = check_named(result, FRESH)
    assert fresh is not None
    assert fresh.passed is True


def test_stale_status_fails_closed():
    # valid_until is at or before now: the status window has closed.
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(
            produced_at="2026-06-10T00:00:00Z",
            valid_until="2026-06-14T00:00:00Z",
        ),
    )
    fresh = check_named(result, FRESH)
    assert fresh is not None
    assert fresh.passed is False
    assert check_named(result, NOT_REVOKED) is None
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


def test_future_dated_status_fails_closed():
    # produced_at is after now: the status was produced in the future.
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(
            produced_at="2026-06-16T00:00:00Z",
            valid_until="2026-06-17T00:00:00Z",
        ),
    )
    fresh = check_named(result, FRESH)
    assert fresh.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


def test_inverted_window_fails_closed():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(
            produced_at="2026-06-16T00:00:00Z",
            valid_until="2026-06-14T00:00:00Z",
        ),
    )
    fresh = check_named(result, FRESH)
    assert fresh.passed is False
    assert result.decision == DENY


def test_zero_width_window_fails_closed():
    # produced_at == valid_until == now: no instant can satisfy
    # produced_at <= now < valid_until, so freshness fails closed.
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(
            produced_at="2026-06-15T00:00:00Z",
            valid_until="2026-06-15T00:00:00Z",
        ),
    )
    fresh = check_named(result, FRESH)
    assert fresh.passed is False
    assert result.decision == DENY


@pytest.mark.parametrize("bad", NON_STRICT_TIMESTAMPS + [None, 123, ["x"]])
def test_malformed_produced_at_fails_closed(bad):
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(produced_at=bad),
    )
    fresh = check_named(result, FRESH)
    assert fresh is not None
    assert fresh.passed is False
    assert result.decision == DENY


@pytest.mark.parametrize("bad", NON_STRICT_TIMESTAMPS + [None, 123, ["x"]])
def test_malformed_valid_until_fails_closed(bad):
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(valid_until=bad),
    )
    fresh = check_named(result, FRESH)
    assert fresh is not None
    assert fresh.passed is False
    assert result.decision == DENY


@pytest.mark.parametrize("missing", ["produced_at", "valid_until"])
def test_missing_freshness_field_fails_closed_without_raising(missing):
    # Identity binding still passes (the three identity fields are intact), so
    # this proves the freshness check tolerates a missing window field and fails
    # closed rather than raising KeyError.
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status_without(missing),
    )
    assert check_named(result, CHECKED).passed is True
    fresh = check_named(result, FRESH)
    assert fresh is not None
    assert fresh.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


def test_freshness_uses_injected_now_not_wall_clock():
    # With now inside the window the status is fresh; with now outside it is not.
    # The check must therefore depend on the injected now, not the real clock.
    inside = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    from datetime import datetime, timezone

    outside = verify_passport_envelope(
        load_envelope(),
        now=datetime(2026, 6, 20, 0, 0, 0, tzinfo=timezone.utc),
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    assert check_named(inside, FRESH).passed is True
    # now=2026-06-20 is still inside the passport validity window but past the
    # status window (valid_until 2026-06-16), so the freshness check is reached
    # and fails closed as stale. This depends only on the injected now.
    outside_fresh = check_named(outside, FRESH)
    assert outside_fresh is not None
    assert outside_fresh.passed is False
    assert outside.decision == DENY


# --- passport_not_revoked: only active continues ---

def test_active_status_reaches_proof_selected():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    not_revoked = check_named(result, NOT_REVOKED)
    assert not_revoked is not None
    assert not_revoked.passed is True
    assert check_named(result, PROOF_CHECK).passed is True


@pytest.mark.parametrize(
    "bad_status",
    [
        "revoked",
        "suspended",
        "expired",
        "compromised",
        "retired",
        "unknown",
        "ACTIVE",
        "Active",
        "active ",
        " active",
        "",
    ],
)
def test_each_non_active_string_status_fails_closed(bad_status):
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(status=bad_status),
    )
    not_revoked = check_named(result, NOT_REVOKED)
    assert not_revoked is not None
    assert not_revoked.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY
    assert result.valid is False


def test_missing_status_value_fails_closed():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status_without("status"),
    )
    not_revoked = check_named(result, NOT_REVOKED)
    assert not_revoked is not None
    assert not_revoked.passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


@pytest.mark.parametrize("bad_status", [None, 123, ["active"], {"status": "active"}, True])
def test_non_string_status_value_fails_closed(bad_status):
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(status=bad_status),
    )
    not_revoked = check_named(result, NOT_REVOKED)
    assert not_revoked is not None
    assert not_revoked.passed is False
    assert result.decision == DENY


# --- ordering and short-circuit ---

def test_revocation_checks_run_between_issuer_trusted_and_proof_selected():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    issuer_index = check_index(result, ISSUER_CHECK)
    checked_index = check_index(result, CHECKED)
    fresh_index = check_index(result, FRESH)
    not_revoked_index = check_index(result, NOT_REVOKED)
    proof_index = check_index(result, PROOF_CHECK)
    assert -1 not in (
        issuer_index,
        checked_index,
        fresh_index,
        not_revoked_index,
        proof_index,
    )
    assert (
        issuer_index
        < checked_index
        < fresh_index
        < not_revoked_index
        < proof_index
    )


def test_checked_failure_short_circuits_before_fresh_and_not_revoked():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(passport_id="urn:aaid:passport:other"),
    )
    assert check_named(result, CHECKED).passed is False
    assert check_named(result, FRESH) is None
    assert check_named(result, NOT_REVOKED) is None
    assert check_named(result, PROOF_CHECK) is None


def test_fresh_failure_short_circuits_before_not_revoked():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=status(
            produced_at="2026-06-10T00:00:00Z",
            valid_until="2026-06-14T00:00:00Z",
        ),
    )
    assert check_named(result, FRESH).passed is False
    assert check_named(result, NOT_REVOKED) is None
    assert check_named(result, PROOF_CHECK) is None


def test_issuer_trust_failure_short_circuits_before_revocation_checks():
    # No trust configured: the chain stops at issuer_trusted, before revocation.
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, revocation_status=FRESH_STATUS
    )
    assert check_named(result, ISSUER_CHECK).passed is False
    assert check_named(result, CHECKED) is None
    assert check_named(result, FRESH) is None
    assert check_named(result, NOT_REVOKED) is None
    assert result.decision == DENY


# --- valid fresh active status still denies (never ALLOW) ---

def test_valid_fresh_active_reaches_proof_selected_but_final_decision_is_deny():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    assert check_named(result, CHECKED).passed is True
    assert check_named(result, FRESH).passed is True
    assert check_named(result, NOT_REVOKED).passed is True
    assert check_named(result, PROOF_CHECK).passed is True
    signature = check_named(result, SIGNATURE_CHECK)
    assert signature is not None
    assert signature.passed is False
    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False


def test_revocation_freshness_step_never_returns_allow():
    cases = [
        FRESH_STATUS,
        None,
        "not-a-mapping",
        status(status_reference="urn:aaid:revocation:other"),
        status(passport_id="urn:aaid:passport:other"),
        status(status_authority=OTHER_ISSUER),
        status(produced_at="2026-06-10T00:00:00Z", valid_until="2026-06-14T00:00:00Z"),
        status(produced_at="2026-06-16T00:00:00Z", valid_until="2026-06-17T00:00:00Z"),
        status(produced_at="2026-06-16T00:00:00Z", valid_until="2026-06-14T00:00:00Z"),
        status(status="revoked"),
        status(status="suspended"),
        status_without("status"),
    ]
    # Reach the named steps for the good status so this sweep actually exercises
    # the revocation checks rather than stopping earlier.
    reached = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    assert check_named(reached, CHECKED) is not None
    assert check_named(reached, FRESH) is not None
    assert check_named(reached, NOT_REVOKED) is not None
    assert check_named(reached, PROOF_CHECK) is not None

    for case in cases:
        result = verify_passport_envelope(
            load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
            revocation_status=case,
        )
        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW, f"unexpected ALLOW for {case!r}"
        assert result.decision == DENY
        assert result.valid is False


# --- raw JSON entry point forwards revocation_status ---

def test_verify_passport_json_forwards_revocation_status_parity():
    direct = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    raw = verify_passport_json(
        load_text(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    assert raw.checks[0].name == "raw_json_parsed"
    assert raw.checks[1:] == direct.checks
    assert raw.reason == direct.reason
    assert raw.decision == direct.decision


def test_verify_passport_json_without_revocation_status_fails_checked():
    result = verify_passport_json(
        load_text(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS
    )
    assert check_named(result, "raw_json_parsed").passed is True
    assert check_named(result, CHECKED).passed is False
    assert check_named(result, PROOF_CHECK) is None
    assert result.decision == DENY


def test_verify_passport_json_revoked_status_fails_closed_like_parsed():
    revoked = status(status="revoked")
    direct = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=revoked,
    )
    raw = verify_passport_json(
        load_text(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=revoked,
    )
    assert check_named(raw, NOT_REVOKED).passed is False
    assert raw.checks[1:] == direct.checks
    assert raw.decision == DENY


# --- guard: the revocation path must not introduce network or client imports ---

def test_revocation_path_introduces_no_network_or_client_imports():
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
