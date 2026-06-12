"""Issuer-trust verifier-boundary tests.

These tests record current verifier behavior around trusted issuer
configuration, fail-closed trust misconfiguration, raw JSON trust forwarding,
ordering, short-circuit behavior, and the never-ALLOW boundary.

They do not add network issuer lookup, registry lookup, real signature
verification, or make the passport verifier return `ALLOW`. More tests and
research are still needed around issuer-trust and verifier-boundary behavior.
"""

import json
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
TIME_CHECK = "passport_time_valid"
LIFECYCLE_CHECK = "lifecycle_status_allows_verification"
ISSUER_CHECK = "issuer_trusted"
PROOF_SELECTED_CHECK = "proof_selected"
PAYLOAD_HASH_CHECK = "payload_hash_valid"
KEY_SELECTED_CHECK = "verification_key_selected"
SIGNATURE_CHECK = "signature_verification_not_implemented"

EXAMPLE_ISSUER = "urn:aaid:issuer:aixybertech-issuer"
OTHER_ISSUER = "urn:aaid:issuer:some-other-issuer"

TRUSTED_ISSUER_COLLECTIONS = (
    pytest.param(frozenset({EXAMPLE_ISSUER}), id="frozenset"),
    pytest.param({EXAMPLE_ISSUER}, id="set"),
    pytest.param([EXAMPLE_ISSUER], id="list"),
    pytest.param((EXAMPLE_ISSUER,), id="tuple"),
)

NON_ITERABLE_TRUST_CONFIGS = (
    pytest.param(123, id="int"),
    pytest.param(1.5, id="float"),
    pytest.param(True, id="bool"),
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
    trusted_issuers: Any = None,
    revocation_status: Any = None,
) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=trusted_issuers,
        revocation_status=revocation_status,
    )


def verify_trusted_envelope(envelope: Any) -> VerificationResult:
    return verify_envelope(
        envelope,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def verify_raw_json(
    *,
    trusted_issuers: Any = None,
    revocation_status: Any = None,
) -> VerificationResult:
    return verify_passport_json(
        load_example_text(),
        now=VALID_NOW,
        trusted_issuers=trusted_issuers,
        revocation_status=revocation_status,
    )


def test_trusted_issuer_passes_and_reaches_proof_selected() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    issuer = find_check(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is True
    assert "configured as trusted" in issuer.reason.lower()

    proof_selected = find_check(result, PROOF_SELECTED_CHECK)
    assert proof_selected is not None
    assert proof_selected.passed is True


def test_trusted_issuer_valid_now_still_denies_and_never_allows() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False

    signature = find_check(result, SIGNATURE_CHECK)
    assert signature is not None
    assert signature.passed is False


@pytest.mark.parametrize("trusted_issuers", TRUSTED_ISSUER_COLLECTIONS)
def test_any_collection_form_carrying_the_issuer_passes(
    trusted_issuers: Any,
) -> None:
    result = verify_envelope(
        load_example_envelope(),
        trusted_issuers=trusted_issuers,
    )

    issuer = find_check(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is True


def test_default_none_trust_fails_closed_and_short_circuits() -> None:
    result = verify_envelope(load_example_envelope())

    issuer = find_check(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is False
    assert "no trusted issuers were provided" in issuer.reason.lower()

    assert result.decision == DENY
    assert result.valid is False

    time_check = find_check(result, TIME_CHECK)
    lifecycle = find_check(result, LIFECYCLE_CHECK)
    assert time_check is not None
    assert lifecycle is not None
    assert time_check.passed is True
    assert lifecycle.passed is True

    assert find_check(result, PROOF_SELECTED_CHECK) is None
    assert find_check(result, PAYLOAD_HASH_CHECK) is None
    assert find_check(result, KEY_SELECTED_CHECK) is None
    assert find_check(result, SIGNATURE_CHECK) is None


def test_empty_collection_fails_closed_not_trusted() -> None:
    result = verify_envelope(
        load_example_envelope(),
        trusted_issuers=frozenset(),
    )

    issuer = find_check(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is False
    assert "not configured as trusted" in issuer.reason.lower()

    assert result.decision == DENY
    assert find_check(result, PROOF_SELECTED_CHECK) is None


def test_unknown_issuer_fails_closed_not_trusted() -> None:
    result = verify_envelope(
        load_example_envelope(),
        trusted_issuers=frozenset({OTHER_ISSUER}),
    )

    issuer = find_check(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is False
    assert "not configured as trusted" in issuer.reason.lower()

    assert result.decision == DENY
    assert find_check(result, PROOF_SELECTED_CHECK) is None


def test_string_trust_config_fails_closed_even_if_it_contains_the_issuer() -> None:
    result = verify_envelope(
        load_example_envelope(),
        trusted_issuers=EXAMPLE_ISSUER,
    )

    issuer = find_check(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is False
    assert "not a string" in issuer.reason.lower()

    assert result.decision == DENY
    assert find_check(result, PROOF_SELECTED_CHECK) is None


def test_mapping_trust_config_fails_closed() -> None:
    result = verify_envelope(
        load_example_envelope(),
        trusted_issuers={EXAMPLE_ISSUER: {"note": "demo"}},
    )

    issuer = find_check(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is False
    assert "not a mapping" in issuer.reason.lower()

    assert result.decision == DENY
    assert find_check(result, PROOF_SELECTED_CHECK) is None


@pytest.mark.parametrize("bad_config", NON_ITERABLE_TRUST_CONFIGS)
def test_non_iterable_trust_config_fails_closed_without_raising(
    bad_config: Any,
) -> None:
    result = verify_envelope(
        load_example_envelope(),
        trusted_issuers=bad_config,
    )

    issuer = find_check(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is False
    assert "collection of issuer identifiers" in issuer.reason.lower()

    assert result.decision == DENY
    assert result.valid is False
    assert find_check(result, PROOF_SELECTED_CHECK) is None


def test_issuer_trusted_runs_after_lifecycle_and_before_proof_selected() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    schema_index = check_index(result, SCHEMA_CHECK)
    time_index = check_index(result, TIME_CHECK)
    lifecycle_index = check_index(result, LIFECYCLE_CHECK)
    issuer_index = check_index(result, ISSUER_CHECK)
    proof_index = check_index(result, PROOF_SELECTED_CHECK)

    assert -1 not in (
        schema_index,
        time_index,
        lifecycle_index,
        issuer_index,
        proof_index,
    )
    assert schema_index < time_index < lifecycle_index < issuer_index < proof_index


def test_lifecycle_failure_short_circuits_before_issuer_trusted() -> None:
    envelope = load_example_envelope()
    envelope["passport"]["lifecycle_status"] = "revoked"

    result = verify_trusted_envelope(envelope)

    lifecycle = find_check(result, LIFECYCLE_CHECK)
    assert lifecycle is not None
    assert lifecycle.passed is False
    assert find_check(result, ISSUER_CHECK) is None
    assert result.decision == DENY


def test_issuer_trust_step_never_returns_allow() -> None:
    cases = [
        TRUSTED_ISSUERS,
        None,
        frozenset(),
        frozenset({OTHER_ISSUER}),
        EXAMPLE_ISSUER,
        {EXAMPLE_ISSUER: {"note": "demo"}},
        123,
        1.5,
        True,
    ]

    for trusted_issuers in cases:
        result = verify_envelope(
            load_example_envelope(),
            trusted_issuers=trusted_issuers,
        )

        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW, f"unexpected ALLOW for {trusted_issuers!r}"
        assert result.decision == DENY
        assert result.valid is False


def test_verify_passport_json_forwards_trusted_issuers_pass() -> None:
    result = verify_raw_json(
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )

    raw_json = find_check(result, RAW_JSON_CHECK)
    issuer = find_check(result, ISSUER_CHECK)
    proof_selected = find_check(result, PROOF_SELECTED_CHECK)

    assert raw_json is not None
    assert issuer is not None
    assert proof_selected is not None
    assert raw_json.passed is True
    assert issuer.passed is True
    assert proof_selected.passed is True
    assert result.decision == DENY


def test_verify_passport_json_without_trust_fails_issuer_trusted() -> None:
    result = verify_raw_json()

    raw_json = find_check(result, RAW_JSON_CHECK)
    issuer = find_check(result, ISSUER_CHECK)

    assert raw_json is not None
    assert issuer is not None
    assert raw_json.passed is True
    assert issuer.passed is False
    assert "no trusted issuers were provided" in issuer.reason.lower()

    assert find_check(result, PROOF_SELECTED_CHECK) is None
    assert result.decision == DENY


def test_verify_passport_json_wrong_issuer_fails_closed() -> None:
    result = verify_raw_json(trusted_issuers=frozenset({OTHER_ISSUER}))

    issuer = find_check(result, ISSUER_CHECK)
    assert issuer is not None
    assert issuer.passed is False
    assert result.decision == DENY


def test_raw_and_direct_results_match_with_same_trust_config() -> None:
    direct = verify_trusted_envelope(load_example_envelope())
    raw = verify_raw_json(
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )

    assert raw.checks[0].name == RAW_JSON_CHECK
    assert raw.checks[1:] == direct.checks
    assert raw.reason == direct.reason
    assert raw.decision == direct.decision


def test_no_forbidden_imports_after_issuer_trust() -> None:
    for name in FORBIDDEN_VERIFIER_IMPORTS:
        assert not hasattr(passport_verifier_module, name)

    source = PASSPORT_VERIFIER_SOURCE_PATH.read_text(encoding="utf-8")
    for name in FORBIDDEN_VERIFIER_IMPORTS:
        assert f"import {name}" not in source
        assert f"from {name}" not in source
