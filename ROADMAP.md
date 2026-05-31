# Roadmap

This roadmap describes the staged research path for the autonomous agent identity project.

The project studies how autonomous agents can be given verifiable, accountable, permission-scoped, revocable, auditable, and post-quantum-ready identities.

The work is research-stage. It does not claim production readiness, legal compliance, standards compliance, or replacement of existing identity standards.

The roadmap connects the research models, reference implementation, tests, and evidence record into a clear order of work. It is intended to keep the project focused as the repository grows.

## Research direction

The project follows a standards-aligned research direction.

It treats the agent passport as a research envelope for studying autonomous agent identity. The passport is not presented as a new industry standard. Future work may map the model to established or emerging approaches such as verifiable credentials, decentralized identifiers, workload identity, delegated authority, agentic identity and access management, and post-quantum signature systems.

The central research question is how these areas can work together in a fail-closed identity layer for autonomous agents.

The project focuses on the following properties:

1. An autonomous agent should have a visible and verifiable identity.

2. The agent should be linked to a responsible operator.

3. The agent should have explicit permissions and explicit prohibitions.

4. The default decision should be denial.

5. High-risk or uncertain actions should support human approval or human review.

6. A revoked, expired, suspended, or compromised agent should not be allowed to act.

7. Important decisions should produce audit evidence.

8. Verification should not depend unnecessarily on one central service.

9. The model should support long-term cryptographic change, including post-quantum readiness.

## Foundation rule

No verified identity, no protected action.

An autonomous agent may reason, plan, and prepare a request. Protected external action depends on identity verification, issuer trust, lifecycle status, revocation status, permission scope, human oversight requirements, and audit evidence.

Tool access alone is not authority.

## Research method

The project records research claims through documents, tests, and evidence.

Research results should distinguish between:

1. What has passed.

2. What has failed.

3. What is partially supported.

4. What is blocked.

5. What needs more research.

Implementation should remain small and testable. Larger system features should be introduced only after the identity, verification, trust, revocation, policy, oversight, and audit boundaries are clear.

## Phase 0. Research foundation and project hygiene

This phase establishes the repository as a disciplined research project.

Current status: mostly complete.

This phase includes the project scope, principles, problem statement, research questions, evidence process, reference handling, and repository hygiene.

The evidence log records meaningful milestones. Longer empirical results should later be recorded in dedicated testing logs rather than expanding the active research log indefinitely.

Exit condition: the project has a clear research foundation, passing tests, a clean working tree after milestones, and a roadmap that reflects the current direction.

## Phase 1. Standards positioning

This phase explains how the research model relates to existing and emerging identity work.

The goal is not to claim compliance. The goal is to avoid isolated invention and to make the research understandable to reviewers familiar with identity standards and agent security work.

This phase should map the agent passport concepts to relevant areas such as verifiable credentials, decentralized identifiers, workload identity, delegated authority, agentic identity and access management, agent security risks, and post-quantum signature standards.

The mapping should explain where the research aligns with existing work, where it deliberately remains experimental, and which questions remain unresolved.

Exit condition: the README and a concise standards-positioning document describe the project as standards-aligned research without claiming certification, compliance, or production readiness.

## Phase 2. Canonicalization closure

This phase closes the canonicalization question so signature verification can proceed safely.

The project uses a JSON passport envelope. The long-term target for deterministic JSON signing is RFC 8785 / JSON Canonicalization Scheme.

The current helper remains useful for local research regression tests, but trusted signature verification requires a reviewed canonicalization path and external conformance tests.

This phase should avoid further broad planning around canonicalization. The work should move toward reviewed implementation choice, known-answer tests, invalid-input tests, and a stable minimal passport vector.

Exit condition: the selected canonicalization path is recorded, external vectors pass, ambiguous inputs fail safely, and the minimal passport has a stable canonical representation.

## Phase 3. Signature verification foundation

This phase adds the first real signature verification path.

Signature verification should be performed over canonical passport bytes. The implementation should use maintained cryptographic libraries and should remain algorithm-agile.

A valid signature should not by itself authorize action. It only proves that the passport payload has not been modified and that it was signed by a key that may later be evaluated through issuer trust and lifecycle rules.

Exit condition: valid signatures verify, modified passports fail, unsupported algorithms fail closed, and the verifier still denies protected action until trust, revocation, and policy checks are implemented.

## Phase 4. Issuer trust and key lifecycle

This phase defines how a verifier decides whether an issuer and key are trusted.

The research should cover issuer metadata, trust anchors, key identifiers, key purpose, key status, key rotation, and failure behavior for unknown or unsuitable keys.

The system should not treat any syntactically valid key as trusted by default.

Exit condition: trusted issuers and active keys can be recognized, unknown issuers fail closed, retired or rotated keys fail safely, and trust decisions are recorded as evidence.

## Phase 5. Revocation and lifecycle enforcement

This phase ensures that an agent can lose authority after issuance.

The model already defines lifecycle states such as active, suspended, revoked, expired, compromised, rotated, and pending verification. This phase turns those states into enforceable verifier behavior.

The research should include online status checks, signed or cached revocation evidence, short-lived passports, and the limits of offline verification.

Exit condition: revoked, suspended, expired, and compromised agents are denied; offline limitations are documented; and revocation decisions produce audit evidence.

## Phase 6. Permission and policy evaluation

This phase separates verified identity from action authority.

A verified passport does not mean the agent may perform every action. The requested action must be evaluated against allowed actions, prohibited actions, approval-required actions, lifecycle status, revocation status, and policy context.

The default decision remains denial.

Exit condition: allowed actions can proceed only after all earlier gates pass, prohibited actions always deny, approval-required actions return the correct approval outcome, unclear actions return denial or review according to policy, and decision reasons are recorded.

## Phase 7. Human oversight

This phase studies how human approval, review, escalation, pause, and intervention should work.

Human approval is not unlimited authority. It should be specific, attributable, time-bounded, and auditable. It should not override prohibited actions, revocation, expiry, suspension, compromise, or audit requirements.

The research should also study emergency stop behavior and the conditions under which an agent should be paused or prevented from continuing a workflow.

Exit condition: approval and review outcomes are tested, approval cannot override core safety boundaries, approval records expire, replay is prevented, and oversight decisions produce audit evidence.

## Phase 8. Audit evidence

This phase records identity, policy, lifecycle, and oversight decisions in a reviewable form.

Audit evidence should explain what happened, why it happened, which evidence was available at the time, and which decision was made. It should support later review, incident response, research evaluation, and future governance mapping.

The audit model should minimize sensitive data and prefer identifiers, hashes, scopes, references, and decision reasons over raw operational content.

Exit condition: allowed actions, denied actions, approval decisions, review decisions, revocation events, and lifecycle changes produce audit evidence; tampered audit evidence can be detected; and unnecessary sensitive data is avoided.

## Phase 9. Post-quantum research

This phase studies long-term cryptographic readiness.

The project treats post-quantum readiness as a research and design requirement, not a readiness claim. The first research direction includes ML-DSA for signatures, SLH-DSA as an independent backup signature family, and ML-KEM later for key establishment when secure communication becomes in scope.

The project should not implement cryptographic primitives from scratch.

Exit condition: controlled experiments record key sizes, signature sizes, verification latency, passport size impact, failure behavior, key rotation, algorithm migration, and the limits of the current implementation.

## Phase 10. Local research demo

This phase demonstrates the model in a controlled local setting using dummy data only.

The demo should show a complete decision path: issue a dummy passport, verify it, check issuer trust, check revocation, evaluate permissions, require approval where appropriate, deny prohibited actions, deny after revocation, and record audit evidence.

The demo should not use real users, real secrets, production systems, or production data.

Exit condition: a reviewer can run the demo locally and see allowed, denied, approval-required, review-required, and revoked-agent outcomes with audit evidence.

## Phase 11. Controlled deployment research

This phase may begin only after the local research demo is stable.

The goal is to study whether the local model can be exposed safely in a controlled demo environment without weakening the research boundaries.

This phase may consider local APIs, separated demo configuration, controlled hosting, external protocol boundaries, and secret-handling rules. It should not introduce production claims.

Exit condition: deployment scope is documented, secrets remain outside the repository, local tests pass, and no production, legal, or standards-compliance claim is made.

## Deferred research topics

The following topics are important, but should not drive near-term implementation before the core identity and verifier path is stable.

1. Continuous identity heartbeat and runtime state monitoring.

2. Runtime isolation and abuse control.

3. Operator verification and legal-entity binding.

4. Delegation and agent-to-agent verification.

5. Scope narrowing for child or delegated agents.

6. Cell-based trust and scale models.

7. Tool identity and supply-chain binding.

8. Model, tool, dependency, and runtime attestation.

9. External protocol boundaries.

10. Managed demo storage.

11. Transparency logs and timestamp anchoring.

12. Multi-organization verification.

13. Controlled live researcher demo.

These topics should be introduced through small, reviewed research steps after the core verifier, trust, revocation, policy, oversight, and audit path is working.

## Near-term focus

The near-term work should stay narrow.

1. Align the README with the current research stage.

2. Add a concise standards-positioning map.

3. Close canonicalization through external conformance tests.

4. Add signature verification behind a small abstraction.

5. Add issuer trust and key lifecycle checks.

6. Add revocation and lifecycle enforcement.

7. Add permission and policy evaluation.

8. Add audit evidence for each important decision.

9. Build the local dummy demo.

Each step should keep the repository clean, the tests passing, and the research claims limited to what has been implemented, tested, and recorded.
