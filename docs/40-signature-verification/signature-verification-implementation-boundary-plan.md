# Signature Verification Implementation Boundary Plan

## Purpose

This document records the first implementation-boundary plan for future real
passport signature verification.

The goal is to define the smallest safe boundary for pure direct external
ML-DSA-65 message-mode verification before changing verifier behavior.

This is planning only. It does not adopt a dependency, install packages into the
repository environment, change requirements or lockfiles, change verifier source,
change schema, implement real signature verification, or create a passport-verifier
`ALLOW` path.

## Current boundary

The current verifier already prepares canonical passport payload bytes and
records `signature_input_prepared`.

The current verifier records `signature_verification_not_implemented` and returns
`DENY`.

The passport verifier cannot return `ALLOW`.

The current signature proof profile is scoped to ML-DSA-65 pure direct external
message-mode verification only.

## First implementation shape

If implementation is approved later, the first change should be a small internal
signature-verification adapter.

The adapter should accept only:

- prepared canonical passport payload bytes;
- selected public-key metadata;
- selected proof metadata;
- configured signature profile information.

The adapter should not perform:

- raw JSON parsing;
- duplicate-key handling;
- schema validation;
- canonicalization;
- issuer trust decisions;
- revocation freshness decisions;
- authorization;
- approval validation;
- audit preparation;
- enforcement decisions;
- gateway or MCP execution.

## First supported profile

The first supported profile should be:

- algorithm family: ML-DSA;
- parameter set: ML-DSA-65;
- mode: pure direct external message-mode verification;
- signed message: prepared canonical passport payload bytes;
- public key: raw ML-DSA-65 public-key bytes after explicit encoding decision;
- signature: raw ML-DSA-65 signature bytes after explicit encoding decision.

Context handling remains a blocker until the exact context rule is recorded.

## Explicitly unsupported modes

The first implementation should fail closed for:

- test-level `hashAlg` / HashML-DSA modes;
- internal-interface modes;
- `externalMu` modes;
- `mu` inputs;
- signing operations;
- reconstructed internal ML-DSA values;
- unsupported algorithms;
- unsupported parameter sets;
- unsupported proof suites;
- unsupported key encodings;
- unsupported signature encodings.

Unsupported modes should return named failed checks and `DENY`, not unhandled
exceptions.

## Proposed adapter result model

The adapter should return a small deterministic result object with:

- `verified`;
- `reason`;
- `checks`.

The adapter result should not grant execution and should not decide final policy.

A verified signature should mean only that the candidate signature verified
against the selected public key and prepared message under the supported profile.

## Proposed verifier checks

Future check names should be short and explicit. Candidate names:

- `signature_profile_supported`;
- `signature_public_key_decoded`;
- `signature_value_decoded`;
- `signature_public_key_length_valid`;
- `signature_value_length_valid`;
- `signature_runtime_available`;
- `signature_verified`.

Unsupported or malformed cases should have separate check reasons.

## Failure behavior

Future implementation should fail closed for:

- missing runtime support;
- unsupported signature profile;
- unsupported or mismatched algorithm metadata;
- malformed base64url public-key value;
- malformed base64url signature value;
- wrong public-key byte length;
- wrong signature byte length;
- public-key import failure;
- invalid signature;
- runtime verification exception.

All such failures should produce `DENY`.

## Tests required before implementation

Before implementation, create or update tests for:

1. supported profile metadata;
2. unsupported `hashAlg` profile failure;
3. unsupported internal-interface profile failure;
4. unsupported `mu` profile failure;
5. malformed public-key base64url failure;
6. malformed signature base64url failure;
7. wrong public-key length failure;
8. wrong signature length failure;
9. invalid signature failure;
10. runtime exception fail-closed behavior;
11. no verifier `ALLOW` result;
12. no change to authorization, composition, approval, audit, or enforcement behavior.

## Dependency blocker

The repository must not import a real cryptographic runtime until dependency
adoption is explicitly approved.

Any implementation proposal that depends on `cryptography` or another runtime
must first record:

- dependency decision;
- version pinning approach;
- package artifact evidence;
- license and attribution review;
- runtime support evidence;
- rollback plan.

## Non-goals

This document does not cover:

- dependency adoption;
- package installation in the repository;
- requirements or lockfile changes;
- verifier source changes;
- schema changes;
- example passport updates;
- new passport signatures;
- real signature verification;
- signing-key generation;
- full official vector compatibility;
- test-level `hashAlg` handling;
- internal-interface vector execution;
- `mu` interface vector execution;
- issuer trust registry;
- signed revocation evidence;
- authorization policy changes;
- approval enforcement changes;
- audit storage;
- gateway, MCP, Civo, Supabase, or cloud integration;
- production readiness;
- legal or compliance conclusions;
- certification;
- passport-verifier `ALLOW` path.

## Next step

Review this boundary against the existing verifier code and tests before deciding
whether to create adapter-interface tests without importing a cryptographic
runtime.
