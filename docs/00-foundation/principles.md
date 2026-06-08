# Principles

## Purpose

This document records the core principles for the autonomous agent identity research.

The principles guide QSAG Layer 1:

Agent identity and action-decision evidence.

These principles may change as the research develops and as standards, tests, and review feedback improve the work.

## No identity, no action

An autonomous agent should not perform meaningful actions in a digital system without verifiable identity evidence.

Without identity, an action cannot be reliably connected to an operator, permission scope, lifecycle state, revocation status, or audit record.

## No hidden agents

Autonomous agents should not hide behind human accounts, shared API keys, generic service accounts, or unlabelled workloads.

A system should be able to distinguish between a human user, software service, workload, device, and autonomous agent.

## Operator accountability

Every autonomous agent should be linked to a responsible operator or controller.

The identity layer should make responsibility explicit while avoiding unnecessary personal or sensitive data.

## Explicit permission

Agent identity evidence should help explain what the agent is allowed to request.

Permissions should be specific, limited, and understandable.

## Explicit prohibition

Agent identity evidence should help explain what the agent is not allowed to do.

Some actions should remain denied even if the agent has technical access to a tool, credential, or environment.

## Default deny

The default posture should be denial.

Actions should continue only when the required identity, trust, lifecycle, revocation, permission, approval, audit, and enforcement evidence is present and valid for the decision being made.

## Human oversight

Some actions should require human approval, review, escalation, pause, or intervention.

Human approval should be specific, context-bound, and unable to override failed identity, revocation, prohibition, or missing trust evidence.

## Portable verification

Agent identity evidence should be inspectable beyond the issuing system where appropriate.

This supports future cross-organization verification, dummy scenarios, and standards-aligned research.

## Revocability

An agent must be removable from trust.

The identity layer should support expiry, suspension, revocation, compromise handling, retirement, and key-rotation evidence.

## Audit minimization

Important action decisions should produce evidence for later review.

Audit evidence should explain what happened and why while avoiding unnecessary sensitive data.

## Post-quantum readiness

Agent identity evidence may need to remain verifiable over time.

The research should consider algorithm agility, post-quantum signature paths, key rotation, and migration without claiming production post-quantum security.

## Research honesty

The research should clearly separate what is implemented, what is planned, what is experimental, what is deferred, and what remains unresolved.
