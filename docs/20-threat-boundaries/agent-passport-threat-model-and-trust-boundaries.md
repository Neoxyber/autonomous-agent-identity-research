# Agent Passport Threat Model and Trust Boundaries

## Purpose

This document focuses on where trust can break when an agent passport is parsed,
checked, and used as part of an autonomous-agent action decision.

It is about the passport verifier path: where trust enters, where it can fail,
where the verifier stops, and why these steps matter for later signature,
revocation, approval, audit, enforcement, and connectivity work.

This document is not the full roadmap, standards map, deployment plan, legal
position, or product description.

This document can change as the research improves, tests expand, mistakes are
found, and better designs become clear.

## Research focus

The agent passport is a research envelope for identity and action-decision
evidence.

It can contain identity information, issuer information, lifecycle state, key
metadata, revocation references, permission scope, and proof metadata.

Those fields are useful only when the verifier checks each boundary carefully and
stops when something is missing, stale, unsupported, mismatched, or unclear.

A passport is not authority by itself. It is one part of a wider decision
process.

## Main question

Where does trust enter, and where can it fail?

For this research, the answer is not only signature verification. The path also
includes raw JSON parsing, schema validation, canonicalization, payload hashing,
proof selection, key checks, issuer trust, lifecycle checks, revocation
freshness, permission evaluation, human oversight, audit evidence, and later
enforcement.

The current passport verifier remains fail-closed and cannot return `ALLOW`.

## What the passport helps study

The passport helps study whether a verifier has enough evidence to continue
from one boundary to the next.

Important checks include:

- safe raw JSON parsing;
- schema validation;
- duplicate-key rejection before canonicalization;
- shared canonical payload bytes for hash and later signature input;
- proof and key selection;
- caller-provided issuer trust;
- active lifecycle status;
- fresh revocation or status evidence;
- requested action within permission scope;
- approval or review evidence when needed;
- evidence that can explain the decision later.

Some of this is implemented locally. Some remains future work.

## What the passport does not prove by itself

A passport does not prove that:

- the agent can perform every action;
- every verifier trusts the issuer;
- the runtime, model, memory, tool session, or dependency chain is safe;
- the agent is still uncompromised after issuance;
- revocation state is current without fresh status evidence;
- approval exists without approval evidence;
- audit evidence has been stored or made tamper-evident.

## Assets in scope

The main assets for this document are:

- raw JSON input;
- parsed passport envelope;
- canonical passport payload bytes;
- payload hash;
- proof metadata;
- public key metadata;
- issuer identifier;
- lifecycle status;
- revocation or status evidence;
- permission and approval evidence;
- verification and decision results.

## Trust boundaries

The trust-boundary path is:

1. raw JSON text to parsed object;
2. parsed object to schema-valid envelope;
3. schema-valid envelope to canonical payload bytes;
4. canonical payload bytes to payload hash;
5. payload hash to signature verification;
6. signature verification to issuer trust;
7. issuer trust to lifecycle and revocation;
8. lifecycle and revocation to permission evaluation;
9. permission evaluation to human oversight;
10. decision result to audit evidence;
11. audit evidence to any later enforcement boundary.

Each boundary is useful because later work depends on it. Signature verification,
revocation, approval, audit, enforcement, and future connectivity are easier to
reason about when earlier boundaries are clear and tested.

## Attacker model

The verifier model studies inputs and situations such as:

- malformed JSON;
- duplicate JSON object member names;
- canonicalization ambiguity;
- changed payload or proof metadata;
- old passports or stale status evidence;
- expired, revoked, suspended, compromised, or retired identities;
- untrusted issuer evidence;
- valid identity used outside permission scope;
- unsupported algorithms or proof formats;
- tool misuse after identity verification;
- runtime compromise after issuance;
- missing, changed, or hidden audit evidence;
- dependency, package, build-chain, or runtime weaknesses.

## Current fail-closed behavior

The current verifier fails closed for malformed raw JSON, duplicate object member
names, non-mapping envelopes, missing required fields, malformed structural
shape, schema invalidity, validity-window failure, non-active lifecycle status,
untrusted issuer configuration, missing or stale revocation status evidence,
multi-proof envelopes, payload-hash mismatch, unsuitable key metadata,
unsupported canonicalization, unsupported signature algorithm, and absence of
real signature verification.

The verifier cannot return `ALLOW`.

## Current trust-boundary gaps

The main remaining gaps for this document are:

- real passport signature verification;
- adopted runtime canonicalizer dependency;
- production issuer registry or external trust anchor model;
- signed revocation or status evidence;
- replay and nonce protection;
- production policy and approval enforcement;
- audit storage and tamper-evidence;
- gateway or runtime enforcement;
- production post-quantum signature support.

## Interoperability note

The passport model can be compared with identity, credential, workload,
delegated authorization, provenance, agent-tool, and post-quantum cryptography
work over time.

This document only records the trust-boundary view. Deeper standards mapping
belongs in focused standards-positioning documents.

## Open risks for later research

The risks that still need careful research include replay, freshness,
delegation, inter-agent trust, tool-boundary abuse, runtime compromise, privacy,
audit tamper resistance, dependency risk, build-chain risk, and post-quantum
migration.

These risks are part of the learning path. They guide future tests and review.

## Non-goals for this document

This document does not implement dependencies, canonicalizer replacement,
signature verification, external registry lookup, signed revocation
verification, production policy enforcement, audit storage, human approval
workflows, post-quantum signing, gateway execution, cloud deployment, or live
multi-organization operation.

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

This is documentation alignment only. The reader-facing foundation documents now align with the current lifecycle vocabulary while preserving the evidence history that recorded the earlier mismatch.

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

## Real signature-verification planning boundary

Real signature-verification planning may proceed after the REF-014 adoption
deferral decision, while runtime canonicalizer adoption remains separate.

The first real signature-verification design should stay narrow:

- verify only the already prepared canonical passport payload bytes;
- preserve proof exclusion from the signed input;
- use the selected public key after key selection, key validity, and
  `proof.verification_method` to key `kid` binding have passed;
- keep the algorithm allowlist explicit and narrow;
- fail closed for unsupported algorithms, malformed keys, malformed signatures,
  unsupported encodings, and verifier-library errors;
- keep dependency adoption separate from the verifier behavior decision;
- keep the passport verifier unable to return `ALLOW` until the complete
  signature, revocation, policy, audit, and enforcement gates are intentionally
  connected.

Planning notes:
ML-DSA-65 remains the current research target for the first passport signature
path. A future implementation should not write custom cryptography. It should
use a reviewed library only after dependency, runtime-support, encoding, test
vector, and rollback decisions are recorded.

This section does not implement signature verification, add dependencies, change
requirements or lockfiles, change verifier source, adopt REF-014, or create an
`ALLOW` path.

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
payload fields require a recorded numeric-domain policy and schema bounds before
canonicalizer adoption, golden-vector migration, or signature-verification
planning. Non-finite, ambiguous, or unsupported numeric domains should fail
closed.

Canonicalization and candidate-canonicalizer errors should be represented as
failed verifier checks and `DENY` results. They should not escape as unhandled
exceptions in verifier paths intended to produce `VerificationResult`.

This decision does not adopt REF-014, install packages, change requirements,
replace the canonicalizer, migrate golden vectors, implement numeric-domain
enforcement, or add real signature verification.

## Canonical payload preparation status

Canonical payload preparation is now an explicit verifier boundary.

The verifier records `canonical_payload_prepared` after `proof_selected` and before `payload_hash_valid`. It prepares canonical payload bytes once, fails closed on canonicalization or candidate-canonicalizer errors, and makes later payload-hash and signature-input checks use the same canonical bytes.

Canonicalization errors are not reported as hash mismatches, unsupported canonicalization schemes, or signature-input failures. They fail the `canonical_payload_prepared` check and return `DENY`.

This status does not adopt REF-014, install packages, change requirements, replace the canonicalizer, execute REF-014 tests, migrate golden vectors, or add signature verification.

## Next step

Review the existing verifier and tests against the signature implementation-boundary plan before adding signature adapter-interface tests.

The next step should not adopt dependencies, import a cryptographic runtime, change requirements or lockfiles, implement real signature verification, or create a passport-verifier `ALLOW` path.
