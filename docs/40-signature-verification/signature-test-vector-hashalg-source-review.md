# Signature Test-Vector hashAlg Source Review

## Purpose

This document records source-review findings for ML-DSA `hashAlg`,
internal-interface, `externalMu`, and `mu` mapping.

The goal is to decide what must be understood before expanding isolated
ML-DSA-65 `sigVer` vector execution beyond the direct external non-hash subset.

This is source review only. It does not execute more vectors, adopt a
dependency, install packages into the repository environment, change requirements
or lockfiles, change verifier source, change schema, implement real signature
verification, or create a passport-verifier `ALLOW` path.

## Current repository boundary

The repository has recorded isolated ML-DSA-65 `sigVer` execution evidence for
Python `cryptography==48.0.0`.

The direct external non-hash subset passed with:

- 15 executed cases;
- 15 matches;
- 0 mismatches.

The first broader external run executed 30 cases and produced 3 mismatches. All
3 mismatches were in `tgId` 4, where follow-up inspection showed test-level
`hashAlg` values on all 15 cases.

The current result remains PARTIAL.

## Source review findings

### FIPS 204

FIPS 204 is the final NIST standard for ML-DSA.

The source-review conclusion is that any future ML-DSA compatibility statement
must stay aligned with FIPS 204 terminology and must not treat pure ML-DSA,
HashML-DSA, internal-interface inputs, and `mu` inputs as interchangeable.

### ACVP ML-DSA JSON specification

The ACVP ML-DSA JSON specification defines JSON structures for testing ML-DSA
implementations.

The source-review conclusion is that ACVP vector fields need explicit mapping
before execution. `hashAlg`, `signatureInterface`, `externalMu`, and `mu` cannot
be silently treated as ordinary message-mode inputs.

### cryptography runtime support

Python `cryptography==48.0.0` passed the direct external non-hash ML-DSA-65
`sigVer` subset in isolated testing.

The source-review conclusion is that this does not prove HashML-DSA support or
internal-interface support. Candidate runtime documentation and issue history
must be reviewed before attempting `hashAlg`, internal-interface, or `mu` cases.

### Protocol profile context

ML-DSA protocol profiles may intentionally choose pure ML-DSA and exclude
HashML-DSA.

The source-review conclusion is that protocol usage should not assume that
HashML-DSA is required or appropriate for every integration. Passport signature
verification can initially remain scoped to direct external message-mode
verification unless a later profile decision records otherwise.

## Mapping risks

The main mapping risks are:

1. treating `hashAlg` cases as ordinary message-mode verification;
2. treating `mu` as a public protocol input without justification;
3. treating internal-interface vectors as passport-verifier requirements;
4. treating candidate runtime limitations as verifier behavior;
5. overstating compatibility after only the direct external non-hash subset;
6. mixing pure ML-DSA and HashML-DSA semantics without a recorded profile
   decision.

## Research decision

The project should not expand official vector execution until these questions
are answered:

1. Does the candidate runtime expose HashML-DSA verification?
2. If it does, what exact API and input format are required?
3. If it does not, should `hashAlg` cases remain out of scope?
4. Are internal-interface and `mu` cases intended for implementation-internal
   validation rather than passport protocol verification?
5. Should the passport proof profile initially support only pure direct external
   ML-DSA message-mode verification?
6. What verifier check names should represent unsupported or unmapped signature
   modes?

## Evaluation classification

| Area | Result |
| --- | --- |
| Direct external non-hash ML-DSA-65 `sigVer` | already PASS for selected subset |
| `hashAlg` mapping | NEEDS_RESEARCH |
| HashML-DSA runtime support | NEEDS_RESEARCH |
| internal-interface mapping | NEEDS_RESEARCH |
| `mu` mapping | NEEDS_RESEARCH |
| passport proof-profile decision | NEEDS_RESEARCH |
| additional vector execution readiness | BLOCKED until mapping review |
| verifier integration readiness | PARTIAL |

Overall result: NEEDS_RESEARCH.

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
- legal or compliance conclusions;
- certification;
- passport-verifier `ALLOW` path.

## Next step

Review FIPS 204 and ACVP ML-DSA mapping details more closely before deciding
whether to keep passport signature verification scoped to pure direct external
ML-DSA message-mode verification for the first implementation plan.
