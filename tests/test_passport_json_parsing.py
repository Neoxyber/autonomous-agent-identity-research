"""Raw JSON parsing boundary tests.

These tests pin the behaviour of the raw JSON parsing boundary that rejects
duplicate object member names before schema validation or canonicalization.

Duplicate object member names exist only in raw JSON text. After ordinary
``json.loads`` parsing they are silently collapsed into a single Python mapping
key, so they cannot be detected later from a parsed ``Mapping``. This boundary
catches them at parse time.

These tests do not claim full RFC 8785/JCS or full I-JSON conformance. They only
pin the duplicate-key rejection behaviour of this parsing helper.
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

from aaid.json_parsing import parse_json_no_duplicate_keys


def test_valid_json_parses_normally():
    """Valid JSON without duplicate keys parses like json.loads."""

    text = '{"b": 2, "a": {"x": 1}, "list": [1, 2, {"y": 3}]}'

    assert parse_json_no_duplicate_keys(text) == json.loads(text)


def test_top_level_duplicate_key_raises_value_error():
    """A duplicate member name in the top-level object is rejected."""

    with pytest.raises(ValueError, match="Duplicate JSON object member name"):
        parse_json_no_duplicate_keys('{"a": 1, "a": 2}')


def test_nested_duplicate_key_raises_value_error():
    """A duplicate member name in a nested object is rejected."""

    with pytest.raises(ValueError, match="Duplicate JSON object member name"):
        parse_json_no_duplicate_keys('{"outer": {"a": 1, "a": 2}}')


def test_duplicate_key_inside_array_object_raises_value_error():
    """A duplicate member name inside an object within an array is rejected."""

    with pytest.raises(ValueError, match="Duplicate JSON object member name"):
        parse_json_no_duplicate_keys('[{"a": 1, "a": 2}]')


def test_same_key_in_sibling_objects_is_allowed():
    """The same member name in different sibling objects is allowed."""

    text = '{"first": {"x": 1}, "second": {"x": 2}}'

    assert parse_json_no_duplicate_keys(text) == {
        "first": {"x": 1},
        "second": {"x": 2},
    }


def test_invalid_json_raises_value_error():
    """Malformed JSON surfaces through the ValueError family.

    ``json.JSONDecodeError`` is a subclass of ``ValueError``, so callers can
    catch malformed input and duplicate-key rejection with the same exception
    type.
    """

    with pytest.raises(ValueError):
        parse_json_no_duplicate_keys('{"a": }')
