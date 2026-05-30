"""Passport canonicalization helper.

This is a first research helper for the current agent passport schema. It
produces deterministic JSON bytes for a passport payload so the same payload
hashes and signs to the same input. It is not a complete independent RFC 8785
(JSON Canonicalization Scheme) implementation and must not be relied on for full
JCS compliance. Before relying on signatures, test against a reviewed RFC 8785
compatible library.
"""

import hashlib
import json
from collections.abc import Mapping
from typing import Any

_SUPPORTED_HASH_ALGORITHMS = {
    "SHA-256": "sha256",
    "SHA-384": "sha384",
    "SHA-512": "sha512",
}


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


def hash_passport_payload(
    passport: Mapping[str, Any], hash_alg: str = "SHA-256"
) -> str:
    """Return the lowercase hex digest of the canonical passport payload.

    The digest is computed over the canonical bytes from
    ``canonicalize_passport_payload`` using one of the allowed hash algorithms
    (``SHA-256``, ``SHA-384``, ``SHA-512``). This is a payload hash only; it is
    not a signature. Algorithm names are matched exactly, and unsupported
    algorithms fail closed with ``ValueError``.
    """
    try:
        hashlib_name = _SUPPORTED_HASH_ALGORITHMS[hash_alg]
    except KeyError:
        supported = ", ".join(sorted(_SUPPORTED_HASH_ALGORITHMS))
        raise ValueError(
            f"Unsupported hash algorithm: {hash_alg!r}. "
            f"Supported algorithms: {supported}."
        ) from None
    canonical = canonicalize_passport_payload(passport)
    return hashlib.new(hashlib_name, canonical).hexdigest()
