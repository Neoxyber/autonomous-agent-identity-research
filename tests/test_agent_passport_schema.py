import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "specs" / "agent-passport.schema.json"
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def test_agent_passport_schema_is_valid() -> None:
    schema = load_json(SCHEMA_PATH)

    Draft202012Validator.check_schema(schema)


def test_minimal_agent_passport_example_matches_schema() -> None:
    schema = load_json(SCHEMA_PATH)
    example = load_json(EXAMPLE_PATH)

    validator = Draft202012Validator(schema)
    validator.validate(example)


SCHEMA = load_json(SCHEMA_PATH)
VALIDATOR = Draft202012Validator(SCHEMA)


def base_envelope() -> dict:
    """A fresh, schema-valid envelope.

    Each call re-parses the example file, so per-test mutations stay isolated.
    The valid baseline itself is asserted by
    test_minimal_agent_passport_example_matches_schema.
    """
    return load_json(EXAMPLE_PATH)


def has_violation(envelope, keyword, path, needle=None) -> bool:
    """True if validation reports a `keyword` error at `path`.

    `path` is compared against jsonschema's absolute_path. When `needle` is
    given it must also appear in the error message (used to name the offending
    property for `required` / `additionalProperties` errors, which are reported
    on the containing object).
    """
    for error in VALIDATOR.iter_errors(envelope):
        if error.validator == keyword and list(error.absolute_path) == path:
            if needle is None or needle in error.message:
                return True
    return False


def test_missing_operator_is_rejected() -> None:
    env = base_envelope()
    del env["passport"]["operator"]
    assert has_violation(env, "required", ["passport"], "operator")


def test_missing_proofs_is_rejected() -> None:
    env = base_envelope()
    del env["proofs"]
    assert has_violation(env, "required", [], "proofs")


def test_invalid_risk_class_is_rejected() -> None:
    env = base_envelope()
    env["passport"]["risk_class"] = "critical"
    assert has_violation(env, "enum", ["passport", "risk_class"])


def test_invalid_lifecycle_status_is_rejected() -> None:
    env = base_envelope()
    env["passport"]["lifecycle_status"] = "deactivated"
    assert has_violation(env, "enum", ["passport", "lifecycle_status"])


def test_unexpected_passport_field_is_rejected() -> None:
    env = base_envelope()
    env["passport"]["unexpected_field"] = "x"
    assert has_violation(env, "additionalProperties", ["passport"], "unexpected_field")


def test_invalid_payload_hash_length_is_rejected() -> None:
    env = base_envelope()
    # 63 hex chars: valid charset, but not 64/96/128 -> pattern fails on length only
    env["proofs"][0]["payload_hash"] = "a" * 63
    assert has_violation(env, "pattern", ["proofs", 0, "payload_hash"])
