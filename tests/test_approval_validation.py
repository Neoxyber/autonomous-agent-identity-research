import ast
import copy
import dataclasses
import json
import sys
from collections.abc import Mapping
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aaid import approval_validation, authorization, composition, verification
from aaid.approval import prepare_approval_evidence
from aaid.approval_validation import ApprovalValidation, validate_approval
from aaid.audit import ERROR, prepare_audit_event
from aaid.verification import VerificationCheck

ALLOW = verification.ALLOW
DENY = verification.DENY
REQUIRE_HUMAN_APPROVAL = verification.REQUIRE_HUMAN_APPROVAL
REQUIRE_HUMAN_REVIEW = verification.REQUIRE_HUMAN_REVIEW
VerificationResult = verification.VerificationResult
AuthorizationDecision = authorization.AuthorizationDecision
ComposedDecision = composition.ComposedDecision

EXAMPLE_PATH = ROOT / "specs" / "examples" / "agent-passport.minimal.json"
REQUEST = {"action": "summarize_public_text", "resource_scope": "demo.public_text"}
APPROVAL = {
    "approver_id": "urn:aaid:approver:reviewer-1",
    "approver_role": "operator_admin",
    "approval_outcome": "approved",
    "approval_reason": "reviewed in research demo",
    "approval_scope": "demo.public_text",
    "approval_expires_at": "2026-06-03T01:00:00Z",
}
PLANTED_SECRETS = ["SIGSECRET", "TOKENSECRET", "MFASECRET", "DOCSECRET", "BIOSECRET"]
SECRET_APPROVAL = {
    **APPROVAL,
    "approval_signature": "SIGSECRET",
    "approver_token": "TOKENSECRET",
    "mfa_code": "MFASECRET",
    "justification_document": "DOCSECRET",
    "biometric": "BIOSECRET",
}
SENSITIVE_VALUES = [
    "VGhpcy1pcy1hLWRlbW8tcHVibGljLWtleQ",
    "VGhpcy1pcy1hLWRlbW8tc2lnbmF0dXJl",
    "b85a7ddfefccb9582bf6ab23dac42a968cc0b6aabfc1d29d416ea25e27bfb6bc",
    "urn:aaid:key:018fd7c2-8c44-72ff-91ab-2e81e9fd4422",
    "urn:aaid:proof:018fd7c2-a110-70ac-81d0-f934ed842010",
]
BOUND_FIELDS = [
    "passport_id",
    "agent_id",
    "operator_id",
    "issuer_id",
    "requested_action",
    "resource_scope",
    "authorization_decision",
    "composed_decision",
]


def load_passport():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)["passport"]


def make_audit(decision=REQUIRE_HUMAN_APPROVAL, *, passport=None):
    comp = None if decision == ERROR else ComposedDecision(decision, "composed")
    return prepare_audit_event(
        passport=load_passport() if passport is None else passport,
        request=REQUEST,
        verification=VerificationResult(valid=False, decision=DENY, reason="v"),
        authorization=AuthorizationDecision(REQUIRE_HUMAN_APPROVAL, "a"),
        composition=comp,
        event_type="action_decision",
        occurred_at="2026-06-03T00:00:00Z",
    )


def pair(decision=REQUIRE_HUMAN_APPROVAL, *, passport=None):
    audit_event = make_audit(decision, passport=passport)
    return audit_event, prepare_approval_evidence(
        audit_event=audit_event,
        approval=APPROVAL,
    )


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, Mapping):
        for value in obj.values():
            yield from strings(value)
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            yield from strings(value)


def validation_text(result):
    return "\n".join(strings(dataclasses.asdict(result)))


def booleans(result):
    return (
        result.valid,
        result.matches_context,
        result.applicable,
        result.grants_execution,
    )


def test_valid_match_for_require_human_approval():
    audit_event, evidence = pair()
    result = validate_approval(audit_event=audit_event, approval_evidence=evidence)
    assert booleans(result) == (True, True, True, False)


def test_grants_execution_always_false():
    audit_event, evidence = pair()
    deny_audit, deny_evidence = pair(DENY)
    results = [
        validate_approval(audit_event=audit_event, approval_evidence=evidence),
        validate_approval(
            audit_event=audit_event,
            approval_evidence=dataclasses.replace(evidence, passport_id="X"),
        ),
        validate_approval(audit_event=None, approval_evidence=evidence),
        validate_approval(audit_event=deny_audit, approval_evidence=deny_evidence),
    ]
    assert all(result.grants_execution is False for result in results)


@pytest.mark.parametrize("field", BOUND_FIELDS)
def test_context_mismatch_fails(field):
    audit_event, evidence = pair()
    tampered = dataclasses.replace(evidence, **{field: "DIFFERENT-VALUE"})
    result = validate_approval(audit_event=audit_event, approval_evidence=tampered)
    assert result.matches_context is False
    assert result.valid is False
    failed = next(c for c in result.checks if c.name == f"context_bound_{field}")
    assert failed.passed is False


@pytest.mark.parametrize("decision", [DENY, ERROR, ALLOW, REQUIRE_HUMAN_REVIEW])
def test_non_approval_decisions_not_applicable(decision):
    audit_event, evidence = pair(decision)
    result = validate_approval(audit_event=audit_event, approval_evidence=evidence)
    assert result.applicable is False
    assert result.valid is False
    assert result.grants_execution is False


def test_allow_context_non_executing():
    audit_event, evidence = pair(ALLOW)
    result = validate_approval(audit_event=audit_event, approval_evidence=evidence)
    assert result.valid is False
    assert result.grants_execution is False


def test_two_none_values_do_not_match():
    audit_event, evidence = pair(passport={})
    result = validate_approval(audit_event=audit_event, approval_evidence=evidence)
    check = next(c for c in result.checks if c.name == "context_bound_passport_id")
    assert check.passed is False
    assert result.matches_context is False


@pytest.mark.parametrize("bad", [None, "x", 123, object(), {}])
def test_malformed_audit_event(bad):
    _, evidence = pair()
    result = validate_approval(audit_event=bad, approval_evidence=evidence)
    assert booleans(result) == (False, False, False, False)


@pytest.mark.parametrize("bad", [None, "x", 123, object(), {}])
def test_malformed_approval_evidence(bad):
    audit_event, _ = pair()
    result = validate_approval(audit_event=audit_event, approval_evidence=bad)
    assert booleans(result) == (False, False, False, False)


def test_expiry_is_ignored():
    audit_event, evidence = pair()
    past = dataclasses.replace(evidence, approval_expires_at="2000-01-01T00:00:00Z")
    future = dataclasses.replace(evidence, approval_expires_at="2999-01-01T00:00:00Z")
    a = validate_approval(audit_event=audit_event, approval_evidence=past)
    b = validate_approval(audit_event=audit_event, approval_evidence=future)
    assert a == b
    assert a.valid is True


def test_reason_non_empty():
    audit_event, evidence = pair()
    assert validate_approval(audit_event=audit_event, approval_evidence=evidence).reason


def test_checks_ordered_and_typed():
    audit_event, evidence = pair()
    checks = validate_approval(audit_event=audit_event, approval_evidence=evidence).checks
    assert [c.name for c in checks] == [
        "context_bound_passport_id",
        "context_bound_agent_id",
        "context_bound_operator_id",
        "context_bound_issuer_id",
        "context_bound_requested_action",
        "context_bound_resource_scope",
        "context_bound_authorization_decision",
        "context_bound_composed_decision",
        "applicable_require_human_approval",
    ]
    assert all(isinstance(c, VerificationCheck) for c in checks)


def test_inputs_not_mutated():
    audit_event, evidence = pair()
    snapshots = copy.deepcopy((audit_event, evidence))
    validate_approval(audit_event=audit_event, approval_evidence=evidence)
    assert (audit_event, evidence) == snapshots


def test_validation_is_frozen():
    audit_event, evidence = pair()
    result = validate_approval(audit_event=audit_event, approval_evidence=evidence)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.valid = False


def test_deterministic():
    audit_event, evidence = pair()
    a = validate_approval(audit_event=audit_event, approval_evidence=evidence)
    b = validate_approval(audit_event=audit_event, approval_evidence=evidence)
    assert a == b


def test_no_leak_scan():
    audit_event = make_audit()
    evidence = prepare_approval_evidence(audit_event=audit_event, approval=SECRET_APPROVAL)
    text = validation_text(
        validate_approval(
            audit_event=audit_event,
            approval_evidence=evidence,
        )
    )
    for value in SENSITIVE_VALUES + PLANTED_SECRETS:
        assert value not in text


FORBIDDEN_IMPORTS = {
    "hashlib", "hmac", "secrets", "cryptography", "ssl", "socket", "urllib",
    "http", "requests", "httpx", "subprocess", "sqlite3", "shelve", "pickle",
    "logging", "rfc8785", "jcs", "sigstore", "cosign", "rekor", "fulcio",
    "boto3", "google", "azure", "passport_verifier",
}
FORBIDDEN_ENGINES = (
    "verify_passport_envelope",
    "authorize_action",
    "compose_decision",
    "prepare_audit_event",
    "prepare_approval_evidence",
    "passport_verifier",
)
FORBIDDEN_SINKS = (
    "open(", ".write(", "print(", "logging", "socket", "requests", "httpx",
    "subprocess", "hashlib", ".hexdigest", "sha256", "sqlite", "pickle",
    "previous_event", "chain(", "sign(", "time", "datetime", "random", "uuid",
)


def test_no_forbidden_imports_or_engines():
    source = Path(approval_validation.__file__).read_text(encoding="utf-8")
    imported = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.update(alias.name.split("."))
        elif isinstance(node, ast.ImportFrom):
            imported.update((node.module or "").split("."))
    assert not (imported & FORBIDDEN_IMPORTS), imported & FORBIDDEN_IMPORTS
    for engine in FORBIDDEN_ENGINES:
        assert engine not in source


def test_no_io_clock_random_in_source():
    source = Path(approval_validation.__file__).read_text(encoding="utf-8")
    for snippet in FORBIDDEN_SINKS:
        assert snippet not in source, snippet
