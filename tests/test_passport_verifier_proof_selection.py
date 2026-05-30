import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.canonicalization import hash_passport_payload

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"


def load_envelope():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


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


def envelope_with_second_proof(payload_hash):
    # Append a schema-valid second proof whose only meaningful difference is its
    # payload_hash. proof_id reuses the proven aaid-valid pattern; duplicates are
    # allowed because the schema sets no uniqueItems constraint on proofs.
    envelope = load_envelope()
    second = copy.deepcopy(envelope["proofs"][0])
    second["proof_id"] = "urn:aaid:proof:second-test-proof"
    second["payload_hash"] = payload_hash
    envelope["proofs"].append(second)
    return envelope


def test_minimal_example_records_proof_selected_passed():
    # The minimal example reaches proof selection, which records proof_selected
    # as a distinct, passing check.
    result = verify_passport_envelope(load_envelope())
    selected = check_named(result, "proof_selected")
    assert selected is not None
    assert selected.passed is True


def test_proof_selected_between_schema_valid_and_payload_hash_valid():
    # Proof selection is explicit: it runs after schema validation and before the
    # payload hash is checked.
    result = verify_passport_envelope(load_envelope())
    schema_index = check_index(result, "schema_valid")
    proof_index = check_index(result, "proof_selected")
    payload_index = check_index(result, "payload_hash_valid")
    assert schema_index != -1
    assert proof_index != -1
    assert payload_index != -1
    assert schema_index < proof_index < payload_index


def test_proof_selected_reason_mentions_first_proof_rule():
    # The recorded reason must make the first-version rule explicit and auditable.
    result = verify_passport_envelope(load_envelope())
    selected = check_named(result, "proof_selected")
    assert selected is not None
    reason = selected.reason.lower()
    assert "first proof" in reason
    assert "first-version" in reason


def test_payload_hash_valid_uses_selected_first_proof():
    # The payload hash step consumes the selected proof. The minimal example's
    # first proof carries the real digest, so payload_hash_valid passes; corrupting
    # that selected proof's hash makes it fail.
    result = verify_passport_envelope(load_envelope())
    assert check_named(result, "payload_hash_valid").passed is True

    tampered = load_envelope()
    tampered["proofs"][0]["payload_hash"] = "a" * 64
    result = verify_passport_envelope(tampered)
    assert check_named(result, "payload_hash_valid").passed is False


def test_mismatched_second_proof_does_not_affect_first_proof_selection():
    # A later proof with a wrong hash is ignored; selection stays on the first
    # proof and the payload hash still matches.
    envelope = envelope_with_second_proof("a" * 64)
    result = verify_passport_envelope(envelope)
    assert check_named(result, "proof_selected").passed is True
    assert check_named(result, "payload_hash_valid").passed is True


def test_mismatched_first_proof_fails_even_if_later_proof_correct():
    # A correct later proof must not rescue a wrong first proof: selection binds to
    # the first proof and payload_hash_valid fails.
    envelope = load_envelope()
    correct = hash_passport_payload(
        envelope["passport"], envelope["proofs"][0]["hash_alg"]
    )
    second = copy.deepcopy(envelope["proofs"][0])
    second["proof_id"] = "urn:aaid:proof:second-test-proof"
    second["payload_hash"] = correct
    envelope["proofs"].append(second)
    envelope["proofs"][0]["payload_hash"] = "b" * 64

    result = verify_passport_envelope(envelope)
    assert check_named(result, "proof_selected").passed is True
    assert check_named(result, "payload_hash_valid").passed is False
    assert result.decision == DENY


def test_schema_invalid_input_does_not_run_proof_selected():
    # A schema violation short-circuits before proof selection runs.
    envelope = load_envelope()
    envelope["passport"]["risk_class"] = "critical"
    result = verify_passport_envelope(envelope)
    assert check_named(result, "schema_valid").passed is False
    assert check_named(result, "proof_selected") is None


def test_structural_invalid_input_does_not_run_proof_selected():
    # Structural failures short-circuit before proof selection runs.
    structural_cases = [
        ["passport", "proofs"],
        {"passport": {"subject": "demo"}, "proofs": []},
    ]
    for case in structural_cases:
        result = verify_passport_envelope(case)
        assert check_named(result, "proof_selected") is None, (
            f"proof_selected must not run for structurally invalid {case!r}"
        )


def test_proof_selection_step_never_returns_allow():
    # Proof selection never opens an ALLOW path.
    cases = [
        load_envelope(),
        envelope_with_second_proof(
            hash_passport_payload(
                load_envelope()["passport"],
                load_envelope()["proofs"][0]["hash_alg"],
            )
        ),
        envelope_with_second_proof("a" * 64),
        {"passport": {"subject": "demo"}, "proofs": []},
    ]
    wrong_first = load_envelope()
    wrong_first["proofs"][0]["payload_hash"] = "b" * 64
    cases.append(wrong_first)
    schema_invalid = load_envelope()
    schema_invalid["passport"]["risk_class"] = "critical"
    cases.append(schema_invalid)

    for case in cases:
        result = verify_passport_envelope(case)
        assert result.decision != ALLOW, f"unexpected ALLOW for {case!r}"
        assert result.decision == DENY
        assert result.valid is False


def test_signature_verification_still_not_implemented():
    # Adding proof selection must not introduce signature verification.
    result = verify_passport_envelope(load_envelope())
    signature = check_named(result, "signature_verification_not_implemented")
    assert signature is not None
    assert signature.passed is False
    assert result.decision == DENY
