"""Structured verification result model for the agent passport.

This module provides immutable data containers that record the outcome of an
agent passport verification, using the four decision outcomes from the
permission model: ``ALLOW``, ``DENY``, ``REQUIRE_HUMAN_APPROVAL``, and
``REQUIRE_HUMAN_REVIEW``.

It is a result model only. It does not verify signatures, does not perform any
cryptography, does not sign anything, does not verify proofs, and does not
implement a policy engine. It records what a separate verifier or policy
evaluation decided so the decision can be explained and audited. Invalid or
failed results fail closed to ``DENY``. Before relying on any real verification
outcome, the verification and policy logic must be implemented and reviewed
separately.
"""

from collections.abc import Iterable
from dataclasses import dataclass

ALLOW = "ALLOW"
DENY = "DENY"
REQUIRE_HUMAN_APPROVAL = "REQUIRE_HUMAN_APPROVAL"
REQUIRE_HUMAN_REVIEW = "REQUIRE_HUMAN_REVIEW"

_DECISIONS = frozenset(
    {ALLOW, DENY, REQUIRE_HUMAN_APPROVAL, REQUIRE_HUMAN_REVIEW}
)


@dataclass(frozen=True)
class VerificationCheck:
    """A single named check recorded during verification.

    ``passed`` is a recorded outcome only; it does not assert that any
    cryptographic verification was performed. ``reason`` is a human-readable
    explanation and is preserved unchanged.
    """

    name: str
    passed: bool
    reason: str


@dataclass(frozen=True)
class VerificationResult:
    """The immutable outcome of an agent passport verification.

    This is a data container. It records a decision and the checks that led to
    it; it does not perform verification, signing, proof checking, or
    cryptography. Invalid or failed results fail closed to ``DENY``.

    ``checks`` is always stored as a tuple so the result is stable and
    hashable. ``decision`` must be one of the four supported decision outcomes;
    an unsupported value fails closed with ``ValueError``.
    """

    valid: bool
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

    @classmethod
    def passed(
        cls, reason: str, checks: Iterable[VerificationCheck] = ()
    ) -> "VerificationResult":
        """Build a result from checks that are expected to pass.

        The result is valid only when every recorded check passed (an empty
        ``checks`` is treated as valid). If any check failed, the result fails
        closed to ``valid=False`` and ``DENY``. ``reason`` is preserved
        unchanged and ``checks`` is stored as a tuple.
        """
        checks = tuple(checks)
        valid = all(check.passed for check in checks)
        return cls(
            valid=valid,
            decision=ALLOW if valid else DENY,
            reason=reason,
            checks=checks,
        )

    @classmethod
    def failed(
        cls,
        reason: str,
        checks: Iterable[VerificationCheck] = (),
        decision: str = DENY,
    ) -> "VerificationResult":
        """Build an invalid result that fails closed.

        ``valid`` is always ``False``. ``decision`` defaults to ``DENY`` but may
        be ``REQUIRE_HUMAN_APPROVAL`` or ``REQUIRE_HUMAN_REVIEW`` for outcomes
        that are not a hard deny. ``reason`` is preserved unchanged and
        ``checks`` is stored as a tuple.
        """
        return cls(
            valid=False,
            decision=decision,
            reason=reason,
            checks=tuple(checks),
        )
