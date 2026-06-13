"""Tests for proof-count hardening before proof selection.

These cases keep multi-proof envelopes fail-closed before proof selection,
payload-hash validation, key selection, and signature-stage checks.

A passing proof-count check does not grant `ALLOW`. More research and testing
are needed to improve future multi-proof policy over time.
"""

import copy
import json
from pathlib import Path
from typing import Any

from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope, verify_passport_json
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PASSPORT_VERIFIER_SOURCE_PATH = ROOT / "src" / "aaid" / "passport_verifier.py"

RAW_JSON_CHECK = "raw_json_parsed"
PROOFS_PRESENT_CHECK = "proofs_present"
PROOFS_SEQUENCE_CHECK = "proofs_is_sequence"
PROOFS_NON_EMPTY_CHECK = "proofs_non_empty"
PROOF_COUNT_CHECK = "proof_count_allowed"
PROOF_SELECTED_CHECK = "proof_selected"
PAYLOAD_CHECK = "payload_hash_valid"
KEY_CHECK = "verification_key_selected"
KEY_VALIDITY_CHECK = "verification_key_valid_for_proof"
CANONICALIZATION_CHECK = "signature_canonicalization_supported"
INPUT_CHECK = "signature_input_prepared"
ALGORITHM_CHECK = "signature_algorithm_supported"
SIGNATURE_CHECK = "signature_verification_not_implemented"

SIGNATURE_STAGE_CHECKS = (
    PROOF_SELECTED_CHECK,
    PAYLOAD_CHECK,
    KEY_CHECK,
    KEY_VALIDITY_CHECK,
    CANONICALIZATION_CHECK,
    INPUT_CHECK,
    ALGORITHM_CHECK,
    SIGNATURE_CHECK,
)

FORBIDDEN_VERIFIER_IMPORTS = (
    "requests",
    "httpx",
    "urllib",
    "socket",
    "http.client",
    "hashlib",
    "hmac",
    "base64",
    "ssl",
    "secrets",
    "cryptography",
    "pqcrypto",
    "oqs",
)


def load_example_envelope() -> dict[str, Any]:
    return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))


def load_example_text() -> str:
    return EXAMPLE_PATH.read_text(encoding="utf-8")


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


def envelope_with_n_proofs(proof_count: int) -> dict[str, Any]:
    envelope = load_example_envelope()
    first = envelope["proofs"][0]
    extras = []

    for index in range(1, proof_count):
        extra = copy.deepcopy(first)
        extra["proof_id"] = f"urn:aaid:proof:extra-proof-{index}"
        extras.append(extra)

    envelope["proofs"] = [first, *extras]
    return envelope


def verify_trusted_envelope(envelope: Any) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def verify_trusted_json(raw_json: str) -> VerificationResult:
    return verify_passport_json(
        raw_json,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def test_single_proof_example_passes_count_check_and_still_denies() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    count = find_check(result, PROOF_COUNT_CHECK)
    selected = find_check(result, PROOF_SELECTED_CHECK)
    signature = find_check(result, SIGNATURE_CHECK)

    assert count is not None
    assert selected is not None
    assert signature is not None
    assert count.passed is True
    assert selected.passed is True
    assert signature.passed is False

    assert result.decision != ALLOW
    assert result.decision == DENY
    assert result.valid is False


def test_two_proof_envelope_fails_closed_at_count_check() -> None:
    result = verify_trusted_envelope(envelope_with_n_proofs(2))

    count = find_check(result, PROOF_COUNT_CHECK)

    assert count is not None
    assert count.passed is False
    assert result.decision == DENY
    assert result.valid is False


def test_two_proof_envelope_does_not_record_proof_selected() -> None:
    result = verify_trusted_envelope(envelope_with_n_proofs(2))

    assert find_check(result, PROOF_SELECTED_CHECK) is None


def test_two_proof_envelope_does_not_record_payload_hash_valid() -> None:
    result = verify_trusted_envelope(envelope_with_n_proofs(2))

    assert find_check(result, PAYLOAD_CHECK) is None


def test_two_proof_envelope_does_not_record_verification_key_selected() -> None:
    result = verify_trusted_envelope(envelope_with_n_proofs(2))

    assert find_check(result, KEY_CHECK) is None


def test_two_proof_envelope_does_not_reach_signature_stage_checks() -> None:
    result = verify_trusted_envelope(envelope_with_n_proofs(2))

    for name in SIGNATURE_STAGE_CHECKS:
        assert find_check(result, name) is None, (
            f"{name} must not run for a multi-proof envelope"
        )


def test_three_proof_envelope_also_fails_closed() -> None:
    result = verify_trusted_envelope(envelope_with_n_proofs(3))

    count = find_check(result, PROOF_COUNT_CHECK)

    assert count is not None
    assert count.passed is False
    assert find_check(result, PROOF_SELECTED_CHECK) is None
    assert result.decision == DENY


def test_count_check_runs_after_proofs_non_empty_and_before_proof_selected() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    non_empty_index = check_index(result, PROOFS_NON_EMPTY_CHECK)
    count_index = check_index(result, PROOF_COUNT_CHECK)
    proof_index = check_index(result, PROOF_SELECTED_CHECK)

    assert -1 not in (non_empty_index, count_index, proof_index)
    assert non_empty_index < count_index < proof_index


def test_empty_proofs_still_fails_at_proofs_non_empty_not_count_check() -> None:
    result = verify_passport_envelope(
        {"passport": {"subject": "demo"}, "proofs": []},
    )

    non_empty = find_check(result, PROOFS_NON_EMPTY_CHECK)

    assert non_empty is not None
    assert non_empty.passed is False
    assert find_check(result, PROOF_COUNT_CHECK) is None
    assert result.decision == DENY


def test_missing_proofs_still_fails_at_proofs_present_not_count_check() -> None:
    result = verify_passport_envelope({"passport": {"subject": "demo"}})

    present = find_check(result, PROOFS_PRESENT_CHECK)

    assert present is not None
    assert present.passed is False
    assert find_check(result, PROOF_COUNT_CHECK) is None


def test_non_sequence_proofs_still_fails_at_proofs_is_sequence_not_count_check() -> None:
    result = verify_passport_envelope(
        {"passport": {"subject": "demo"}, "proofs": "not-a-sequence"},
    )

    is_sequence = find_check(result, PROOFS_SEQUENCE_CHECK)

    assert is_sequence is not None
    assert is_sequence.passed is False
    assert find_check(result, PROOF_COUNT_CHECK) is None


def test_proof_count_step_never_returns_allow() -> None:
    cases = [
        load_example_envelope(),
        envelope_with_n_proofs(2),
        envelope_with_n_proofs(3),
        {"passport": {"subject": "demo"}, "proofs": []},
    ]

    reached = verify_trusted_envelope(load_example_envelope())
    assert find_check(reached, PROOF_COUNT_CHECK) is not None

    for case in cases:
        result = verify_trusted_envelope(case)

        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW, f"unexpected ALLOW for {case!r}"
        assert result.decision == DENY
        assert result.valid is False


def test_raw_json_parity_includes_count_check() -> None:
    direct = verify_trusted_envelope(load_example_envelope())
    raw = verify_trusted_json(load_example_text())

    assert raw.checks[0].name == RAW_JSON_CHECK
    assert raw.checks[1:] == direct.checks
    assert raw.reason == direct.reason
    assert raw.decision == direct.decision

    count = find_check(raw, PROOF_COUNT_CHECK)

    assert count is not None
    assert count.passed is True


def test_no_forbidden_imports_after_proof_count() -> None:
    import aaid.passport_verifier as module

    for name in FORBIDDEN_VERIFIER_IMPORTS:
        top = name.split(".", maxsplit=1)[0]
        assert not hasattr(module, top), f"verifier must not import {name}"

    source = PASSPORT_VERIFIER_SOURCE_PATH.read_text(encoding="utf-8")

    for name in FORBIDDEN_VERIFIER_IMPORTS:
        assert f"import {name}" not in source
        assert f"from {name}" not in source
