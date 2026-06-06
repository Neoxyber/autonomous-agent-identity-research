# Documentation Index

## Purpose

This is the central index for the project documentation.

It is designed to work like a table of contents. It helps researchers,
students, security experts, and contributors understand the research areas,
reading order, and current boundaries.

## Start here

Read these first:

1. `00-foundation/principles.md`
2. `00-foundation/problem-statement.md`
3. `00-foundation/scope.md`
4. `00-foundation/research-questions.md`
5. `00-foundation/limitations.md`
6. `50-standards-positioning/standards-positioning.md`
7. `00-foundation/documentation-organization-plan.md`

## Chapters

### 00 Foundation

Purpose, scope, limitations, research questions, and evaluation method.

Files:

- `00-foundation/principles.md`
- `00-foundation/problem-statement.md`
- `00-foundation/research-questions.md`
- `00-foundation/scope.md`
- `00-foundation/limitations.md`
- `00-foundation/evaluation-method.md`

### 10 Models

Core autonomous agent identity research models.

Files:

- `10-models/identity-layer.md`
- `10-models/permission-model.md`
- `10-models/human-oversight-model.md`
- `10-models/revocation-model.md`
- `10-models/decentralized-verification.md`
- `10-models/audit-model.md`
- `10-models/post-quantum-readiness.md`

### 20 Threat Boundaries

Threat model and trust-boundary research.

Files:

- `20-threat-boundaries/agent-passport-threat-model-and-trust-boundaries.md`

### 30 Canonicalization

Canonicalization planning, candidate evaluation, and adoption-readiness evidence.

Suggested reading order:

1. `30-canonicalization/canonicalization-candidate-matrix.md`
2. `30-canonicalization/canonicalization-isolated-evaluation-plan.md`
3. `30-canonicalization/canonicalization-evaluation-results-template.md`
4. `30-canonicalization/canonicalization-evaluation-results-ref014-rfc8785-0.1.4.md`
5. `30-canonicalization/canonicalization-evaluation-results-ref015-jcs-0.2.1.md`
6. `30-canonicalization/canonicalization-candidate-comparison-ref014-ref015.md`
7. `30-canonicalization/canonicalization-number-serialization-gate-ref014-ref015.md`
8. `30-canonicalization/canonicalization-parse-and-payload-domain-gate.md`
9. `30-canonicalization/canonicalization-candidate-decision-readiness.md`
10. `30-canonicalization/canonicalization-ref014-provenance-verification-plan.md`
11. `30-canonicalization/canonicalization-ref014-provisional-integration-plan.md`

Current status: REF-014 adoption is deferred. Canonicalizer replacement,
requirements changes, lockfile changes, and real signature verification remain
separate future decisions.

### 40 Signature Verification

Signature-verification planning, ML-DSA runtime research, vector evidence,
profile scope, and implementation-boundary planning.

Suggested reading order:

1. `40-signature-verification/signature-verification-planning.md`
2. `40-signature-verification/signature-verification-runtime-research.md`
3. `40-signature-verification/signature-verification-isolated-experiment-plan.md`
4. `40-signature-verification/signature-runtime-evaluation-results-cryptography-48.0.0.md`
5. `40-signature-verification/signature-runtime-artifact-evidence-cryptography-48.0.0.md`
6. `40-signature-verification/signature-test-vector-compatibility-plan.md`
7. `40-signature-verification/signature-test-vector-format-inspection-mldsa-fips204.md`
8. `40-signature-verification/signature-test-vector-execution-results-cryptography-48.0.0-mldsa65-sigver.md`
9. `40-signature-verification/signature-test-vector-hashalg-internal-mapping-plan.md`
10. `40-signature-verification/signature-test-vector-hashalg-source-review.md`
11. `40-signature-verification/signature-proof-profile-initial-scope.md`
12. `40-signature-verification/signature-verification-implementation-boundary-plan.md`

Current status: the first future signature profile is scoped to ML-DSA-65 pure
direct external message-mode verification. Real signature verification is not
implemented, dependency adoption is not approved, and the verifier cannot return
`ALLOW`.

### 50 Standards Positioning

External ecosystem positioning and standards-alignment research.

Files:

- `50-standards-positioning/standards-positioning.md`

## References

The central reference register stays at:

- `references.md`

## Evidence

Evidence logs stay outside `docs/`:

- `../evidence/research-log-archive-001.md`
- `../evidence/research-log-archive-002.md`
- `../evidence/research-log.md`

Evidence is chronological and should not be reorganized by topic.

## Current non-goals

This index does not claim production readiness, legal compliance,
certification, real signature verification, gateway integration, cloud
deployment readiness, or passport-verifier `ALLOW` behavior.

## Maintenance rule

When new research areas become large enough, add a new chapter folder and update
this index. Avoid empty folders and avoid unnecessary documents.
