# Scope

## Purpose

This document defines the current scope of the autonomous agent identity research.

The research is focused on QSAG Layer 1:

Agent identity and action-decision evidence.

This scope may change as the research develops and as standards, tests, and review feedback improve the work.

## In scope

### Agent identity evidence

The research studies what evidence an autonomous agent identity should contain.

This includes agent identifier, purpose, risk class, issuer reference, operator reference, public-key metadata, proof metadata, lifecycle status, issue time, expiry time, and passport metadata.

### Action-decision evidence

The research studies what evidence is needed before an autonomous-agent action can be trusted.

This includes issuer trust, key validity, proof selection, payload hash, canonical payload preparation, revocation freshness, permission scope, approval requirements, audit context, and decision reason.

### Fail-closed verification

The research studies verifier behavior for malformed, missing, stale, mismatched, unsupported, expired, revoked, compromised, or ambiguous evidence.

The verifier should not return `ALLOW` until the required signature, trust, revocation, permission, approval, audit, and enforcement gates are intentionally connected and tested.

### Permission and prohibition

The research studies how an agent passport can include or reference allowed actions, approval-required actions, prohibited actions, default decision, unknown-action handling, and audit requirements.

### Human oversight

The research studies when actions should require human approval, review, escalation, pause, or intervention.

Human approval must not override prohibited actions, failed identity, missing issuer trust, expired or revoked status, stale revocation evidence, or missing audit and enforcement boundaries.

### Revocation and lifecycle

The research studies active, suspended, revoked, expired, compromised, and retired lifecycle states.

Only `active` allows verification to continue. Rotation and onboarding remain outside `lifecycle_status` in the current schema.

### Canonicalization and signed bytes

The research studies canonical payload preparation, payload hashing, canonicalization boundaries, and signed-byte decisions.

Canonicalizer adoption and golden-vector migration remain separate decisions.

### Signature proof-profile research

The research studies future ML-DSA-65 verification boundaries, proof-profile scope, key encoding, signature encoding, runtime candidates, and NIST/ACVP-style test-vector evidence.

Real signature verification and dependency adoption are not implemented.

### Audit minimization

The research studies how decision evidence can be useful for later review while avoiding unnecessary sensitive data.

### Dummy cross-organization scenarios

The research may use simulated organizations, dummy agents, and dummy data to test portable verification and action-decision evidence.

## Out of scope for the current phase

The current phase does not include:

1. production deployment;
2. commercial platform development;
3. legal or compliance certification;
4. production identity proofing;
5. live issuer registry;
6. live revocation service;
7. real signature verification;
8. cryptographic runtime dependency adoption;
9. production policy engine;
10. audit storage;
11. gateway enforcement;
12. cloud deployment;
13. MCP, A2A, workflow, or tool integration;
14. live multi-organization operation;
15. payment execution;
16. autonomous child-agent creation.

These areas may become future QSAG layers or later research phases after Layer 1 is clearer and better tested.

## Current boundary

The current work should remain narrow, testable, and verifier-side.

Small implementation steps are acceptable when they support the research model, negative tests, fail-closed behavior, and evidence recording.

Broad product architecture, deployment design, and integration work should stay deferred until the Layer 1 trust boundaries are better understood.
