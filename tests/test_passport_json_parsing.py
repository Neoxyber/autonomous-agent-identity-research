"""Raw JSON parsing boundary tests.

These tests record the current raw JSON parsing boundary that rejects duplicate
object member names before schema validation or canonicalization.

Duplicate object member names exist only in raw JSON text. After ordinary
``json.loads`` parsing they are silently collapsed into a single Python mapping
key, so they cannot be detected later from a parsed ``Mapping``. This boundary
catches them at parse time.

These tests do not present the parser as full RFC 8785/JCS or full I-JSON
conformance work. They only record the current duplicate-key rejection behavior
of this parsing helper. More tests and research are still needed around this
boundary.
"""

import json

import pytest

from aaid.json_parsing import parse_json_no_duplicate_keys

DUPLICATE_KEY_ERROR = "Duplicate JSON object member name"


def test_valid_json_parses_normally() -> None:
    """Valid JSON without duplicate keys parses like json.loads."""

    text = '{"b": 2, "a": {"x": 1}, "list": [1, 2, {"y": 3}]}'

    assert parse_json_no_duplicate_keys(text) == json.loads(text)


@pytest.mark.parametrize(
    "text",
    [
        pytest.param('{"a": 1, "a": 2}', id="top-level-object"),
        pytest.param('{"outer": {"a": 1, "a": 2}}', id="nested-object"),
        pytest.param('[{"a": 1, "a": 2}]', id="object-inside-array"),
    ],
)
def test_duplicate_key_raises_value_error(text: str) -> None:
    """Duplicate member names are rejected wherever the object appears."""

    with pytest.raises(ValueError, match=DUPLICATE_KEY_ERROR):
        parse_json_no_duplicate_keys(text)


def test_same_key_in_sibling_objects_is_allowed() -> None:
    """The same member name in different sibling objects is allowed."""

    text = '{"first": {"x": 1}, "second": {"x": 2}}'

    assert parse_json_no_duplicate_keys(text) == {
        "first": {"x": 1},
        "second": {"x": 2},
    }


def test_invalid_json_raises_value_error() -> None:
    """Malformed JSON surfaces through the ValueError family.

    ``json.JSONDecodeError`` is a subclass of ``ValueError``, so callers can
    catch malformed input and duplicate-key rejection with the same exception
    type.
    """

    with pytest.raises(ValueError):
        parse_json_no_duplicate_keys('{"a": }')
