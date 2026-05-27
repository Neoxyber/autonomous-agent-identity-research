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
