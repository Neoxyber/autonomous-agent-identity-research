"""Local approval validation."""

from dataclasses import dataclass

from aaid.approval import ApprovalEvidence
from aaid.audit import AuditEvent
from aaid.verification import REQUIRE_HUMAN_APPROVAL, VerificationCheck

_BINDING_FIELDS = (
    ("passport_id", "passport_id"),
    ("agent_id", "agent_id"),
    ("operator_id", "operator_id"),
    ("issuer_id", "issuer_id"),
    ("requested_action", "requested_action"),
    ("resource_scope", "resource_scope"),
    ("authorization_decision", "authorization_decision"),
    ("composed_decision", "decision"),
)


@dataclass(frozen=True)
class ApprovalValidation:
    valid: bool
    matches_context: bool
    applicable: bool
    grants_execution: bool
    reason: str
    checks: "tuple[VerificationCheck, ...]"


def _check(name: str, passed: bool, reason: str) -> VerificationCheck:
    return VerificationCheck(name=name, passed=passed, reason=reason)


def validate_approval(*, audit_event, approval_evidence) -> ApprovalValidation:
    if not isinstance(audit_event, AuditEvent) or not isinstance(
        approval_evidence, ApprovalEvidence
    ):
        return ApprovalValidation(
            valid=False,
            matches_context=False,
            applicable=False,
            grants_execution=False,
            reason="audit_event or approval_evidence is not the expected type",
            checks=(_check("inputs_well_formed", False, "inputs are not the expected types"),),
        )

    checks = []
    matches_context = True
    for evidence_attr, audit_attr in _BINDING_FIELDS:
        evidence_value = getattr(approval_evidence, evidence_attr)
        audit_value = getattr(audit_event, audit_attr)
        passed = evidence_value is not None and evidence_value == audit_value
        matches_context = matches_context and passed
        checks.append(
            _check(
                f"context_bound_{evidence_attr}",
                passed,
                f"{evidence_attr} matches the audit event"
                if passed
                else f"{evidence_attr} does not match the audit event",
            )
        )

    applicable = (
        audit_event.decision == REQUIRE_HUMAN_APPROVAL
        and approval_evidence.approval_applicable is True
    )
    checks.append(
        _check(
            "applicable_require_human_approval",
            applicable,
            "decision is REQUIRE_HUMAN_APPROVAL and approval evidence is applicable"
            if applicable
            else "decision is not REQUIRE_HUMAN_APPROVAL or approval evidence is not applicable",
        )
    )

    valid = matches_context and applicable
    if valid:
        reason = "approval evidence is context-bound and applicable; this does not grant execution"
    elif not matches_context:
        reason = "approval evidence is not bound to the audit event context"
    else:
        reason = "approval evidence is not applicable to this decision"
    return ApprovalValidation(
        valid=valid,
        matches_context=matches_context,
        applicable=applicable,
        grants_execution=False,
        reason=reason,
        checks=tuple(checks),
    )
