"""Local approval evidence preparation."""

from collections.abc import Mapping
from dataclasses import dataclass

from aaid.audit import AuditEvent
from aaid.verification import REQUIRE_HUMAN_APPROVAL


@dataclass(frozen=True)
class ApprovalEvidence:
    passport_id: "str | None"
    agent_id: "str | None"
    operator_id: "str | None"
    issuer_id: "str | None"
    requested_action: "str | None"
    resource_scope: "str | None"
    authorization_decision: "str | None"
    composed_decision: "str | None"
    approver_id: "str | None"
    approver_role: "str | None"
    approval_outcome: "str | None"
    approval_reason: "str | None"
    approval_scope: "str | None"
    approval_expires_at: "str | None"
    occurred_at: "str | None"
    approval_applicable: bool
    grants_execution: bool


def _str_or_none(value: object) -> "str | None":
    return value if isinstance(value, str) else None


def _audit_field(audit_event: object, name: str) -> "str | None":
    if not isinstance(audit_event, AuditEvent):
        return None
    return _str_or_none(getattr(audit_event, name, None))


def _approval_field(approval: object, key: str) -> "str | None":
    return _str_or_none(approval.get(key)) if isinstance(approval, Mapping) else None


def prepare_approval_evidence(
    *,
    audit_event: object,
    approval: object,
    occurred_at: object = None,
) -> ApprovalEvidence:
    composed_decision = _audit_field(audit_event, "decision")
    return ApprovalEvidence(
        passport_id=_audit_field(audit_event, "passport_id"),
        agent_id=_audit_field(audit_event, "agent_id"),
        operator_id=_audit_field(audit_event, "operator_id"),
        issuer_id=_audit_field(audit_event, "issuer_id"),
        requested_action=_audit_field(audit_event, "requested_action"),
        resource_scope=_audit_field(audit_event, "resource_scope"),
        authorization_decision=_audit_field(audit_event, "authorization_decision"),
        composed_decision=composed_decision,
        approver_id=_approval_field(approval, "approver_id"),
        approver_role=_approval_field(approval, "approver_role"),
        approval_outcome=_approval_field(approval, "approval_outcome"),
        approval_reason=_approval_field(approval, "approval_reason"),
        approval_scope=_approval_field(approval, "approval_scope"),
        approval_expires_at=_approval_field(approval, "approval_expires_at"),
        occurred_at=_str_or_none(occurred_at),
        approval_applicable=composed_decision == REQUIRE_HUMAN_APPROVAL,
        grants_execution=False,
    )
