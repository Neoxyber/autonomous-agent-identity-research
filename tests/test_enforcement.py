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

from aaid import authorization, composition, enforcement, verification
from aaid.approval import prepare_approval_evidence
from aaid.approval_validation import validate_approval
from aaid.audit import ERROR, prepare_audit_event
from aaid.enforcement import EnforcementDecision, compose_enforcement
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
DECISIONS = [DENY, ALLOW, REQUIRE_HUMAN_APPROVAL, REQUIRE_HUMAN_REVIEW, ERROR]


def load_passport():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)["passport"]


def make_audit(decision=REQUIRE_HUMAN_APPROVAL):
    comp = None if decision == ERROR else ComposedDecision(decision, "composed")
    return prepare_audit_event(
        passport=load_passport(),
        request=REQUEST,
        verification=VerificationResult(valid=False, decision=DENY, reason="v"),
        authorization=AuthorizationDecision(REQUIRE_HUMAN_APPROVAL, "a"),
        composition=comp,
        event_type="action_decision",
        occurred_at="2026-06-03T00:00:00Z",
    )


def make_validation(decision=REQUIRE_HUMAN_APPROVAL, *, approval=APPROVAL):
    audit_event = make_audit(decision)
    evidence = prepare_approval_evidence(audit_event=audit_event, approval=approval)
    return validate_approval(audit_event=audit_event, approval_evidence=evidence)


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, Mapping):
        for value in obj.values():
            yield from strings(value)
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            yield from strings(value)


def result_text(result):
    return "\n".join(strings(dataclasses.asdict(result)))


@pytest.mark.parametrize("decision", DECISIONS)
def test_decision_passes_through(decision):
    assert compose_enforcement(audit_event=make_audit(decision)).decision == decision


@pytest.mark.parametrize("decision", DECISIONS)
def test_execution_allowed_always_false(decision):
    assert compose_enforcement(audit_event=make_audit(decision)).execution_allowed is False


def test_execution_allowed_false_for_synthetic_allow():
    assert compose_enforcement(audit_event=make_audit(ALLOW)).execution_allowed is False


def test_require_human_approval_with_valid_approval():
    result = compose_enforcement(
        audit_event=make_audit(REQUIRE_HUMAN_APPROVAL),
        approval_validation=make_validation(REQUIRE_HUMAN_APPROVAL),
    )
    assert result.approval_satisfied is True
    assert result.decision == REQUIRE_HUMAN_APPROVAL
    assert result.execution_allowed is False


def test_require_human_approval_without_approval():
    result = compose_enforcement(audit_event=make_audit(REQUIRE_HUMAN_APPROVAL))
    assert result.approval_satisfied is False


@pytest.mark.parametrize("bad", [None, "x", 123, object()])
def test_require_human_approval_with_malformed_approval(bad):
    result = compose_enforcement(
        audit_event=make_audit(REQUIRE_HUMAN_APPROVAL),
        approval_validation=bad,
    )
    assert result.approval_satisfied is False


def test_require_human_approval_with_inapplicable_validation():
    result = compose_enforcement(
        audit_event=make_audit(REQUIRE_HUMAN_APPROVAL),
        approval_validation=make_validation(DENY),
    )
    assert result.approval_satisfied is False


@pytest.mark.parametrize("decision", [DENY, ERROR, ALLOW, REQUIRE_HUMAN_REVIEW])
def test_valid_approval_does_not_affect_non_approval_decisions(decision):
    result = compose_enforcement(
        audit_event=make_audit(decision),
        approval_validation=make_validation(REQUIRE_HUMAN_APPROVAL),
    )
    assert result.decision == decision
    assert result.approval_satisfied is False
    assert result.execution_allowed is False


@pytest.mark.parametrize("bad", [None, "x", 123, object(), {}])
def test_malformed_audit_event(bad):
    result = compose_enforcement(audit_event=bad)
    assert result.decision == "ERROR"
    assert result.approval_satisfied is False
    assert result.execution_allowed is False


def test_malformed_approval_validation_does_not_raise():
    result = compose_enforcement(
        audit_event=make_audit(REQUIRE_HUMAN_APPROVAL),
        approval_validation="x",
    )
    assert result.approval_satisfied is False


def test_reason_non_empty():
    assert compose_enforcement(audit_event=make_audit(DENY)).reason


def test_checks_ordered_and_typed():
    checks = compose_enforcement(audit_event=make_audit(REQUIRE_HUMAN_APPROVAL)).checks
    assert [c.name for c in checks] == [
        "inputs_well_formed",
        "decision_recorded",
        "approval_gate",
        "execution_withheld",
    ]
    assert all(isinstance(c, VerificationCheck) for c in checks)


def test_inputs_not_mutated():
    audit_event = make_audit(REQUIRE_HUMAN_APPROVAL)
    validation = make_validation(REQUIRE_HUMAN_APPROVAL)
    snapshots = copy.deepcopy((audit_event, validation))
    compose_enforcement(audit_event=audit_event, approval_validation=validation)
    assert (audit_event, validation) == snapshots


def test_enforcement_decision_is_frozen():
    result = compose_enforcement(audit_event=make_audit(DENY))
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.execution_allowed = True


def test_deterministic():
    audit_event = make_audit(REQUIRE_HUMAN_APPROVAL)
    validation = make_validation(REQUIRE_HUMAN_APPROVAL)
    a = compose_enforcement(audit_event=audit_event, approval_validation=validation)
    b = compose_enforcement(audit_event=audit_event, approval_validation=validation)
    assert a == b


def test_no_leak_scan():
    audit_event = make_audit(REQUIRE_HUMAN_APPROVAL)
    evidence = prepare_approval_evidence(audit_event=audit_event, approval=SECRET_APPROVAL)
    validation = validate_approval(audit_event=audit_event, approval_evidence=evidence)
    text = result_text(
        compose_enforcement(
            audit_event=audit_event,
            approval_validation=validation,
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
    "validate_approval",
    "passport_verifier",
)
FORBIDDEN_SINKS = (
    "open(", ".write(", "print(", "logging", "socket", "requests", "httpx",
    "subprocess", "hashlib", ".hexdigest", "sha256", "sqlite", "pickle",
    "previous_event", "chain(", "sign(", "time", "datetime", "random", "uuid",
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
