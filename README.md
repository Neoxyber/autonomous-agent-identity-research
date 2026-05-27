# Autonomous Agent Identity Research

This repository studies a complete identity layer for autonomous AI agents.

The central position is simple: an autonomous agent should not be able to act anonymously inside a digital system. Before an agent performs meaningful actions, it should be able to prove what it is, who is responsible for it, what it is allowed to do, what it is not allowed to do, and whether it is still trusted.

This is a research-first repository. The implementation will be added as a reference implementation after the initial identity model is defined.

## Research focus

The first research focus is the identity layer for autonomous agents.

This includes agent identity, operator accountability, allowed actions, prohibited actions, human approval requirements, revocation status, decentralized verification, post quantum readiness, and audit evidence.

## Problem

Autonomous agents can call tools, access systems, make decisions, and act across organizational boundaries. Existing identity systems are mainly designed for humans, service accounts, applications, workloads, and devices.

Autonomous agents need a clearer identity model because they can perform actions with real consequences. If an agent is hidden behind a shared account, generic API key, or unlabelled workload, it becomes difficult to know which agent acted, who was responsible, what authority it had, and whether the action should have been allowed.

## Research questions

The initial research questions are:

1. What identity attributes are required for autonomous agents?

2. How can agent identity be bound to a responsible operator?

3. How can permissions and prohibitions be encoded into an agent passport?

4. How can an agent passport be verified globally without depending on one central service?

5. How can revocation work in both online and offline environments?

6. How can post quantum signatures support long term trust in agent identities?

7. What audit evidence is needed to prove that an agent acted within or outside its authority?

## Initial design principles

The research is guided by the following principles:

1. No agent can act anonymously.

2. Every agent has a verifiable identity.

3. Every action is linked to an accountable operator.

4. Every permission is explicit.

5. Every prohibition is explicit.

6. Every denial is explainable.

7. High risk actions can require human approval.

8. Every passport can be verified globally.

9. The system is decentralized where possible.

10. The cryptography is post quantum ready.

11. Important actions produce audit evidence.

## Repository structure

docs contains the research documents.

evidence contains the research log and future evidence records.

specs will contain machine readable schemas when the identity model is ready.

src will contain the reference implementation when implementation begins.

tests will contain unit, integration, security, and evaluation tests when implementation begins.

## Current status

The repository is in the research foundation stage.

The first milestone is to define the complete identity model before starting the reference implementation.

## Scope

This repository focuses first on the identity layer.

The initial scope includes agent identity, operator binding, allowed actions, prohibited actions, human approval, revocation, global verification, decentralized verification, post quantum readiness, and audit evidence.

The initial scope does not include a production service, commercial platform, or legal compliance claim.

## References

External references are maintained in docs/references.md.

Research documents may refer to reference identifiers from that file. Implementation files should not contain citations, legal claims, or research references.

## Limitations

This repository is experimental research. It does not claim production readiness, legal compliance, or final standardization.

The purpose is to develop and evaluate a disciplined identity model for autonomous agents.
