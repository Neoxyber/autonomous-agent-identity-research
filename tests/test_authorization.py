import ast
import copy
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

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
ACTION_ENTRY = {"action": "do_thing", "resource_scope": "scope.a"}


def make_action_entry(action, resource_scope):
    return {"action": action, "resource_scope": resource_scope}


def make_passport_with_permissions(*, allowed=(), approval=(), prohibited=()):
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
        pytest.param(
            make_passport_with_permissions(allowed=[ACTION_ENTRY]),
            ALLOW,
            id="allowed-action",
        ),
        pytest.param(
            make_passport_with_permissions(approval=[ACTION_ENTRY]),
            REQUIRE_HUMAN_APPROVAL,
            id="approval-required-action",
        ),
        pytest.param(
            make_passport_with_permissions(prohibited=[ACTION_ENTRY]),
            DENY,
            id="prohibited-action",
        ),
        pytest.param(
            make_passport_with_permissions(
                allowed=[make_action_entry("other", "scope.a")]
            ),
            DENY,
            id="different-action",
        ),
        pytest.param(
            make_passport_with_permissions(
                allowed=[ACTION_ENTRY],
                prohibited=[ACTION_ENTRY],
            ),
            DENY,
            id="prohibited-over-allowed",
        ),
        pytest.param(
            make_passport_with_permissions(
                allowed=[ACTION_ENTRY],
                approval=[ACTION_ENTRY],
            ),
            REQUIRE_HUMAN_APPROVAL,
            id="approval-over-allowed",
        ),
        pytest.param(
            make_passport_with_permissions(
                approval=[ACTION_ENTRY],
                prohibited=[ACTION_ENTRY],
            ),
            DENY,
            id="prohibited-over-approval",
        ),
    ],
)
def test_decision_precedence(passport, expected):
    assert authorize_action(passport, dict(ACTION_ENTRY)).decision == expected


def test_unknown_action_review_policy():
    passport = make_passport_with_permissions(
        allowed=[make_action_entry("other", "scope.a")]
    )
    decision = authorize_action(
        passport,
        dict(ACTION_ENTRY),
        unknown_action=REQUIRE_HUMAN_REVIEW,
    )
    assert decision.decision == REQUIRE_HUMAN_REVIEW


@pytest.mark.parametrize(
    "request_arg",
    [
        pytest.param(
            make_action_entry("do_thing", "scope.b"),
            id="resource-scope-mismatch",
        ),
        pytest.param(
            make_action_entry("Do_Thing", "scope.a"),
            id="action-case-mismatch",
        ),
    ],
)
def test_exact_action_scope_match_required(request_arg):
    decision = authorize_action(
        make_passport_with_permissions(allowed=[ACTION_ENTRY]),
        request_arg,
    )
    assert decision.decision == DENY


@pytest.mark.parametrize(
    "bad_request",
    [
        None,
        "do_thing",
        {},
        {"action": "do_thing"},
        {"action": 1, "resource_scope": "scope.a"},
    ],
)
def test_malformed_request_fails_closed(bad_request):
    decision = authorize_action(
        make_passport_with_permissions(allowed=[ACTION_ENTRY]),
        bad_request,
    )
    assert decision.decision == DENY


@pytest.mark.parametrize(
    "bad_passport",
    [
        None,
        {},
        {"permissions": "x"},
        {"permissions": {"approval_required_actions": [], "prohibited_actions": []}},
        {
            "permissions": {
                "allowed_actions": "x",
                "approval_required_actions": [],
                "prohibited_actions": [],
            }
        },
        {
            "permissions": {
                "allowed_actions": [],
                "approval_required_actions": [],
                "prohibited_actions": [],
            }
        },
        {
            "permissions": {
                "allowed_actions": [ACTION_ENTRY],
                "approval_required_actions": [],
                "prohibited_actions": [],
                "default_decision": "ALLOW",
            }
        },
    ],
)
def test_malformed_permissions_fails_closed(bad_passport):
    assert authorize_action(bad_passport, dict(ACTION_ENTRY)).decision == DENY


def test_unsupported_unknown_action_policy_fails_closed():
    decision = authorize_action(
        make_passport_with_permissions(allowed=[ACTION_ENTRY]),
        dict(ACTION_ENTRY),
        unknown_action="MAYBE",
    )
    assert decision.decision == DENY


def test_decision_rejects_unknown_value():
    with pytest.raises(ValueError):
        AuthorizationDecision(decision="MAYBE", reason="x")


def test_result_is_explainable():
    decision = authorize_action(
        make_passport_with_permissions(allowed=[ACTION_ENTRY]),
        dict(ACTION_ENTRY),
    )
    assert decision.reason
    assert decision.checks
    assert all(isinstance(check, VerificationCheck) for check in decision.checks)


def test_inputs_not_mutated():
    passport = make_passport_with_permissions(
        allowed=[ACTION_ENTRY],
        prohibited=[make_action_entry("c", "d")],
    )
    request = dict(ACTION_ENTRY)
    passport_snapshot = copy.deepcopy(passport)
    request_snapshot = copy.deepcopy(request)
    authorize_action(passport, request)
    assert passport == passport_snapshot
    assert request == request_snapshot


def test_authorization_allows_while_verifier_denies():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        envelope = json.load(handle)

    verification_result = verify_passport_envelope(
        envelope,
        now=VALID_NOW,
        trusted_issuers=TRUSTED_ISSUERS,
        revocation_status=FRESH_STATUS,
    )
    authorization_decision = authorize_action(
        envelope["passport"],
        {"action": "summarize_public_text", "resource_scope": "demo.public_text"},
    )

    assert verification_result.decision == DENY
    assert authorization_decision.decision == ALLOW


FORBIDDEN_IMPORTS = {
    "cosign",
    "cryptography",
    "fulcio",
    "hashlib",
    "hmac",
    "http",
    "jcs",
    "passport_verifier",
    "requests",
    "rekor",
    "rfc8785",
    "secrets",
    "sigstore",
    "socket",
    "ssl",
    "subprocess",
    "urllib",
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
