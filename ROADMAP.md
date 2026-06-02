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

## Phase 2. Verifier trust boundaries

This phase hardens verifier trust boundaries before real signature verification.

The research should cover issuer trust, key selection, key status, key validity,
verification-method binding, lifecycle checks, caller-provided revocation
freshness, and proof-selection hardening.

The system should not treat any syntactically valid issuer, key, proof, or status
record as trusted by default.

Exit condition: issuer trust, active-key selection, selected-key validity,
verification-method binding, revocation freshness, and single-proof enforcement
fail closed and are recorded as verifier checks.

## Phase 3. Canonicalization closure

This phase settles canonicalization before real signature verification.

The current helper remains useful for local research regression tests, but real
signature verification requires a reviewed canonicalization path, external
conformance evidence, fail-closed input handling, and a deliberate golden-vector
migration if canonical bytes change.

Exit condition: the selected canonicalization path is recorded, external vectors
pass for the accepted input domain, ambiguous inputs fail safely, and the
minimal passport has a stable canonical representation.

## Phase 4. Signature verification foundation

This phase adds the first real signature verification path only after verifier
trust boundaries and canonicalization are settled.

Signature verification should be performed over canonical passport bytes. The
implementation should use reviewed cryptographic libraries and should remain
algorithm-agile.

A valid signature should not by itself authorize action. It only proves that the
passport payload has not been modified and that it was signed by a key that is
evaluated through issuer trust, lifecycle, revocation, and policy rules.

Exit condition: valid signatures verify, modified passports fail, unsupported
algorithms fail closed, and the verifier still denies protected action until
permission, approval, and audit policy checks are implemented.

## Phase 5. Permission and policy evaluation

This phase separates verified identity from action authority.

A verified passport does not mean the agent may perform every action. The requested action must be evaluated against allowed actions, prohibited actions, approval-required actions, lifecycle status, revocation status, and policy context.

The default decision remains denial.

Exit condition: allowed actions can proceed only after all earlier gates pass, prohibited actions always deny, approval-required actions return the correct approval outcome, unclear actions return denial or review according to policy, and decision reasons are recorded.

## Phase 6. Human oversight

This phase studies how human approval, review, escalation, pause, and intervention should work.

Human approval is not unlimited authority. It should be specific, attributable, time-bounded, and auditable. It should not override prohibited actions, revocation, expiry, suspension, compromise, or audit requirements.

The research should also study emergency stop behavior and the conditions under which an agent should be paused or prevented from continuing a workflow.

Exit condition: approval and review outcomes are tested, approval cannot override core safety boundaries, approval records expire, replay is prevented, and oversight decisions produce audit evidence.

## Phase 7. Audit evidence

This phase records identity, policy, lifecycle, and oversight decisions in a reviewable form.

Audit evidence should explain what happened, why it happened, which evidence was available at the time, and which decision was made. It should support later review, incident response, research evaluation, and future governance mapping.

The audit model should minimize sensitive data and prefer identifiers, hashes, scopes, references, and decision reasons over raw operational content.

Exit condition: allowed actions, denied actions, approval decisions, review decisions, revocation events, and lifecycle changes produce audit evidence; tampered audit evidence can be detected; and unnecessary sensitive data is avoided.

## Phase 8. Post-quantum research

This phase studies long-term cryptographic readiness.

The project treats post-quantum readiness as a research and design requirement, not a readiness claim. The first research direction includes ML-DSA for signatures, SLH-DSA as an independent backup signature family, and ML-KEM later for key establishment when secure communication becomes in scope.

The project should not implement cryptographic primitives from scratch.

Exit condition: controlled experiments record key sizes, signature sizes, verification latency, passport size impact, failure behavior, key rotation, algorithm migration, and the limits of the current implementation.

## Phase 9. Local research demo

This phase demonstrates the model in a controlled local setting using dummy data only.

The demo should show a complete decision path: issue a dummy passport, verify it, check issuer trust, check revocation, evaluate permissions, require approval where appropriate, deny prohibited actions, deny after revocation, and record audit evidence.

The demo should not use real users, real secrets, production systems, or production data.

Exit condition: a reviewer can run the demo locally and see allowed, denied, approval-required, review-required, and revoked-agent outcomes with audit evidence.

## Phase 10. Controlled deployment research

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

1. Keep the README aligned with the current research stage.

2. Keep standards positioning concise and evidence-based.

3. Maintain verifier trust-boundary checks before any `ALLOW` path.

4. Close canonicalization through isolated candidate evaluation and external
   conformance evidence.

5. Record any canonicalizer adoption decision before requirements, lockfile,
   canonicalizer, or golden-vector changes.

6. Plan real signature verification only after canonicalization is settled.

7. Add permission, approval, and audit evaluation after identity verification
   boundaries are complete.

8. Add audit evidence for each important decision.

9. Build the local dummy demo.

Each step should keep the repository clean, the tests passing, and the research claims limited to what has been implemented, tested, and recorded.
