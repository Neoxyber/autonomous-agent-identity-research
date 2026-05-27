# Roadmap

This roadmap describes the planned research path for the repository.

The project will grow in stages. Each stage should produce clear documents, specifications, tests, or evidence before the next stage begins.

## Current phase

Research foundation.

## Phase 1. Research foundation

Define the basic research foundation.

Expected outputs:
README.md
docs/principles.md
docs/problem-statement.md
docs/research-questions.md
docs/scope.md
docs/references.md
evidence/research-log.md

Completion condition:
A reader can understand the purpose of the repository, the research problem, the initial questions, the scope, and the reference process.

## Phase 2. Identity model

Define the complete identity model for autonomous agents.

Expected outputs:
docs/identity-layer.md
docs/permission-model.md
docs/human-approval-model.md
docs/revocation-model.md
docs/decentralized-verification.md
docs/audit-model.md
docs/evaluation-method.md
docs/limitations.md

Completion condition:
A reader can understand what an agent identity contains, how it is linked to an operator, what the agent is allowed to do, what it is not allowed to do, how revocation works, and how verification can happen outside the issuing system.

## Phase 3. Research records

Add formal research record structures.

Expected outputs:
docs/rdr/
docs/etl/

Completion condition:
Major design decisions are recorded as Research Decision Records, and empirical tests are recorded as Empirical Testing Logs.

## Phase 4. Specifications

Define the first machine-readable schemas.

Expected outputs:
specs/agent-passport.schema.json
specs/capability-policy.schema.json
specs/prohibited-actions.schema.json
specs/revocation-status.schema.json
specs/audit-event.schema.json

Completion condition:
The identity model can be expressed as inspectable schemas that can later be used by the reference implementation.

## Phase 5. Reference implementation

Build a minimal reference implementation.

Expected outputs:
src/
tests/
requirements.txt
.github/workflows/ci.yml

Completion condition:
The implementation can create, verify, revoke, and evaluate an autonomous agent passport in a controlled research setting.

## Phase 6. Evaluation

Run controlled tests against the reference implementation.

Expected tests:
offline verification
passport tamper detection
allowed action enforcement
prohibited action denial
human approval decision flow
revocation enforcement
audit event generation

Completion condition:
Each test has a recorded method, result, and evidence trail.

## Phase 7. Review and future work

Review limitations, unresolved questions, and possible future research directions.

Possible future areas:
runtime workload identity
agent-to-agent delegation
supply-chain binding
decentralized registries
operator identity assurance
formal verification
cross-organization verification
