import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(TESTS))

import pytest

from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.verification import VerificationResult

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"

TIME_CHECK = "passport_time_valid"
LIFECYCLE_CHECK = "lifecycle_status_allows_verification"

ISSUED_AT = datetime(2026, 5, 29, 0, 0, 0, tzinfo=timezone.utc)
EXPIRES_AT = datetime(2026, 6, 29, 0, 0, 0, tzinfo=timezone.utc)


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


# --- Time window: passing boundaries ---

def test_time_valid_passes_with_injected_now_inside_window():
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW)
    time_check = check_named(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is True


def test_now_equal_issued_at_is_inclusive_pass():
    # issued_at is inclusive: now == issued_at must pass.
    result = verify_passport_envelope(load_envelope(), now=ISSUED_AT)
    assert check_named(result, TIME_CHECK).passed is True


def test_now_equal_expires_at_is_exclusive_fail():
    # expires_at is exclusive: now == expires_at must fail closed.
    result = verify_passport_envelope(load_envelope(), now=EXPIRES_AT)
    time_check = check_named(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False
    assert result.decision == DENY
    assert result.valid is False


def test_now_after_expires_at_fails():
    later = datetime(2026, 7, 1, 0, 0, 0, tzinfo=timezone.utc)
    result = verify_passport_envelope(load_envelope(), now=later)
    time_check = check_named(result, TIME_CHECK)
    assert time_check.passed is False
    assert "expire" in time_check.reason.lower()
    assert result.decision == DENY


def test_now_before_issued_at_fails():
    earlier = datetime(2026, 5, 1, 0, 0, 0, tzinfo=timezone.utc)
    result = verify_passport_envelope(load_envelope(), now=earlier)
    time_check = check_named(result, TIME_CHECK)
    assert time_check.passed is False
    assert "not yet valid" in time_check.reason.lower()
    assert result.decision == DENY


def test_issued_at_after_expires_at_fails():
    envelope = load_envelope()
    envelope["passport"]["issued_at"] = "2026-06-30T00:00:00Z"
    envelope["passport"]["expires_at"] = "2026-06-29T00:00:00Z"
    result = verify_passport_envelope(envelope, now=VALID_NOW)
    time_check = check_named(result, TIME_CHECK)
    assert time_check.passed is False
    assert "after expires_at" in time_check.reason.lower()
    assert result.decision == DENY


# --- Time window: strict, non-Z, unparseable timestamps fail closed ---

NON_STRICT_TIMESTAMPS = [
    "2026-06-29T00:00:00+05:00",  # explicit offset, not Z
    "2026-06-29T00:00:00+00:00",  # +00:00 is not the Z form
    "2026-06-29 00:00:00Z",       # space separator
    "2026-06-29T00:00:00.500Z",   # fractional seconds
    "2026-06-29T00:00:00z",       # lowercase z
    "2026-06-29T00:00:00Z ",      # trailing whitespace
    " 2026-06-29T00:00:00Z",      # leading whitespace
    "2026-06-29",                 # date only
    "",                           # empty string
    "2026-13-01T00:00:00Z",       # calendar-invalid month (matches shape)
    "2026-06-29T24:00:00Z",       # calendar-invalid hour (matches shape)
]


@pytest.mark.parametrize("bad", NON_STRICT_TIMESTAMPS)
def test_non_strict_expires_at_fails_closed(bad):
    envelope = load_envelope()
    envelope["passport"]["expires_at"] = bad
    result = verify_passport_envelope(envelope, now=VALID_NOW)
    time_check = check_named(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False
    assert "expires_at" in time_check.reason.lower()
    assert result.decision == DENY
    assert result.valid is False


@pytest.mark.parametrize("bad", NON_STRICT_TIMESTAMPS)
def test_non_strict_issued_at_fails_closed(bad):
    envelope = load_envelope()
    envelope["passport"]["issued_at"] = bad
    result = verify_passport_envelope(envelope, now=VALID_NOW)
    time_check = check_named(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False
    assert "issued_at" in time_check.reason.lower()
    assert result.decision == DENY


# --- Lifecycle status ---

NON_ACTIVE_STATUSES = ["suspended", "revoked", "expired", "compromised", "retired"]


@pytest.mark.parametrize("status", NON_ACTIVE_STATUSES)
def test_each_non_active_lifecycle_status_fails(status):
    envelope = load_envelope()
    envelope["passport"]["lifecycle_status"] = status
    result = verify_passport_envelope(envelope, now=VALID_NOW)
    # Time still passes; lifecycle is the failing gate.
    assert check_named(result, TIME_CHECK).passed is True
    lifecycle = check_named(result, LIFECYCLE_CHECK)
    assert lifecycle is not None
    assert lifecycle.passed is False
    assert result.decision == DENY
    assert result.valid is False


def test_active_lifecycle_passes_lifecycle_check():
    result = verify_passport_envelope(load_envelope(), now=VALID_NOW)
    lifecycle = check_named(result, LIFECYCLE_CHECK)
    assert lifecycle is not None
    assert lifecycle.passed is True


# --- Ordering and short-circuit ---

def test_time_and_lifecycle_run_after_schema_valid_and_before_proof_selected():
    result = verify_passport_envelope(
        load_envelope(), now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS
    )
    schema_index = check_index(result, "schema_valid")
    time_index = check_index(result, TIME_CHECK)
    lifecycle_index = check_index(result, LIFECYCLE_CHECK)
    proof_index = check_index(result, "proof_selected")
    assert schema_index != -1
    assert time_index != -1
    assert lifecycle_index != -1
    assert proof_index != -1
    assert schema_index < time_index < lifecycle_index < proof_index


def test_time_failure_short_circuits_before_proof_selected():
    later = datetime(2026, 7, 1, 0, 0, 0, tzinfo=timezone.utc)
    result = verify_passport_envelope(load_envelope(), now=later)
    assert check_named(result, TIME_CHECK).passed is False
    assert check_named(result, LIFECYCLE_CHECK) is None
    assert check_named(result, "proof_selected") is None
    assert check_named(result, "payload_hash_valid") is None


def test_lifecycle_failure_short_circuits_before_proof_selected():
    envelope = load_envelope()
    envelope["passport"]["lifecycle_status"] = "revoked"
    result = verify_passport_envelope(envelope, now=VALID_NOW)
    assert check_named(result, TIME_CHECK).passed is True
    assert check_named(result, LIFECYCLE_CHECK).passed is False
    assert check_named(result, "proof_selected") is None


# --- Never ALLOW ---

def test_expiration_lifecycle_never_returns_allow():
    inverted = load_envelope()
    inverted["passport"]["issued_at"] = "2026-06-30T00:00:00Z"
    inverted["passport"]["expires_at"] = "2026-06-29T00:00:00Z"
    bad_ts = load_envelope()
    bad_ts["passport"]["expires_at"] = "2026-06-29T00:00:00+05:00"

    cases = [
        (load_envelope(), datetime(2026, 7, 1, tzinfo=timezone.utc)),  # expired
        (load_envelope(), datetime(2026, 5, 1, tzinfo=timezone.utc)),  # not yet valid
        (inverted, VALID_NOW),                                          # inverted window
        (bad_ts, VALID_NOW),                                            # non-strict ts
    ]
    for status in NON_ACTIVE_STATUSES:
        env = load_envelope()
        env["passport"]["lifecycle_status"] = status
        cases.append((env, VALID_NOW))

    for envelope, now in cases:
        result = verify_passport_envelope(envelope, now=now)
        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.decision == DENY
        assert result.valid is False


# --- now flows through the raw-JSON entry point ---

def test_now_flows_through_verify_passport_json():
    later = datetime(2026, 7, 1, 0, 0, 0, tzinfo=timezone.utc)
    result = verify_passport_json(load_text(), now=later)
    assert check_named(result, "raw_json_parsed").passed is True
    assert check_named(result, TIME_CHECK).passed is False
    assert result.decision == DENY


def test_verify_passport_json_now_inside_window_reaches_time_pass():
    result = verify_passport_json(load_text(), now=VALID_NOW)
    assert check_named(result, TIME_CHECK).passed is True
    assert check_named(result, LIFECYCLE_CHECK).passed is True


# --- now=None default path (must not assert wall-clock-dependent outcome) ---

def test_now_none_runs_records_time_check_and_never_allows():
    result = verify_passport_envelope(load_envelope())
    assert isinstance(result, VerificationResult)
    assert check_named(result, TIME_CHECK) is not None
    assert result.decision != ALLOW


# --- now contract: naive and non-UTC aware ---

def test_naive_now_is_assumed_utc():
    naive = datetime(2026, 6, 15, 0, 0, 0)  # no tzinfo
    aware = datetime(2026, 6, 15, 0, 0, 0, tzinfo=timezone.utc)
    naive_result = verify_passport_envelope(load_envelope(), now=naive)
    aware_result = verify_passport_envelope(load_envelope(), now=aware)
    assert check_named(naive_result, TIME_CHECK).passed is True
    assert check_named(naive_result, TIME_CHECK).passed == check_named(
        aware_result, TIME_CHECK
    ).passed


def test_tz_aware_non_utc_now_compares_by_instant():
    # 2026-06-29T05:00:00+05:00 == 2026-06-29T00:00:00Z == expires_at (exclusive),
    # so it must fail closed even though the local wall time looks later.
    plus5 = timezone(timedelta(hours=5))
    now = datetime(2026, 6, 29, 5, 0, 0, tzinfo=plus5)
    result = verify_passport_envelope(load_envelope(), now=now)
    assert check_named(result, TIME_CHECK).passed is False
    assert result.decision == DENY


# --- guard: no forbidden imports introduced ---

def test_no_forbidden_imports_after_change():
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
    # The strict parser must not call the lenient fromisoformat (the docstring
    # may still mention it to explain why it is avoided).
    assert "fromisoformat(" not in source
