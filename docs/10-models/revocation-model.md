# Revocation Model

## Purpose

This document defines the revocation model for autonomous-agent identity.

Revocation explains how an agent identity, passport, key, or status evidence can
be removed from trust.

This model may change as the research develops and as standards, tests, and
review feedback improve the project.

## Why it matters

Autonomous agents may act quickly, repeatedly, and across systems.

If an agent is compromised, expired, suspended, revoked, or retired, verifiers
need a clear way to stop trusting that identity before further action decisions
continue.

The gap is:

How can a verifier know whether an autonomous-agent identity is still trusted
enough for action-decision evaluation to continue?

## Core rule

Revocation is part of identity.

A valid-looking passport is not enough. The verifier must also evaluate lifecycle
status, expiry, issuer trust, and revocation freshness.

Only `active` allows verification to continue. Other lifecycle states fail
closed.

## Lifecycle states

Current schema lifecycle states are:

1. `active` means the identity may continue to later checks, subject to trust,
   revocation, permission, approval, audit, and enforcement boundaries.
2. `suspended` means the identity is temporarily removed from trust.
3. `revoked` means the identity is removed from trust and should not act unless a
   new valid identity or later governance process is defined.
4. `expired` means the identity is outside its validity window.
5. `compromised` means the agent, key material, operator binding, runtime, or
   environment may no longer be trustworthy.
6. `retired` means the passport identity has been superseded or intentionally
   withdrawn and must not be used for action.

A retired passport identity is different from retired public-key material. The
first applies to `lifecycle_status`; the second applies to public key status.

Rotation and onboarding are not `lifecycle_status` values in the current schema.
Rotation is a transition or reason. Onboarding and review happen before an
identity becomes active.

## Revocation evidence

Revocation evidence may include:

1. caller-provided status evidence;
2. signed status evidence;
3. signed revocation lists;
4. cached status records;
5. short-lived passport validity;
6. future registry or status-service responses.

Current verifier behavior uses caller-provided revocation status evidence. It
does not perform network lookup, registry lookup, signed status verification, or
replay protection beyond the freshness window.

## Freshness

Revocation status must be fresh enough for the decision being made.

Stale, missing, malformed, mismatched, unknown, or non-active status evidence
should fail closed.

Short-lived passports may reduce stale-trust risk, but they do not replace
revocation evidence when current status is required.

## Emergency stop

Emergency stop is future research.

It may be needed when there is evidence of compromise, unsafe behavior,
unauthorized action, or policy violation.

Emergency stop behavior should be recorded as evidence and should not silently
erase the reason an agent was paused, suspended, revoked, or blocked.

## Current boundary

The repository includes caller-provided revocation freshness checks in the local
passport verifier.

Current revocation research does not define a live status service, registry,
signed revocation-list format, emergency stop system, storage system, gateway
integration, or production revocation process.

## Future work

Future revocation research may include signed status evidence, signed revocation
lists, replay protection, registry or status-service design, emergency stop
behavior, key-rotation evidence, cross-organization dummy scenarios, and later
gateway enforcement integration.

These areas should be researched in small steps and recorded through tests,
focused evidence, and review.
