# Revocation Model

## Purpose

This document defines the first revocation model for autonomous agent identity.

Revocation is the process of removing an agent from trust. It is required when an agent should no longer be allowed to act, verify, delegate, or continue a workflow.

## Core rule

Revocation is part of identity.

An autonomous agent identity is incomplete unless it can be suspended, revoked, expired, marked compromised, or retired.

A revoked agent must not be allowed to act.

## Lifecycle states

The lifecycle states are the schema lifecycle_status values:

1. active

2. suspended

3. revoked

4. expired

5. compromised

6. retired

These states should be visible to verifiers and enforcement systems. Only active allows verification to continue; the others fail closed.

## State meanings

active means the agent identity is currently valid, subject to policy and permission checks.

suspended means the agent is temporarily removed from trust and should not act until restored.

revoked means the agent is permanently removed from trust unless a new identity is issued.

expired means the identity is no longer valid because its validity period has ended.

compromised means the agent, key material, operator account, runtime, or environment may no longer be trustworthy.

retired means the passport identity has been superseded or intentionally withdrawn and must not be used for action. A retired passport identity (lifecycle_status) is distinct from a retired public key (public_key.status), which marks superseded key material.

Rotation and onboarding are not lifecycle_status values. Rotation is a transition process and a revocation or audit reason: superseded identity or key material is recorded as retired, newly issued material is active, and the rotation is captured as a reason. Onboarding and review happen before an identity becomes active; operator-level onboarding is represented by operator.verification_status, including pending_review.

## Revocation reasons

A revocation or suspension should include a reason.

Example reasons include:

1. Operator request.

2. Key compromise.

3. Policy violation.

4. Suspicious behaviour.

5. Expired identity.

6. Incorrect identity data.

7. Unauthorized tool use.

8. Audit failure.

9. Regulatory or administrative action.

10. Research test condition.

Reason codes help later audit, investigation, and evaluation.

## Online revocation

Online revocation checks allow a verifier to ask for current status.

An online status check may answer whether an agent is active, suspended, revoked, expired, compromised, or retired.

Online checks are useful when live trust information is available, but they should not be the only verification method.

## Offline revocation

Offline environments may not be able to contact a live status service.

The model should support offline evidence such as signed revocation lists, cached status records, short-lived passports, and warning modes.

Offline verification can check signatures, structure, expiry, and cached status. It may not know the newest revocation state unless updated revocation evidence is available.

## Short-lived passports

Short-lived passports reduce the risk of stale trust.

If revocation status cannot always be checked live, shorter passport validity periods can limit how long an agent identity remains usable without fresh verification.

## Emergency stop

The model should support emergency stop behaviour.

Emergency stop may pause or block an agent when there is evidence of compromise, unsafe behaviour, unauthorized action, or policy violation.

Emergency stop should be recorded as audit evidence and should explain why the agent was stopped.

## Kill switch research

Future research will study kill switch behaviour for autonomous agents.

This includes when an agent should be paused, suspended, revoked, prevented from continuing a workflow, or blocked from calling tools.

The research should record what passes, what fails, and what needs improvement.

## Enforcement rule

Before an action is allowed, the verifier or gateway should check lifecycle status.

If the agent is revoked, expired, suspended, compromised, or retired, the action should be denied. Only active allows the action to continue.

Rotation and onboarding are not lifecycle_status values. Rotation is handled as a transition and a reason: superseded identity or key material is recorded as retired and a newly issued identity or key is used. Onboarding and review happen before an identity becomes active and are represented by operator.verification_status, including pending_review, not by lifecycle_status.

## Audit evidence

Revocation events should produce audit evidence.

The audit record should include the agent, operator, lifecycle state, reason, timestamp, authority that changed the status, revocation reference, and any related incident or investigation reference.

## Current boundary

This document defines the initial revocation model.

It does not define the final schema, registry, status endpoint, signed revocation list format, user interface, or implementation. Those will be developed later through specifications, reference implementation, controlled tests, and recorded evaluation results.
