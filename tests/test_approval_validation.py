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
from aaid import approval_validation, authorization, composition, verification
from aaid.approval import prepare_approval_evidence
from aaid.approval_validation import validate_approval
from aaid.audit import ERROR, prepare_audit_event
from aaid.verification import VerificationCheck

ALLOW = verification.ALLOW
DENY = verification.DENY
REQUIRE_HUMAN_APPROVAL = verification.REQUIRE_HUMAN_APPROVAL
REQUIRE_HUMAN_REVIEW = verification.REQUIRE_HUMAN_REVIEW
VerificationResult = verification.VerificationResult
AuthorizationDecision = authorization.AuthorizationDecision
ComposedDecision = composition.ComposedDecision

BOUND_FIELDS = (
    "passport_id",
    "agent_id",
    "operator_id",
    "issuer_id",
    "requested_action",
    "resource_scope",
    "authorization_decision",
    "composed_decision",
)

BOUND_FIELD_CASES = [
    pytest.param("passport_id", id="passport-id"),
    pytest.param("agent_id", id="agent-id"),
    pytest.param("operator_id", id="operator-id"),
    pytest.param("issuer_id", id="issuer-id"),
    pytest.param("requested_action", id="requested-action"),
    pytest.param("resource_scope", id="resource-scope"),
    pytest.param("authorization_decision", id="authorization-decision"),
    pytest.param("composed_decision", id="composed-decision"),
]

NON_APPROVAL_DECISION_CASES = [
    pytest.param(DENY, id="deny"),
    pytest.param(ERROR, id="audit-error"),
    pytest.param(ALLOW, id="synthetic-allow"),
    pytest.param(REQUIRE_HUMAN_REVIEW, id="human-review"),
]

MALFORMED_AUDIT_EVENT_CASES = [
    pytest.param(None, id="none"),
    pytest.param("x", id="string"),
    pytest.param(123, id="integer"),
    pytest.param(object(), id="object"),
    pytest.param({}, id="mapping"),
]

MALFORMED_APPROVAL_EVIDENCE_CASES = [
    pytest.param(None, id="none"),
    pytest.param("x", id="string"),
    pytest.param(123, id="integer"),
    pytest.param(object(), id="object"),
    pytest.param({}, id="mapping"),
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


def make_audit_and_approval_evidence(decision=REQUIRE_HUMAN_APPROVAL, *, passport=None):
    audit_event = make_audit_event(decision, passport=passport)
    approval_evidence = prepare_approval_evidence(
        audit_event=audit_event,
        approval=APPROVAL,
    )
    return audit_event, approval_evidence


def iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, Mapping):
        for value in obj.values():
            yield from iter_strings(value)
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            yield from iter_strings(value)


def approval_validation_text(result):
    return "\n".join(iter_strings(dataclasses.asdict(result)))


def validation_booleans(result):
    return (
        result.valid,
        result.matches_context,
        result.applicable,
        result.grants_execution,
    )


def test_valid_match_for_require_human_approval():
    audit_event, approval_evidence = make_audit_and_approval_evidence()
    result = validate_approval(
        audit_event=audit_event,
        approval_evidence=approval_evidence,
    )
    assert validation_booleans(result) == (True, True, True, False)


def test_grants_execution_always_false():
    audit_event, approval_evidence = make_audit_and_approval_evidence()
    deny_audit_event, deny_approval_evidence = make_audit_and_approval_evidence(DENY)

    results = [
        validate_approval(
            audit_event=audit_event,
            approval_evidence=approval_evidence,
        ),
        validate_approval(
            audit_event=audit_event,
            approval_evidence=dataclasses.replace(
                approval_evidence,
                passport_id="X",
            ),
        ),
        validate_approval(
            audit_event=None,
            approval_evidence=approval_evidence,
        ),
        validate_approval(
            audit_event=deny_audit_event,
            approval_evidence=deny_approval_evidence,
        ),
    ]
    assert all(result.grants_execution is False for result in results)


@pytest.mark.parametrize("field", BOUND_FIELD_CASES)
def test_context_mismatch_fails(field):
    audit_event, approval_evidence = make_audit_and_approval_evidence()
    tampered = dataclasses.replace(
        approval_evidence,
        **{field: "DIFFERENT-VALUE"},
    )
    result = validate_approval(audit_event=audit_event, approval_evidence=tampered)
    assert result.matches_context is False
    assert result.valid is False
    failed = next(check for check in result.checks if check.name == f"context_bound_{field}")
    assert failed.passed is False


@pytest.mark.parametrize("decision", NON_APPROVAL_DECISION_CASES)
def test_non_approval_decisions_not_applicable(decision):
    audit_event, approval_evidence = make_audit_and_approval_evidence(decision)
    result = validate_approval(
        audit_event=audit_event,
        approval_evidence=approval_evidence,
    )
    assert result.applicable is False
    assert result.valid is False
    assert result.grants_execution is False


def test_allow_context_non_executing():
    audit_event, approval_evidence = make_audit_and_approval_evidence(ALLOW)
    result = validate_approval(
        audit_event=audit_event,
        approval_evidence=approval_evidence,
    )
    assert result.valid is False
    assert result.grants_execution is False


def test_two_none_values_do_not_match():
    audit_event, approval_evidence = make_audit_and_approval_evidence(passport={})
    result = validate_approval(
        audit_event=audit_event,
        approval_evidence=approval_evidence,
    )
    check = next(
        check
        for check in result.checks
        if check.name == "context_bound_passport_id"
    )
    assert check.passed is False
    assert result.matches_context is False


@pytest.mark.parametrize("bad_audit_event", MALFORMED_AUDIT_EVENT_CASES)
def test_malformed_audit_event(bad_audit_event):
    _, approval_evidence = make_audit_and_approval_evidence()
    result = validate_approval(
        audit_event=bad_audit_event,
        approval_evidence=approval_evidence,
    )
    assert validation_booleans(result) == (False, False, False, False)


@pytest.mark.parametrize("bad_approval_evidence", MALFORMED_APPROVAL_EVIDENCE_CASES)
def test_malformed_approval_evidence(bad_approval_evidence):
    audit_event, _ = make_audit_and_approval_evidence()
    result = validate_approval(
        audit_event=audit_event,
        approval_evidence=bad_approval_evidence,
    )
    assert validation_booleans(result) == (False, False, False, False)


def test_expiry_is_ignored():
    audit_event, approval_evidence = make_audit_and_approval_evidence()
    past_approval = dataclasses.replace(
        approval_evidence,
        approval_expires_at="2000-01-01T00:00:00Z",
    )
    future_approval = dataclasses.replace(
        approval_evidence,
        approval_expires_at="2999-01-01T00:00:00Z",
    )

    past_result = validate_approval(
        audit_event=audit_event,
        approval_evidence=past_approval,
    )
    future_result = validate_approval(
        audit_event=audit_event,
        approval_evidence=future_approval,
    )

    assert past_result == future_result
    assert past_result.valid is True


def test_reason_non_empty():
    audit_event, approval_evidence = make_audit_and_approval_evidence()
    result = validate_approval(
        audit_event=audit_event,
        approval_evidence=approval_evidence,
    )
    assert result.reason


def test_checks_ordered_and_typed():
    audit_event, approval_evidence = make_audit_and_approval_evidence()
    checks = validate_approval(
        audit_event=audit_event,
        approval_evidence=approval_evidence,
    ).checks
    assert [check.name for check in checks] == [
        *(f"context_bound_{field}" for field in BOUND_FIELDS),
        "applicable_require_human_approval",
    ]
    assert all(isinstance(check, VerificationCheck) for check in checks)


def test_inputs_not_mutated():
    audit_event, approval_evidence = make_audit_and_approval_evidence()
    snapshots = copy.deepcopy((audit_event, approval_evidence))
    validate_approval(audit_event=audit_event, approval_evidence=approval_evidence)
    assert (audit_event, approval_evidence) == snapshots


def test_validation_is_frozen():
    audit_event, approval_evidence = make_audit_and_approval_evidence()
    result = validate_approval(
        audit_event=audit_event,
        approval_evidence=approval_evidence,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.valid = False


def test_deterministic():
    audit_event, approval_evidence = make_audit_and_approval_evidence()
    first_result = validate_approval(
        audit_event=audit_event,
        approval_evidence=approval_evidence,
    )
    second_result = validate_approval(
        audit_event=audit_event,
        approval_evidence=approval_evidence,
    )
    assert first_result == second_result


def test_no_leak_scan():
    audit_event = make_audit_event()
    approval_evidence = prepare_approval_evidence(
        audit_event=audit_event,
        approval=SECRET_APPROVAL,
    )
    text = approval_validation_text(
        validate_approval(
            audit_event=audit_event,
            approval_evidence=approval_evidence,
        )
    )
    for value in SENSITIVE_VALUES + PLANTED_SECRETS:
        assert value not in text


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
    "prepare_approval_evidence",
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
