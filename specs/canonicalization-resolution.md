# Canonicalization Resolution Path

## Purpose

This document compares the available paths for resolving the canonicalization
compatibility gap before real signature verification is implemented.

It is a planning and decision-support artifact. It does not add code,
dependencies, or cryptographic verification, and it does not change the verifier
boundary.

## Current blocker

The project declares `json-canonicalization-scheme` as a long-term target
related to the JSON Canonicalization Scheme and RFC 8785.

The current research helper produces deterministic bytes for the current
passport profile, but it is not a complete independent RFC 8785 implementation.
Its tests document current-profile behaviour only and do not establish full
RFC 8785 compatibility.

The current helper also does not yet define a full I-JSON validation boundary,
including duplicate object member key rejection and RFC 8785-compatible number
handling. These remain future compatibility-test concerns, not current
guarantees.

Real signature verification is blocked until this gap is resolved. The verifier
remains fail-closed and returns DENY; it records canonicalization and signature
preparation checks but performs no real signature verification.

## Resolution options

### Option A: Adopt a reviewed RFC 8785-compatible canonicalization

Replace the helper's canonicalization with a reviewed, maintained implementation
that targets RFC 8785 / JSON Canonicalization Scheme, after a separate
dependency review and compatibility test plan.

### Option B: Constrain the passport profile

Keep the current helper and constrain the allowed passport input set, for
example the value types, character ranges, and ordering already exercised by the
current profile, so the helper remains valid for every accepted passport.

### Option C: Rename the declared canonicalization scheme

Rename the declared scheme so it no longer implies full RFC 8785 / JCS
compatibility, and describe the exact canonical form the project actually
produces.

## Comparison matrix

| Dimension | A: Adopt JCS-compatible | B: Constrain profile | C: Rename scheme |
| --- | --- | --- | --- |
| Security strength | Strongest; based on a reviewed standard, reducing canonicalization-confusion risk | Moderate; safe only within the constrained profile | Unchanged; relabels the gap without closing it |
| Interoperability | Highest; aligns with common RFC 8785 verifiers | Limited; other parties must accept the same constraints | Low; a project-specific scheme is not portable by default |
| Implementation risk | Higher upfront; integrate and validate a third-party implementation | Lower; tighten validation, no new canonicalizer | Lowest; naming and description change only |
| Testing burden | Highest; known-vector and compatibility tests | Moderate; profile-boundary and rejection tests | Low; naming-consistency tests |
| Dependency risk | Introduces a dependency needing review and maintenance | None | None |
| Schema / example / verifier impact | Verifier canonicalizer changes; allowlist may extend | Schema tightens; example must fit the profile | Schema enum, verifier allowlist, and example rename in lockstep |
| Suitability for future real signature verification | Best; gives a reviewed canonical form to sign and verify over | Conditional; acceptable only while inputs stay in profile | Insufficient alone; defers the underlying problem |

## Recommended path

The preferred long-term path is Option A: evaluate and later adopt a reviewed
RFC 8785-compatible canonicalization implementation before trusted real
signature verification.

This recommendation does not change the current state:

1. Option A is not implemented in this step.
2. No dependency is adopted in this step.
3. No RFC 8785 / JCS compatibility is claimed in this step.
4. The current helper remains acceptable only for local research tests and
   deterministic current-profile regression tests.
5. Real signature verification remains blocked.

Candidate implementations require a later dependency review and a compatibility
test plan before adoption. If Option A is not adopted, the project must instead
apply Option B (constrain the profile) or Option C (rename the scheme) so the
declared scheme does not imply a compatibility the implementation does not
provide.

The chosen canonical form should remain independent of the signature algorithm,
so future signature-scheme changes, including post-quantum rotation, do not
require redefining the canonical payload.

## Required future tests

A later compatibility test plan should cover, at a high level:

1. RFC 8785 / JCS known answer vectors.
2. I-JSON input constraints.
3. Duplicate object member key rejection strategy.
4. Number serialization behaviour.
5. String escaping and control characters.
6. Unicode and non-ASCII object member ordering.
7. Nested object member ordering.
8. Array order preservation.
9. A minimal passport regression vector.
10. Comparison across candidate implementations.

## Non-goals for this step

This step does not add code, dependencies, schema changes, examples, real
cryptographic verification, post-quantum signing, issuer trust, revocation,
policy evaluation, a runtime gateway, or cloud or network integrations.

## Next step after this document

A later, separate step should evaluate candidate RFC 8785-compatible
implementations and design the compatibility test plan outlined above. That
evaluation is out of scope for this document.
