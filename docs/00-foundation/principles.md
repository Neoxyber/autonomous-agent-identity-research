# Principles

This document defines the first principles for the autonomous agent identity research.

The principles are intended to stay simple, stable, and understandable. They guide the identity model, the permission model, the reference implementation, and the evaluation work.

## No identity, no action

An autonomous agent should not be allowed to perform meaningful actions inside a digital system unless it presents a valid and verifiable identity.

This principle exists because an agent without identity cannot be reliably linked to an operator, permission set, revocation status, or audit trail.

## No hidden agents

Autonomous agents should not hide behind human accounts, shared API keys, generic service accounts, or unlabelled workloads.

A system should be able to distinguish between a human user, a software service, a device, a workload, and an autonomous agent.

## Operator accountability

Every autonomous agent should be linked to a responsible operator.

The operator may be a person, organization, legal entity, research group, or system owner. The identity layer should make responsibility explicit while avoiding unnecessary exposure of personal or sensitive information.

## Explicit permission

An agent identity should describe what the agent is allowed to do.

Permissions should be specific, limited, and understandable. A verifier should be able to inspect an agent passport and understand the agent's permitted scope.

## Explicit prohibition

An agent identity should describe what the agent is not allowed to do.

Some actions should remain outside the agent's authority even if the agent has access to a tool, credential, or environment.

## Default deny

The default decision should be denial.

An agent should only be allowed to perform an action when the action is explicitly permitted, the passport is valid, the identity is trusted, the agent is not revoked, and the policy allows it.

## Human approval for high-risk actions

Some actions should require human approval before execution.

The identity model should be able to distinguish between actions that are allowed automatically, actions that require approval, and actions that are never allowed.

## Global verification

An agent identity should be verifiable outside the issuing system.

A verifier should be able to check the identity, signatures, permissions, expiry, and trust status using open and inspectable data wherever possible.

## Decentralized trust

The identity model should avoid unnecessary dependence on one central service.

Central services may still exist for registration, revocation, and governance, but the design should support portable credentials and decentralized verification where possible.

## Revocability

An agent must be removable from trust.

The identity layer should support suspension, revocation, expiry, compromise handling, and key rotation.

## Auditability

Important actions should produce evidence.

The system should record which agent acted, which operator was responsible, what action was requested, what policy was applied, and why the action was allowed or denied.

## Post-quantum readiness

Agent identities may need to remain verifiable for many years.

The identity layer should support post-quantum signatures and cryptographic agility so that algorithms can change over time without redesigning the full system.

## Research honesty

The repository should clearly separate what is implemented, what is proposed, what is experimental, and what remains unresolved.
