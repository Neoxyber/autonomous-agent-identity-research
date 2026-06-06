# Signature Verification Planning

## Purpose

This document records the first planning boundary for real passport signature
verification.

It separates signature-verification planning from canonicalization planning,
post-quantum readiness, issuer trust, revocation, authorization, approval,
audit, and enforcement.

This is planning only. It does not implement cryptographic verification, adopt a
dependency, change requirements or lockfiles, change verifier behavior, or create
a passport-verifier `ALLOW` path.

## Current repository boundary

The verifier currently prepares the canonical passport payload bytes and records
`signature_input_prepared`.

The signed input is the canonical `passport` object only. It excludes the
envelope wrapper, the `proofs` array, proof metadata, and `signature_b64u`.

The verifier currently records `signature_verification_not_implemented` as a
failed check and returns `DENY`.

The verifier cannot return `ALLOW`.

## Current implemented gates before the future signature step

The current verifier already requires these gates before the future signature
step can be reached:

1. raw JSON parsing with duplicate-key rejection when using the raw JSON entry
   point;
2. envelope shape checks;
3. schema validation;
4. passport validity-window check;
5. lifecycle status check;
6. caller-provided issuer trust;
7. caller-provided revocation freshness evidence;
8. exactly one proof;
9. payload-hash validation over the canonical passport payload;
10. selected public key matching the proof `kid` and algorithm;
11. selected-key status and purpose checks;
12. selected-key validity-window checks;
13. exact `proof.verification_method` to selected key `kid` binding;
14. supported canonicalization metadata;
15. prepared canonical passport payload bytes;
16. supported signature algorithm metadata.

Any future real signature verifier must preserve this order unless a separate
security review records a different order.

## Algorithm direction

ML-DSA-65 remains the first research target for passport signature verification.

SLH-DSA remains a backup signature-family research direction.

This does not mean that a library, backend, key format, signature format, or
proof suite has been selected.

The project must not implement ML-DSA, SLH-DSA, ML-KEM, or any other
cryptographic primitive from scratch.

## Runtime-support boundary

The repository currently has no adopted cryptographic dependency for real
signature verification. Passport verification code does not import a
cryptographic signing or verification library, and dependency adoption remains a
separate research decision.

Candidate libraries and backends still require review. The project has not
selected a library, backend, key encoding, signature encoding, or test-vector
source for ML-DSA-65 verification.

## Encoding questions

The current schema includes:

- `public_key_b64u`
- `signature_b64u`

The schema currently constrains these fields as base64url strings, but it does
not yet define the exact byte format for real ML-DSA public keys or signatures.

Before implementation, the project must decide whether these fields contain:

1. raw ML-DSA public-key and signature bytes;
2. standardized encoded key containers;
3. library-specific serialized bytes; or
4. another documented proof format.

## Initial encoding position

The initial planning position is to treat `public_key_b64u` and
`signature_b64u` as unpadded base64url encodings of raw ML-DSA-65 public-key
bytes and raw ML-DSA-65 signature bytes.

This position is not final. It must be confirmed or replaced after library,
backend, and test-vector review.

The current minimal passport example uses demo public-key and signature strings.
It must not be treated as a real ML-DSA signature test vector.

## Test-vector requirements

Real signature verification must not be implemented until test-vector sources
are reviewed and recorded.

The first test-vector plan should cover:

1. a valid ML-DSA-65 signature over the prepared canonical passport payload;
2. failure when a signed passport field is modified;
3. failure when `signature_b64u` is modified;
4. failure when `public_key_b64u` is malformed;
5. failure when `signature_b64u` is malformed;
6. failure when the public key has the wrong length or encoding;
7. failure when the signature has the wrong length or encoding;
8. failure when the key algorithm is unsupported;
9. failure when proof metadata and selected key metadata disagree;
10. no accidental `ALLOW` result.

## Failure semantics

A future verifier must fail closed for:

- unsupported algorithms;
- unsupported key encodings;
- unsupported signature encodings;
- malformed base64url values;
- malformed public-key bytes;
- malformed signature bytes;
- verifier-library errors;
- missing runtime support;
- mismatched proof and key metadata;
- invalid signatures.

These failures should be represented as named verifier checks and `DENY`
results, not as unhandled exceptions.

## Implementation boundary

The first real signature implementation, if approved later, should use a small
internal adapter.

The adapter should accept prepared canonical payload bytes, selected key
metadata, and selected proof metadata. It should not perform parsing,
canonicalization, issuer trust, revocation, authorization, approval, audit, or
enforcement decisions.

Even if a future signature verifies, the passport verifier must not become a
general execution gateway.

## Adoption blockers

Before implementation, the project must record decisions for:

1. cryptographic library;
2. runtime backend support;
3. key encoding;
4. signature encoding;
5. test-vector source;
6. malformed-input behavior;
7. verifier check naming;
8. rollback plan;
9. dependency-risk review;
10. no-`ALLOW` behavior.

## Non-goals

This document does not cover:

- dependency adoption;
- package installation;
- requirements or lockfile changes;
- verifier source changes;
- schema changes;
- new example passport values;
- real signature verification;
- signing key generation;
- issuer trust registry;
- signed revocation evidence;
- authorization policy;
- approval enforcement;
- audit storage;
- gateway, MCP, Civo, Supabase, or cloud integration;
- production readiness;
- legal compliance;
- certification.

## Next step

Review candidate ML-DSA runtime support, key encoding, signature encoding, and
test-vector sources before any implementation proposal.
