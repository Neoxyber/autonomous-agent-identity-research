"""Expiration and lifecycle verifier-boundary tests.

These tests record current verifier behavior around passport time-window checks,
lifecycle status checks, raw JSON now handling, timezone handling, and
fail-closed short-circuit behavior.

They do not add wall-clock-dependent allow behavior, real signature
verification, or make the passport verifier return `ALLOW`. More tests and
research are still needed around time, lifecycle, and raw-JSON verifier
boundaries.
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pytest

import aaid.passport_verifier as passport_verifier_module
from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PASSPORT_VERIFIER_SOURCE_PATH = ROOT / "src" / "aaid" / "passport_verifier.py"

RAW_JSON_CHECK = "raw_json_parsed"
SCHEMA_CHECK = "schema_valid"
ENVELOPE_MAPPING_CHECK = "envelope_is_mapping"
TIME_CHECK = "passport_time_valid"
LIFECYCLE_CHECK = "lifecycle_status_allows_verification"
PROOF_SELECTED_CHECK = "proof_selected"
PAYLOAD_HASH_CHECK = "payload_hash_valid"

ISSUED_AT = datetime(2026, 5, 29, 0, 0, 0, tzinfo=timezone.utc)
EXPIRES_AT = datetime(2026, 6, 29, 0, 0, 0, tzinfo=timezone.utc)

NON_STRICT_TIMESTAMP_CASES = [
    pytest.param("2026-06-29T00:00:00+05:00", id="explicit-offset"),
    pytest.param("2026-06-29T00:00:00+00:00", id="utc-offset-not-z"),
    pytest.param("2026-06-29 00:00:00Z", id="space-separator"),
    pytest.param("2026-06-29T00:00:00.500Z", id="fractional-seconds"),
    pytest.param("2026-06-29T00:00:00z", id="lowercase-z"),
    pytest.param("2026-06-29T00:00:00Z ", id="trailing-whitespace"),
    pytest.param(" 2026-06-29T00:00:00Z", id="leading-whitespace"),
    pytest.param("2026-06-29", id="date-only"),
    pytest.param("", id="empty-string"),
    pytest.param("2026-13-01T00:00:00Z", id="invalid-month"),
    pytest.param("2026-06-29T24:00:00Z", id="invalid-hour"),
]

NON_ACTIVE_STATUSES = (
    "suspended",
    "revoked",
    "expired",
    "compromised",
    "retired",
)

FORBIDDEN_VERIFIER_IMPORTS = (
    "hashlib",
    "hmac",
    "base64",
    "ssl",
    "secrets",
    "cryptography",
    "pqcrypto",
    "oqs",
    "requests",
    "httpx",
    "socket",
    "urllib",
)


def load_example_text() -> str:
    return EXAMPLE_PATH.read_text(encoding="utf-8")


def load_example_envelope() -> dict[str, Any]:
    return json.loads(load_example_text())


def find_check(
    result: VerificationResult,
    name: str,
) -> VerificationCheck | None:
    for check in result.checks:
        if check.name == name:
            return check
    return None


def check_index(result: VerificationResult, name: str) -> int:
    for index, check in enumerate(result.checks):
        if check.name == name:
            return index
    return -1


def verify_envelope(
    envelope: Any,
    *,
    now: datetime | None = VALID_NOW,
) -> VerificationResult:
    return verify_passport_envelope(envelope, now=now)


def verify_trusted_envelope(
    envelope: Any,
    *,
    now: datetime | None = VALID_NOW,
) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=now,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def test_time_valid_passes_with_injected_now_inside_window() -> None:
    result = verify_envelope(load_example_envelope(), now=VALID_NOW)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is True


def test_now_equal_issued_at_is_inclusive_pass() -> None:
    result = verify_envelope(load_example_envelope(), now=ISSUED_AT)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is True


def test_now_equal_expires_at_is_exclusive_fail() -> None:
    result = verify_envelope(load_example_envelope(), now=EXPIRES_AT)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False

    assert result.decision == DENY
    assert result.valid is False


def test_now_after_expires_at_fails() -> None:
    later = datetime(2026, 7, 1, 0, 0, 0, tzinfo=timezone.utc)

    result = verify_envelope(load_example_envelope(), now=later)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False
    assert "expire" in time_check.reason.lower()
    assert result.decision == DENY


def test_now_before_issued_at_fails() -> None:
    earlier = datetime(2026, 5, 1, 0, 0, 0, tzinfo=timezone.utc)

    result = verify_envelope(load_example_envelope(), now=earlier)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False
    assert "not yet valid" in time_check.reason.lower()
    assert result.decision == DENY


def test_issued_at_after_expires_at_fails() -> None:
    envelope = load_example_envelope()
    envelope["passport"]["issued_at"] = "2026-06-30T00:00:00Z"
    envelope["passport"]["expires_at"] = "2026-06-29T00:00:00Z"

    result = verify_envelope(envelope, now=VALID_NOW)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False
    assert "after expires_at" in time_check.reason.lower()
    assert result.decision == DENY


@pytest.mark.parametrize("bad_timestamp", NON_STRICT_TIMESTAMP_CASES)
def test_non_strict_expires_at_fails_closed(bad_timestamp: str) -> None:
    envelope = load_example_envelope()
    envelope["passport"]["expires_at"] = bad_timestamp

    result = verify_envelope(envelope, now=VALID_NOW)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False
    assert "expires_at" in time_check.reason.lower()

    assert result.decision == DENY
    assert result.valid is False


@pytest.mark.parametrize("bad_timestamp", NON_STRICT_TIMESTAMP_CASES)
def test_non_strict_issued_at_fails_closed(bad_timestamp: str) -> None:
    envelope = load_example_envelope()
    envelope["passport"]["issued_at"] = bad_timestamp

    result = verify_envelope(envelope, now=VALID_NOW)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False
    assert "issued_at" in time_check.reason.lower()
    assert result.decision == DENY


@pytest.mark.parametrize("status", NON_ACTIVE_STATUSES)
def test_each_non_active_lifecycle_status_fails(status: str) -> None:
    envelope = load_example_envelope()
    envelope["passport"]["lifecycle_status"] = status

    result = verify_envelope(envelope, now=VALID_NOW)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is True

    lifecycle = find_check(result, LIFECYCLE_CHECK)
    assert lifecycle is not None
    assert lifecycle.passed is False

    assert result.decision == DENY
    assert result.valid is False


def test_active_lifecycle_passes_lifecycle_check() -> None:
    result = verify_envelope(load_example_envelope(), now=VALID_NOW)

    lifecycle = find_check(result, LIFECYCLE_CHECK)
    assert lifecycle is not None
    assert lifecycle.passed is True


def test_time_and_lifecycle_run_after_schema_valid_and_before_proof_selected() -> None:
    result = verify_trusted_envelope(load_example_envelope(), now=VALID_NOW)

    schema_index = check_index(result, SCHEMA_CHECK)
    time_index = check_index(result, TIME_CHECK)
    lifecycle_index = check_index(result, LIFECYCLE_CHECK)
    proof_index = check_index(result, PROOF_SELECTED_CHECK)

    assert schema_index != -1
    assert time_index != -1
    assert lifecycle_index != -1
    assert proof_index != -1
    assert schema_index < time_index < lifecycle_index < proof_index


def test_time_failure_short_circuits_before_proof_selected() -> None:
    later = datetime(2026, 7, 1, 0, 0, 0, tzinfo=timezone.utc)

    result = verify_envelope(load_example_envelope(), now=later)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False
    assert find_check(result, LIFECYCLE_CHECK) is None
    assert find_check(result, PROOF_SELECTED_CHECK) is None
    assert find_check(result, PAYLOAD_HASH_CHECK) is None


def test_lifecycle_failure_short_circuits_before_proof_selected() -> None:
    envelope = load_example_envelope()
    envelope["passport"]["lifecycle_status"] = "revoked"

    result = verify_envelope(envelope, now=VALID_NOW)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is True

    lifecycle = find_check(result, LIFECYCLE_CHECK)
    assert lifecycle is not None
    assert lifecycle.passed is False
    assert find_check(result, PROOF_SELECTED_CHECK) is None


def test_expiration_lifecycle_never_returns_allow() -> None:
    inverted = load_example_envelope()
    inverted["passport"]["issued_at"] = "2026-06-30T00:00:00Z"
    inverted["passport"]["expires_at"] = "2026-06-29T00:00:00Z"

    bad_timestamp = load_example_envelope()
    bad_timestamp["passport"]["expires_at"] = "2026-06-29T00:00:00+05:00"

    cases = [
        (load_example_envelope(), datetime(2026, 7, 1, tzinfo=timezone.utc)),
        (load_example_envelope(), datetime(2026, 5, 1, tzinfo=timezone.utc)),
        (inverted, VALID_NOW),
        (bad_timestamp, VALID_NOW),
    ]

    for status in NON_ACTIVE_STATUSES:
        envelope = load_example_envelope()
        envelope["passport"]["lifecycle_status"] = status
        cases.append((envelope, VALID_NOW))

    for envelope, now in cases:
        result = verify_envelope(envelope, now=now)

        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.decision == DENY
        assert result.valid is False


def test_now_flows_through_verify_passport_json() -> None:
    later = datetime(2026, 7, 1, 0, 0, 0, tzinfo=timezone.utc)

    result = verify_passport_json(load_example_text(), now=later)

    raw_json_parsed = find_check(result, RAW_JSON_CHECK)
    assert raw_json_parsed is not None
    assert raw_json_parsed.passed is True

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False

    assert result.decision == DENY


def test_verify_passport_json_now_inside_window_reaches_time_pass() -> None:
    result = verify_passport_json(load_example_text(), now=VALID_NOW)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is True

    lifecycle = find_check(result, LIFECYCLE_CHECK)
    assert lifecycle is not None
    assert lifecycle.passed is True


def test_now_none_runs_records_time_check_and_never_allows() -> None:
    result = verify_passport_envelope(load_example_envelope())

    assert isinstance(result, VerificationResult)
    assert find_check(result, TIME_CHECK) is not None
    assert result.decision != ALLOW


def test_naive_now_is_assumed_utc() -> None:
    naive = datetime(2026, 6, 15, 0, 0, 0)
    aware = datetime(2026, 6, 15, 0, 0, 0, tzinfo=timezone.utc)

    naive_result = verify_envelope(load_example_envelope(), now=naive)
    aware_result = verify_envelope(load_example_envelope(), now=aware)

    naive_time = find_check(naive_result, TIME_CHECK)
    aware_time = find_check(aware_result, TIME_CHECK)
    assert naive_time is not None
    assert aware_time is not None
    assert naive_time.passed is True
    assert naive_time.passed == aware_time.passed


def test_tz_aware_non_utc_now_compares_by_instant() -> None:
    plus5 = timezone(timedelta(hours=5))
    now = datetime(2026, 6, 29, 5, 0, 0, tzinfo=plus5)

    result = verify_envelope(load_example_envelope(), now=now)

    time_check = find_check(result, TIME_CHECK)
    assert time_check is not None
    assert time_check.passed is False
    assert result.decision == DENY


def test_no_forbidden_imports_after_change() -> None:
    for name in FORBIDDEN_VERIFIER_IMPORTS:
        assert not hasattr(passport_verifier_module, name)

    source = PASSPORT_VERIFIER_SOURCE_PATH.read_text(encoding="utf-8")
    for name in FORBIDDEN_VERIFIER_IMPORTS:
        assert f"import {name}" not in source
        assert f"from {name}" not in source

    assert "fromisoformat(" not in source
