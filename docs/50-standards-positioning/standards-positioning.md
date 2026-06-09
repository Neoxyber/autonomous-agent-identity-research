# Standards Positioning

## Purpose

This document explains how the autonomous agent identity research relates to existing identity, security, and governance work.

The goal is alignment, not replacement.

The agent passport is treated as a research envelope for studying autonomous agent identity, authority, lifecycle status, approval, audit evidence, and future proof formats. It is not presented as a new industry standard, production identity system, or regulatory framework.

## Position

The research studies how several ideas can work together in one fail-closed model:

1. verifiable agent identity
2. operator accountability
3. explicit permissions and prohibitions
4. revocation and lifecycle status
5. human approval and review
6. audit evidence
7. decentralized or offline verification
8. post-quantum-ready proof boundaries

The model is intended to be understandable to reviewers familiar with verifiable credentials, decentralized identifiers, workload identity, delegated authority, agentic identity and access management, agent security risks, and post-quantum signature migration.

## Current boundaries

This repository does not present itself as:

1. compliance with any standard
2. legal or regulatory readiness
3. production readiness
4. replacement of existing identity standards
5. a final protocol or wire format
6. a final trust framework
7. a complete security solution
8. post-quantum signing as an implemented capability

These boundaries remain visible until each area is separately specified, implemented, tested, reviewed, and recorded.

## Concept mapping

| Research concept | Related external area | Alignment | Current boundary |
| --- | --- | --- | --- |
| Agent passport | Verifiable credentials and agent identity credentials | A portable identity document can carry information about an agent, issuer, subject, proof, status, and scope. | The passport is a research envelope, not a VC profile. |
| Agent identifier | Decentralized identifiers, workload identity, and agent identity registries | A stable identifier helps verifiers distinguish an agent from a human, workload, device, or generic service account. | No DID method, registry, or workload identity binding is selected yet. |
| Operator binding | Delegated authority and accountability models | The model links an agent to a responsible operator so actions are not anonymous. | Legal identity proofing and operator assurance are outside the current implementation. |
| Issuer | Credential issuers, trust anchors, and workload identity authorities | The issuer represents the authority that creates or signs the passport. | No production issuer trust registry is implemented. |
| Public keys and proof metadata | Credential proofs, JOSE-style proof metadata, and post-quantum signature research | Proof material supports tamper detection and later issuer trust checks. | Real signature verification is not implemented yet. |
| Canonicalization | Deterministic signing inputs for JSON credentials | Stable canonical bytes are required before trusted signature verification. | Full RFC 8785/JCS compatibility is not stated until reviewed and tested. |
| Permissions | OAuth-style scopes, authorization inputs, and policy models | Explicit permissions describe what the agent may do when identity, trust, and policy checks pass. | No final policy language is defined yet. |
| Prohibitions | Policy constraints, deny rules, and agent safety controls | Explicit prohibitions describe actions the agent must not perform even if a tool is technically available. | The model is not a universal policy engine. |
| Human approval and review | Governance controls and approval workflows | Some actions require human approval or review before proceeding. | No production approval workflow or user interface is implemented. |
| Revocation and lifecycle status | Credential status, key lifecycle, status services, and revocation lists | A verifier needs current or cached evidence that the agent remains trusted. | No final revocation registry, status endpoint, or signed list format is implemented. |
| Audit evidence | Accountability logs and decision records | Decisions can be reviewed later with the evidence available at decision time. | The research does not state legal record-keeping readiness. |
| Decentralized or offline verification | DIDs, portable credentials, signed metadata, cached status evidence, and transparency systems | Verification can be designed to avoid unnecessary dependence on one live central service. | Blockchain, DID methods, and transparency services remain future research topics. |
| Post-quantum readiness | ML-DSA, SLH-DSA, hybrid migration, and cryptographic agility | The model can leave room for algorithm and proof-format migration over time. | Post-quantum signing is not implemented yet. |
| Agent security risks | Agentic application security and non-human identity governance | The model supports research into identity abuse, privilege misuse, tool misuse, revocation failure, and audit gaps. | Threat mappings and adversarial tests remain future work. |

## Research alignment

The research aligns with existing identity and security work in five ways.

First, it treats agent identity as separate from human identity, service accounts, generic workloads, and shared credentials.

Second, it separates identity from authority. A verified identity does not automatically authorize an action.

Third, it keeps revocation, human oversight, and audit evidence inside the decision boundary rather than treating them as later add-ons.

Fourth, it keeps room for cryptographic migration by separating the passport model from any single permanent algorithm.

Fifth, it treats decentralized verification as a research direction while avoiding unnecessary dependence on blockchain or any single registry design.

## Open research questions

Standards alignment remains incomplete.

Open questions include:

1. whether the passport later becomes a verifiable credential profile, a workload identity profile, or remains a research envelope with mappings
2. which identifier methods fit local, offline, cross-organization, and future deployed settings
3. how delegated authority can be represented without allowing privilege expansion
4. how revocation evidence works when online status checks are unavailable
5. how policy decisions map to scopes, claims, or external authorization systems
6. how audit evidence supports review while minimizing sensitive data
7. how post-quantum signatures can be introduced without locking the model to one algorithm or library
8. how agent-to-agent trust works without losing operator accountability

## Current status

This document positions the research model.

It does not select a final external standard, DID method, credential profile, trust registry, proof suite, policy language, revocation mechanism, deployment architecture, or legal readiness position.

Future standards alignment will proceed through small research steps, tests, review, and recorded evidence.
