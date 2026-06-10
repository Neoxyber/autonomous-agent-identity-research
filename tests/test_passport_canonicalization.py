import copy
import hashlib
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

from aaid.canonicalization import (
    canonicalize_passport_payload,
    hash_passport_payload,
)

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"


def load_envelope():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_returns_bytes():
    envelope = load_envelope()
    result = canonicalize_passport_payload(envelope["passport"])
    assert isinstance(result, bytes)


def test_key_order_does_not_change_output():
    ordered = {
        "agent_id": "urn:aaid:agent:demo",
        "subject": "Demo",
        "nested": {"alpha": "one", "beta": "two"},
    }
    reordered = {
        "nested": {"beta": "two", "alpha": "one"},
        "subject": "Demo",
        "agent_id": "urn:aaid:agent:demo",
    }
    assert canonicalize_passport_payload(ordered) == canonicalize_passport_payload(
        reordered
    )


def test_proofs_excluded_from_payload():
    envelope = load_envelope()
    result = canonicalize_passport_payload(envelope["passport"])
    assert b"proofs" not in result
    assert b"signature_b64u" not in result


def test_changing_a_proof_does_not_change_payload():
    envelope = load_envelope()
    before = canonicalize_passport_payload(envelope["passport"])

    mutated = copy.deepcopy(envelope)
    mutated["proofs"][0]["signature_b64u"] = "VGFtcGVyZWQtc2lnbmF0dXJl"
    after = canonicalize_passport_payload(mutated["passport"])

    assert before == after


def test_changing_the_passport_changes_output():
    envelope = load_envelope()
    before = canonicalize_passport_payload(envelope["passport"])

    mutated = copy.deepcopy(envelope)
    mutated["passport"]["subject"] = "A different subject"
    after = canonicalize_passport_payload(mutated["passport"])

    assert before != after


def test_sha256_hash_from_canonical_bytes():
    envelope = load_envelope()
    canonical = canonicalize_passport_payload(envelope["passport"])

    digest = hashlib.sha256(canonical).hexdigest()
    again = hashlib.sha256(
        canonicalize_passport_payload(envelope["passport"])
    ).hexdigest()

    assert re.fullmatch(r"[a-f0-9]{64}", digest)
    assert digest == again


def test_hash_passport_payload_sha256_is_64_lowercase_hex():
    envelope = load_envelope()
    digest = hash_passport_payload(envelope["passport"], "SHA-256")
    assert re.fullmatch(r"[0-9a-f]{64}", digest)


def test_hash_passport_payload_sha384_is_96_lowercase_hex():
    envelope = load_envelope()
    digest = hash_passport_payload(envelope["passport"], "SHA-384")
    assert re.fullmatch(r"[0-9a-f]{96}", digest)


def test_hash_passport_payload_sha512_is_128_lowercase_hex():
    envelope = load_envelope()
    digest = hash_passport_payload(envelope["passport"], "SHA-512")
    assert re.fullmatch(r"[0-9a-f]{128}", digest)


def test_hash_passport_payload_is_deterministic():
    envelope = load_envelope()
    first = hash_passport_payload(envelope["passport"])
    second = hash_passport_payload(envelope["passport"])
    assert first == second


def test_changing_a_proof_does_not_change_hash():
    envelope = load_envelope()
    before = hash_passport_payload(envelope["passport"])

    mutated = copy.deepcopy(envelope)
    mutated["proofs"][0]["signature_b64u"] = "VGFtcGVyZWQtc2lnbmF0dXJl"
    after = hash_passport_payload(mutated["passport"])

    assert before == after


def test_changing_the_passport_changes_hash():
    envelope = load_envelope()
    before = hash_passport_payload(envelope["passport"])

    mutated = copy.deepcopy(envelope)
    mutated["passport"]["subject"] = "A different subject"
    after = hash_passport_payload(mutated["passport"])

    assert before != after


def test_hash_passport_payload_rejects_unsupported_algorithm():
    envelope = load_envelope()
    for unsupported in ("MD5", "sha256", "SHA3-256"):
        with pytest.raises(ValueError):
            hash_passport_payload(envelope["passport"], unsupported)


def test_hash_passport_payload_matches_hashlib_on_canonical_bytes():
    envelope = load_envelope()
    canonical = canonicalize_passport_payload(envelope["passport"])
    cases = {"SHA-256": "sha256", "SHA-384": "sha384", "SHA-512": "sha512"}
    for hash_alg, hashlib_name in cases.items():
        expected = hashlib.new(hashlib_name, canonical).hexdigest()
        assert hash_passport_payload(envelope["passport"], hash_alg) == expected
