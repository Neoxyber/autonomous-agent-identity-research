# Agent Passport Threat Model and Trust Boundaries

## Purpose

This document records the current threat model and trust boundaries for the
agent passport research model.

The project studies an interoperable identity and control layer for autonomous
agents. It does not claim to replace verifiable credentials, decentralized
identifiers, workload identity, OAuth/OIDC, Sigstore, SLSA, SCITT, MCP,
post-quantum standards, or other existing ecosystems.

## Research position

The passport is a research envelope for studying how an autonomous agent can
present verifiable identity, bounded authority, lifecycle state, key material,
revocation references, and proof metadata.

The model is intended to connect with existing identity, credential,
supply-chain, policy, and cryptographic ecosystems rather than replace them.

## Core security question

The central question is:

Can a verifier make a fail-closed, explainable decision about whether an
autonomous agent identity is authentic, current, trusted, authorized for a
specific action, and auditable?

The current repository answers only part of this question. It verifies
structure, schema shape, payload hash consistency, selected key metadata,
declared canonicalization support, signature-input preparation, and fail-closed
signature-not-implemented behavior.

## What the passport may prove later

A fully developed passport system may help prove:

- the passport payload was not modified after signing;
- the selected proof references a known key identifier;
- the selected public key metadata is suitable for signature verification;
- the declared canonicalization and algorithm are supported;
- the issuer is trusted under a configured trust policy;
- the passport is not expired, revoked, suspended, or compromised;
- the requested action is within the agent's permission scope;
- the decision produced audit evidence.

These are future claims. The current implementation does not prove all of them.

## What the passport does not prove by itself

A valid passport must not be treated as unlimited authority.

By itself, a passport does not prove:

- the agent should be allowed to perform every action;
- the issuer is trusted by every verifier;
- the operator is legally accountable in a verified way;
- the software, model, tool, runtime, or dependency chain is safe;
- the agent is not compromised at runtime;
- the requested action is safe or policy-compliant;
- revocation state is current;
- human approval has been granted;
- audit evidence has been retained.

## Assets

The main assets are:

- canonical passport payload bytes;
- payload hash;
- proof metadata;
- signature value when implemented;
- issuer identifier;
- public key metadata;
- lifecycle status;
- revocation reference;
- permission and policy claims;
- verification result checks;
- audit evidence.

## Trust boundaries

The current and future trust boundaries are:

1. Raw JSON text to parsed object.
   Duplicate object member names and malformed JSON must fail before schema
   validation or canonicalization.

2. Parsed object to schema-valid envelope.
   Schema validation establishes expected shape only. It does not establish
   authenticity or authorization.

3. Schema-valid envelope to canonical payload bytes.
   Canonicalization must be deterministic and fail closed on unsupported input.

4. Canonical payload bytes to payload hash.
   A matching payload hash proves consistency with the selected proof metadata
   only. It is not a signature.

5. Payload hash to signature verification.
   Signature verification proves integrity and key possession only after a real
   signature implementation exists.

6. Signature verification to issuer trust.
   A valid signature does not make an issuer trusted by default.

7. Issuer trust to lifecycle and revocation.
   Trusted issuance is not enough if the passport or key is expired, revoked,
   suspended, compromised, or rotated.

8. Lifecycle and revocation to permission policy.
   A current identity still needs action-specific authorization.

9. Policy to human oversight.
   Some actions should require approval, review, escalation, or denial.

10. Decision to audit evidence.
    Important decisions should produce reviewable evidence without collecting
    unnecessary sensitive data.

## Attacker model

The project should consider attackers who can:

- submit malformed JSON;
- use duplicate JSON object member names;
- exploit canonicalization ambiguity;
- alter passport fields after signing;
- alter proof metadata;
- replay an old passport;
- use expired, revoked, suspended, or compromised credentials;
- use a valid identity outside its permission scope;
- present an untrusted issuer as if it were trusted;
- confuse a verifier with unsupported algorithms or canonicalization schemes;
- compromise an agent runtime after issuance;
- trick an agent into tool misuse or policy bypass;
- exploit dependency, package, or build-chain weaknesses;
- hide or tamper with audit evidence.

## Current fail-closed behavior

The current verifier is intentionally conservative.

It denies malformed raw JSON, duplicate JSON object member names, non-mapping
envelopes, missing required fields, malformed structural shape, schema
invalidity, passport validity-window failure, non-active lifecycle status,
payload-hash mismatch, unsuitable key metadata, unsupported canonicalization,
unsupported signature algorithm, and the absence of real signature
verification.

The verifier cannot return allow today.

## Current known gaps

The current repository still lacks:

- adopted RFC 8785/JCS canonicalizer;
- real signature verification;
- issuer trust registry or trust anchor model;
- key rotation enforcement;
- revocation checking;
- permission and policy evaluation;
- human approval or review enforcement;
- audit evidence implementation;
- cryptographic provenance verification for dependencies;
- legal compatibility determination;
- post-quantum signature implementation.

## Interoperability posture

The project should map to existing ecosystems instead of replacing them:

- verifiable credentials for issuer/verifier credential concepts;
- decentralized identifiers for possible identifier and key-resolution patterns;
- workload identity for infrastructure identity comparison;
- OAuth/OIDC or delegated authorization systems for access-control comparison;
- Sigstore, SLSA, and SCITT for software and artifact provenance comparison;
- MCP and agent tool ecosystems for tool-boundary comparison;
- NIST post-quantum standards for future signature algorithm agility.

The passport model should remain small enough to be evaluated independently and
mapped to these ecosystems later.

## 2026 and 2027 research implications

The 2026 and 2027 environment increases the importance of evidence.

Agentic systems need identity, privilege, tool-use, supply-chain, and runtime
control boundaries. Product-like software needs vulnerability handling,
dependency provenance, secure update thinking, and auditability. Long-term
cryptographic systems need algorithm agility for post-quantum migration.

This repository should continue to record evidence before adopting dependencies,
changing verifier behavior, or claiming readiness.

## Review questions

Before implementation continues, reviewers should be able to answer:

- What exact action is being authorized?
- Which identity claims are being trusted?
- Which issuer is trusted, and why?
- Which key signed the passport, and is it active?
- Is the passport expired, revoked, suspended, or compromised?
- Which canonical bytes were signed?
- Which proof was selected, and why?
- Which policy allowed, denied, or required review?
- What evidence was recorded for audit?
- What fails closed if an input is ambiguous or unsupported?

## Reviewer-critical open risks

The following risks should remain visible to reviewers and future collaborators:

- Replay and freshness: a signed passport may be old, copied, or used outside
  the intended time window unless expiry, challenge, nonce, or status rules are
  later enforced.
- Delegation and inter-agent trust: parent agents, child agents, delegated
  agents, and agent-to-agent verification need explicit scope narrowing and
  failure behavior.
- Tool-boundary abuse: a valid identity can still misuse a tool if action,
  purpose, data, time, and approval constraints are not evaluated.
- Runtime compromise: a passport can identify an issued agent, but it does not
  prove that the current runtime, model context, memory, or tool session remains
  uncompromised.
- Privacy and data minimization: passports and audit records should avoid raw
  sensitive operational content where identifiers, hashes, scopes, and decision
  reasons are sufficient.
- Audit tamper resistance: future audit evidence may need signed records,
  timestamp anchoring, append-only storage, or transparency-log style review.
- Evaluation quality: the research should provide negative tests, stable
  vectors, failure-mode tables, and standards mapping before claiming maturity.

These risks do not block this document, but they should guide later research
gates before implementation expands.

## Non-goals

This document does not implement:

- dependency adoption;
- canonicalizer replacement;
- real signature verification;
- issuer trust;
- revocation;
- permission evaluation;
- audit storage;
- human oversight;
- post-quantum signing;
- cloud deployment;
- external integrations.

## Raw JSON verifier-boundary decision

The research boundary should support two verifier entry points with different
trust assumptions.

`verify_passport_json(text: str)` should be the public boundary for untrusted raw
JSON input. It should parse with `parse_json_no_duplicate_keys()` before schema
validation, canonicalization, payload-hash comparison, or signature processing.
Malformed JSON and duplicate object member names should fail closed and produce
a reviewable verification result.

`verify_passport_envelope(envelope: object)` may remain the parsed-object
boundary for internal use and caller-trusted mappings. If the original source
was raw JSON, callers must provide duplicate-key parsing guarantees before using
this boundary.

This boundary is now implemented by `verify_passport_json(text: str)`, while
`verify_passport_envelope(envelope: object)` remains available for parsed
objects with explicit trust assumptions.

## Expiration and lifecycle verifier-boundary decision

The next verifier boundary should run after `schema_valid` and before
`proof_selected`. The planned checks are `passport_time_valid` and
`lifecycle_status_allows_verification`.

For this stage, timestamps should be strict UTC RFC3339-style strings ending in
`Z`. `issued_at` is inclusive. `expires_at` is exclusive, so
`now >= expires_at` fails closed. The verifier should also fail closed when
timestamps cannot be parsed safely, when `issued_at` is after `expires_at`, or
when `now < issued_at`.

Only `active` lifecycle status should allow verification to continue. The
statuses `suspended`, `revoked`, `expired`, `compromised`, and `retired` should
fail closed. This boundary is now implemented with deterministic UTC `now`
injection support. It does not implement issuer trust, revocation checking,
policy evaluation, signatures, dependency adoption, or canonicalizer
replacement.

## Issuer trust and revocation ordering decision

Issuer trust should be decided before revocation or freshness checks.

A revocation result is only useful when the verifier knows which issuer,
registry, trust anchor, or status authority is allowed to provide that result.
Without that trust basis, a verifier could accept status evidence from the wrong
source or treat an unknown authority as meaningful.

The planned future issuer-trust check is `issuer_trusted`. It should fail closed
when the issuer is unknown, inactive, unsuitable, or not configured as trusted.
Later revocation checks may include `revocation_status_checked`,
`revocation_status_fresh`, and `passport_not_revoked`.

This decision records ordering only. It does not implement issuer trust,
revocation checking, network lookup, policy evaluation, audit storage,
signatures, dependency adoption, or canonicalizer replacement.

## Next step

Plan the smallest issuer-trust verifier boundary before revocation, policy
evaluation, canonicalizer adoption, or signature verification.
