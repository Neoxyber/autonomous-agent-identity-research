"""Shared, deterministic test constants for the verifier test suite.

The minimal example passport is valid over the half-open window
``[2026-05-29T00:00:00Z, 2026-06-29T00:00:00Z)``. ``VALID_NOW`` is a fixed,
timezone-aware UTC instant inside that window. Verifier tests inject it as the
``now`` argument so their outcomes do not depend on the real wall clock.

``TRUSTED_ISSUERS`` is the explicit issuer-trust configuration tests inject as
the ``trusted_issuers`` argument when they intentionally exercise checks beyond
``lifecycle_status_allows_verification``. It holds only the minimal example's
``issuer_id`` and is frozen so a test cannot mutate it and leak state.

``FRESH_STATUS`` is the good caller-provided revocation status evidence bound to
the minimal example. Tests inject it as the ``revocation_status`` argument when
they intentionally exercise checks beyond ``issuer_trusted``. Its identity
fields match the example's ``revocation.status_reference``, ``passport_id``, and
``issuer_id`` (which is also in ``TRUSTED_ISSUERS``), its freshness window
``[2026-06-14T00:00:00Z, 2026-06-16T00:00:00Z)`` straddles ``VALID_NOW`` so that
``produced_at <= VALID_NOW < valid_until``, and its ``status`` is ``active``.
All values are flat strings, so a negative test that needs a tampered variant
must build a copy (for example ``{**FRESH_STATUS, "status": "revoked"}``) rather
than mutating the shared constant.
"""

from datetime import datetime, timezone
from pathlib import Path

VALID_NOW = datetime(2026, 6, 15, 0, 0, 0, tzinfo=timezone.utc)

TRUSTED_ISSUERS = frozenset({"urn:aaid:issuer:aixybertech-issuer"})

FRESH_STATUS = {
    "status_reference": "urn:aaid:revocation:018fd7c2-9d55-7a11-8a22-24b1e3f92310",
    "passport_id": "urn:aaid:passport:018fd7c2-6f1e-7a4e-9b18-3d7a9d93c111",
    "status_authority": "urn:aaid:issuer:aixybertech-issuer",
    "produced_at": "2026-06-14T00:00:00Z",
    "valid_until": "2026-06-16T00:00:00Z",
    "status": "active",
}

_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = _ROOT / "specs" / "examples" / "agent-passport.minimal.json"

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
