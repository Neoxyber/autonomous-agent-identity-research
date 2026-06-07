# Scope

This document defines the initial scope of the autonomous agent identity research.

The scope is intentionally narrow for the first phase. The repository begins with the identity layer because later work on enforcement, revocation, policy, audit, and implementation depends on a clear identity model.

## In scope

The first phase includes the following areas.

### Agent identity

The research will define what an autonomous agent identity should contain.

This includes the agent identifier, purpose, risk class, public keys, issue time, expiry time, lifecycle status, and passport metadata.

### Operator accountability

The research will define how an agent identity can be linked to a responsible operator.

The operator may be a person, organization, legal entity, research group, or system owner. The first phase focuses on the structure of the binding, not on production identity proofing.

### Allowed actions

The research will define how an agent passport can describe actions the agent is allowed to perform.

Allowed actions should be explicit, limited, and understandable.

### Prohibited actions

The research will define how an agent passport can describe actions the agent is not allowed to perform.

Prohibited actions should remain denied even if the agent has access to a tool or environment that could technically perform them.

### Human approval

The research will define how an identity model can indicate that some actions require human approval.

The first phase will distinguish between automatically allowed actions, actions requiring approval, and actions that are never allowed.

### Revocation and status

The research will define basic lifecycle states for agent identity.

Current lifecycle states are active, suspended, revoked, expired, compromised, and retired. Rotation is treated as a transition or reason, and pending review is handled outside `lifecycle_status` unless a later schema decision changes that boundary.

### Global verification

The research will study how an agent passport can be verified outside the original issuing system.

This includes portable credentials, public keys, expiry, signatures, and verification evidence.

### Decentralized verification

The research will study how identity verification can avoid unnecessary dependence on a single central service.

The first phase focuses on the model and requirements, not on deploying a decentralized registry.

### Post-quantum readiness

The research will study how post-quantum signatures can support long-term verification of agent identity.

The first phase focuses on cryptographic design requirements and algorithm agility, not on claiming final standardization.

### Audit evidence

The research will define what evidence should be produced when an agent requests or performs an important action.

Audit evidence should support review of identity, operator responsibility, requested action, policy decision, and denial reason.

## Out of scope for the first phase

The following areas are not part of the first phase.

1. Production deployment.

2. Commercial platform development.

3. Legal compliance claims.

4. Full identity proofing of human or legal entity operators.

5. Runtime workload attestation.

6. Agent-to-agent delegation.

7. Reputation scoring.

8. Formal verification.

9. Payment execution.

10. Autonomous creation of child agents.

11. Production governance registry.

12. User interface design.

These areas may be considered in later phases after the identity model is documented and tested.

## First milestone

The first milestone is to define the complete identity model for autonomous agents.

The milestone is complete when the repository contains clear documents for principles, problem statement, research questions, scope, references, and the initial research log.
