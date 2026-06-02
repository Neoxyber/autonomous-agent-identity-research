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
   Trusted issuance is not enough if the passport identity is expired, revoked,
   suspended, compromised, or retired, or if the key material has been retired
   or superseded.

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
- issuer trust registry or external trust anchor model;
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
- external issuer registry or network lookup;
- signed revocation or status evidence;
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

The `issuer_trusted` check is now implemented as a caller-provided explicit
issuer-trust boundary. It fails closed when issuer trust is not configured,
when the configuration is a string or mapping, or when the passport issuer is
not explicitly configured as trusted. It performs no registry lookup, network
lookup, revocation checking, signature verification, policy evaluation, audit
storage, dependency adoption, or canonicalizer replacement.

Later revocation checks may include `revocation_status_checked`,
`revocation_status_fresh`, and `passport_not_revoked`.

## Lifecycle vocabulary alignment decision

The committed schema and the verifier use one lifecycle vocabulary for
`lifecycle_status`: `active`, `suspended`, `revoked`, `expired`, `compromised`,
and `retired`. Only `active` allows verification to continue; every other value
fails closed. Some earlier model documents also listed `rotated` and
`pending_verification` as lifecycle states, which the current schema does not
define. This decision reconciles the prose documents to the existing schema
vocabulary. It changes no schema, verifier, test, or example, and the verifier
still cannot return `ALLOW`.

This model uses `retired` to mean superseded or intentionally withdrawn material,
at two distinct scopes: a `lifecycle_status` of `retired` describes a superseded
or withdrawn passport identity, and a `public_key.status` of `retired` describes
superseded key material. They are consistent in intent but enforced at different
levels; they are not one field.

`rotated` is treated as a transition process and a revocation or audit reason,
not a `lifecycle_status` value. When identity or key material is replaced, the
superseded material is recorded as `retired`, newly issued material is `active`,
and the rotation is captured as a reason. Key material may be rotated or replaced
over time, so this mapping is a cryptographic-agility cue, not a final
key-management design.

`pending_verification` is treated as an onboarding and review state outside the
current `lifecycle_status` enum. Operator-level onboarding is already represented
by `operator.verification_status`, including `pending_review`. A passport-level
pending state would require a separate later schema decision; until then, an
identity that has not completed onboarding has no `active` passport and fails
closed under default deny.

This is documentation alignment only. The forward-looking documents
(`ROADMAP.md`, `docs/research-questions.md`, `docs/scope.md`) still list
`rotated` and `pending_verification` and are deferred to a later reconciliation
pass, so this change does not claim repo-wide lifecycle consistency.

## Revocation and freshness verifier-boundary decision

The next verifier boundary should check caller-provided revocation status after
`issuer_trusted` and before `proof_selected`. The planned checks are
`revocation_status_checked`, `revocation_status_fresh`, and
`passport_not_revoked`. Each check should fail closed and stop the chain on
failure. The verifier still cannot return `ALLOW`.

For this stage, status evidence is an in-memory object supplied by the caller.
The verifier should not perform network lookup, registry lookup, signed status
evidence parsing, schema changes, or cryptographic verification of status
evidence.

`revocation_status_checked` should pass only when the status evidence is bound
to the exact passport and issuer: `status_reference` matches
`passport.revocation.status_reference`, `passport_id` matches
`passport.passport_id`, and `status_authority` matches `passport.issuer_id` and
is present in `trusted_issuers`. Exact string equality is required. Matching
only `status_reference` is not enough, and status from another issuer should
fail closed even if that issuer is otherwise trusted.

`revocation_status_fresh` should use strict UTC `Z` timestamps and the injected
deterministic `now`. Freshness should hold only when
`produced_at <= now < valid_until`; missing, malformed, future-dated, stale, or
inverted timestamp windows should fail closed.

`passport_not_revoked` should pass only when status is exactly `active`. Every
other status value, including missing, unknown, malformed, `revoked`,
`suspended`, `expired`, `compromised`, or `retired`, should fail closed.

This decision records a research boundary only. It does not implement
revocation checking, freshness checking, network lookup, registry lookup,
signed status evidence, replay or rollback protection, policy evaluation, audit
storage, dependency adoption, canonicalizer replacement, or real signature
verification.

## Selected-key validity and verification-method binding decision

Before real signature verification, the verifier should confirm that the selected
verification key is currently usable for the selected proof.

The planned boundary should run after `verification_key_selected` and before
signature-input preparation or signature-algorithm checks. It should fail closed
when the selected key is not active, is not yet valid, is expired, has malformed
time metadata, or is not bound to the proof method being verified.

The selected key's required `created_at` value should be treated as the beginning
of the key validity window and should use the same strict UTC `Z` timestamp
rules as passport and revocation time checks. If `not_after` is present, it
should be exclusive. The planned validity rule is
`created_at <= now < not_after` when `not_after` exists, and `created_at <= now`
when it does not. The check should use the already injected deterministic `now`
and should not read the wall clock again.

The proof `verification_method` should be bound to the selected public key before
signature verification is introduced. For the current schema and example, the
planned rule is exact string equality between `proof.verification_method` and the
selected key `kid`. No normalization, prefix matching, substring matching, or
case folding should be used.

This decision records a research boundary only. It does not implement key-time
validity, verification-method binding, proof-selection hardening, canonicalizer
replacement, dependency adoption, real signature verification, policy evaluation,
audit storage, or post-quantum signing.

## Proof-selection hardening and downgrade-policy decision

Before real signature verification, the verifier should avoid treating proof
ordering as a trust policy.

The current first-version verifier selects the first proof only. That behavior is
acceptable while the verifier cannot return `ALLOW`, but it should not become a
signature-verification trust model. Once real signatures, algorithm agility, or
future hybrid and post-quantum proofs are introduced, accepting the first proof
could allow downgrade or substitution risk.

The next verifier boundary should therefore fail closed when more than one proof
is present. This keeps the current research implementation simple and prevents a
multi-proof envelope from being interpreted before a full proof-selection policy
exists.

The planned check should run before `proof_selected`. It should pass only when
the envelope contains exactly one proof. Missing, non-sequence, or empty proof
collections are already handled by earlier structural checks. A proof sequence
with more than one proof should fail closed before payload-hash validation, key
selection, canonicalization, or signature-stage checks.

This decision does not define long-term multi-proof, hybrid-signature, or
post-quantum proof selection. A later policy may select proofs by issuer policy,
key purpose, verification method, algorithm family, assurance level, or
classical/PQ hybrid requirements. Until that policy is specified and tested,
multi-proof envelopes should not continue through the verifier.

This decision records a research boundary only. It does not implement
multi-proof policy, real signature verification, canonicalizer replacement,
dependency adoption, policy evaluation, audit storage, or post-quantum signing.

## Canonicalization adoption boundary decision

Before real signature verification, canonicalization must be settled as a trust
boundary.

The current helper remains a research-stage canonicalization helper. It provides
deterministic bytes for the current passport fixtures and tests, but it is not a
complete independent RFC 8785 / JSON Canonicalization Scheme implementation and
should not be treated as signature-ready for interoperable verification.

Real signature verification should remain blocked until the project records a
canonicalization adoption decision, completes isolated candidate evaluation, and
reviews dependency, provenance, license, and security risks. Any candidate
canonicalizer should be evaluated outside the repository before adoption. No
package installation, requirements change, lockfile change, or canonicalizer
replacement should occur without explicit review.

Canonicalizer replacement may change canonical bytes and therefore may require a
deliberate golden-vector migration, including the minimal example payload hash
and pinned canonicalization tests. Such migration should be reviewed as a
separate compatibility event, not as an incidental side effect of signature work.

This decision records a research boundary only. It does not adopt a
canonicalizer, verify signatures, change requirements, change the schema, update
golden vectors, implement policy evaluation, implement audit storage, or add
post-quantum signing.

## Verifier canonicalization-boundary decision

Canonicalization should remain behind the verifier's existing parse and schema
boundaries.

Raw JSON input should be parsed with duplicate-key rejection before schema
validation or canonicalization-dependent checks. The envelope verifier should
continue to operate on parsed mappings only. Callers that bypass the raw JSON
entry point are responsible for providing duplicate-key-safe parsed input.

Schema validation should remain before payload-hash comparison, canonicalization
scheme checks, signature-input preparation, and any future canonicalizer
candidate integration.

The current passport payload profile remains numeric-field-free. Future numeric
payload fields require a recorded numeric-domain policy before canonicalizer
adoption, golden-vector migration, or signature-verification planning. Ambiguous
or unsupported numeric domains should fail closed.

Canonicalization and candidate-canonicalizer errors should be represented as
failed verifier checks and `DENY` results. They should not escape as unhandled
exceptions in verifier paths intended to produce `VerificationResult`.

This decision does not adopt REF-014, install packages, change requirements,
replace the canonicalizer, migrate golden vectors, implement numeric-domain
enforcement, or add real signature verification.

## Next step

Review REF-014 integration-test planning and remaining adoption requirements
before dependency adoption, canonicalizer replacement, golden-vector migration,
or signature-verification planning.
