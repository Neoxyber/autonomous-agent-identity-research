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
