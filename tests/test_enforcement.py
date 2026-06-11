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
from aaid import authorization, composition, enforcement, verification
from aaid.approval import prepare_approval_evidence
from aaid.approval_validation import validate_approval
from aaid.audit import ERROR, prepare_audit_event
from aaid.enforcement import compose_enforcement
from aaid.verification import VerificationCheck

ALLOW = verification.ALLOW
DENY = verification.DENY
REQUIRE_HUMAN_APPROVAL = verification.REQUIRE_HUMAN_APPROVAL
REQUIRE_HUMAN_REVIEW = verification.REQUIRE_HUMAN_REVIEW
VerificationResult = verification.VerificationResult
AuthorizationDecision = authorization.AuthorizationDecision
ComposedDecision = composition.ComposedDecision

DECISION_CASES = [
    pytest.param(DENY, id="deny"),
    pytest.param(ALLOW, id="synthetic-allow"),
    pytest.param(REQUIRE_HUMAN_APPROVAL, id="approval-required"),
    pytest.param(REQUIRE_HUMAN_REVIEW, id="human-review"),
    pytest.param(ERROR, id="error"),
]

NON_APPROVAL_DECISION_CASES = [
    pytest.param(DENY, id="deny"),
    pytest.param(ERROR, id="error"),
    pytest.param(ALLOW, id="synthetic-allow"),
    pytest.param(REQUIRE_HUMAN_REVIEW, id="human-review"),
]

MALFORMED_APPROVAL_VALIDATION_CASES = [
    pytest.param(None, id="none"),
    pytest.param("x", id="string"),
    pytest.param(123, id="integer"),
    pytest.param(object(), id="object"),
]

MALFORMED_AUDIT_EVENT_CASES = [
    pytest.param(None, id="none"),
    pytest.param("x", id="string"),
    pytest.param(123, id="integer"),
    pytest.param(object(), id="object"),
    pytest.param({}, id="mapping"),
]


def load_example_passport():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)["passport"]


def make_audit_event(decision=REQUIRE_HUMAN_APPROVAL):
    composed_decision = None
    if decision != ERROR:
        composed_decision = ComposedDecision(decision, "composed")

    return prepare_audit_event(
        passport=load_example_passport(),
        request=REQUEST,
        verification=VerificationResult(valid=False, decision=DENY, reason="v"),
        authorization=AuthorizationDecision(REQUIRE_HUMAN_APPROVAL, "a"),
        composition=composed_decision,
        event_type="action_decision",
        occurred_at="2026-06-03T00:00:00Z",
    )


def make_approval_validation(decision=REQUIRE_HUMAN_APPROVAL, *, approval=APPROVAL):
    audit_event = make_audit_event(decision)
    approval_evidence = prepare_approval_evidence(
        audit_event=audit_event,
        approval=approval,
    )
    return validate_approval(
        audit_event=audit_event,
        approval_evidence=approval_evidence,
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


def enforcement_result_text(result):
    return "\n".join(iter_strings(dataclasses.asdict(result)))


@pytest.mark.parametrize("decision", DECISION_CASES)
def test_decision_passes_through(decision):
    assert compose_enforcement(audit_event=make_audit_event(decision)).decision == decision


@pytest.mark.parametrize("decision", DECISION_CASES)
def test_execution_allowed_always_false(decision):
    result = compose_enforcement(audit_event=make_audit_event(decision))
    assert result.execution_allowed is False


def test_execution_allowed_false_for_synthetic_allow():
    result = compose_enforcement(audit_event=make_audit_event(ALLOW))
    assert result.execution_allowed is False


def test_require_human_approval_with_valid_approval():
    result = compose_enforcement(
        audit_event=make_audit_event(REQUIRE_HUMAN_APPROVAL),
        approval_validation=make_approval_validation(REQUIRE_HUMAN_APPROVAL),
    )
    assert result.approval_satisfied is True
    assert result.decision == REQUIRE_HUMAN_APPROVAL
    assert result.execution_allowed is False


def test_require_human_approval_without_approval():
    result = compose_enforcement(audit_event=make_audit_event(REQUIRE_HUMAN_APPROVAL))
    assert result.approval_satisfied is False


@pytest.mark.parametrize("bad_approval_validation", MALFORMED_APPROVAL_VALIDATION_CASES)
def test_require_human_approval_with_malformed_approval(bad_approval_validation):
    result = compose_enforcement(
        audit_event=make_audit_event(REQUIRE_HUMAN_APPROVAL),
        approval_validation=bad_approval_validation,
    )
    assert result.approval_satisfied is False


def test_require_human_approval_with_inapplicable_validation():
    result = compose_enforcement(
        audit_event=make_audit_event(REQUIRE_HUMAN_APPROVAL),
        approval_validation=make_approval_validation(DENY),
    )
    assert result.approval_satisfied is False


@pytest.mark.parametrize("decision", NON_APPROVAL_DECISION_CASES)
def test_valid_approval_does_not_affect_non_approval_decisions(decision):
    result = compose_enforcement(
        audit_event=make_audit_event(decision),
        approval_validation=make_approval_validation(REQUIRE_HUMAN_APPROVAL),
    )
    assert result.decision == decision
    assert result.approval_satisfied is False
    assert result.execution_allowed is False


@pytest.mark.parametrize("bad_audit_event", MALFORMED_AUDIT_EVENT_CASES)
def test_malformed_audit_event(bad_audit_event):
    result = compose_enforcement(audit_event=bad_audit_event)
    assert result.decision == "ERROR"
    assert result.approval_satisfied is False
    assert result.execution_allowed is False


def test_malformed_approval_validation_does_not_raise():
    result = compose_enforcement(
        audit_event=make_audit_event(REQUIRE_HUMAN_APPROVAL),
        approval_validation="x",
    )
    assert result.approval_satisfied is False


def test_reason_non_empty():
    assert compose_enforcement(audit_event=make_audit_event(DENY)).reason


def test_checks_ordered_and_typed():
    checks = compose_enforcement(
        audit_event=make_audit_event(REQUIRE_HUMAN_APPROVAL)
    ).checks
    assert [check.name for check in checks] == [
        "inputs_well_formed",
        "decision_recorded",
        "approval_gate",
        "execution_withheld",
    ]
    assert all(isinstance(check, VerificationCheck) for check in checks)


def test_inputs_not_mutated():
    audit_event = make_audit_event(REQUIRE_HUMAN_APPROVAL)
    approval_validation = make_approval_validation(REQUIRE_HUMAN_APPROVAL)
    snapshots = copy.deepcopy((audit_event, approval_validation))
    compose_enforcement(
        audit_event=audit_event,
        approval_validation=approval_validation,
    )
    assert (audit_event, approval_validation) == snapshots


def test_enforcement_decision_is_frozen():
    result = compose_enforcement(audit_event=make_audit_event(DENY))
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.execution_allowed = True


def test_deterministic():
    audit_event = make_audit_event(REQUIRE_HUMAN_APPROVAL)
    approval_validation = make_approval_validation(REQUIRE_HUMAN_APPROVAL)

    first_result = compose_enforcement(
        audit_event=audit_event,
        approval_validation=approval_validation,
    )
    second_result = compose_enforcement(
        audit_event=audit_event,
        approval_validation=approval_validation,
    )

    assert first_result == second_result


def test_no_leak_scan():
    audit_event = make_audit_event(REQUIRE_HUMAN_APPROVAL)
    approval_evidence = prepare_approval_evidence(
        audit_event=audit_event,
        approval=SECRET_APPROVAL,
    )
    approval_validation = validate_approval(
        audit_event=audit_event,
        approval_evidence=approval_evidence,
    )
    text = enforcement_result_text(
        compose_enforcement(
            audit_event=audit_event,
            approval_validation=approval_validation,
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
    "validate_approval",
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
    source = Path(enforcement.__file__).read_text(encoding="utf-8")
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
    source = Path(enforcement.__file__).read_text(encoding="utf-8")
    for snippet in FORBIDDEN_SINKS:
        assert snippet not in source, snippet
