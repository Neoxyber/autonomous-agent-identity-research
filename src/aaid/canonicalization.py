"""Passport canonicalization helper.

This is a first research helper for the current agent passport schema. It
produces deterministic JSON bytes for a passport payload so the same payload
hashes and signs to the same input. It is not a complete independent RFC 8785
(JSON Canonicalization Scheme) implementation and must not be relied on for full
JCS compliance. Before relying on signatures, test against a reviewed RFC 8785
compatible library.
"""

import json
from collections.abc import Mapping
from typing import Any


def canonicalize_passport_payload(passport: Mapping[str, Any]) -> bytes:
    """Return canonical JSON bytes for a passport payload.

    The input must be the ``passport`` object from a passport envelope
    (``envelope["passport"]``). The ``proofs`` array is detached proof metadata
    and is not part of the signed payload, so it must not be passed in. Object
    member order does not affect the output; timestamp and identifier strings are
    passed through unchanged.
    """
    return json.dumps(
        passport,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
