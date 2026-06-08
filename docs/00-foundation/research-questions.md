# Research Questions

## Purpose

This document records the main research questions for QSAG Layer 1:

Agent identity and action-decision evidence.

These questions may change as the research develops and as standards, tests, and review feedback improve the work.

## Primary question

What must be checked before an autonomous AI agent action is trusted?

## Supporting questions

### RQ1. Agent identity

What identity attributes are needed for an autonomous agent?

This includes agent identifier, purpose, risk class, operator reference, issuer reference, lifecycle status, validity window, public-key metadata, proof metadata, permissions, revocation reference, and audit references.

### RQ2. Operator accountability

How can an agent be linked to a responsible operator or controller without exposing unnecessary personal or sensitive data?

### RQ3. Permission and prohibition

How can action scope be represented so a verifier can distinguish allowed, approval-required, review-required, unknown, and prohibited actions?

### RQ4. Revocation and freshness

How can a verifier decide whether status evidence is fresh, bound to the right passport and issuer, and active enough for verification to continue?

### RQ5. Signed evidence

Which bytes should be signed, which proof profile should be supported, and how should malformed, unsupported, mismatched, or invalid proof evidence fail closed?

### RQ6. Post-quantum readiness

How should the research prepare for ML-DSA, SLH-DSA, key rotation, algorithm agility, and long-term migration without adopting dependencies too early?

### RQ7. Human oversight

When should an action require approval, review, escalation, pause, or intervention, and what evidence proves that oversight was context-bound?

### RQ8. Audit minimization

What evidence is needed to review decisions later without collecting unnecessary sensitive data, secrets, prompts, or operational content?

### RQ9. Cross-organization verification

How can dummy cross-organization scenarios test whether identity and action-decision evidence remains understandable outside the issuing system?

## Current boundary

These questions guide the current Layer 1 research.

Later QSAG layers may study behavior evidence, delegation chains, gateway enforcement, audit replay, cloud deployment, MCP or workflow integration, and live multi-organization operation.
