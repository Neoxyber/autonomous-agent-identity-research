"""Tests for the signature abstraction verifier boundary.

These cases keep signature handling at the explicit not-implemented verifier
boundary while preserving earlier structural, schema, proof-selection, and
payload-hash short-circuit behavior.

A signature-stage result does not grant `ALLOW`. More research and testing are
needed before real signature verification can be added.
"""

import json
from pathlib import Path
from typing import Any

import aaid.passport_verifier as passport_verifier_module
from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import ALLOW, DENY, verify_passport_envelope
from aaid.verification import VerificationCheck, VerificationResult

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
PASSPORT_VERIFIER_SOURCE_PATH = ROOT / "src" / "aaid" / "passport_verifier.py"

SCHEMA_CHECK = "schema_valid"
PROOF_SELECTED_CHECK = "proof_selected"
PAYLOAD_HASH_CHECK = "payload_hash_valid"
SIGNATURE_CHECK = "signature_verification_not_implemented"
ENVELOPE_IS_MAPPING_CHECK = "envelope_is_mapping"

FORBIDDEN_CRYPTO_OR_NETWORK_IMPORTS = (
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


def load_example_envelope() -> dict[str, Any]:
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def find_check(
    result: VerificationResult,
    name: str,
) -> VerificationCheck | None:
    for check in result.checks:
        if check.name == name:
            return check
    return None


def find_check_index(result: VerificationResult, name: str) -> int:
    for index, check in enumerate(result.checks):
        if check.name == name:
            return index
    return -1


def verify_with_trusted_context(envelope: Any) -> VerificationResult:
    return verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )


def assert_check_passed(result: VerificationResult, name: str) -> None:
    check = find_check(result, name)

    assert check is not None
    assert check.passed is True


def assert_check_failed(result: VerificationResult, name: str) -> None:
    check = find_check(result, name)

    assert check is not None
    assert check.passed is False


def make_envelope_with_broken_payload_hash() -> dict[str, Any]:
    envelope = load_example_envelope()
    envelope["proofs"][0]["payload_hash"] = "0" * 64
    return envelope


def make_envelope_with_changed_signature() -> dict[str, Any]:
    # signature_b64u is base64url metadata in the proof, not part of the signed
    # payload, so a same-length, same-charset edit stays schema-valid and leaves
    # the payload hash valid.
    envelope = load_example_envelope()
    original = envelope["proofs"][0]["signature_b64u"]
    replacement = "k" if original[-1] != "k" else "j"

    envelope["proofs"][0]["signature_b64u"] = original[:-1] + replacement

    return envelope


def test_valid_envelope_reaches_signature_verification_not_implemented() -> None:
    result = verify_with_trusted_context(load_example_envelope())

    assert_check_passed(result, SCHEMA_CHECK)
    assert_check_passed(result, PROOF_SELECTED_CHECK)
    assert_check_passed(result, PAYLOAD_HASH_CHECK)
    assert find_check(result, SIGNATURE_CHECK) is not None


def test_signature_check_recorded_after_payload_hash_valid() -> None:
    result = verify_with_trusted_context(load_example_envelope())

    payload_index = find_check_index(result, PAYLOAD_HASH_CHECK)
    signature_index = find_check_index(result, SIGNATURE_CHECK)

    assert payload_index != -1
    assert signature_index != -1
    assert payload_index < signature_index


def test_signature_check_is_failed_not_passed() -> None:
    result = verify_with_trusted_context(load_example_envelope())

    assert_check_failed(result, SIGNATURE_CHECK)


def test_valid_envelope_final_result_is_invalid_and_denied() -> None:
    result = verify_with_trusted_context(load_example_envelope())

    assert result.valid is False
    assert result.decision == DENY


def test_signature_abstraction_step_never_returns_allow() -> None:
    cases = [
        load_example_envelope(),
        make_envelope_with_broken_payload_hash(),
        make_envelope_with_changed_signature(),
        ["not", "a", "mapping"],
        {"passport": {"subject": "demo"}, "proofs": []},
        {"passport": {"subject": "demo"}, "proofs": [{"proof_id": "x"}]},
        {},
        None,
    ]

    # Reach the named step for the valid, trusted example so this sweep actually
    # exercises signature_verification_not_implemented rather than stopping at
    # issuer_trusted.
    reached = verify_with_trusted_context(load_example_envelope())

    assert find_check(reached, SIGNATURE_CHECK) is not None

    for case in cases:
        result = verify_with_trusted_context(case)

        assert isinstance(result, VerificationResult)
        assert result.decision != ALLOW
        assert result.valid is False


def test_payload_hash_failure_short_circuits_before_signature() -> None:
    result = verify_with_trusted_context(make_envelope_with_broken_payload_hash())

    assert_check_failed(result, PAYLOAD_HASH_CHECK)
    assert find_check(result, SIGNATURE_CHECK) is None
    assert result.decision == DENY


def test_schema_failure_short_circuits_before_signature() -> None:
    envelope = load_example_envelope()

    # Proof objects set additionalProperties: false, so an unknown key fails
    # schema validation while leaving the envelope structurally intact.
    envelope["proofs"][0]["unexpected_field"] = "x"

    result = verify_passport_envelope(envelope)

    assert_check_failed(result, SCHEMA_CHECK)
    assert find_check(result, PROOF_SELECTED_CHECK) is None
    assert find_check(result, PAYLOAD_HASH_CHECK) is None
    assert find_check(result, SIGNATURE_CHECK) is None


def test_structural_failure_short_circuits_before_signature() -> None:
    result = verify_passport_envelope(["passport", "proofs"])

    assert_check_failed(result, ENVELOPE_IS_MAPPING_CHECK)
    assert find_check(result, SCHEMA_CHECK) is None
    assert find_check(result, SIGNATURE_CHECK) is None


def test_changing_signature_b64u_does_not_allow() -> None:
    result = verify_with_trusted_context(make_envelope_with_changed_signature())

    assert_check_passed(result, PAYLOAD_HASH_CHECK)
    assert_check_failed(result, SIGNATURE_CHECK)
    assert result.decision == DENY
    assert result.valid is False


def test_no_public_signing_or_verification_callable_beyond_api() -> None:
    public_callables = [
        name
        for name in dir(passport_verifier_module)
        if not name.startswith("_")
        and callable(getattr(passport_verifier_module, name))
    ]

    for name in public_callables:
        assert "sign" not in name.lower(), (
            f"unexpected signing-like public callable: {name}"
        )

    verify_like = [name for name in public_callables if "verify" in name.lower()]

    assert verify_like == ["verify_passport_envelope", "verify_passport_json"]


def test_passport_verifier_imports_no_crypto_or_network_modules() -> None:
    for module_name in FORBIDDEN_CRYPTO_OR_NETWORK_IMPORTS:
        assert not hasattr(passport_verifier_module, module_name), (
            f"passport_verifier must not import {module_name}"
        )

    source = PASSPORT_VERIFIER_SOURCE_PATH.read_text(encoding="utf-8")

    for module_name in FORBIDDEN_CRYPTO_OR_NETWORK_IMPORTS:
        assert f"import {module_name}" not in source
        assert f"from {module_name}" not in source


def test_signature_helper_exists_and_returns_failed_named_check() -> None:
    helper = passport_verifier_module._signature_verification_not_implemented_check
    envelope = load_example_envelope()

    check = helper(envelope["passport"], envelope["proofs"][0])

    assert isinstance(check, VerificationCheck)
    assert check.name == SIGNATURE_CHECK
    assert check.passed is False
    assert isinstance(check.reason, str) and check.reason.strip()


def test_signature_helper_fails_closed_regardless_of_arguments() -> None:
    helper = passport_verifier_module._signature_verification_not_implemented_check
    samples = [
        ({"a": 1}, {"b": 2}),
        ({}, {}),
        (load_example_envelope()["passport"], {}),
    ]

    for passport, proof in samples:
        check = helper(passport, proof)

        assert check.name == SIGNATURE_CHECK
        assert check.passed is False
