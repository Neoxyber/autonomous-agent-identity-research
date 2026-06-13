"""Tests for the verifier payload-hash boundary.

These cases keep payload-hash validation separate from structural validation,
schema validation, proof selection, key selection, and signature verification.

A passing payload hash does not grant `ALLOW`. A failing payload hash stops
before later signature-related checks. More research and testing are needed to
improve the payload-hash boundary over time.
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

ENVELOPE_MAPPING_CHECK = "envelope_is_mapping"
PASSPORT_PRESENT_CHECK = "passport_present"
PASSPORT_MAPPING_CHECK = "passport_is_mapping"
PROOFS_PRESENT_CHECK = "proofs_present"
PROOFS_SEQUENCE_CHECK = "proofs_is_sequence"
PROOFS_NON_EMPTY_CHECK = "proofs_non_empty"
SCHEMA_CHECK = "schema_valid"
PROOF_COUNT_CHECK = "proof_count_allowed"
PAYLOAD_CHECK = "payload_hash_valid"
SIGNATURE_CHECK = "signature_verification_not_implemented"

STRUCTURAL_CHECK_NAMES = (
    ENVELOPE_MAPPING_CHECK,
    PASSPORT_PRESENT_CHECK,
    PASSPORT_MAPPING_CHECK,
    PROOFS_PRESENT_CHECK,
    PROOFS_SEQUENCE_CHECK,
    PROOFS_NON_EMPTY_CHECK,
)

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


def verify_trusted_envelope(envelope: Any) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def envelope_with_passport_subject(subject: str) -> dict[str, Any]:
    envelope = copy.deepcopy(load_example_envelope())
    envelope["passport"]["subject"] = subject
    return envelope


def envelope_with_proof_payload_hash(payload_hash: str) -> dict[str, Any]:
    envelope = copy.deepcopy(load_example_envelope())
    envelope["proofs"][0]["payload_hash"] = payload_hash
    return envelope


def envelope_with_proof_signature(signature_b64u: str) -> dict[str, Any]:
    envelope = copy.deepcopy(load_example_envelope())
    envelope["proofs"][0]["signature_b64u"] = signature_b64u
    return envelope


def envelope_with_second_proof(payload_hash: str) -> dict[str, Any]:
    envelope = copy.deepcopy(load_example_envelope())
    second = copy.deepcopy(envelope["proofs"][0])
    second["proof_id"] = SECOND_PROOF_ID
    second["payload_hash"] = payload_hash
    envelope["proofs"].append(second)
    return envelope


def test_minimal_example_reaches_payload_hash_valid_true() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    for name in STRUCTURAL_CHECK_NAMES:
        check = find_check(result, name)
        assert check is not None
        assert check.passed is True

    schema = find_check(result, SCHEMA_CHECK)
    payload_hash = find_check(result, PAYLOAD_CHECK)

    assert schema is not None
    assert payload_hash is not None
    assert schema.passed is True
    assert payload_hash.passed is True


def test_minimal_example_denied_with_signature_not_implemented() -> None:
    result = verify_trusted_envelope(load_example_envelope())

    payload_hash = find_check(result, PAYLOAD_CHECK)
    signature = find_check(result, SIGNATURE_CHECK)

    assert payload_hash is not None
    assert signature is not None
    assert payload_hash.passed is True
    assert signature.passed is False

    assert result.valid is False
    assert result.decision == DENY
    assert "signature" in result.reason.lower()


def test_tampering_passport_content_fails_payload_hash() -> None:
    result = verify_trusted_envelope(
        envelope_with_passport_subject("A tampered subject"),
    )

    payload_hash = find_check(result, PAYLOAD_CHECK)

    assert payload_hash is not None
    assert payload_hash.passed is False
    assert result.valid is False
    assert result.decision == DENY


def test_tampering_proof_payload_hash_fails() -> None:
    result = verify_trusted_envelope(envelope_with_proof_payload_hash("b" * 64))

    payload_hash = find_check(result, PAYLOAD_CHECK)

    assert payload_hash is not None
    assert payload_hash.passed is False
    assert result.valid is False
    assert result.decision == DENY


def test_unsupported_hash_alg_fails_closed() -> None:
    envelope = copy.deepcopy(load_example_envelope())
    envelope["proofs"][0]["hash_alg"] = "SHA3-256"

    result = verify_passport_envelope(envelope)

    schema = find_check(result, SCHEMA_CHECK)

    assert schema is not None
    assert schema.passed is False
    assert find_check(result, PAYLOAD_CHECK) is None
    assert result.valid is False
    assert result.decision == DENY


def test_schema_invalid_input_does_not_run_payload_hash() -> None:
    envelope = copy.deepcopy(load_example_envelope())
    envelope["passport"]["risk_class"] = "critical"

    result = verify_passport_envelope(envelope)

    schema = find_check(result, SCHEMA_CHECK)

    assert schema is not None
    assert schema.passed is False
    assert find_check(result, PAYLOAD_CHECK) is None
    assert result.valid is False
    assert result.decision == DENY


def test_malformed_structural_input_does_not_run_payload_hash() -> None:
    malformed_cases = [
        ["passport", "proofs"],
        {"proofs": [{"proof_id": "x"}]},
        {"passport": "not-a-mapping", "proofs": [{"proof_id": "x"}]},
        {"passport": {"subject": "demo"}},
        {"passport": {"subject": "demo"}, "proofs": []},
    ]

    for case in malformed_cases:
        result = verify_passport_envelope(case)

        assert find_check(result, PAYLOAD_CHECK) is None, (
            f"payload_hash_valid must not run for structurally invalid {case!r}"
        )
        assert result.valid is False
        assert result.decision == DENY


def test_payload_hash_failure_short_circuits_before_signature_check() -> None:
    result = verify_trusted_envelope(envelope_with_proof_payload_hash("b" * 64))

    payload_hash = find_check(result, PAYLOAD_CHECK)

    assert payload_hash is not None
    assert payload_hash.passed is False
    assert find_check(result, SIGNATURE_CHECK) is None


def test_payload_hash_step_never_returns_allow() -> None:
    envelope = load_example_envelope()

    wrong_hash = envelope_with_proof_payload_hash("b" * 64)
    tampered_passport = envelope_with_passport_subject("tampered")

    bad_alg = copy.deepcopy(envelope)
    bad_alg["proofs"][0]["hash_alg"] = "SHA3-256"

    malformed = {"passport": {"subject": "demo"}, "proofs": []}
    cases = [load_example_envelope(), wrong_hash, tampered_passport, bad_alg, malformed]

    reached = verify_trusted_envelope(load_example_envelope())
    assert find_check(reached, PAYLOAD_CHECK) is not None

    for case in cases:
        result = verify_trusted_envelope(case)

        assert result.decision != ALLOW, f"unexpected ALLOW for {case!r}"
        assert result.decision == DENY
        assert result.valid is False


def test_no_signature_verification_in_this_step() -> None:
    result = verify_trusted_envelope(
        envelope_with_proof_signature("QW5vdGhlci1zaWduYXR1cmU"),
    )

    payload_hash = find_check(result, PAYLOAD_CHECK)
    signature = find_check(result, SIGNATURE_CHECK)

    assert payload_hash is not None
    assert signature is not None
    assert payload_hash.passed is True
    assert signature.passed is False

    assert result.decision == DENY
    assert "signature" in result.reason.lower()


def test_multi_proof_envelope_fails_closed_before_payload_hash() -> None:
    result = verify_trusted_envelope(envelope_with_second_proof("c" * 64))

    proof_count = find_check(result, PROOF_COUNT_CHECK)

    assert proof_count is not None
    assert proof_count.passed is False
    assert find_check(result, PAYLOAD_CHECK) is None
    assert result.decision == DENY
    assert result.valid is False


def test_multi_proof_fails_closed_even_with_correct_later_proof() -> None:
    envelope = load_example_envelope()
    correct_hash = hash_passport_payload(
        envelope["passport"],
        envelope["proofs"][0]["hash_alg"],
    )

    result = verify_trusted_envelope(envelope_with_second_proof(correct_hash))

    proof_count = find_check(result, PROOF_COUNT_CHECK)

    assert proof_count is not None
    assert proof_count.passed is False
    assert find_check(result, PAYLOAD_CHECK) is None
    assert result.decision == DENY


def test_hash_alg_length_mismatch_fails_payload_hash() -> None:
    envelope = copy.deepcopy(load_example_envelope())
    envelope["proofs"][0]["hash_alg"] = "SHA-512"
    envelope["proofs"][0]["payload_hash"] = "a" * 64

    result = verify_trusted_envelope(envelope)

    schema = find_check(result, SCHEMA_CHECK)
    payload_hash = find_check(result, PAYLOAD_CHECK)

    assert schema is not None
    assert payload_hash is not None
    assert schema.passed is True
    assert payload_hash.passed is False

    assert result.decision == DENY
    assert find_check(result, SIGNATURE_CHECK) is None


def test_changing_a_proof_field_does_not_affect_payload_hash() -> None:
    result = verify_trusted_envelope(
        envelope_with_proof_signature("QW5vdGhlci1zaWduYXR1cmU"),
    )

    payload_hash = find_check(result, PAYLOAD_CHECK)

    assert payload_hash is not None
    assert payload_hash.passed is True


def test_payload_hash_failure_reason_is_about_hash_not_signature() -> None:
    result = verify_trusted_envelope(envelope_with_proof_payload_hash("b" * 64))

    payload_hash = find_check(result, PAYLOAD_CHECK)

    assert payload_hash is not None
    assert payload_hash.passed is False
    assert payload_hash.name == PAYLOAD_CHECK
    assert payload_hash.reason
    assert "payload hash" in payload_hash.reason.lower()
    assert "signature" not in payload_hash.reason.lower()
    assert "payload hash" in result.reason.lower()
    assert "signature" not in result.reason.lower()
