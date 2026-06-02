"""Local decision composition."""

from dataclasses import dataclass

from aaid.authorization import AuthorizationDecision
from aaid.verification import (
    ALLOW,
    DENY,
    REQUIRE_HUMAN_APPROVAL,
    REQUIRE_HUMAN_REVIEW,
    VerificationCheck,
    VerificationResult,
)

_DECISIONS = frozenset({ALLOW, DENY, REQUIRE_HUMAN_APPROVAL, REQUIRE_HUMAN_REVIEW})
_RANK = {DENY: 0, REQUIRE_HUMAN_REVIEW: 1, REQUIRE_HUMAN_APPROVAL: 2, ALLOW: 3}


@dataclass(frozen=True)
class ComposedDecision:
    decision: str
    reason: str
    checks: "tuple[VerificationCheck, ...]" = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", tuple(self.checks))
        if self.decision not in _DECISIONS:
            supported = ", ".join(sorted(_DECISIONS))
            raise ValueError(
                f"Unknown decision: {self.decision!r}. "
                f"Supported decisions: {supported}."
            )


def _check(name: str, passed: bool, reason: str) -> VerificationCheck:
    return VerificationCheck(name=name, passed=passed, reason=reason)


def _verification_contribution(verification: object) -> str:
    if not isinstance(verification, VerificationResult):
        return DENY
    if verification.valid is True and verification.decision == ALLOW:
        return ALLOW
    if verification.decision in _RANK and verification.decision != ALLOW:
        return verification.decision
    return DENY


def _authorization_contribution(authorization: object) -> str:
    if not isinstance(authorization, AuthorizationDecision):
        return DENY
    if authorization.decision in _RANK:
        return authorization.decision
    return DENY


def compose_decision(
    verification: object, authorization: object
) -> ComposedDecision:
    verification_decision = _verification_contribution(verification)
    authorization_decision = _authorization_contribution(authorization)
    composed = min(
        (verification_decision, authorization_decision), key=_RANK.__getitem__
    )

    checks = [
        _check(
            "passport_verification_allowed",
            verification_decision == ALLOW,
            f"passport verification contributes {verification_decision}",
        ),
        _check(
            "action_authorization_allowed",
            authorization_decision == ALLOW,
            f"action authorization contributes {authorization_decision}",
        ),
        _check(
            "composed_decision",
            composed == ALLOW,
            (
                "composed decision is the most restrictive of verification "
                f"({verification_decision}) and authorization ({authorization_decision})"
            ),
        ),
    ]
    reason = (
        "passport verification and action authorization both allow the action"
        if composed == ALLOW
        else f"composed decision {composed}; ALLOW requires both verification and authorization to allow"
    )
    return ComposedDecision(composed, reason, checks)
