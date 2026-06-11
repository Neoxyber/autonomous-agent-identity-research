import copy
import hashlib
import json
import re
from pathlib import Path

import pytest

from aaid.canonicalization import (
    canonicalize_passport_payload,
    hash_passport_payload,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"


def load_example_envelope() -> dict:
    with EXAMPLE_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def test_returns_bytes() -> None:
    envelope = load_example_envelope()
    result = canonicalize_passport_payload(envelope["passport"])

    assert isinstance(result, bytes)


def test_key_order_does_not_change_output() -> None:
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


def test_proofs_excluded_from_payload() -> None:
    envelope = load_example_envelope()
    result = canonicalize_passport_payload(envelope["passport"])

    assert b"proofs" not in result
    assert b"signature_b64u" not in result


def test_changing_a_proof_does_not_change_payload() -> None:
    envelope = load_example_envelope()
    before = canonicalize_passport_payload(envelope["passport"])

    mutated = copy.deepcopy(envelope)
    mutated["proofs"][0]["signature_b64u"] = "VGFtcGVyZWQtc2lnbmF0dXJl"
    after = canonicalize_passport_payload(mutated["passport"])

    assert before == after


def test_changing_the_passport_changes_output() -> None:
    envelope = load_example_envelope()
    before = canonicalize_passport_payload(envelope["passport"])

    mutated = copy.deepcopy(envelope)
    mutated["passport"]["subject"] = "A different subject"
    after = canonicalize_passport_payload(mutated["passport"])

    assert before != after


def test_sha256_hash_from_canonical_bytes() -> None:
    envelope = load_example_envelope()
    canonical = canonicalize_passport_payload(envelope["passport"])

    digest = hashlib.sha256(canonical).hexdigest()
    again = hashlib.sha256(
        canonicalize_passport_payload(envelope["passport"])
    ).hexdigest()

    assert re.fullmatch(r"[a-f0-9]{64}", digest)
    assert digest == again


@pytest.mark.parametrize(
    ("hash_algorithm", "expected_length"),
    [
        pytest.param("SHA-256", 64, id="sha-256"),
        pytest.param("SHA-384", 96, id="sha-384"),
        pytest.param("SHA-512", 128, id="sha-512"),
    ],
)
def test_hash_passport_payload_returns_lowercase_hex(
    hash_algorithm: str,
    expected_length: int,
) -> None:
    envelope = load_example_envelope()
    digest = hash_passport_payload(envelope["passport"], hash_algorithm)

    assert re.fullmatch(rf"[0-9a-f]{{{expected_length}}}", digest)


def test_hash_passport_payload_is_deterministic() -> None:
    envelope = load_example_envelope()

    first = hash_passport_payload(envelope["passport"])
    second = hash_passport_payload(envelope["passport"])

    assert first == second


def test_changing_a_proof_does_not_change_hash() -> None:
    envelope = load_example_envelope()
    before = hash_passport_payload(envelope["passport"])

    mutated = copy.deepcopy(envelope)
    mutated["proofs"][0]["signature_b64u"] = "VGFtcGVyZWQtc2lnbmF0dXJl"
    after = hash_passport_payload(mutated["passport"])

    assert before == after


def test_changing_the_passport_changes_hash() -> None:
    envelope = load_example_envelope()
    before = hash_passport_payload(envelope["passport"])

    mutated = copy.deepcopy(envelope)
    mutated["passport"]["subject"] = "A different subject"
    after = hash_passport_payload(mutated["passport"])

    assert before != after


@pytest.mark.parametrize(
    "unsupported_algorithm",
    [
        pytest.param("MD5", id="md5"),
        pytest.param("sha256", id="lowercase-sha256"),
        pytest.param("SHA3-256", id="sha3-256"),
    ],
)
def test_hash_passport_payload_rejects_unsupported_algorithm(
    unsupported_algorithm: str,
) -> None:
    envelope = load_example_envelope()

    with pytest.raises(ValueError):
        hash_passport_payload(envelope["passport"], unsupported_algorithm)


@pytest.mark.parametrize(
    ("hash_algorithm", "hashlib_name"),
    [
        pytest.param("SHA-256", "sha256", id="sha-256"),
        pytest.param("SHA-384", "sha384", id="sha-384"),
        pytest.param("SHA-512", "sha512", id="sha-512"),
    ],
)
def test_hash_passport_payload_matches_hashlib_on_canonical_bytes(
    hash_algorithm: str,
    hashlib_name: str,
) -> None:
    envelope = load_example_envelope()
    canonical = canonicalize_passport_payload(envelope["passport"])

    expected = hashlib.new(hashlib_name, canonical).hexdigest()

    assert hash_passport_payload(envelope["passport"], hash_algorithm) == expected
