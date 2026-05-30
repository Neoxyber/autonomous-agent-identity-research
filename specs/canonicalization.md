# Passport Canonicalization Rules

## Purpose

These rules define the first canonicalization boundary for agent passports.

Canonicalization is required before hashing, signing, verification, and tamper detection.

## Signed payload

The signed payload is the `passport` object inside the passport envelope.

The `proofs` array is detached proof metadata.

The `proofs` array is not part of the passport payload being signed.

## Canonicalization method

The first canonicalization candidate is JSON Canonicalization Scheme.

The schema value is:

`json-canonicalization-scheme`

Later implementation should test an RFC 8785 compatible library before relying on signatures.

## Canonicalization compatibility decision

The declared scheme `json-canonicalization-scheme` names the JSON Canonicalization Scheme as the long-term target. The current research helper is not a complete independent RFC 8785 implementation.

The current canonicalization tests document the helper's deterministic behaviour for the current research passport profile only. They do not establish full RFC 8785 or JSON Canonicalization Scheme compliance.

The decision for this stage is:

1. The long-term target is a reviewed RFC 8785 compatible canonicalization, adopted before any trusted real signature verification.
2. The current helper is acceptable only for local research tests and deterministic current-profile regression tests. It is not a basis for trusted signature verification.
3. If a reviewed RFC 8785 compatible canonicalization is not adopted, the project must either constrain the passport profile to inputs the current helper handles deterministically, or rename the declared canonicalization scheme so it does not imply full RFC 8785 compliance.
4. Real signature verification is blocked until this canonicalization compatibility is resolved. No real cryptographic verification is added before then.

This decision prevents later work from treating the current helper as a full RFC 8785 implementation.

## Hash input

`payload_hash` is the hash of the canonical `passport` object.

The hash input is the canonical byte representation, not formatted display text.

The proof records the hash algorithm used.

Allowed first hash algorithms are:

1. SHA-256
2. SHA-384
3. SHA-512

## Signature input

The proof records the canonicalization method, hash algorithm, payload hash, key id, algorithm, and signature.

The implementation will define the exact signing input for each supported algorithm.

The schema should not assume that all signature libraries sign the same input form.

## Proof boundary

Proofs are detached from the signed payload.

A verifier must reject a proof if:

1. The canonicalization method is unsupported.
2. The hash algorithm is unsupported.
3. The payload hash does not match the canonical passport payload.
4. The proof key id does not match an active public key.
5. The signature algorithm is unsupported.
6. The signature cannot be verified.

## Field handling

Object member order must not affect the canonical hash.

String values are case-sensitive unless a later rule says otherwise.

Identifier values are case-sensitive.

Timestamp values must remain RFC 3339 UTC strings ending in `Z`.

Implementations must not rewrite timestamps during verification.

Arrays keep their semantic order unless a later specification defines a deterministic sorting rule.

## Security boundary

Canonicalization does not prove that an agent is trustworthy.

Canonicalization only ensures that the same passport payload produces the same bytes for hashing and signing.

Policy, revocation, lifecycle status, issuer trust, and human oversight are separate checks.

## Current boundary

These rules define the first research boundary for passport hashing and signing.

They do not define a final cryptographic implementation, post-quantum library, proof suite, DID method, COSE format, JWS profile, blockchain anchor, or production security claim.
