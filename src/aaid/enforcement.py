"""Local enforcement composition."""

from dataclasses import dataclass

from aaid.approval_validation import ApprovalValidation
from aaid.audit import AuditEvent
from aaid.verification import REQUIRE_HUMAN_APPROVAL, VerificationCheck


@dataclass(frozen=True)
class EnforcementDecision:
    decision: str
    execution_allowed: bool
    approval_satisfied: bool
    reason: str
    checks: "tuple[VerificationCheck, ...]"


def _check(name: str, passed: bool, reason: str) -> VerificationCheck:
    return VerificationCheck(name=name, passed=passed, reason=reason)


def compose_enforcement(*, audit_event, approval_validation=None) -> EnforcementDecision:
    if not isinstance(audit_event, AuditEvent):
        return EnforcementDecision(
            decision="ERROR",
            execution_allowed=False,
            approval_satisfied=False,
            reason="audit_event is not an AuditEvent; failing closed",
            checks=(
                _check("inputs_well_formed", False, "audit_event is not the expected type"),
                _check("execution_withheld", True, "execution is not allowed in this local model"),
            ),
        )

    decision = audit_event.decision
    approval_valid = (
        isinstance(approval_validation, ApprovalValidation)
        and approval_validation.valid is True
    )
    approval_satisfied = decision == REQUIRE_HUMAN_APPROVAL and approval_valid

    checks = (
        _check("inputs_well_formed", True, "audit_event is an AuditEvent"),
        _check("decision_recorded", True, "decision recorded from the audit event"),
        _check(
            "approval_gate",
            approval_satisfied,
            "valid approval supplied for a REQUIRE_HUMAN_APPROVAL decision"
            if approval_satisfied
            else "no applicable valid approval for this decision",
        ),
        _check("execution_withheld", True, "execution is not allowed in this local model"),
    )
    reason = (
        "valid approval recorded for a REQUIRE_HUMAN_APPROVAL decision; "
        "execution is not allowed in this local model"
        if approval_satisfied
        else "enforcement decision recorded; execution is not allowed in this local model"
    )
    return EnforcementDecision(
        decision=decision,
        execution_allowed=False,
        approval_satisfied=approval_satisfied,
        reason=reason,
        checks=checks,
    )
