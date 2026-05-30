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
