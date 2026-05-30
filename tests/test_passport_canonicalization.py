import copy
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aaid.canonicalization import canonicalize_passport_payload

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
