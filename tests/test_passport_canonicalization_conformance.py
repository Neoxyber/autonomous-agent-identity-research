"""Conformance and regression tests for the current canonicalization helper.

These tests record the current observed behavior for the current agent passport
profile only: deterministic, compact, UTF-8, order-independent canonical bytes,
and a hash taken over exactly those bytes. This behavior is part of the current
research boundary and is expected to improve with more testing and research.
These tests do not assert full independent RFC 8785 / JSON Canonicalization
Scheme compliance, which is left to a later research step.
"""

import copy
import hashlib
import json
from pathlib import Path

import pytest

import aaid.passport_verifier as passport_verifier_module
from aaid.canonicalization import (
    canonicalize_passport_payload,
    hash_passport_payload,
)

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
CANON_SOURCE_PATH = SRC / "aaid" / "canonicalization.py"
PV_SOURCE_PATH = SRC / "aaid" / "passport_verifier.py"

EXPECTED_MINIMAL_PASSPORT_SHA256 = (
    "b85a7ddfefccb9582bf6ab23dac42a968cc0b6aabfc1d29d416ea25e27bfb6bc"
)

FORBIDDEN_VERIFIER_IMPORTS = (
    "hashlib",
    "hmac",
    "base64",
    "ssl",
    "secrets",
    "cryptography",
    "pqcrypto",
    "oqs",
    "requests",
    "httpx",
    "socket",
    "urllib",
)


def load_example_envelope() -> dict:
    with EXAMPLE_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def load_example_passport() -> dict:
    return load_example_envelope()["passport"]


def reverse_mapping_keys(mapping: dict) -> dict:
    """Rebuild a mapping with keys inserted in reverse order."""
    return {key: mapping[key] for key in reversed(list(mapping.keys()))}


def test_canonicalize_returns_bytes() -> None:
    assert isinstance(canonicalize_passport_payload(load_example_passport()), bytes)


def test_canonicalize_is_deterministic_across_calls() -> None:
    passport = load_example_passport()

    assert canonicalize_passport_payload(passport) == canonicalize_passport_payload(
        passport
    )


def test_top_level_key_insertion_order_does_not_change_output() -> None:
    ordered = {
        "agent_id": "urn:aaid:agent:demo",
        "subject": "Demo",
        "risk_class": "standard",
    }
    reordered = {
        "risk_class": "standard",
        "subject": "Demo",
        "agent_id": "urn:aaid:agent:demo",
    }

    assert canonicalize_passport_payload(ordered) == canonicalize_passport_payload(
        reordered
    )


def test_nested_key_insertion_order_does_not_change_output() -> None:
    ordered = {
        "outer": {
            "alpha": "one",
            "beta": "two",
            "gamma": {"x": "1", "y": "2"},
        },
    }
    reordered = {
        "outer": {
            "gamma": {"y": "2", "x": "1"},
            "beta": "two",
            "alpha": "one",
        },
    }

    assert canonicalize_passport_payload(ordered) == canonicalize_passport_payload(
        reordered
    )


def test_canonical_output_is_compact() -> None:
    data = {"b": "two", "a": "one", "nested": {"d": "four", "c": "three"}}
    output = canonicalize_passport_payload(data)

    assert output == b'{"a":"one","b":"two","nested":{"c":"three","d":"four"}}'
    assert b" " not in output
    assert b"\n" not in output
    assert b"\t" not in output


def test_canonical_output_is_utf8_bytes() -> None:
    passport = load_example_passport()
    output = canonicalize_passport_payload(passport)

    assert json.loads(output.decode("utf-8")) == passport

    # Printable non-ASCII remains UTF-8 here, but this is not a full
    # RFC 8785/JCS assertion.
    non_ascii_output = canonicalize_passport_payload({"subject": "Café"})

    assert isinstance(non_ascii_output, bytes)
    assert "Café".encode("utf-8") in non_ascii_output


@pytest.mark.parametrize(
    ("hash_algorithm", "hashlib_name"),
    [
        pytest.param("SHA-256", "sha256", id="sha-256"),
        pytest.param("SHA-384", "sha384", id="sha-384"),
        pytest.param("SHA-512", "sha512", id="sha-512"),
    ],
)
def test_hash_uses_exact_canonical_bytes(
    hash_algorithm: str,
    hashlib_name: str,
) -> None:
    passport = load_example_passport()
    canonical = canonicalize_passport_payload(passport)

    expected = hashlib.new(hashlib_name, canonical).hexdigest()

    assert hash_passport_payload(passport, hash_algorithm) == expected


def test_example_top_level_reorder_does_not_change_output() -> None:
    passport = load_example_passport()
    reordered = reverse_mapping_keys(passport)

    assert list(reordered.keys()) != list(passport.keys())
    assert canonicalize_passport_payload(reordered) == canonicalize_passport_payload(
        passport
    )


def test_example_nested_reorder_does_not_change_output() -> None:
    passport = load_example_passport()
    reordered = copy.deepcopy(passport)
    reordered["operator"] = reverse_mapping_keys(passport["operator"])
    reordered["public_keys"][0] = reverse_mapping_keys(passport["public_keys"][0])
    reordered["permissions"] = reverse_mapping_keys(passport["permissions"])

    assert canonicalize_passport_payload(reordered) == canonicalize_passport_payload(
        passport
    )


def test_proof_data_excluded_from_payload() -> None:
    envelope = load_example_envelope()
    output = canonicalize_passport_payload(envelope["passport"])
    proof = envelope["proofs"][0]

    assert b"proofs" not in output
    assert proof["proof_id"].encode("utf-8") not in output
    assert proof["proof_type"].encode("utf-8") not in output
    assert proof["proof_purpose"].encode("utf-8") not in output


def test_signature_b64u_excluded_from_payload() -> None:
    envelope = load_example_envelope()
    output = canonicalize_passport_payload(envelope["passport"])

    assert b"signature_b64u" not in output
    assert envelope["proofs"][0]["signature_b64u"].encode("utf-8") not in output


def test_signature_input_helper_matches_canonicalization() -> None:
    passport = load_example_passport()

    _, signature_input = passport_verifier_module._prepare_signature_input(passport)

    assert signature_input == canonicalize_passport_payload(passport)


def test_helper_documents_jcs_non_compliance() -> None:
    normalized = " ".join(CANON_SOURCE_PATH.read_text(encoding="utf-8").split())

    assert "RFC 8785" in normalized
    assert "not a complete independent RFC 8785" in normalized
    assert "must not be relied on for full JCS compliance" in normalized


def test_passport_verifier_imports_no_crypto_or_network_modules() -> None:
    # Keep this verifier boundary inert until real signature verification is
    # explicitly designed and tested.
    for module_name in FORBIDDEN_VERIFIER_IMPORTS:
        assert not hasattr(passport_verifier_module, module_name), (
            f"passport_verifier must not import {module_name}"
        )

    source = PV_SOURCE_PATH.read_text(encoding="utf-8")
    for module_name in FORBIDDEN_VERIFIER_IMPORTS:
        assert f"import {module_name}" not in source
        assert f"from {module_name}" not in source


def test_boolean_serializes_as_lowercase_true() -> None:
    assert canonicalize_passport_payload({"audit_required": True}) == (
        b'{"audit_required":true}'
    )


def test_array_element_order_is_significant() -> None:
    # Array order is significant; reordering security-relevant action lists
    # must change canonical bytes.
    assert canonicalize_passport_payload(
        {"a": ["x", "y"]}
    ) != canonicalize_passport_payload({"a": ["y", "x"]})

    passport = load_example_passport()
    reordered = copy.deepcopy(passport)
    reordered["permissions"]["prohibited_actions"] = list(
        reversed(passport["permissions"]["prohibited_actions"])
    )

    assert canonicalize_passport_payload(
        reordered
    ) != canonicalize_passport_payload(passport)


def test_example_canonical_sha256_is_frozen_golden_vector() -> None:
    # The golden vector catches silent canonical-byte or payload-hash drift.
    envelope = load_example_envelope()
    digest = hash_passport_payload(envelope["passport"], "SHA-256")

    assert digest == envelope["proofs"][0]["payload_hash"]
    assert digest == EXPECTED_MINIMAL_PASSPORT_SHA256
