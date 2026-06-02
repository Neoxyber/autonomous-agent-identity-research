import ast
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = ROOT / "tests"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(TESTS))

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


def verif(decision, *, valid=None, reason="verification"):
    if valid is None:
        valid = decision == ALLOW
    return VerificationResult(valid=valid, decision=decision, reason=reason)


def authz(decision, reason="authorization"):
    return AuthorizationDecision(decision, reason)


@pytest.mark.parametrize(
    "verification, authorization, expected",
    [
        (verif(ALLOW), authz(ALLOW), ALLOW),
        (verif(ALLOW), authz(DENY), DENY),
        (verif(ALLOW), authz(REQUIRE_HUMAN_APPROVAL), REQUIRE_HUMAN_APPROVAL),
        (verif(ALLOW), authz(REQUIRE_HUMAN_REVIEW), REQUIRE_HUMAN_REVIEW),
        (verif(DENY), authz(ALLOW), DENY),
        (verif(REQUIRE_HUMAN_REVIEW), authz(ALLOW), REQUIRE_HUMAN_REVIEW),
        (verif(REQUIRE_HUMAN_APPROVAL), authz(ALLOW), REQUIRE_HUMAN_APPROVAL),
        (verif(DENY), authz(REQUIRE_HUMAN_APPROVAL), DENY),
    ],
)
def test_composition_precedence(verification, authorization, expected):
    assert compose_decision(verification, authorization).decision == expected


def test_defensive_clamp_invalid_allow():
    assert compose_decision(verif(ALLOW, valid=False), authz(ALLOW)).decision == DENY


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
        (None, authz(ALLOW)),
        (verif(ALLOW), None),
        ("x", authz(ALLOW)),
        (verif(ALLOW), "x"),
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
    result = compose_decision(verif(ALLOW), authz(ALLOW))
    assert result.reason
    assert result.checks
    assert all(isinstance(check, VerificationCheck) for check in result.checks)


def test_inputs_not_mutated():
    verification = verif(ALLOW)
    authorization = authz(ALLOW)
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
