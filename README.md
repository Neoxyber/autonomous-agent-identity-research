# Autonomous Agent Identity Research

This repository studies a standards-aligned identity layer for autonomous AI agents.

The central position is simple: an autonomous agent should not be able to act anonymously inside a digital system. Before an agent performs protected actions, a verifier should be able to check what the agent is, who is responsible for it, what it is allowed to do, what it is not allowed to do, whether it is still trusted, and what evidence should be recorded.

The work is research-stage. It does not claim production readiness, legal compliance, standards compliance, or replacement of existing identity standards.

## Research focus

The project studies how verifiable agent passports, operator accountability, scoped permissions, explicit prohibitions, revocation, human oversight, audit evidence, decentralized or offline verification, and post-quantum readiness can work together in a fail-closed reference model.

The research is intended to align with and learn from existing and emerging work in verifiable credentials, decentralized identifiers, workload identity, delegated authority, agentic identity and access management, agent security guidance, and post-quantum signature systems.

## Problem

Autonomous agents can call tools, access systems, make decisions, and act across organizational boundaries. Existing identity systems are mainly designed for humans, service accounts, applications, workloads, and devices.

Autonomous agents need a clearer identity model because they can perform actions with real consequences. If an agent is hidden behind a shared account, generic API key, or unlabelled workload, it becomes difficult to know which agent acted, who was responsible, what authority it had, whether the action was allowed, and whether the agent should still be trusted.

## Research questions

The initial research questions are:

1. What identity attributes are required for autonomous agents?

2. How can agent identity be bound to a responsible operator?

3. How can permissions and prohibitions be encoded into an agent passport?

4. How can an agent passport be verified globally without depending on one central service?

5. How can revocation work in both online and offline environments?

6. How can post-quantum signatures support long-term trust in agent identities?

7. What audit evidence is needed to prove that an agent acted within or outside its authority?

## Design principles

The research is guided by the following principles:

1. No verified identity, no protected action.

2. Every agent should have a visible and verifiable identity.

3. Every agent should be linked to an accountable operator.

4. Every permission should be explicit.

5. Every prohibition should be explicit.

6. The default decision should be denial.

7. High-risk or uncertain actions should support human approval or human review.

8. Agent passports should support verification outside the issuing system.

9. The system should avoid unnecessary dependence on one central service.

10. The model should support long-term cryptographic change, including post-quantum readiness.

11. Important decisions should produce audit evidence.

## Current status

The repository is in the research and reference-implementation foundation stage.

The project currently includes research models, an initial agent passport schema and example, deterministic current-profile canonicalization helpers, payload hash checks, verifier pipeline checks, verification result models, and tests.

The local verifier remains fail-closed. Real signature verification, issuer trust, revocation enforcement, policy evaluation, audit implementation, post-quantum signing, gateway logic, cloud deployment, and external integrations are not implemented yet.

The current roadmap focuses on standards positioning, canonicalization closure, signature verification foundation, issuer trust, revocation, permission evaluation, human oversight, audit evidence, post-quantum research, and a local dummy demo.

## Repository structure

`docs/` contains the research models and supporting documents.

`specs/` contains machine-readable schemas, examples, and specification notes.

`src/` contains the research reference implementation.

`tests/` contains the current automated tests.

`evidence/` contains the active research log, archived research log entries, and future evidence records.

`ROADMAP.md` defines the staged research and implementation path.

## Scope

This repository focuses first on the identity layer for autonomous agents.

The initial scope includes agent identity, operator binding, allowed actions, prohibited actions, human approval, revocation, global verification, decentralized verification, post-quantum readiness, audit evidence, and a fail-closed local verifier.

The scope does not include a production service, commercial platform, legal compliance claim, standards-compliance claim, real-user deployment, or production credential handling.

## References

External references are maintained in `docs/references.md`.

Research documents may refer to reference identifiers from that file. Implementation files should not contain citations, legal claims, or research references.

## Limitations

This repository is experimental research.

It does not claim production readiness, legal compliance, standards compliance, final standardization, or complete security.

The purpose is to develop and evaluate a disciplined identity model and reference verifier for autonomous agents.
