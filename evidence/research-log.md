# Research Log

## Purpose

This file records the chronological progress of the autonomous agent identity research project.

The research log is used to track meaningful project steps, not every small edit. It records what changed, why it changed, which files were affected, and what the next step is.

Detailed design decisions will be recorded separately in Research Decision Records when the project reaches that stage. Empirical tests and benchmark results will be recorded separately in Empirical Testing Logs when implementation and testing begin.

## Entry 001

Date: 2026-05-27

Type: Foundation

Summary: Created the initial public research repository for autonomous agent identity.

Reason: The project needs a clean, reviewable, and long-term structure before implementation begins.

Files created:
README.md
ROADMAP.md
SECURITY.md
CITATION.cff
LICENSE
docs/principles.md
docs/problem-statement.md
docs/research-questions.md
docs/scope.md
docs/references.md
evidence/research-log.md

Decision:
The repository will be research-first. The implementation will be added later as a reference implementation after the initial identity model is defined.

Next step:
Complete the first signed commit for the research foundation.

## Entry 002

Date: 2026-05-27

Type: Research model

Summary: Added the first identity layer model for autonomous agents.

Reason: The project needs a clear identity model before later work on enforcement, revocation, audit, schemas, and reference implementation.

Files created:
docs/identity-layer.md

Files updated:
evidence/research-log.md

Decision:
The first identity layer model defines the agent passport, operator accountability, explicit permissions, explicit prohibitions, human approval requirements, lifecycle status, revocation reference, global verification, decentralized verification, post-quantum readiness, and audit evidence.

Next step:
Define the permission model.

## Entry 003

Date: 2026-05-27

Type: Research model

Summary: Added the initial permission model for autonomous agent identity.

Reason: The identity layer needs a clear model for allowed actions, approval-required actions, prohibited actions, default-deny behaviour, and explainable decisions.

Files created:
docs/permission-model.md

Files updated:
evidence/research-log.md

Decision:
The first permission model uses three outcomes: ALLOW, DENY, and REQUIRE_HUMAN_APPROVAL.

Next step:
Define the human oversight model.

## Entry 004

Date: 2026-05-28

Type: Research model

Summary: Added the initial human oversight model for autonomous agent identity.

Reason: The permission model needs a clear approach for actions that require human approval, human review, escalation, pause, intervention, and audit evidence.

Files created:
docs/human-oversight-model.md

Files updated:
evidence/research-log.md

Decision:
The model uses four outcomes: ALLOW, DENY, REQUIRE_HUMAN_APPROVAL, and REQUIRE_HUMAN_REVIEW. Human approval cannot override prohibited actions or allow revoked, expired, suspended, or compromised agents to act.

Next step:
Define the revocation model.

## Entry 005

Date: 2026-05-28

Type: Research model

Summary: Added the initial revocation model for autonomous agent identity.

Reason: The identity model needs a clear way to remove an agent from trust, pause unsafe activity, handle compromise, expire identities, rotate trust material, and support future emergency stop research.

Files created:
docs/revocation-model.md

Files updated:
evidence/research-log.md

Decision:
The model treats revocation as part of identity. A revoked, expired, suspended, or compromised agent should not be allowed to act.

Next step:
Define the decentralized verification model.

## Entry 006

Date: 2026-05-28

Type: Research model

Summary: Added the initial decentralized verification model for autonomous agent identity.

Reason: The identity system needs a clear way to support portable verification, offline and online checks, revocation evidence, trust material resolution, DID research, and future evidence anchoring without depending unnecessarily on one central runtime system.

Files created:
docs/decentralized-verification.md

Files updated:
evidence/research-log.md

Decision:
The model prioritizes portable verification first. DID support is treated as phased research, with did:web and did:key as early candidates. Blockchain is treated as optional research for evidence anchoring, not as a required foundation.

Next step:
Define the audit model.

## Entry 007

Date: 2026-05-28

Type: Research model

Summary: Added the initial audit model for autonomous agent identity.

Reason: The identity system needs a clear evidence model for action decisions, lifecycle changes, human oversight, revocation review, incident response, and future compliance mapping.

Files created:
docs/audit-model.md

Files updated:
evidence/research-log.md

Decision:
The audit model treats audit evidence as part of the trust system, not only as debugging output. It records decision evidence, lifecycle evidence, human oversight evidence, available status evidence, and tamper-evidence direction.

Next step:
Define the evaluation method.

## Entry 008

Date: 2026-05-28

Type: Security model

Summary: Added the initial post-quantum readiness model for autonomous agent identity.

Reason: The identity system needs a clear top-level security model for long-term verification, post-quantum signatures, hybrid transition, key rotation, algorithm migration, and cryptographic agility.

Files created:
docs/post-quantum-readiness.md

Files updated:
evidence/research-log.md

Decision:
The model treats post-quantum readiness as a design requirement, not a marketing claim. The first research direction uses ML-DSA as the primary passport signature candidate, SLH-DSA as an independent backup signature family, ML-KEM as a future key establishment candidate, and cryptographic agility as a mandatory design property.

Next step:
Define the evaluation method.

## Entry 009

Date: 2026-05-28

Type: Research method

Summary: Added the initial evaluation method for autonomous agent identity research.

Reason: The project needs a clear way to test the research models, record pass and fail results, identify blocked areas, and decide what needs improvement before implementation expands.

Files created:
docs/evaluation-method.md

Files updated:
evidence/research-log.md

Decision:
The evaluation method uses PASS, FAIL, PARTIAL, BLOCKED, and NEEDS_RESEARCH result categories. Detailed test results will later be recorded in Empirical Testing Logs.

Next step:
Define the research limitations.

## Entry 010

Date: 2026-05-28

Type: Research boundary

Summary: Added the initial research limitations document.

Reason: The project needs a clear statement of what the research does not yet prove, what has not been implemented, what does not claim legal compliance, and what still needs testing and review.

Files created:
docs/limitations.md

Files updated:
evidence/research-log.md

Decision:
The limitations document states that the repository is research-stage work and does not claim production readiness, legal compliance, final standardization, or production cryptographic security.

Next step:
Review the research model set before starting specifications.
