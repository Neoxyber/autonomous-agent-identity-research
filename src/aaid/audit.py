"""Local audit event preparation."""

from collections.abc import Mapping
from dataclasses import dataclass

from aaid.authorization import AuthorizationDecision
from aaid.composition import ComposedDecision
from aaid.verification import (
    ALLOW,
    DENY,
    REQUIRE_HUMAN_APPROVAL,
    REQUIRE_HUMAN_REVIEW,
    VerificationResult,
)

ERROR = "ERROR"
_VALID_DECISIONS = frozenset(
    {ALLOW, DENY, REQUIRE_HUMAN_APPROVAL, REQUIRE_HUMAN_REVIEW}
)


@dataclass(frozen=True)
class AuditEvent:
    event_type: "str | None"
    occurred_at: "str | None"
    decision: str
    decision_reason: "str | None"
    verification_decision: "str | None"
    authorization_decision: "str | None"
    requested_action: "str | None"
    resource_scope: "str | None"
    passport_id: "str | None"
    agent_id: "str | None"
    operator_id: "str | None"
    issuer_id: "str | None"
    lifecycle_status: "str | None"
    risk_class: "str | None"
    policy_id: "str | None"
    audit_stream_id: "str | None"
    revocation_reference: "str | None"


def _field(mapping: object, key: str) -> object:
    return mapping.get(key) if isinstance(mapping, Mapping) else None


def _str_or_none(value: object) -> "str | None":
    return value if isinstance(value, str) else None


def prepare_audit_event(
    *,
    passport: object,
    request: object,
    verification: object,
    authorization: object,
    composition: object,
    event_type: object,
    occurred_at: object = None,
) -> AuditEvent:
    if (
        isinstance(composition, ComposedDecision)
        and composition.decision in _VALID_DECISIONS
    ):
        decision = composition.decision
        decision_reason = _str_or_none(composition.reason)
    else:
        decision = ERROR
        decision_reason = None

    verification_decision = (
        verification.decision
        if isinstance(verification, VerificationResult)
        else None
    )
    authorization_decision = (
        authorization.decision
        if isinstance(authorization, AuthorizationDecision)
        else None
    )

    operator = _field(passport, "operator")
    permissions = _field(passport, "permissions")
    audit = _field(passport, "audit")
    revocation = _field(passport, "revocation")

    return AuditEvent(
        event_type=_str_or_none(event_type),
        occurred_at=_str_or_none(occurred_at),
        decision=decision,
        decision_reason=decision_reason,
        verification_decision=_str_or_none(verification_decision),
        authorization_decision=_str_or_none(authorization_decision),
        requested_action=_str_or_none(_field(request, "action")),
        resource_scope=_str_or_none(_field(request, "resource_scope")),
        passport_id=_str_or_none(_field(passport, "passport_id")),
        agent_id=_str_or_none(_field(passport, "agent_id")),
        operator_id=_str_or_none(_field(operator, "operator_id")),
        issuer_id=_str_or_none(_field(passport, "issuer_id")),
        lifecycle_status=_str_or_none(_field(passport, "lifecycle_status")),
        risk_class=_str_or_none(_field(passport, "risk_class")),
        policy_id=_str_or_none(_field(permissions, "policy_id")),
        audit_stream_id=_str_or_none(_field(audit, "audit_stream_id")),
        revocation_reference=_str_or_none(_field(revocation, "status_reference")),
    )
