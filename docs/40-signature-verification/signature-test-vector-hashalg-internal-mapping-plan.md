# Signature Test-Vector hashAlg and Internal Mapping Plan

## Purpose

This document records the next research boundary for ML-DSA test-vector
compatibility.

The goal is to understand how NIST ACVP-Server ML-DSA FIPS204 `sigVer`
test-level `hashAlg`, internal-interface, `externalMu`, and `mu` fields should
map to candidate runtime APIs before expanding isolated vector execution.

This is mapping research only. It does not execute more vectors, adopt a
dependency, install packages into the repository environment, change requirements
or lockfiles, change verifier source, change schema, implement real signature
verification, or create a passport-verifier `ALLOW` path.

## Current boundary

The repository has recorded isolated ML-DSA-65 `sigVer` execution evidence for
Python `cryptography==48.0.0`.

The direct external non-hash ML-DSA-65 `sigVer` subset passed:

- 15 executed cases
- 15 matches
- 0 mismatches

The first broader external run executed 30 cases and produced 3 mismatches. All
3 mismatches were in `tgId` 4, where follow-up inspection showed test-level
`hashAlg` values on all 15 cases.

The current result remains PARTIAL.

## Research question

The next question is not whether the candidate can verify ordinary ML-DSA
message-mode signatures.

The next question is how ACVP `hashAlg`, internal-interface, `externalMu`, and
`mu` test cases should be interpreted and whether the candidate runtime exposes
the required interface safely and clearly.

## Mapping topics

The next research step should clarify:

1. whether test-level `hashAlg` maps to HashML-DSA / pre-hash verification;
2. whether the candidate runtime supports HashML-DSA verification directly;
3. whether `hashAlg` values identify the hash applied before ML-DSA verification;
4. whether the ACVP `message` field remains the original message for `hashAlg`
   cases;
5. whether the ACVP `mu` field represents an internal digest/input that should
   not be reconstructed by the repository;
6. how `externalMu` changes the meaning of the supplied input;
7. whether internal-interface cases are intended for implementation-internal
   validation rather than public protocol use;
8. whether context handling differs between pure and hash/pre-hash modes;
9. whether failures can still map cleanly to fail-closed verifier checks;
10. whether unsupported mapping should remain `NEEDS_RESEARCH` rather than being
    forced into implementation.

## Source review targets

The next source review should use official or authoritative sources first:

1. NIST FIPS 204 final standard;
2. NIST ACVP ML-DSA JSON specification;
3. NIST ACVP-Server sample vector files and release notes;
4. Python `cryptography` ML-DSA documentation and changelog;
5. relevant pyca/cryptography issue or release notes for HashML-DSA support;
6. IETF ML-DSA encoding/profile documents only as protocol-context evidence.

Non-authoritative commentary may inform risk questions, but it should not drive
implementation decisions.

## Possible outcomes

Future mapping research may conclude:

| Area | Possible result |
| --- | --- |
| Pure direct external `sigVer` | already PASS for selected subset |
| test-level `hashAlg` | PASS, NEEDS_RESEARCH, BLOCKED, or NOT SUPPORTED |
| internal interface | PASS, NEEDS_RESEARCH, BLOCKED, or NOT SUITABLE |
| `mu` interface | PASS, NEEDS_RESEARCH, BLOCKED, or NOT SUITABLE |
| candidate runtime support | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL |
| verifier integration readiness | PARTIAL until implementation planning is complete |

Unsupported or unclear mappings should not be forced into verifier
implementation.

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

Review FIPS 204, the ACVP ML-DSA JSON specification, and the candidate runtime
documentation to decide whether `hashAlg`, internal-interface, and `mu` cases can
be executed safely in isolation or should remain explicitly out of scope.
