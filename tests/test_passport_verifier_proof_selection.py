"""Tests for the verifier proof-selection boundary.

These cases keep proof selection explicit after structural and schema checks and
before payload-hash validation.

A selected proof does not grant `ALLOW`. Multi-proof envelopes fail closed before
proof selection and payload-hash validation. More research and testing are
needed to improve proof-selection handling over time.
"""

import copy
import json
from pathlib import Path
from typing import Any

from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.canonicalization import hash_passport_payload
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"

SCHEMA_CHECK = "schema_valid"
PROOF_COUNT_CHECK = "proof_count_allowed"
PROOF_SELECTED_CHECK = "proof_selected"
PAYLOAD_CHECK = "payload_hash_valid"
SIGNATURE_CHECK = "signature_verification_not_implemented"

SECOND_PROOF_ID = "urn:aaid:proof:second-test-proof"


def load_example_envelope() -> dict[str, Any]:
    return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))


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


def verify_trusted_envelope(envelope: Any) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def hash_for_example_passport(envelope: dict[str, Any]) -> str:
    return hash_passport_payload(
        envelope["passport"],
        envelope["proofs"][0]["hash_alg"],
    )


def envelope_with_second_proof(payload_hash: str) -> dict[str, Any]:
    envelope = load_example_envelope()
    second = copy.deepcopy(envelope["proofs"][0])
    second["proof_id"] = SECOND_PROOF_ID
    second["payload_hash"] = payload_hash
    envelope["proofs"].append(second)
    return envelope


def envelope_with_selected_payload_hash(payload_hash: str) -> dict[str, Any]:
    envelope = load_example_envelope()
    envelope["proofs"][0]["payload_hash"] = payload_hash
    return envelope


def schema_invalid_envelope() -> dict[str, Any]:
    envelope = load_example_envelope()
    envelope["passport"]["risk_class"] = "critical"
    return envelope


def test_minimal_example_records_proof_selected_passed() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    selected = find_check(result, PROOF_SELECTED_CHECK)

    assert selected is not None
    assert selected.passed is True


def test_proof_selected_between_schema_valid_and_payload_hash_valid() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    schema_index = check_index(result, SCHEMA_CHECK)
    proof_index = check_index(result, PROOF_SELECTED_CHECK)
    payload_index = check_index(result, PAYLOAD_CHECK)

    assert schema_index != -1
    assert proof_index != -1
    assert payload_index != -1
    assert schema_index < proof_index < payload_index


def test_proof_selected_reason_mentions_first_proof_rule() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    selected = find_check(result, PROOF_SELECTED_CHECK)

    assert selected is not None
    reason = selected.reason.lower()
    assert "first proof" in reason
    assert "first-version" in reason


def test_payload_hash_valid_uses_selected_first_proof() -> None:
    valid = verify_trusted_envelope(load_example_envelope())

    valid_payload = find_check(valid, PAYLOAD_CHECK)
    assert valid_payload is not None
    assert valid_payload.passed is True

    tampered = envelope_with_selected_payload_hash("a" * 64)
    invalid = verify_trusted_envelope(tampered)

    invalid_payload = find_check(invalid, PAYLOAD_CHECK)
    assert invalid_payload is not None
    assert invalid_payload.passed is False


def test_two_proofs_fail_closed_before_proof_selected() -> None:
    result = verify_trusted_envelope(envelope_with_second_proof("a" * 64))

    count = find_check(result, PROOF_COUNT_CHECK)

    assert count is not None
    assert count.passed is False
    assert find_check(result, PROOF_SELECTED_CHECK) is None
    assert find_check(result, PAYLOAD_CHECK) is None
    assert result.decision == DENY
    assert result.valid is False


def test_two_proofs_fail_closed_even_with_correct_later_proof() -> None:
    envelope = load_example_envelope()
    correct_hash = hash_for_example_passport(envelope)

    result = verify_trusted_envelope(envelope_with_second_proof(correct_hash))

    count = find_check(result, PROOF_COUNT_CHECK)

    assert count is not None
    assert count.passed is False
    assert find_check(result, PROOF_SELECTED_CHECK) is None
    assert find_check(result, PAYLOAD_CHECK) is None
    assert result.decision == DENY


def test_schema_invalid_input_does_not_run_proof_selected() -> None:
    result = verify_passport_envelope(schema_invalid_envelope())

    schema = find_check(result, SCHEMA_CHECK)

    assert schema is not None
    assert schema.passed is False
    assert find_check(result, PROOF_SELECTED_CHECK) is None


def test_structural_invalid_input_does_not_run_proof_selected() -> None:
    structural_cases = [
        ["passport", "proofs"],
        {"passport": {"subject": "demo"}, "proofs": []},
    ]

    for case in structural_cases:
        result = verify_passport_envelope(case)

        assert find_check(result, PROOF_SELECTED_CHECK) is None, (
            f"proof_selected must not run for structurally invalid {case!r}"
        )


def test_proof_selection_step_never_returns_allow() -> None:
    envelope = load_example_envelope()
    correct_hash = hash_for_example_passport(envelope)

    cases = [
        load_example_envelope(),
        envelope_with_second_proof(correct_hash),
        envelope_with_second_proof("a" * 64),
        {"passport": {"subject": "demo"}, "proofs": []},
        envelope_with_selected_payload_hash("b" * 64),
        schema_invalid_envelope(),
    ]

    reached = verify_trusted_envelope(load_example_envelope())
    assert find_check(reached, PROOF_SELECTED_CHECK) is not None

    for case in cases:
        result = verify_trusted_envelope(case)

        assert result.decision != ALLOW, f"unexpected ALLOW for {case!r}"
        assert result.decision == DENY
        assert result.valid is False


def test_signature_verification_still_not_implemented() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    signature = find_check(result, SIGNATURE_CHECK)

    assert signature is not None
    assert signature.passed is False
    assert result.decision == DENY
