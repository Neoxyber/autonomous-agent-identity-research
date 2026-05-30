# Research Log

## Purpose

This file records the chronological progress of the autonomous agent identity research project.

The research log is used to track meaningful project steps, not every small edit. It records what changed, why it changed, which files were affected, and what the next step is.

Detailed design decisions will be recorded separately in Research Decision Records when the project reaches that stage. Empirical tests and benchmark results will be recorded separately in Empirical Testing Logs when implementation and testing begin.

## Entry 001

Date: 2026-05-27

Type: Foundation

Summary: Created the initial public research repository for autonomous agent identity.

Reason: The project needs a clean, reviewable, and long-term structure before implementation begins.

Files created:
README.md
ROADMAP.md
SECURITY.md
CITATION.cff
LICENSE
docs/principles.md
docs/problem-statement.md
docs/research-questions.md
docs/scope.md
docs/references.md
evidence/research-log.md

Decision:
The repository will be research-first. The implementation will be added later as a reference implementation after the initial identity model is defined.

Next step:
Complete the first signed commit for the research foundation.

## Entry 002

Date: 2026-05-27

Type: Research model

Summary: Added the first identity layer model for autonomous agents.

Reason: The project needs a clear identity model before later work on enforcement, revocation, audit, schemas, and reference implementation.

Files created:
docs/identity-layer.md

Files updated:
evidence/research-log.md

Decision:
The first identity layer model defines the agent passport, operator accountability, explicit permissions, explicit prohibitions, human approval requirements, lifecycle status, revocation reference, global verification, decentralized verification, post-quantum readiness, and audit evidence.

Next step:
Define the permission model.

## Entry 003

Date: 2026-05-27

Type: Research model

Summary: Added the initial permission model for autonomous agent identity.

Reason: The identity layer needs a clear model for allowed actions, approval-required actions, prohibited actions, default-deny behaviour, and explainable decisions.

Files created:
docs/permission-model.md

Files updated:
evidence/research-log.md

Decision:
The first permission model uses three outcomes: ALLOW, DENY, and REQUIRE_HUMAN_APPROVAL.

Next step:
Define the human oversight model.

## Entry 004

Date: 2026-05-28

Type: Research model

Summary: Added the initial human oversight model for autonomous agent identity.

Reason: The permission model needs a clear approach for actions that require human approval, human review, escalation, pause, intervention, and audit evidence.

Files created:
docs/human-oversight-model.md

Files updated:
evidence/research-log.md

Decision:
The model uses four outcomes: ALLOW, DENY, REQUIRE_HUMAN_APPROVAL, and REQUIRE_HUMAN_REVIEW. Human approval cannot override prohibited actions or allow revoked, expired, suspended, or compromised agents to act.

Next step:
Define the revocation model.

## Entry 005

Date: 2026-05-28

Type: Research model

Summary: Added the initial revocation model for autonomous agent identity.

Reason: The identity model needs a clear way to remove an agent from trust, pause unsafe activity, handle compromise, expire identities, rotate trust material, and support future emergency stop research.

Files created:
docs/revocation-model.md

Files updated:
evidence/research-log.md

Decision:
The model treats revocation as part of identity. A revoked, expired, suspended, or compromised agent should not be allowed to act.

Next step:
Define the decentralized verification model.

## Entry 006

Date: 2026-05-28

Type: Research model

Summary: Added the initial decentralized verification model for autonomous agent identity.

Reason: The identity system needs a clear way to support portable verification, offline and online checks, revocation evidence, trust material resolution, DID research, and future evidence anchoring without depending unnecessarily on one central runtime system.

Files created:
docs/decentralized-verification.md

Files updated:
evidence/research-log.md

Decision:
The model prioritizes portable verification first. DID support is treated as phased research, with did:web and did:key as early candidates. Blockchain is treated as optional research for evidence anchoring, not as a required foundation.

Next step:
Define the audit model.

## Entry 007

Date: 2026-05-28

Type: Research model

Summary: Added the initial audit model for autonomous agent identity.

Reason: The identity system needs a clear evidence model for action decisions, lifecycle changes, human oversight, revocation review, incident response, and future compliance mapping.

Files created:
docs/audit-model.md

Files updated:
evidence/research-log.md

Decision:
The audit model treats audit evidence as part of the trust system, not only as debugging output. It records decision evidence, lifecycle evidence, human oversight evidence, available status evidence, and tamper-evidence direction.

Next step:
Define the evaluation method.

## Entry 008

Date: 2026-05-28

Type: Security model

Summary: Added the initial post-quantum readiness model for autonomous agent identity.

Reason: The identity system needs a clear top-level security model for long-term verification, post-quantum signatures, hybrid transition, key rotation, algorithm migration, and cryptographic agility.

Files created:
docs/post-quantum-readiness.md

Files updated:
evidence/research-log.md

Decision:
The model treats post-quantum readiness as a design requirement, not a marketing claim. The first research direction uses ML-DSA as the primary passport signature candidate, SLH-DSA as an independent backup signature family, ML-KEM as a future key establishment candidate, and cryptographic agility as a mandatory design property.

Next step:
Define the evaluation method.

## Entry 009

Date: 2026-05-28

Type: Research method

Summary: Added the initial evaluation method for autonomous agent identity research.

Reason: The project needs a clear way to test the research models, record pass and fail results, identify blocked areas, and decide what needs improvement before implementation expands.

Files created:
docs/evaluation-method.md

Files updated:
evidence/research-log.md

Decision:
The evaluation method uses PASS, FAIL, PARTIAL, BLOCKED, and NEEDS_RESEARCH result categories. Detailed test results will later be recorded in Empirical Testing Logs.

Next step:
Define the research limitations.

## Entry 010

Date: 2026-05-28

Type: Research boundary

Summary: Added the initial research limitations document.

Reason: The project needs a clear statement of what the research does not yet prove, what has not been implemented, what does not claim legal compliance, and what still needs testing and review.

Files created:
docs/limitations.md

Files updated:
evidence/research-log.md

Decision:
The limitations document states that the repository is research-stage work and does not claim production readiness, legal compliance, final standardization, or production cryptographic security.

Next step:
Review the research model set before starting specifications.

## Entry 011

Date: 2026-05-30

Type: Reference implementation

Summary: Added the first local verifier foundation for autonomous agent passports.

Reason: The project needs a tested local verification path before adding payload hash verification, signature verification, revocation, policy evaluation, runtime gateway logic, or deployment work.

Files created:
src/aaid/passport_verifier.py
tests/test_passport_verifier_skeleton.py
tests/test_passport_verifier_schema_validation.py

Files updated:
src/aaid/__init__.py
src/aaid/passport_verifier.py
evidence/research-log.md

Result:
The implementation now has a verification result model, a local passport verifier skeleton, structural envelope checks, and schema validation using the committed agent passport schema. Malformed and schema-invalid envelopes fail closed to DENY. Schema-valid envelopes also fail closed to DENY because signature verification is intentionally not implemented yet.

Tests:
60 tests passed.

Not implemented in this milestone:
payload_hash verification
signature verification
post-quantum signing
issuer trust registry
revocation enforcement
policy evaluation
runtime gateway enforcement
external integrations

Decision:
The verifier foundation remains fail-closed. Schema validation confirms envelope shape only; it does not prove payload integrity, signature validity, issuer trust, revocation status, or action permission.

Next step:
Add payload_hash verification into the verifier.

## Entry 012

Date: 2026-05-30

Type: Reference implementation

Summary: Added payload_hash verification into the local passport verifier.

Reason: The verifier needs to bind detached proof metadata to the canonical passport payload before later signature verification, issuer trust, revocation, policy, or gateway work.

Files created:
tests/test_passport_verifier_payload_hash.py

Files updated:
src/aaid/passport_verifier.py
specs/examples/agent-passport.minimal.json
tests/test_passport_verifier_schema_validation.py
evidence/research-log.md

Result:
The verifier now recomputes the canonical payload hash over the passport payload and compares it with the first proof's recorded payload_hash. Matching payload hashes are recorded as payload_hash_valid. Passport tampering, proof payload_hash tampering, unsupported hash algorithms, and schema-invalid inputs fail closed to DENY. The example passport now contains the real canonical SHA-256 digest for its passport payload.

Tests:
74 tests passed.

Not implemented in this milestone:
signature verification
post-quantum signing
issuer trust registry
revocation enforcement
policy evaluation
runtime gateway enforcement
multi-proof signature selection
cross-implementation canonicalization validation
external integrations

Decision:
payload_hash verification confirms that the first proof's recorded payload_hash matches the canonical passport payload. It does not prove signature validity, issuer trust, revocation status, action permission, or legal compliance. The verifier remains fail-closed and still returns DENY for schema-valid and payload-hash-valid envelopes because signature verification is intentionally not implemented yet.

Next step:
Plan the signature verification abstraction and proof selection rules before adding real signature verification.

## Entry 013

Date: 2026-05-30

Type: Reference implementation

Summary: Added explicit proof selection rules to the local passport verifier.

Reason: The verifier needs a clear and testable proof-selection rule before adding signature verification, issuer trust, post-quantum signature support, revocation checks, policy evaluation, or runtime gateway enforcement.

Files created:
tests/test_passport_verifier_proof_selection.py

Files updated:
src/aaid/passport_verifier.py
evidence/research-log.md

Result:
The verifier now records proof_selected after schema validation and before payload_hash verification. The first-version rule selects the first proof only. The selected proof is then used for payload_hash verification. Multi-proof behavior is now explicit and tested: a mismatched second proof does not affect the current first-proof rule, and a mismatched first proof fails even if a later proof contains the correct payload_hash.

Tests:
84 tests passed.

Not implemented in this milestone:
signature verification
post-quantum signing
issuer trust registry
revocation enforcement
policy evaluation
runtime gateway enforcement
full multi-proof signature policy
external integrations

Decision:
Proof selection is now an explicit verifier step rather than an implicit proofs[0] access. The rule remains intentionally narrow for the first verifier version and must be revisited before real signature verification or hybrid classical/post-quantum proof handling is added.

Next step:
Plan the signature verification abstraction without adding real cryptographic verification yet.

## Entry 014

Date: 2026-05-30

Type: Reference implementation

Summary: Added a signature verification abstraction without real cryptographic verification.

Reason: The verifier needs a clear internal boundary for future signature verification before adding real cryptographic algorithms, post-quantum signatures, issuer trust, revocation checks, policy evaluation, or runtime gateway enforcement.

Files created:
tests/test_passport_verifier_signature_abstraction.py

Files updated:
src/aaid/passport_verifier.py
evidence/research-log.md

Result:
The verifier now routes the signature verification placeholder through a private internal helper that receives the passport and selected proof. The helper currently performs no cryptographic verification and always records signature_verification_not_implemented as a failed check. The verifier remains fail-closed and continues to return DENY for schema-valid, proof-selected, and payload-hash-valid envelopes.

Tests:
97 tests passed.

Not implemented in this milestone:
real signature verification
post-quantum signing
issuer trust registry
key selection
revocation enforcement
policy evaluation
runtime gateway enforcement
external integrations

Decision:
Signature verification is now represented as an explicit internal abstraction rather than inline placeholder logic. The abstraction is intentionally non-authoritative and cannot allow an envelope. Real verification must be added only after key selection, proof algorithm handling, trust-anchor rules, and failure behavior are tested.

Next step:
Plan key selection and proof algorithm matching before adding real signature verification.

## Entry 015

Date: 2026-05-30

Type: Reference implementation

Summary: Added public key selection checks before signature verification.

Reason: The verifier needs to select the public key referenced by the selected proof and validate basic key metadata before real signature verification can be added safely.

Files created:
tests/test_passport_verifier_key_selection.py

Files updated:
src/aaid/passport_verifier.py
evidence/research-log.md

Result:
The verifier now records verification_key_selected after payload_hash validation and before the signature verification placeholder. The selected proof's kid must match exactly one public key in the passport. The selected key must use the same algorithm as the proof, have active status, and have a suitable purpose. Missing keys, duplicate key identifiers, algorithm mismatches, retired keys, and compromised keys fail closed to DENY before the signature step.

Tests:
112 tests passed.

Not implemented in this milestone:
real signature verification
post-quantum signing
issuer trust registry
revocation enforcement
policy evaluation
runtime gateway enforcement
external integrations

Decision:
Key selection is now an explicit verifier step. This selects and validates public-key metadata only; it does not prove that the key or issuer is trusted and does not verify a signature. Real signature verification must still be added separately after signature input rules, algorithm handling, trust-anchor rules, and failure behavior are tested.

Next step:
Plan signature input rules and unsupported signature algorithm failure behavior before adding real cryptographic verification.

## Entry 016

Date: 2026-05-30

Type: Reference implementation

Summary: Added signature input and algorithm support checks before signature verification.

Reason: The verifier needs to define the future signature input and fail closed on unsupported signature algorithms before real cryptographic verification can be added safely.

Files created:
tests/test_passport_verifier_signature_input.py

Files updated:
src/aaid/passport_verifier.py
evidence/research-log.md

Result:
The verifier now records signature_input_prepared after verification_key_selected and before signature_algorithm_supported. The future signature input is the canonical passport payload bytes, excluding the envelope, proofs, and signature material. The verifier also records signature_algorithm_supported using the selected public key's algorithm. ML-DSA-65 is the only supported algorithm in this milestone. Unsupported algorithms fail closed to DENY before the signature verification placeholder.

Tests:
127 tests passed.

Not implemented in this milestone:
real signature verification
post-quantum signing
issuer trust registry
revocation enforcement
policy evaluation
runtime gateway enforcement
external integrations

Decision:
Signature input preparation and algorithm support are now explicit verifier steps. The implementation remains non-authoritative: it prepares canonical bytes and checks algorithm support, but it does not decode signatures, load public keys, verify cryptographic signatures, establish issuer trust, check revocation, or authorize actions.

Known follow-up:
The current canonicalization helper is reused for signature input, but it is not yet a complete independent RFC 8785/JCS implementation. Before real signature verification is trusted, the project must reconcile the declared canonicalization scheme with a reviewed canonicalization implementation or add a dedicated canonicalization-support check.

Next step:
Plan canonicalization scheme validation before adding real cryptographic verification.
