"""Raw JSON parsing boundary helper.

This is a research helper that parses raw JSON text while rejecting duplicate
object member names. Duplicate member names exist only in raw JSON text; once
``json.loads`` builds a Python mapping, repeated names are silently collapsed to
a single key, so they cannot be detected later from a parsed ``Mapping``.

This helper is a raw JSON parsing boundary only. It is not schema validation, it
is not canonicalization, and it does not claim full RFC 8785 (JSON
Canonicalization Scheme) or full I-JSON conformance.
"""

import json
from typing import Any


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build an object from member pairs, failing closed on duplicate names.

    ``json.loads`` calls this hook with the ordered ``(name, value)`` pairs of
    every JSON object, including objects nested inside arrays. Repeated member
    names are preserved in ``pairs`` here, so a duplicate is detected before the
    pairs are collapsed into a single mapping.
    """
    seen: set[str] = set()
    for name, _value in pairs:
        if name in seen:
            raise ValueError(
                f"Duplicate JSON object member name: {name!r}"
            )
        seen.add(name)
    return dict(pairs)


def parse_json_no_duplicate_keys(text: str) -> object:
    """Parse JSON text and reject any object with duplicate member names.

    Returns the normally parsed JSON value for valid input. Raises ``ValueError``
    when any object (including nested objects and objects inside arrays) contains
    a duplicate member name. Malformed JSON raises ``json.JSONDecodeError``,
    which is a subclass of ``ValueError``, so callers can catch both failure
    modes through the ``ValueError`` family.
    """
    return json.loads(text, object_pairs_hook=_reject_duplicate_keys)
