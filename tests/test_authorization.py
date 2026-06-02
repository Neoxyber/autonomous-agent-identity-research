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
from aaid import authorization
from aaid.authorization import AuthorizationDecision, authorize_action
from aaid.passport_verifier import verify_passport_envelope
from aaid.verification import (
    ALLOW,
    DENY,
    REQUIRE_HUMAN_APPROVAL,
    REQUIRE_HUMAN_REVIEW,
    VerificationCheck,
)

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
ACT = {"action": "do_thing", "resource_scope": "scope.a"}


def scope(action, resource_scope):
    return {"action": action, "resource_scope": resource_scope}


def passport_with(*, allowed=(), approval=(), prohibited=()):
    return {
        "permissions": {
            "allowed_actions": list(allowed),
            "approval_required_actions": list(approval),
            "prohibited_actions": list(prohibited),
            "default_decision": "DENY",
        }
    }


@pytest.mark.parametrize(
    "passport, expected",
    [
        (passport_with(allowed=[ACT]), ALLOW),
        (passport_with(approval=[ACT]), REQUIRE_HUMAN_APPROVAL),
        (passport_with(prohibited=[ACT]), DENY),
        (passport_with(allowed=[scope("other", "scope.a")]), DENY),
        (passport_with(allowed=[ACT], prohibited=[ACT]), DENY),
        (passport_with(allowed=[ACT], approval=[ACT]), REQUIRE_HUMAN_APPROVAL),
        (passport_with(approval=[ACT], prohibited=[ACT]), DENY),
    ],
)
def test_decision_precedence(passport, expected):
    assert authorize_action(passport, dict(ACT)).decision == expected


def test_unknown_action_review_policy():
    passport = passport_with(allowed=[scope("other", "scope.a")])
    decision = authorize_action(passport, dict(ACT), unknown_action=REQUIRE_HUMAN_REVIEW)
    assert decision.decision == REQUIRE_HUMAN_REVIEW


@pytest.mark.parametrize(
    "request_arg",
    [scope("do_thing", "scope.b"), scope("Do_Thing", "scope.a")],
)
def test_exact_action_scope_match_required(request_arg):
    assert authorize_action(passport_with(allowed=[ACT]), request_arg).decision == DENY


@pytest.mark.parametrize(
    "bad_request",
    [None, "do_thing", {}, {"action": "do_thing"}, {"action": 1, "resource_scope": "scope.a"}],
)
def test_malformed_request_fails_closed(bad_request):
    assert authorize_action(passport_with(allowed=[ACT]), bad_request).decision == DENY


@pytest.mark.parametrize(
    "bad_passport",
    [
        None,
        {},
        {"permissions": "x"},
        {"permissions": {"approval_required_actions": [], "prohibited_actions": []}},
        {"permissions": {"allowed_actions": "x", "approval_required_actions": [], "prohibited_actions": []}},
        {"permissions": {"allowed_actions": [], "approval_required_actions": [], "prohibited_actions": []}},
        {"permissions": {"allowed_actions": [ACT], "approval_required_actions": [], "prohibited_actions": [], "default_decision": "ALLOW"}},
    ],
)
def test_malformed_permissions_fails_closed(bad_passport):
    assert authorize_action(bad_passport, dict(ACT)).decision == DENY


def test_unsupported_unknown_action_policy_fails_closed():
    decision = authorize_action(passport_with(allowed=[ACT]), dict(ACT), unknown_action="MAYBE")
    assert decision.decision == DENY


def test_decision_rejects_unknown_value():
    with pytest.raises(ValueError):
        AuthorizationDecision(decision="MAYBE", reason="x")


def test_result_is_explainable():
    decision = authorize_action(passport_with(allowed=[ACT]), dict(ACT))
    assert decision.reason
    assert decision.checks
    assert all(isinstance(check, VerificationCheck) for check in decision.checks)


def test_inputs_not_mutated():
    passport = passport_with(allowed=[ACT], prohibited=[scope("c", "d")])
    request = dict(ACT)
    passport_snapshot = copy.deepcopy(passport)
    request_snapshot = copy.deepcopy(request)
    authorize_action(passport, request)
    assert passport == passport_snapshot
    assert request == request_snapshot


def test_authorization_allows_while_verifier_denies():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        envelope = json.load(handle)
    verifier = verify_passport_envelope(
        envelope, now=VALID_NOW, trusted_issuers=TRUSTED_ISSUERS, revocation_status=FRESH_STATUS
    )
    authz = authorize_action(
        envelope["passport"],
        {"action": "summarize_public_text", "resource_scope": "demo.public_text"},
    )
    assert verifier.decision == DENY
    assert authz.decision == ALLOW


FORBIDDEN_IMPORTS = {
    "hashlib", "hmac", "secrets", "cryptography", "ssl", "socket", "urllib",
    "http", "requests", "subprocess", "rfc8785", "jcs", "sigstore", "cosign",
    "rekor", "fulcio", "passport_verifier",
}


def test_no_forbidden_imports():
    tree = ast.parse(Path(authorization.__file__).read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.update(alias.name.split("."))
        elif isinstance(node, ast.ImportFrom):
            imported.update((node.module or "").split("."))
    assert not (imported & FORBIDDEN_IMPORTS), imported & FORBIDDEN_IMPORTS
