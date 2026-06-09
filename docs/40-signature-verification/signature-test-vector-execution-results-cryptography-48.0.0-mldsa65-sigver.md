# Signature Test-Vector Execution Results: cryptography 48.0.0 ML-DSA-65 sigVer

## Purpose

This document records the first isolated ML-DSA-65 signature-verification
compatibility test against NIST ACVP-Server ML-DSA FIPS204 `sigVer` JSON files.

The goal was to test whether Python `cryptography==48.0.0` can verify selected
ML-DSA-65 signature-verification vectors using raw public-key bytes, raw
signature bytes, message bytes, and context bytes.

This is isolated test-vector execution evidence only. It does not adopt a
dependency, install packages into the repository environment, change
requirements or lockfiles, change verifier source, change schema, implement real
passport signature verification, or create a passport-verifier `ALLOW` path.

## Environment

Repository state before the isolated test:

- repository path: `$AAID_PROJECT_ROOT`
- repository commit: `0d0712a`
- repository virtual environment: `.venv`
- isolated test workspace: `$AAID_SIGNATURE_SANDBOX/mldsa-sigver-compat`
- isolated virtual environment: `$AAID_SIGNATURE_SANDBOX/mldsa-sigver-compat/.venv`
- Python version: `3.12.3`
- candidate package: `cryptography==48.0.0`

The package was installed and executed only in the isolated signature test-vector
workspace.

No package was installed into the repository virtual environment.

## Source files

The isolated run downloaded these NIST ACVP-Server files under the isolated
signature test-vector workspace only:

- `ML-DSA-sigVer-FIPS204/prompt.json`
- `ML-DSA-sigVer-FIPS204/expectedResults.json`

Observed SHA-256 hashes:

| File | SHA-256 |
| --- | --- |
| `ML-DSA-sigVer-FIPS204/prompt.json` | `2a9b7fcbefdd8e69dd6fbe6b4abb7130d855e8429aaa6f4904385e68b7e63d3a` |
| `ML-DSA-sigVer-FIPS204/expectedResults.json` | `33e0ea7dd9c3b0206712da50286ad746864371433977225ab77e8aae76358842` |

No vector files were copied into the repository.

## Candidate package

Observed installed package metadata:

- package: `cryptography`
- version: `48.0.0`
- runtime dependency: `cffi==2.0.0`
- transitive dependency: `pycparser==3.0`
- isolated installation path: `$AAID_SIGNATURE_SANDBOX/mldsa-sigver-compat/.venv`

## Test scope

The first compatibility run targeted ML-DSA-65 `sigVer` groups where
`signatureInterface` was `external`.

The first run did not support:

- `internal` interface groups;
- `mu` interface behavior;
- test-level `hashAlg` pre-hash behavior.

The first run selected external groups using group-level metadata only. During
analysis, the run showed that `hashAlg` appears at the test-case level in one
ML-DSA-65 external group.

## First run result

The first run selected two ML-DSA-65 external groups:

- `tgId` 3
- `tgId` 4

Observed result:

| Area | Result |
| --- | ---: |
| total cases executed | 30 |
| matches | 27 |
| mismatches | 3 |
| unexpected errors | 0 |

Group result:

| Group | Description | Matches | Total |
| --- | --- | ---: | ---: |
| `tgId` 3 | external, no `hashAlg` test cases | 15 | 15 |
| `tgId` 4 | external, test-level `hashAlg` cases | 12 | 15 |

The mismatches were:

| Group | Test case | Expected | Observed |
| --- | ---: | --- | --- |
| `tgId` 4 | `tcId` 48 | `true` | `false` |
| `tgId` 4 | `tcId` 49 | `true` | `false` |
| `tgId` 4 | `tcId` 51 | `true` | `false` |

Result: NEEDS_RESEARCH for the first broad external run.

The mismatch pattern was concentrated in `tgId` 4 and did not indicate a general
failure of raw public-key or signature verification.

## Follow-up classification

A follow-up inspection classified ML-DSA-65 `sigVer` groups by test-level
`hashAlg`.

Observed ML-DSA-65 groups:

| Group | Interface | Test-level `hashAlg` | Expected labels |
| --- | --- | --- | --- |
| `tgId` 3 | external | none | 3 pass, 12 fail |
| `tgId` 4 | external | present on all 15 tests | 3 pass, 12 fail |
| `tgId` 9 | internal | none | 3 pass, 12 fail |
| `tgId` 10 | internal | none | 3 pass, 12 fail |

The `tgId` 4 tests used hash algorithms including SHA2, SHA3, SHAKE, and
SHA2-512 truncated variants. The earlier mismatched expected-valid cases were
inside this test-level `hashAlg` group.

## Corrected direct external non-hash run

The corrected run executed only direct external ML-DSA-65 `sigVer` test cases
that did not include test-level `hashAlg`.

Observed result:

| Area | Count |
| --- | ---: |
| total executed | 15 |
| matches | 15 |
| mismatches | 0 |
| skipped test-level `hashAlg` cases | 15 |
| skipped internal-interface cases | 30 |

Result: PASS for direct external ML-DSA-65 `sigVer` cases excluding test-level
`hashAlg` and internal-interface cases.

## Interpretation

The isolated result supports three separate conclusions:

1. Direct external ML-DSA-65 signature verification over message bytes and
   context bytes matched the NIST ACVP-Server expected `testPassed` labels for
   the non-`hashAlg` subset.
2. Test-level `hashAlg` cases require separate pre-hash or hash-interface
   handling and must not be treated as ordinary message-mode verification.
3. Internal-interface and `mu` cases remain untested.

Overall result: PARTIAL.

This is a useful compatibility finding because it identifies a clear boundary
between direct external message verification and hash/pre-hash vector handling.

## Evaluation classification

| Area | Result |
| --- | --- |
| Isolated signature-sandbox execution | PASS |
| Repository non-adoption | PASS |
| ML-DSA-65 direct external non-hash `sigVer` | PASS |
| Test-level `hashAlg` detection | PASS |
| Test-level `hashAlg` execution | NEEDS_RESEARCH |
| Internal interface execution | NOT TESTED |
| `mu` interface execution | NOT TESTED |
| Full official vector compatibility | PARTIAL |
| Repository dependency adoption | NOT APPROVED |
| Verifier integration readiness | PARTIAL |

## Security and research notes

No unexpected successful verification was observed in the executed cases.

The initial mismatches were expected-valid test cases observed as invalid when
test-level `hashAlg` handling was not implemented in the test script.

This should be treated as an API and vector-format mapping boundary, not as a
library vulnerability.

No runtime behavior in this isolated run changed the repository safety boundary.

This result is not a security audit of `cryptography`.

## Not implemented

This evaluation did not implement:

- repository dependency adoption;
- package installation in the repository environment;
- requirements or lockfile changes;
- verifier source changes;
- schema changes;
- example passport updates;
- full official vector execution;
- test-level `hashAlg` handling;
- internal-interface vector execution;
- `mu` interface vector execution;
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
- legal or compliance conclusions;
- certification;
- passport-verifier `ALLOW` path.

## Next step

Research the correct ML-DSA `hashAlg` and internal-interface mapping before
expanding official vector execution beyond direct external non-hash `sigVer`
cases.
