# Documentation Index

## Purpose

This is the central index for the research documentation.

It works like a table of contents. It helps researchers, students, security reviewers, and contributors understand the reading order, research areas, and current boundaries.

## Start here

Read these first:

1. [Principles](00-foundation/principles.md)
2. [Problem Statement](00-foundation/problem-statement.md)
3. [Scope](00-foundation/scope.md)
4. [Research Questions](00-foundation/research-questions.md)
5. [Limitations](00-foundation/limitations.md)
6. [Standards Positioning](50-standards-positioning/standards-positioning.md)

## Chapters

### 00 Foundation

Purpose, scope, limitations, research questions, and evaluation method.

Files:

1. [Principles](00-foundation/principles.md)
2. [Problem Statement](00-foundation/problem-statement.md)
3. [Research Questions](00-foundation/research-questions.md)
4. [Scope](00-foundation/scope.md)
5. [Limitations](00-foundation/limitations.md)
6. [Evaluation Method](00-foundation/evaluation-method.md)

### 10 Models

Core autonomous agent identity research models.

Files:

1. [Identity Layer](10-models/identity-layer.md)
2. [Permission Model](10-models/permission-model.md)
3. [Human Oversight Model](10-models/human-oversight-model.md)
4. [Revocation Model](10-models/revocation-model.md)
5. [Decentralized Verification](10-models/decentralized-verification.md)
6. [Audit Model](10-models/audit-model.md)
7. [Post-Quantum Readiness](10-models/post-quantum-readiness.md)

### 20 Threat Boundaries

Threat model and trust-boundary research.

Files:

1. [Agent Passport Threat Model and Trust Boundaries](20-threat-boundaries/agent-passport-threat-model-and-trust-boundaries.md)

### 30 Canonicalization

Canonicalization planning, candidate evaluation, and adoption-readiness evidence.

Suggested reading order:

1. [Candidate Matrix](30-canonicalization/canonicalization-candidate-matrix.md)
2. [Isolated Evaluation Plan](30-canonicalization/canonicalization-isolated-evaluation-plan.md)
3. [Evaluation Results Template](30-canonicalization/canonicalization-evaluation-results-template.md)
4. [REF-014 Evaluation Results](30-canonicalization/canonicalization-evaluation-results-ref014-rfc8785-0.1.4.md)
5. [REF-015 Evaluation Results](30-canonicalization/canonicalization-evaluation-results-ref015-jcs-0.2.1.md)
6. [Candidate Comparison](30-canonicalization/canonicalization-candidate-comparison-ref014-ref015.md)
7. [Number Serialization Gate](30-canonicalization/canonicalization-number-serialization-gate-ref014-ref015.md)
8. [Parse and Payload Domain Gate](30-canonicalization/canonicalization-parse-and-payload-domain-gate.md)
9. [Candidate Decision Readiness](30-canonicalization/canonicalization-candidate-decision-readiness.md)
10. [REF-014 Provenance Verification Plan](30-canonicalization/canonicalization-ref014-provenance-verification-plan.md)
11. [REF-014 Provisional Integration Plan](30-canonicalization/canonicalization-ref014-provisional-integration-plan.md)

Current status: REF-014 adoption is deferred. Canonicalizer replacement, requirements changes, lockfile changes, and real signature verification remain separate future decisions.

### 40 Signature Verification

Signature-verification planning, ML-DSA runtime research, vector evidence, profile scope, and implementation-boundary planning.

Suggested reading order:

1. [Signature Verification Planning](40-signature-verification/signature-verification-planning.md)
2. [Runtime Research](40-signature-verification/signature-verification-runtime-research.md)
3. [Isolated Experiment Plan](40-signature-verification/signature-verification-isolated-experiment-plan.md)
4. [Runtime Evaluation Results](40-signature-verification/signature-runtime-evaluation-results-cryptography-48.0.0.md)
5. [Runtime Artifact Evidence](40-signature-verification/signature-runtime-artifact-evidence-cryptography-48.0.0.md)
6. [Test Vector Compatibility Plan](40-signature-verification/signature-test-vector-compatibility-plan.md)
7. [Test Vector Format Inspection](40-signature-verification/signature-test-vector-format-inspection-mldsa-fips204.md)
8. [Test Vector Execution Results](40-signature-verification/signature-test-vector-execution-results-cryptography-48.0.0-mldsa65-sigver.md)
9. [Hash Algorithm and Internal Mapping Plan](40-signature-verification/signature-test-vector-hashalg-internal-mapping-plan.md)
10. [Hash Algorithm Source Review](40-signature-verification/signature-test-vector-hashalg-source-review.md)
11. [Initial Proof Profile Scope](40-signature-verification/signature-proof-profile-initial-scope.md)
12. [Implementation Boundary Plan](40-signature-verification/signature-verification-implementation-boundary-plan.md)

Current status: the first future signature profile is scoped to ML-DSA-65 pure direct external message-mode verification. Real signature verification is not implemented, dependency adoption is not approved, and the verifier cannot return `ALLOW`.

### 50 Standards Positioning

External ecosystem positioning and standards-alignment research.

Files:

1. [Standards Positioning](50-standards-positioning/standards-positioning.md)

## References

The central reference register stays at:

1. [References](references.md)

## Evidence

Evidence logs stay outside `docs/`:

1. [Research Log Archive 001](../evidence/research-log-archive-001.md)
2. [Research Log Archive 002](../evidence/research-log-archive-002.md)
3. [Research Log Archive 003](../evidence/research-log-archive-003.md)
4. [Current Research Log](../evidence/research-log.md)

Evidence is chronological and must not be reorganized by topic.

## Current boundaries

This index does not present the research as production ready, legally ready, certified, signature-verifying, gateway-integrated, cloud-deployment ready, or able to return passport-verifier `ALLOW`.

## Maintenance rule

When a research area becomes large enough, add a focused chapter folder and update this index.

Avoid empty folders and unnecessary documents.
