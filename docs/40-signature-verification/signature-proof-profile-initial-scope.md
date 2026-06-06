# Signature Proof Profile Initial Scope

## Purpose

This document records the initial passport signature-proof profile scope for
future real signature-verification planning.

The goal is to define the first supported signature-verification boundary before
any verifier implementation, dependency adoption, schema change, or `ALLOW` path.

This is a profile-scope decision only. It does not execute vectors, adopt a
dependency, install packages into the repository environment, change requirements
or lockfiles, change verifier source, change schema, implement real signature
verification, or create a passport-verifier `ALLOW` path.

## Current evidence boundary

The repository has recorded isolated ML-DSA-65 `sigVer` evidence for Python
`cryptography==48.0.0`.

The direct external non-hash ML-DSA-65 `sigVer` subset passed:

- 15 executed cases;
- 15 matches;
- 0 mismatches.

The broader external run remains PARTIAL because 3 mismatches occurred in
`tgId` 4, where follow-up inspection showed test-level `hashAlg` values on all
15 cases.

The current source review concludes that pure ML-DSA, HashML-DSA,
internal-interface inputs, `externalMu`, and `mu` inputs must not be treated as
interchangeable.

## Initial profile scope

The first passport signature-verification profile should be scoped to:

- ML-DSA-65;
- pure direct external message-mode verification;
- canonical passport payload bytes as the signed message;
- explicit context handling only after a profile decision records the context
  value;
- raw public-key bytes only after key encoding is finalized;
- raw signature bytes only after signature encoding is finalized.

This scope matches the only official-vector subset currently recorded as passing
in isolated testing.

## Explicitly out of scope

The first profile should not include:

- test-level `hashAlg` cases;
- HashML-DSA;
- internal-interface cases;
- `externalMu` cases;
- `mu` input handling;
- reconstructed internal ML-DSA values;
- signing operations;
- generated passport test signatures;
- verifier `ALLOW` behavior.

These areas remain unresolved until separate mapping research records a clear
and testable decision.

## Required implementation preconditions

Before implementing real signature verification, the project must still decide:

1. exact proof algorithm identifier;
2. exact key encoding;
3. exact signature encoding;
4. exact context value or explicit empty-context rule;
5. exact failure check names for unsupported signature modes;
6. exact malformed-input behavior;
7. exact dependency adoption decision;
8. exact rollback plan;
9. targeted tests for invalid signatures and malformed encodings;
10. whether a verified signature is allowed to change the verifier result, or
    whether the verifier still remains non-ALLOW during the first implementation.

## Failure behavior

Unsupported signature modes should fail closed.

Examples include:

- unsupported algorithm metadata;
- unsupported signature profile;
- `hashAlg` / HashML-DSA cases;
- internal-interface cases;
- `mu` inputs;
- unsupported key encoding;
- unsupported signature encoding;
- malformed public-key bytes;
- malformed signature bytes;
- runtime verification errors;
- invalid signatures.

These should be represented as named verifier checks and `DENY` results, not as
unhandled exceptions.

## Research position

The project should not claim full ML-DSA compatibility.

The project should only claim that the selected direct external non-hash
ML-DSA-65 `sigVer` subset passed in isolated testing.

The passport proof profile should remain narrow until additional mapping and
runtime evidence is recorded.

## Non-goals

This document does not cover:

- additional vector execution;
- package installation in the repository;
- dependency adoption;
- requirements or lockfile changes;
- verifier source changes;
- schema changes;
- example passport updates;
- real passport signature verification;
- full official vector compatibility;
- test-level `hashAlg` handling implementation;
- internal-interface vector execution;
- `mu` interface vector execution;
- permanent runtime integration;
- signing-key generation in the repository;
- issuer trust registry;
- signed revocation evidence;
- authorization policy changes;
- approval enforcement changes;
- audit storage;
- gateway, MCP, Civo, Supabase, or cloud integration;
- production readiness;
- legal compliance;
- certification;
- passport-verifier `ALLOW` path.

## Next step

Plan the first implementation boundary for pure direct external ML-DSA-65
message-mode verification without changing verifier behavior yet.
