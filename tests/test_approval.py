import ast
import copy
import dataclasses
import json
from collections.abc import Mapping
from pathlib import Path

import pytest

from _support import (
    APPROVAL,
    EXAMPLE_PATH,
    PLANTED_SECRETS,
    REQUEST,
    SECRET_APPROVAL,
    SENSITIVE_VALUES,
)
from aaid import approval, authorization, composition, verification
from aaid.approval import prepare_approval_evidence
from aaid.audit import ERROR, prepare_audit_event

ALLOW = verification.ALLOW
DENY = verification.DENY
REQUIRE_HUMAN_APPROVAL = verification.REQUIRE_HUMAN_APPROVAL
REQUIRE_HUMAN_REVIEW = verification.REQUIRE_HUMAN_REVIEW
VerificationResult = verification.VerificationResult
AuthorizationDecision = authorization.AuthorizationDecision
ComposedDecision = composition.ComposedDecision

OCCURRED_AT_CASES = [
    pytest.param(
        "2026-06-03T02:00:00Z",
        "2026-06-03T02:00:00Z",
        id="timestamp",
    ),
    pytest.param(None, None, id="none"),
    pytest.param(123, None, id="integer"),
    pytest.param({"t": 1}, None, id="mapping"),
    pytest.param(object(), None, id="object"),
]

DECISION_BINDING_CASES = [
    pytest.param(REQUIRE_HUMAN_APPROVAL, True, id="approval-required"),
    pytest.param(DENY, False, id="deny"),
    pytest.param(ALLOW, False, id="synthetic-allow"),
    pytest.param(ERROR, False, id="audit-error"),
    pytest.param(REQUIRE_HUMAN_REVIEW, False, id="human-review"),
]

MALFORMED_AUDIT_EVENT_CASES = [
    pytest.param(None, id="none"),
    pytest.param("x", id="string"),
    pytest.param(123, id="integer"),
    pytest.param(object(), id="object"),
    pytest.param({}, id="mapping"),
]

MALFORMED_APPROVAL_CASES = [
    pytest.param(None, id="none"),
    pytest.param("x", id="string"),
    pytest.param(123, id="integer"),
    pytest.param(object(), id="object"),
    pytest.param([], id="list"),
]


def load_example_passport():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)["passport"]


def make_audit_event(decision=REQUIRE_HUMAN_APPROVAL, *, passport=None):
    composed_decision = None
    if decision != ERROR:
        composed_decision = ComposedDecision(decision, "composed")

    return prepare_audit_event(
        passport=load_example_passport() if passport is None else passport,
        request=REQUEST,
        verification=VerificationResult(valid=False, decision=DENY, reason="v"),
        authorization=AuthorizationDecision(REQUIRE_HUMAN_APPROVAL, "a"),
        composition=composed_decision,
        event_type="action_decision",
        occurred_at="2026-06-03T00:00:00Z",
    )


def make_approval_evidence(
    decision=REQUIRE_HUMAN_APPROVAL,
    *,
    approval=APPROVAL,
    occurred_at=None,
    passport=None,
):
    return prepare_approval_evidence(
        audit_event=make_audit_event(decision, passport=passport),
        approval=approval,
        occurred_at=occurred_at,
    )


def iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, Mapping):
        for value in obj.values():
            yield from iter_strings(value)
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            yield from iter_strings(value)


def approval_evidence_text(evidence):
    return "\n".join(iter_strings(dataclasses.asdict(evidence)))


def test_bound_context_copied_from_audit_event():
    passport = load_example_passport()
    evidence = make_approval_evidence(passport=passport)
    assert evidence.passport_id == passport["passport_id"]
    assert evidence.agent_id == passport["agent_id"]
    assert evidence.operator_id == passport["operator"]["operator_id"]
    assert evidence.issuer_id == passport["issuer_id"]
    assert (evidence.requested_action, evidence.resource_scope) == (
        "summarize_public_text",
        "demo.public_text",
    )
    assert evidence.authorization_decision == REQUIRE_HUMAN_APPROVAL
    assert evidence.composed_decision == REQUIRE_HUMAN_APPROVAL


def test_approval_metadata_copied():
    evidence = make_approval_evidence()
    assert evidence.approver_id == "urn:aaid:approver:reviewer-1"
    assert evidence.approver_role == "operator_admin"
    assert evidence.approval_outcome == "approved"
    assert evidence.approval_reason == "reviewed in research demo"
    assert evidence.approval_scope == "demo.public_text"
    assert evidence.approval_expires_at == "2026-06-03T01:00:00Z"


def test_non_scalar_approval_values_recorded_none():
    approval_mapping = {
        "approver_id": 123,
        "approver_role": {"x": 1},
        "approval_outcome": ["a"],
        "approval_reason": object(),
        "approval_scope": None,
        "approval_expires_at": 5.0,
    }
    evidence = make_approval_evidence(approval=approval_mapping)
    fields = (
        evidence.approver_id,
        evidence.approver_role,
        evidence.approval_outcome,
        evidence.approval_reason,
        evidence.approval_scope,
        evidence.approval_expires_at,
    )
    assert fields == (None,) * 6


@pytest.mark.parametrize("value, expected", OCCURRED_AT_CASES)
def test_occurred_at_scalar_handling(value, expected):
    assert make_approval_evidence(occurred_at=value).occurred_at == expected


def test_occurred_at_omitted_default_none():
    assert make_approval_evidence().occurred_at is None


@pytest.mark.parametrize("decision, applicable", DECISION_BINDING_CASES)
def test_decision_binding_is_inert(decision, applicable):
    evidence = make_approval_evidence(
        decision,
        approval={**APPROVAL, "approval_outcome": "approved"},
    )
    assert evidence.composed_decision == decision
    assert evidence.approval_applicable is applicable
    assert evidence.grants_execution is False


@pytest.mark.parametrize("bad_audit_event", MALFORMED_AUDIT_EVENT_CASES)
def test_malformed_audit_event_records_none(bad_audit_event):
    evidence = prepare_approval_evidence(
        audit_event=bad_audit_event,
        approval=APPROVAL,
    )
    bound = (
        evidence.passport_id,
        evidence.agent_id,
        evidence.operator_id,
        evidence.issuer_id,
        evidence.requested_action,
        evidence.resource_scope,
        evidence.authorization_decision,
        evidence.composed_decision,
    )
    assert bound == (None,) * 8
    assert evidence.approval_applicable is False
    assert evidence.grants_execution is False


@pytest.mark.parametrize("bad_approval", MALFORMED_APPROVAL_CASES)
def test_malformed_approval_records_none(bad_approval):
    evidence = prepare_approval_evidence(
        audit_event=make_audit_event(),
        approval=bad_approval,
    )
    fields = (
        evidence.approver_id,
        evidence.approval_outcome,
        evidence.approval_scope,
    )
    assert fields == (None, None, None)


def test_no_leak_scan():
    text = approval_evidence_text(
        prepare_approval_evidence(
            audit_event=make_audit_event(),
            approval=SECRET_APPROVAL,
        )
    )
    for value in SENSITIVE_VALUES + PLANTED_SECRETS:
        assert value not in text


def test_inputs_not_mutated():
    audit_event = make_audit_event()
    approval_mapping = dict(APPROVAL)
    snapshots = copy.deepcopy((audit_event, approval_mapping))
    prepare_approval_evidence(
        audit_event=audit_event,
        approval=approval_mapping,
        occurred_at="t",
    )
    assert (audit_event, approval_mapping) == snapshots


def test_approval_evidence_is_frozen():
    with pytest.raises(dataclasses.FrozenInstanceError):
        make_approval_evidence().grants_execution = True


def test_deterministic():
    audit_event = make_audit_event()
    args = {
        "audit_event": audit_event,
        "approval": APPROVAL,
        "occurred_at": "t",
    }
    assert prepare_approval_evidence(**args) == prepare_approval_evidence(**args)


FORBIDDEN_IMPORTS = {
    "azure",
    "boto3",
    "cosign",
    "cryptography",
    "fulcio",
    "google",
    "hashlib",
    "hmac",
    "http",
    "httpx",
    "jcs",
    "logging",
    "passport_verifier",
    "pickle",
    "requests",
    "rekor",
    "rfc8785",
    "secrets",
    "shelve",
    "sigstore",
    "socket",
    "sqlite3",
    "ssl",
    "subprocess",
    "urllib",
}
FORBIDDEN_ENGINES = (
    "authorize_action",
    "compose_decision",
    "passport_verifier",
    "prepare_audit_event",
    "verify_passport_envelope",
)
FORBIDDEN_SINKS = (
    ".hexdigest",
    ".write(",
    "chain(",
    "datetime",
    "hashlib",
    "logging",
    "open(",
    "pickle",
    "previous_event",
    "print(",
    "random",
    "requests",
    "sha256",
    "sign(",
    "socket",
    "sqlite",
    "subprocess",
    "time",
    "uuid",
)


def test_no_forbidden_imports_or_engines():
    source = Path(approval.__file__).read_text(encoding="utf-8")
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
    source = Path(approval.__file__).read_text(encoding="utf-8")
    for snippet in FORBIDDEN_SINKS:
        assert snippet not in source, snippet
