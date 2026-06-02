"""Shared, deterministic test constants for the verifier test suite.

The minimal example passport is valid over the half-open window
``[2026-05-29T00:00:00Z, 2026-06-29T00:00:00Z)``. ``VALID_NOW`` is a fixed,
timezone-aware UTC instant inside that window. Verifier tests inject it as the
``now`` argument so their outcomes do not depend on the real wall clock.

``TRUSTED_ISSUERS`` is the explicit issuer-trust configuration tests inject as
the ``trusted_issuers`` argument when they intentionally exercise checks beyond
``lifecycle_status_allows_verification``. It holds only the minimal example's
``issuer_id`` and is frozen so a test cannot mutate it and leak state.
"""

from datetime import datetime, timezone

VALID_NOW = datetime(2026, 6, 15, 0, 0, 0, tzinfo=timezone.utc)

TRUSTED_ISSUERS = frozenset({"urn:aaid:issuer:aixybertech-issuer"})
