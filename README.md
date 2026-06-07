# Autonomous Agent Identity Research

## Purpose

This repository is the first research layer of the wider Quantum-Secure Autonomous Gateway research direction.

The project studies how autonomous AI agents can present verifiable identity and action-decision evidence before they are trusted to perform protected actions.

The central rule is simple:

No verified identity and authority evidence, no protected action.

This work is research-stage. It does not claim production readiness, legal compliance, standards compliance, certification, or replacement of existing identity standards.

## Research motivation

We are moving closer to more capable artificial intelligence systems, including the possibility of artificial general intelligence and artificial superintelligence. At the same time, quantum-computing timelines and post-quantum migration deadlines are moving closer.

Autonomous AI agents are also becoming more capable, more advanced, and more widely deployed. They can reason, plan, call tools, interact with software systems, coordinate workflows, and act across organizational boundaries. Future AI systems may become increasingly capable of assisting in the improvement of other systems with less direct human involvement.

This makes autonomous-agent research important now.

Across industry, experts, researchers, professionals, standards bodies, governments, and companies are already working to secure, study, govern, and improve AI systems, autonomous agents, identity, authorization, auditability, and post-quantum cryptography. Many organizations have already achieved important milestones and are actively closing parts of the gap.

This research aims to learn from existing industry and standards work, use it where appropriate, and contribute focused research where it can be useful.

The wider research direction is Quantum-Secure Autonomous Gateway research. It starts from the identity layer because identity is the first trust boundary. Before an autonomous agent can be trusted to act, a verifier should be able to check what the agent is, who is responsible for it, what it is allowed to do, whether it is still trusted, whether the evidence is valid, and what should be recorded.

This first layer studies autonomous-agent identity and action-decision evidence. It includes canonicalization research, signature research, fail-closed verifier behavior, revocation freshness, permission scope, human approval, and audit evidence.

The wider goal is to understand autonomous AI agents step by step, in public, with disciplined research, testing, and evidence. As AI systems become faster and more capable, more people will need to work together to understand how these systems should be verified, governed, and safely connected to real digital systems.

## Why identity is the first layer

Identity is not the whole problem, but it is the first trust layer.

Before an autonomous agent performs a protected action, a verifier should be able to ask:

- which agent is acting;
- who operates or controls it;
- which issuer or authority is trusted for it;
- which key or proof is bound to it;
- whether the agent is active, expired, suspended, revoked, or compromised;
- what action is requested;
- whether the action is allowed, prohibited, approval-required, or unclear;
- whether revocation evidence is fresh enough;
- whether human approval is valid;
- what audit evidence should be recorded.

The research gap is not basic identity alone. Existing identity systems already support humans, applications, workloads, services, and devices.

The research gap is verifier-side action trust:

What evidence must be checked before an autonomous AI agent action is trusted?

## QSAG Layer 1

This repository focuses on Layer 1 of the QSAG research program:

Agent Identity and Action-Decision Evidence.

This layer will research and use existing industry standards over time, including:

- OAuth/OIDC for delegated access and identity flows;
- SPIFFE/WIMSE for workload identity and workload/delegation thinking;
- DID/VC for portable and verifiable claims;
- JOSE/COSE for signed data formats;
- RFC 9964 for ML-DSA in JOSE and COSE;
- NIST/ACVP for test-vector evidence;
- OWASP/NIST/AIIM for threat and governance alignment.

The goal is to build with existing industry standards and emerging research, to help the industry and contribute focused evidence.

## Agent passport as a research envelope

The current repository uses an agent passport as a research envelope.

The passport is used to study what evidence may need to travel together for autonomous-agent verification.

The research envelope helps test:

- agent identity fields;
- operator binding;
- issuer trust assumptions;
- lifecycle status;
- key material and key status;
- permissions and prohibitions;
- approval requirements;
- revocation freshness assumptions;
- payload hash checks;
- signature proof metadata;
- audit-relevant decision evidence.

Future work should map this research envelope to existing industry standards, workload identity systems, signed data formats, portable credential formats, or other standards-aligned formats where appropriate.

## Canonicalization and signature research

Canonicalization and signature verification are part of Layer 1 because signed evidence must be stable and verifiable.

Canonicalization asks:

What exact bytes are signed and verified?

Signature research asks:

Was the identity and action-decision evidence modified, and was it signed under a supported proof profile?

The repository has researched canonicalization, payload hashing, proof/key binding, signature metadata, ML-DSA runtime evidence, NIST/ACVP vector evidence, and signature implementation boundaries.

Future work should evaluate whether the proof profile should align with JOSE/COSE and RFC 9964 so the project remains close to industry formats.

## Current status

The repository currently includes:

- research models for identity, permissions, human oversight, revocation, decentralized verification, audit evidence, and post-quantum readiness;
- an initial agent passport schema and example;
- deterministic current-profile canonicalization helpers;
- payload hash checks;
- verifier pipeline checks;
- verification result models;
- fail-closed verifier behavior;
- raw JSON parsing with duplicate-key rejection;
- lifecycle and expiry checks;
- issuer trust and revocation freshness boundaries;
- proof selection and key binding checks;
- canonical payload preparation;
- signature verification planning and isolated ML-DSA research;
- automated tests.

The local verifier remains fail-closed.

Real signature verification, dependency adoption, issuer trust registry, live revocation service, production policy engine, audit storage, gateway logic, cloud deployment, and external integrations are not implemented.

## What this repository should produce

This repository should produce:

1. a clear agent identity and action-decision evidence model;
2. fail-closed verifier semantics;
3. negative tests for malformed, expired, revoked, stale, unsupported, and mismatched evidence;
4. proof/key binding checks;
5. canonicalization and signed-byte research;
6. signature proof-profile research aligned with industry formats;
7. audit-minimization rules;
8. simulated cross-organization verification scenarios using dummy data only.

The strongest contribution is a testable verifier-side model for autonomous-agent action trust.

This is a large research area, and mistakes or incomplete assumptions may exist. The project is expected to improve step by step through testing, review, evidence, and feedback from researchers, security professionals, standards communities, and industry contributors.

## What this repository does not do

This repository does not currently build:

- a production gateway;
- a commercial identity service;
- an MCP replacement;
- a full policy language;
- a live multi-organization network;
- a production revocation service;
- a cryptographic library;
- a real-agent execution system;
- a cloud deployment;
- a compliance framework.

MCP, A2A, APIs, workflow engines, cloud platforms, and future agent protocols should be treated as integration layers, not trust foundations.

## Documentation

Start with:

- `docs/README.md`

External references are maintained in:

- `docs/references.md`

The staged research direction is maintained in:

- `ROADMAP.md`

Evidence logs are maintained in:

- `evidence/`

## Current active focus

The current active focus is Layer 1:

Agent identity and action-decision evidence.

The immediate technical focus is signature verification boundary review.

The next technical work should inspect the existing verifier and tests against the signature implementation-boundary plan, then define the smallest signature adapter-interface tests without importing a cryptographic runtime.

## Research direction and community input

This research direction may change over time.

Autonomous AI agents, identity standards, post-quantum cryptography, AI governance, and gateway security are all moving quickly. As new standards, guidance, research, attacks, mitigations, and industry practices emerge, the project should adapt carefully.

Changes should be based on evidence, tests, references, and review, not hype or assumptions.

Community, industry, academic, government, and standards-body feedback is welcome. Useful contributions include threat-model review, standards mapping, negative test cases, verifier failure cases, revocation and approval evidence review, audit-minimization review, post-quantum proof-profile review, and cross-organization dummy scenarios.

The goal is to keep the research aligned with real-world needs while staying narrow, testable, and honest about what has and has not been proven.

## Research discipline

The project should stay narrow and evidence-based.

From this point:

- `docs/README.md` is the living documentation index;
- `docs/references.md` is the source register;
- `evidence/research-log.md` records short milestone entries only;
- detailed experiment evidence belongs in focused result documents;
- no new broad documents should be added unless they reduce confusion;
- dependency adoption requires a separate decision;
- real signature verification requires proof-profile and adoption decisions;
- legal, compliance, certification, and production claims must be avoided.

## Final position

This repository is useful if it remains focused on one verifier-side question:

What must be checked before an autonomous AI agent action is trusted?

That question supports the wider QSAG research direction and can help industry by complementing existing identity standards and emerging autonomous-agent security work.
