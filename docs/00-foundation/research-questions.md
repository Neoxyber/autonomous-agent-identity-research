# Research Questions

This document defines the initial research questions for the autonomous agent identity project.

The questions are focused on the first research area: the complete identity layer for autonomous agents.

## Primary question

How can autonomous agents be given globally verifiable, revocable, permission-scoped, and post-quantum-ready identities that make them accountable for their actions without forcing trust in a single central system?

## Supporting questions

### RQ1. Identity attributes

What identity attributes are required for an autonomous agent?

This includes the agent's identifier, purpose, risk class, operator binding, public keys, status, expiry, permissions, prohibitions, and audit references.

### RQ2. Operator accountability

How can agent identity be bound to a responsible operator?

The operator may be a person, organization, legal entity, research group, or system owner. The research must consider how to express responsibility without exposing unnecessary personal or sensitive information.

### RQ3. Permissions and prohibitions

How can permissions and prohibitions be encoded into an agent passport?

The identity model should describe what an agent is allowed to do, what it is not allowed to do, and which actions require human approval.

### RQ4. Global verification

How can an agent passport be verified globally without depending on one central service?

The research must consider portable credentials, decentralized identifiers, public keys, expiry, revocation references, and offline verification.

### RQ5. Revocation

How can revocation work in both online and offline environments?

The research must consider active, suspended, revoked, expired, compromised, and retired lifecycle states. Rotation should be treated as a transition or reason, and pending review should be handled outside `lifecycle_status` unless a later schema decision changes that boundary.

### RQ6. Post-quantum readiness

How can post-quantum signatures support long-term trust in agent identities?

The research must consider primary signatures, backup signatures, key rotation, algorithm agility, and future key establishment.

### RQ7. Audit evidence

What audit evidence is needed to prove that an agent acted within or outside its authority?

The research must consider signed audit events, policy decisions, action records, passport hashes, operator binding, and denial reasons.

## Current boundary

These questions define the first research phase.

Later phases may study runtime identity, agent-to-agent delegation, supply-chain binding, reputation, decentralized registries, and formal verification.
