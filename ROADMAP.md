# Roadmap

This roadmap defines the staged research and implementation path for autonomous agent identity.

Foundation rule:

No passport, no meaningful agent action.

An autonomous agent may reason, plan, and prepare action requests, but protected external action depends on valid identity, permission scope, revocation status, human oversight rules, and audit evidence.

## Current focus

The project is building the local verifier foundation. The first passport schema, validation tests, canonicalization helper, payload hash helper, and verification result model are in place.

Next implementation step:

- Add local passport verifier skeleton.

Near-term scope remains narrow. Signature verification, post-quantum signing, revocation infrastructure, policy evaluation, managed storage, deployment, blockchain anchoring, and external tool protocols are deferred until the local verifier foundation is structured and tested.

Working rule:

- One topic.
- One focused change.
- One clean commit.

## Phase 1. Research foundation

Status: complete.

Purpose: establish a research-first repository with clear scope, contribution expectations, security reporting, evidence discipline, and reference handling.

Completed scope: repository structure, scope, principles, problem statement, research questions, reference process, security policy, contribution policy, and research log.

## Phase 2. Identity and control model

Status: complete for the current research foundation.

Purpose: define the conceptual model for identity-bound autonomous agent action.

Completed scope: identity layer, permission model, human oversight model, revocation model, decentralized verification model, audit model, post-quantum readiness model, evaluation method, and limitations.

## Phase 3. Agent passport specification

Status: complete for the first version.

Purpose: define the first machine-readable identity contract for an autonomous agent passport.

Completed scope: passport schema using JSON Schema Draft 2020-12, minimal passport example, two-part passport/proofs envelope, internal AAID URNs, detached proof metadata, deterministic public key objects, four decision outcomes, and four risk classes.

Deferred: DID support, verifiable credential binding, production trust framework, and legal compliance claims.

## Phase 4. Schema validation

Status: complete for the current schema.

Purpose: prove that the first passport schema and minimal example can be validated locally.

Completed scope: pinned development validation requirements, pytest, jsonschema, positive validation tests, and negative validation tests.

## Phase 5. Canonicalization and payload hash foundation

Status: complete for the current scope.

Purpose: make passport payload hashing deterministic before signature verification is introduced.

Completed scope: canonicalization rules, canonicalization helper, passport payload hash helper, detached proofs excluded by API boundary, SHA-256/SHA-384/SHA-512 payload hash support, and fail-closed handling for unsupported hash algorithms.

Deferred: full independent RFC 8785 implementation claim, signature verification, and signing implementation.

## Phase 6. Local verifier foundation

Status: in progress.

Purpose: provide a local verification path that can reject malformed or unsupported passport envelopes before any protected action is considered.

Completed scope: verification result model, immutable verification checks, immutable verification result, fail-closed decision validation, and shared decision constants.

Next scope: envelope structure checks, passport presence checks, proof metadata presence checks, schema validation check, payload hash validation check, and clear result reporting through the verification result model.

Deferred: signature verification, post-quantum signing, issuer trust registry, revocation infrastructure, and policy evaluation.

## Phase 7. Strict raw JSON parsing

Status: planned.

Purpose: reject unsafe or ambiguous raw JSON before verification.

Planned scope: malformed JSON rejection, duplicate JSON key rejection, non-object envelope rejection, non-object passport payload rejection, and tests for parser failure modes.

## Phase 8. Proof and signature verification path

Status: planned.

Purpose: create a verification path without locking the project to one signing algorithm too early.

Planned scope: algorithm agility, proof metadata validation, payload hash validation, signature verification abstraction, trusted issuer key lookup, key purpose validation, key status validation, and clear unsupported-algorithm failures.

## Phase 9. Policy decision engine

Status: planned.

Purpose: separate identity verification from action permission.

Planned scope: default deny, prohibited action denial, revoked/expired/suspended/compromised agent denial, approval-required action handling, review-required action handling, and high-risk action oversight.

Rule: tool access alone is not authority.

## Phase 10. Revocation and lifecycle enforcement

Status: planned.

Purpose: ensure an agent can lose authority after issuance.

Planned scope: passport status, agent lifecycle status, issuer status, key status, operator status, delegation status, stale heartbeat handling, and signed revocation feeds later.

Rule: revocation is checked outside the agent.

## Phase 11. Action gateway

Status: planned.

Purpose: make the gateway the only path to protected action.

Planned scope: action request, passport verification, policy evaluation, human oversight trigger, approved tool call, and audit/behaviour evidence.

Rule: a powerful agent must not bypass policy through direct tool access.

## Phase 12. Audit and behaviour evidence

Status: planned.

Purpose: record formal decisions and runtime behaviour after identity exists.

Planned scope: audit event schema, behaviour event model, passport-issued event, action-requested event, tool-call event, human-oversight event, revocation event, and privacy-minimized evidence.

Rule: no passport, no trusted behaviour record.

## Phase 13. Tamper-evident evidence chain

Status: planned.

Purpose: make audit and behaviour evidence tamper-evident.

Planned scope: canonical event, event hash, previous event hash, batch hash, signed batch, and optional external hash anchor later.

Rules: use the term tamper-evident, not tamper-proof. Public anchors must not contain raw logs, prompts, secrets, private data, or full operational content.

## Phase 14. Continuous identity heartbeat

Status: planned.

Purpose: keep identity and runtime state observable without destroying agent autonomy.

Planned scope: agent identifier, passport identifier, session identifier, runtime identifier, timestamp, current status, last decision identifier, and last event hash.

Rule: heartbeat monitors liveness and state; action authorization remains at the gateway.

## Phase 15. Runtime isolation and abuse control

Status: planned.

Purpose: ensure a compromised or malicious agent cannot bypass identity controls or abuse registration.

Planned scope: no direct protected tool credentials, no direct protected tool calls, no direct audit-log writes, no self-modification of passport or revocation state, external kill switch, limited filesystem/network access, operator registration, issuer trust, quotas, rate limits, and abuse monitoring.

## Phase 16. Operator verification readiness

Status: planned.

Purpose: support future binding between agents and verified people or legal entities.

Planned scope: person operator readiness, legal entity operator readiness, company registry readiness, EU Digital Identity Wallet readiness, verifiable credential readiness, trusted issuer attestations, and privacy-minimized verification evidence.

Rule: operator verification is a future trust-strengthening layer, not a first-version dependency.

## Phase 17. Delegation and agent-to-agent verification

Status: planned.

Purpose: support many agents, sub-agents, and agent-to-agent interactions without losing accountability.

Planned scope: parent passport, child/delegated passport, scope narrowing, short expiry, delegation revocation, sender passport verification, receiver policy check, and inter-agent audit event.

Rule: a child agent must never receive broader authority than the parent authority.

## Phase 18. Cell-based trust and scale model

Status: planned.

Purpose: support many agents without one fragile central control point.

Planned scope: root trust policy, issuer cells, operator cells, agent passport cells, local verifiers, signed revocation feeds, local audit chains, and optional external anchors.

Rule: compromised cells should be isolated without compromising all agents.

## Phase 19. Tool identity and supply-chain binding

Status: planned.

Purpose: bind agent authority to trusted tools, code, model references, and runtime context.

Planned scope: tool identity, tool manifest hash, tool risk class, agent build hash, model reference, dependency manifest hash, runtime identifier, deployment identifier, and attestation reference later.

## Phase 20. Post-quantum signing experiments

Status: planned.

Purpose: test post-quantum readiness after the verification pipeline is structurally correct.

Planned scope: ML-DSA passport signing/verification experiments, SLH-DSA backup signature experiment, dual proof passports, signed revocation lists, signed audit/behaviour batches, signature size comparison, verification latency tests, and algorithm migration tests.

Rule: ML-KEM is reserved for future key establishment work, not passport signing.

## Phase 21. Local autonomous agent lab

Status: planned.

Purpose: create a controlled dummy agent runtime.

Planned scope: public dummy text reading, dummy document summarization, dummy low-risk classification, external message request simulation, prohibited action attempt, approval-required action attempt, and revoked-action attempt.

Rule: the agent may reason and plan, but protected action depends on gateway approval.

## Phase 22. Managed demo storage

Status: planned.

Purpose: store controlled demo data.

Planned scope: agents, agent passports, agent sessions, revocation status, audit events, behaviour events, human oversight events, and signed batches.

Rules: use dummy data only. Managed storage should not contain private keys, service role keys, production data, or unnecessary personal data.

## Phase 23. Controlled live deployment

Status: planned.

Purpose: deploy a controlled live demo after local verification and gateway foundations work.

Planned scope: local tests first, local API first, local UI first, secrets outside the repo, controlled deployment configuration, separated demo environment, and logs that do not expose secrets.

## Phase 24. External protocol boundary

Status: planned.

Purpose: define how external tool protocols are introduced safely.

Planned scope: external tool protocols deferred until local verifier/gateway/isolation/audit boundaries exist, read-only access first, least-privilege tool access, manual review before protocol servers, and protocol servers treated as code dependencies.

## Phase 25. Live researcher demo

Status: planned.

Purpose: show the system working in real time.

Planned flow: create dummy operator, create dummy agent, issue passport, start session, show heartbeat, try allowed action, try prohibited action, request approval-required action, revoke passport, deny action after revocation, show audit/behaviour timeline, and show tamper-evident chain break.

Expected result: researchers can see that agent autonomy is preserved for reasoning, while protected external action is identity-bound, permission-scoped, revocable, isolated, and auditable.

## Near-term implementation order

1. Add local passport verifier skeleton.
2. Add schema validation into verifier.
3. Add payload hash verification.
4. Add strict raw JSON duplicate-key parser.
5. Add trust anchor model.
6. Add revocation check model.
7. Add action request and policy evaluation.
8. Add audit event schema.
