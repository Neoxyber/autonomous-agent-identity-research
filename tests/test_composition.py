import ast
import copy
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

from _support import FRESH_STATUS, TRUSTED_ISSUERS, VALID_NOW
from aaid import composition
from aaid.authorization import AuthorizationDecision, authorize_action
from aaid.composition import ComposedDecision, compose_decision
from aaid.passport_verifier import verify_passport_envelope
from aaid.verification import (
    ALLOW,
    DENY,
    REQUIRE_HUMAN_APPROVAL,
    REQUIRE_HUMAN_REVIEW,
    VerificationCheck,
    VerificationResult,
)

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"


def make_verification_result(decision, *, valid=None, reason="verification"):
    if valid is None:
        valid = decision == ALLOW
    return VerificationResult(valid=valid, decision=decision, reason=reason)


def make_authorization_decision(decision, reason="authorization"):
    return AuthorizationDecision(decision, reason)


@pytest.mark.parametrize(
    "verification, authorization, expected",
    [
        (
            make_verification_result(ALLOW),
            make_authorization_decision(ALLOW),
            ALLOW,
        ),
        (
            make_verification_result(ALLOW),
            make_authorization_decision(DENY),
            DENY,
        ),
        (
            make_verification_result(ALLOW),
            make_authorization_decision(REQUIRE_HUMAN_APPROVAL),
            REQUIRE_HUMAN_APPROVAL,
        ),
        (
            make_verification_result(ALLOW),
            make_authorization_decision(REQUIRE_HUMAN_REVIEW),
            REQUIRE_HUMAN_REVIEW,
        ),
        (
            make_verification_result(DENY),
            make_authorization_decision(ALLOW),
            DENY,
        ),
        (
            make_verification_result(REQUIRE_HUMAN_REVIEW),
            make_authorization_decision(ALLOW),
            REQUIRE_HUMAN_REVIEW,
        ),
        (
            make_verification_result(REQUIRE_HUMAN_APPROVAL),
            make_authorization_decision(ALLOW),
            REQUIRE_HUMAN_APPROVAL,
        ),
        (
            make_verification_result(DENY),
            make_authorization_decision(REQUIRE_HUMAN_APPROVAL),
            DENY,
        ),
    ],
)
def test_composition_precedence(verification, authorization, expected):
    assert compose_decision(verification, authorization).decision == expected


def test_defensive_clamp_invalid_allow():
    assert (
        compose_decision(
            make_verification_result(ALLOW, valid=False),
            make_authorization_decision(ALLOW),
        ).decision
        == DENY
    )


def test_real_integration_boundary():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        envelope = json.load(handle)
    verification = verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    authorization = authorize_action(
        envelope["passport"],
        {"action": "summarize_public_text", "resource_scope": "demo.public_text"},
    )
    assert verification.decision == DENY
    assert authorization.decision == ALLOW
    assert compose_decision(verification, authorization).decision == DENY


@pytest.mark.parametrize(
    "verification, authorization",
    [
        (None, make_authorization_decision(ALLOW)),
        (make_verification_result(ALLOW), None),
        ("x", make_authorization_decision(ALLOW)),
        (make_verification_result(ALLOW), "x"),
        (123, 456),
        (object(), object()),
    ],
)
def test_malformed_inputs_fail_closed(verification, authorization):
    assert compose_decision(verification, authorization).decision == DENY


def test_composed_decision_rejects_unknown_value():
    with pytest.raises(ValueError):
        ComposedDecision(decision="MAYBE", reason="x")


def test_result_is_explainable():
    result = compose_decision(make_verification_result(ALLOW), make_authorization_decision(ALLOW))
    assert result.reason
    assert result.checks
    assert all(isinstance(check, VerificationCheck) for check in result.checks)


def test_inputs_not_mutated():
    verification = make_verification_result(ALLOW)
    authorization = make_authorization_decision(ALLOW)
    verification_snapshot = copy.deepcopy(verification)
    authorization_snapshot = copy.deepcopy(authorization)
    compose_decision(verification, authorization)
    assert verification == verification_snapshot
    assert authorization == authorization_snapshot


FORBIDDEN_IMPORTS = {
    "hashlib",
    "hmac",
    "secrets",
    "cryptography",
    "ssl",
    "socket",
    "urllib",
    "http",
    "requests",
    "subprocess",
    "rfc8785",
    "jcs",
    "sigstore",
    "cosign",
    "rekor",
    "fulcio",
    "passport_verifier",
}


def test_no_forbidden_imports():
    tree = ast.parse(Path(composition.__file__).read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.update(alias.name.split("."))
        elif isinstance(node, ast.ImportFrom):
            imported.update((node.module or "").split("."))
    assert not (imported & FORBIDDEN_IMPORTS), imported & FORBIDDEN_IMPORTS
