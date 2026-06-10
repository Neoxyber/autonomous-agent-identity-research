"""Conformance and regression tests for the current canonicalization helper.

These tests document what the current research helper guarantees for the current
agent passport profile only: deterministic, compact, UTF-8, order-independent
canonical bytes, and a hash taken over exactly those bytes. They do not assert,
and must not be read as asserting, full independent RFC 8785 / JSON
Canonicalization Scheme compliance, which is left to a later research step.
"""

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

import aaid.passport_verifier as passport_verifier_module
from aaid.canonicalization import (
    canonicalize_passport_payload,
    hash_passport_payload,
)

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
CANON_SOURCE_PATH = SRC / "aaid" / "canonicalization.py"
PV_SOURCE_PATH = SRC / "aaid" / "passport_verifier.py"


def load_envelope():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_passport():
    return load_envelope()["passport"]


def reverse_keys(mapping):
    # Rebuild a dict with keys inserted in reverse order, to show canonical
    # output is independent of insertion order (object keys only; array element
    # order is intentionally significant and is preserved).
    return {key: mapping[key] for key in reversed(list(mapping.keys()))}


# 1. canonicalize_passport_payload returns bytes.
def test_canonicalize_returns_bytes():
    assert isinstance(canonicalize_passport_payload(load_passport()), bytes)


# 2. canonicalize_passport_payload is deterministic for repeated calls.
def test_canonicalize_is_deterministic_across_calls():
    passport = load_passport()
    assert canonicalize_passport_payload(passport) == canonicalize_passport_payload(
        passport
    )


# 3. Top-level object key insertion order does not change canonical bytes.
def test_top_level_key_insertion_order_does_not_change_output():
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


# 4. Nested object key insertion order does not change canonical bytes.
def test_nested_key_insertion_order_does_not_change_output():
    ordered = {"outer": {"alpha": "one", "beta": "two", "gamma": {"x": "1", "y": "2"}}}
    reordered = {"outer": {"gamma": {"y": "2", "x": "1"}, "beta": "two", "alpha": "one"}}
    assert canonicalize_passport_payload(ordered) == canonicalize_passport_payload(
        reordered
    )


# 5. Canonical output is compact JSON with no unnecessary spaces or newlines.
def test_canonical_output_is_compact():
    data = {"b": "two", "a": "one", "nested": {"d": "four", "c": "three"}}
    output = canonicalize_passport_payload(data)
    assert output == b'{"a":"one","b":"two","nested":{"c":"three","d":"four"}}'
    assert b" " not in output
    assert b"\n" not in output
    assert b"\t" not in output


# 6. Canonical output is UTF-8 bytes.
def test_canonical_output_is_utf8_bytes():
    passport = load_passport()
    output = canonicalize_passport_payload(passport)
    # Valid UTF-8 that round-trips back to the same object.
    assert json.loads(output.decode("utf-8")) == passport
    # The current helper emits raw UTF-8 for non-ASCII (it does not \\u-escape).
    # For printable non-ASCII this coincides with JCS; the helper still makes no
    # JCS conformance claim. The real JCS divergences (control-character escaping
    # and non-ASCII key sort order) are not exercised here and do not occur in
    # the current ASCII-keyed profile.
    non_ascii_output = canonicalize_passport_payload({"subject": "Café"})
    assert isinstance(non_ascii_output, bytes)
    assert "Café".encode("utf-8") in non_ascii_output


# 7. hash_passport_payload hashes exactly the canonical bytes.
def test_hash_uses_exact_canonical_bytes():
    passport = load_passport()
    canonical = canonicalize_passport_payload(passport)
    for hash_alg, hashlib_name in (
        ("SHA-256", "sha256"),
        ("SHA-384", "sha384"),
        ("SHA-512", "sha512"),
    ):
        expected = hashlib.new(hashlib_name, canonical).hexdigest()
        assert hash_passport_payload(passport, hash_alg) == expected


# 8. Reordering top-level passport keys in the example does not change bytes.
def test_example_top_level_reorder_does_not_change_output():
    passport = load_passport()
    reordered = reverse_keys(passport)
    assert list(reordered.keys()) != list(passport.keys())  # genuinely reordered
    assert canonicalize_passport_payload(reordered) == canonicalize_passport_payload(
        passport
    )


# 9. Reordering nested passport objects in the example does not change bytes.
def test_example_nested_reorder_does_not_change_output():
    passport = load_passport()
    reordered = copy.deepcopy(passport)
    reordered["operator"] = reverse_keys(passport["operator"])
    reordered["public_keys"][0] = reverse_keys(passport["public_keys"][0])
    reordered["permissions"] = reverse_keys(passport["permissions"])
    assert canonicalize_passport_payload(reordered) == canonicalize_passport_payload(
        passport
    )


# 10. Proof data is not included in canonical passport payload bytes.
def test_proof_data_excluded_from_payload():
    envelope = load_envelope()
    output = canonicalize_passport_payload(envelope["passport"])
    proof = envelope["proofs"][0]
    assert b"proofs" not in output
    assert proof["proof_id"].encode("utf-8") not in output
    assert proof["proof_type"].encode("utf-8") not in output
    assert proof["proof_purpose"].encode("utf-8") not in output


# 11. signature_b64u is not included in canonical passport payload bytes.
def test_signature_b64u_excluded_from_payload():
    envelope = load_envelope()
    output = canonicalize_passport_payload(envelope["passport"])
    assert b"signature_b64u" not in output
    assert envelope["proofs"][0]["signature_b64u"].encode("utf-8") not in output


# 12. The signature input helper still matches canonicalize_passport_payload.
def test_signature_input_helper_matches_canonicalization():
    passport = load_passport()
    _, signature_input = passport_verifier_module._prepare_signature_input(passport)
    assert signature_input == canonicalize_passport_payload(passport)


# 13. The helper documents that it is not full RFC 8785/JCS (no overclaim).
def test_helper_documents_jcs_non_compliance():
    normalized = " ".join(CANON_SOURCE_PATH.read_text(encoding="utf-8").split())
    assert "RFC 8785" in normalized
    assert "not a complete independent RFC 8785" in normalized
    assert "must not be relied on for full JCS compliance" in normalized


# 14. No crypto/network imports are added to the verifier.
def test_passport_verifier_imports_no_crypto_or_network_modules():
    forbidden = (
        "hashlib", "hmac", "base64", "ssl", "secrets", "cryptography",
        "pqcrypto", "oqs", "requests", "httpx", "socket", "urllib",
    )
    for module_name in forbidden:
        assert not hasattr(passport_verifier_module, module_name), (
            f"passport_verifier must not import {module_name}"
        )
    source = PV_SOURCE_PATH.read_text(encoding="utf-8")
    for module_name in forbidden:
        assert f"import {module_name}" not in source
        assert f"from {module_name}" not in source


# 15. The lone boolean in the profile serializes as the JSON literal true.
def test_boolean_serializes_as_lowercase_true():
    assert canonicalize_passport_payload({"audit_required": True}) == (
        b'{"audit_required":true}'
    )


# 16. Array element order is significant: reordering array elements changes bytes.
def test_array_element_order_is_significant():
    # A simple string-array control (the profile uses no bare numbers).
    assert canonicalize_passport_payload(
        {"a": ["x", "y"]}
    ) != canonicalize_passport_payload({"a": ["y", "x"]})
    # The security-relevant case: reordering prohibited_actions must change the
    # canonical (and therefore signed) bytes so tampering is detectable.
    passport = load_passport()
    reordered = copy.deepcopy(passport)
    reordered["permissions"]["prohibited_actions"] = list(
        reversed(passport["permissions"]["prohibited_actions"])
    )
    assert canonicalize_passport_payload(
        reordered
    ) != canonicalize_passport_payload(passport)


# 17. Frozen golden vector: the example's canonical SHA-256 is pinned and equals
#     the recorded payload_hash, so silent canonical-form drift is caught.
def test_example_canonical_sha256_is_frozen_golden_vector():
    envelope = load_envelope()
    digest = hash_passport_payload(envelope["passport"], "SHA-256")
    assert digest == envelope["proofs"][0]["payload_hash"]
    assert digest == (
        "b85a7ddfefccb9582bf6ab23dac42a968cc0b6aabfc1d29d416ea25e27bfb6bc"
    )
