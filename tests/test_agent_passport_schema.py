import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "specs" / "agent-passport.schema.json"
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def load_valid_envelope() -> dict:
    """Return a fresh schema-valid envelope for each mutation test."""
    return load_json(EXAMPLE_PATH)


SCHEMA = load_json(SCHEMA_PATH)
VALIDATOR = Draft202012Validator(SCHEMA)


def has_schema_violation(envelope, keyword, path, needle=None) -> bool:
    """Return true when schema validation reports the expected violation."""
    for error in VALIDATOR.iter_errors(envelope):
        if error.validator != keyword:
            continue
        if list(error.absolute_path) != path:
            continue
        if needle is not None and needle not in error.message:
            continue
        return True
    return False


def test_agent_passport_schema_is_valid() -> None:
    Draft202012Validator.check_schema(SCHEMA)


def test_minimal_agent_passport_example_matches_schema() -> None:
    VALIDATOR.validate(load_valid_envelope())


def test_missing_operator_is_rejected() -> None:
    envelope = load_valid_envelope()
    del envelope["passport"]["operator"]

    assert has_schema_violation(envelope, "required", ["passport"], "operator")


def test_missing_proofs_is_rejected() -> None:
    envelope = load_valid_envelope()
    del envelope["proofs"]

    assert has_schema_violation(envelope, "required", [], "proofs")


def test_invalid_risk_class_is_rejected() -> None:
    envelope = load_valid_envelope()
    envelope["passport"]["risk_class"] = "critical"

    assert has_schema_violation(envelope, "enum", ["passport", "risk_class"])


def test_invalid_lifecycle_status_is_rejected() -> None:
    envelope = load_valid_envelope()
    envelope["passport"]["lifecycle_status"] = "deactivated"

    assert has_schema_violation(envelope, "enum", ["passport", "lifecycle_status"])


def test_unexpected_passport_field_is_rejected() -> None:
    envelope = load_valid_envelope()
    envelope["passport"]["unexpected_field"] = "x"

    assert has_schema_violation(
        envelope,
        "additionalProperties",
        ["passport"],
        "unexpected_field",
    )


def test_invalid_payload_hash_length_is_rejected() -> None:
    envelope = load_valid_envelope()
    envelope["proofs"][0]["payload_hash"] = "a" * 63

    assert has_schema_violation(envelope, "pattern", ["proofs", 0, "payload_hash"])
