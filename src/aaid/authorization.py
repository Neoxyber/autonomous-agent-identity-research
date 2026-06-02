"""Local action authorization evaluator."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from aaid.verification import (
    ALLOW,
    DENY,
    REQUIRE_HUMAN_APPROVAL,
    REQUIRE_HUMAN_REVIEW,
    VerificationCheck,
)

_DECISIONS = frozenset({ALLOW, DENY, REQUIRE_HUMAN_APPROVAL, REQUIRE_HUMAN_REVIEW})
_UNKNOWN_ACTION_POLICIES = frozenset({DENY, REQUIRE_HUMAN_REVIEW})
_PERMISSION_LISTS = (
    "prohibited_actions",
    "approval_required_actions",
    "allowed_actions",
)


@dataclass(frozen=True)
class AuthorizationDecision:
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


def _normalized_request(request: object) -> "dict[str, str] | None":
    if not isinstance(request, Mapping):
        return None

    action = request.get("action")
    resource_scope = request.get("resource_scope")
    if not isinstance(action, str) or not isinstance(resource_scope, str):
        return None

    return {"action": action, "resource_scope": resource_scope}


def _permission_lists(
    passport: object,
) -> "tuple[Sequence, Sequence, Sequence] | None":
    if not isinstance(passport, Mapping):
        return None

    permissions = passport.get("permissions")
    if not isinstance(permissions, Mapping):
        return None

    if permissions.get("default_decision") != DENY:
        return None

    resolved = []
    for key in _PERMISSION_LISTS:
        if key not in permissions:
            return None

        value = permissions[key]
        if isinstance(value, (str, bytes, bytearray)) or not isinstance(
            value, Sequence
        ):
            return None

        resolved.append(value)

    return tuple(resolved)


def _matches(entries: Sequence, request: "dict[str, str]") -> bool:
    return any(
        isinstance(entry, Mapping) and dict(entry) == request for entry in entries
    )


def _check(name: str, passed: bool, reason: str) -> VerificationCheck:
    return VerificationCheck(name=name, passed=passed, reason=reason)


def authorize_action(
    passport: object,
    request: object,
    *,
    unknown_action: str = DENY,
) -> AuthorizationDecision:
    checks: list[VerificationCheck] = []

    if unknown_action not in _UNKNOWN_ACTION_POLICIES:
        checks.append(
            _check(
                "unknown_action_policy_supported",
                False,
                "unsupported unknown-action policy",
            )
        )
        return AuthorizationDecision(DENY, "unsupported unknown-action policy", checks)

    checks.append(
        _check(
            "unknown_action_policy_supported",
            True,
            "unknown-action policy is DENY or REQUIRE_HUMAN_REVIEW",
        )
    )

    normalized = _normalized_request(request)
    if normalized is None:
        checks.append(
            _check(
                "request_well_formed",
                False,
                "request must carry a string action and resource_scope",
            )
        )
        return AuthorizationDecision(DENY, "action request is malformed", checks)

    checks.append(
        _check(
            "request_well_formed",
            True,
            "request has a string action and resource_scope",
        )
    )

    lists = _permission_lists(passport)
    if lists is None:
        checks.append(
            _check(
                "permissions_well_formed",
                False,
                "passport permissions are missing, malformed, or not default-deny",
            )
        )
        return AuthorizationDecision(
            DENY,
            "passport permissions are missing, malformed, or not default-deny",
            checks,
        )

    prohibited, approval_required, allowed = lists
    checks.append(
        _check(
            "permissions_well_formed",
            True,
            "permissions default to DENY and carry required action lists",
        )
    )

    if _matches(prohibited, normalized):
        checks.append(
            _check("prohibited_action", True, "action matches a prohibited entry")
        )
        return AuthorizationDecision(DENY, "action is prohibited", checks)

    checks.append(_check("prohibited_action", False, "action is not prohibited"))

    if _matches(approval_required, normalized):
        checks.append(
            _check(
                "approval_required_action",
                True,
                "action matches an approval-required entry",
            )
        )
        return AuthorizationDecision(
            REQUIRE_HUMAN_APPROVAL,
            "action requires human approval",
            checks,
        )

    checks.append(
        _check(
            "approval_required_action",
            False,
            "action is not approval-required",
        )
    )

    if _matches(allowed, normalized):
        checks.append(_check("allowed_action", True, "action matches an allowed entry"))
        return AuthorizationDecision(ALLOW, "action is allowed", checks)

    checks.append(_check("allowed_action", False, "action matches no allowed entry"))
    checks.append(_check("unknown_action", False, "action matches no permission entry"))

    reason = (
        "action is unknown to the passport permissions; failing closed to DENY"
        if unknown_action == DENY
        else "action is unknown to the passport permissions; routed to human review"
    )
    return AuthorizationDecision(unknown_action, reason, checks)
