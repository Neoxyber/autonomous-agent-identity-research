# Standards Positioning

## Purpose

This document explains how the autonomous agent identity research model relates to existing and emerging identity, security, and governance work.

The goal is alignment, not replacement.

The project treats the agent passport as a research envelope for studying autonomous agent identity. It is not presented as a new industry standard, a production identity system, or a compliance framework.

## Position

The project studies how several identity and security ideas can work together in one fail-closed research model:

1. verifiable agent identity

2. operator accountability

3. explicit permissions and prohibitions

4. revocation and lifecycle status

5. human approval and review

6. audit evidence

7. decentralized or offline verification

8. post-quantum-ready proof boundaries

The model should be understandable to reviewers familiar with verifiable credentials, decentralized identifiers, workload identity, delegated authority, agentic identity and access management, agent security risks, and post-quantum signatures.

## Non-claims

This repository does not claim:

1. compliance with any standard

2. legal or regulatory compliance

3. production readiness

4. replacement of existing identity standards

5. a final protocol or wire format

6. a final trust framework

7. a complete security solution

8. post-quantum readiness as an implemented capability

These boundaries should remain visible until each claim is separately specified, implemented, tested, reviewed, and recorded.

## Concept mapping

| Project concept | Related external area | Alignment note | Current boundary |
| --- | --- | --- | --- |
| Agent passport | Verifiable credentials and agent identity credentials | A portable identity document can carry claims about an agent, issuer, subject, proof, status, and scope. | The passport is a research envelope, not a claimed VC profile. |
| Agent identifier | Decentralized identifiers, workload identity, and agent identity registries | A stable identifier helps verifiers distinguish an agent from a human, workload, device, or generic service account. | No DID method, registry, or workload identity binding is selected yet. |
| Operator binding | Delegated authority, controller relationships, and accountability models | The model links an agent to a responsible operator so actions are not anonymous. | The project does not perform legal identity proofing or operator assurance yet. |
| Issuer | Credential issuers, trust anchors, and workload identity authorities | The issuer represents the authority that creates or signs the passport. | No production issuer trust registry is implemented. |
| Public keys and proof metadata | Verifiable credential proofs, Data Integrity proofs, JOSE-style proof metadata, and post-quantum signature research | Proof material supports tamper detection and later issuer trust checks. | Real signature verification is not implemented yet. |
| Canonicalization | Deterministic signing inputs for JSON credentials | Stable canonical bytes are required before trusted signature verification. | Full RFC 8785/JCS compatibility is not claimed until reviewed and tested. |
| Permissions | OAuth-style scopes, authorization claims, and policy inputs | Explicit permissions describe what the agent may do if all trust and policy checks pass. | No final policy language is defined yet. |
| Prohibitions | Policy constraints, deny rules, and agent safety controls | Explicit prohibitions describe actions the agent must not perform even if a tool is technically available. | The model is not a universal policy engine. |
| Human approval and review | Governance controls, human oversight, and approval workflows | Some actions require human approval or review before proceeding. | No production approval workflow or user interface is implemented. |
| Revocation and lifecycle status | Credential status, key lifecycle, status services, and revocation lists | A verifier needs current or cached evidence that the agent remains trusted. | No final revocation registry, status endpoint, or signed list format is implemented. |
| Audit evidence | Accountability logs, decision records, and governance evidence | Decisions should be explainable after the fact with evidence available at decision time. | The project does not claim legal record-keeping compliance. |
| Decentralized or offline verification | DIDs, portable credentials, signed metadata, cached status evidence, and transparency systems | Verification should not depend unnecessarily on one live central service. | Blockchain, DID methods, and transparency services are future research topics. |
| Post-quantum readiness | ML-DSA, SLH-DSA, ML-KEM, hybrid migration, and cryptographic agility | The model should be able to change algorithms and proof formats over time. | The project does not implement post-quantum signing yet. |
| Agent security risks | Agentic application security and non-human identity governance | The model supports research into identity abuse, privilege misuse, tool misuse, revocation failure, and audit gaps. | Threat mappings and adversarial tests remain future work. |

## Research alignment

The project is aligned with the direction of existing identity and security work in several ways.

First, it treats agent identity as separate from human identity, service accounts, generic workloads, and shared credentials.

Second, it treats identity and authority as separate. A verified identity does not automatically authorize an action.

Third, it keeps revocation, human oversight, and audit evidence as part of the identity model rather than optional later additions.

Fourth, it keeps the design compatible with future cryptographic migration by separating the passport model from a single permanent algorithm.

Fifth, it keeps decentralized verification as a research goal while avoiding unnecessary dependence on blockchain or any single registry design.

## Open research questions

The standards alignment remains incomplete.

Open questions include:

1. whether the passport should later become a verifiable credential profile, a workload identity profile, or remain a research envelope with mappings

2. which identifier methods are appropriate for local, offline, cross-organization, and future deployed settings

3. how delegated authority should be represented without allowing privilege expansion

4. how revocation evidence should work when online status checks are unavailable

5. how policy decisions should map to scopes, claims, or external authorization systems

6. how audit evidence should support review while minimizing sensitive data

7. how post-quantum signatures should be introduced without locking the model to one algorithm or library

8. how agent-to-agent trust should be handled without losing operator accountability

## Current boundary

This document positions the research model.

It does not select a final external standard, DID method, credential profile, trust registry, proof suite, policy language, revocation mechanism, deployment architecture, or legal compliance approach.

Future standards alignment should proceed through small research steps, tests, and recorded evidence.
