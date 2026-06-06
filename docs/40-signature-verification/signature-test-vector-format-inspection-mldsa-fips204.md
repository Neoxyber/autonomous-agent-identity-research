# Signature Test-Vector Format Inspection: ML-DSA FIPS204

## Purpose

This document records isolated format inspection of NIST ACVP-Server ML-DSA
FIPS204 JSON files.

The goal is to understand whether the official JSON vector structure appears
suitable for later isolated ML-DSA-65 compatibility testing.

This is format inspection only. It does not execute vectors, adopt a dependency,
install packages into the repository environment, change requirements or
lockfiles, change verifier source, change schema, implement real signature
verification, or create a passport-verifier `ALLOW` path.

## Environment

Repository state before the inspection:

- repository path: `~/projects/autonomous-agent-identity-research`
- repository commit: `5856713`
- repository virtual environment: `.venv`
- isolated inspection path: `/tmp/aaid-mldsa-vector-format`

The JSON files were downloaded and inspected only under `/tmp`.

No vector files were copied into the repository.

## Source family

The inspected files came from the `usnistgov/ACVP-Server` repository under:

`gen-val/json-files`

The inspected ML-DSA FIPS204 families were:

- `ML-DSA-keyGen-FIPS204`
- `ML-DSA-sigGen-FIPS204`
- `ML-DSA-sigVer-FIPS204`

## Downloaded files and hashes

Observed files and SHA-256 hashes:

| File | SHA-256 |
| --- | --- |
| `ML-DSA-keyGen-FIPS204/prompt.json` | `02fad612a060bbcf3bbbd164caf7e9da964ba385c90e08bcd26516e3bf8a023d` |
| `ML-DSA-keyGen-FIPS204/expectedResults.json` | `58dca0195226491c9cb117e1f0ec4cb11d4a1e3bd8b0f955371d80c99d4e8810` |
| `ML-DSA-sigGen-FIPS204/prompt.json` | `4305197be3c17be8f99338086eb8033ff2400f7d5b816123fc28b184c6e77a55` |
| `ML-DSA-sigGen-FIPS204/expectedResults.json` | `7b70ffeba6efe24e90760c751a7ebc4907931600645ebfa3f8a2459164d0a95d` |
| `ML-DSA-sigVer-FIPS204/prompt.json` | `2a9b7fcbefdd8e69dd6fbe6b4abb7130d855e8429aaa6f4904385e68b7e63d3a` |
| `ML-DSA-sigVer-FIPS204/expectedResults.json` | `33e0ea7dd9c3b0206712da50286ad746864371433977225ab77e8aae76358842` |

Result: PASS for isolated file hash capture.

## Top-level structure

The inspected JSON files used these common top-level fields:

- `algorithm`
- `mode`
- `revision`
- `testGroups`
- `vsId`
- `isSample`

Observed common values:

- algorithm: `ML-DSA`
- revision: `FIPS204`

Observed modes:

- `keyGen`
- `sigGen`
- `sigVer`

Result: PASS for identifying ML-DSA FIPS204 JSON structure.

## Case counts

Observed case counts:

| Family | Groups | Cases |
| --- | ---: | ---: |
| `ML-DSA-keyGen-FIPS204` | 3 | 75 |
| `ML-DSA-sigGen-FIPS204` | 24 | 360 |
| `ML-DSA-sigVer-FIPS204` | 12 | 180 |

Observed ML-DSA-65 coverage:

- `sigGen`: 8 ML-DSA-65 groups
- `sigVer`: 4 ML-DSA-65 groups

Result: PASS for identifying ML-DSA-65 coverage.

## Signature verification format

For ML-DSA-65 `sigVer`, observed prompt groups included:

- `parameterSet`
- `testType`
- `signatureInterface`
- `message` or `mu`
- `context` where applicable
- `pk`
- `signature`
- `tcId`

Observed ML-DSA-65 `sigVer` byte lengths:

- public key: `1952` bytes
- signature: `3309` bytes
- `mu`: `64` bytes where present

The expected results file mapped each test case to `testPassed`.

Observed ML-DSA-65 `sigVer` groups had 15 tests per group, with observed
expected-result distribution of 3 passing cases and 12 failing cases per
inspected group.

Result: PASS for identifying `sigVer` fields, byte lengths, and pass/fail
labels.

## Signature generation format

For ML-DSA-65 `sigGen`, observed prompt groups included:

- `parameterSet`
- `testType`
- `signatureInterface`
- `message` or `mu`
- `context` where applicable
- `sk`
- `rnd` where applicable
- `tcId`

Observed ML-DSA-65 `sigGen` byte lengths:

- secret key: `4032` bytes
- signature: `3309` bytes
- `rnd`: `32` bytes where present
- `mu`: `64` bytes where present

Result: PASS for identifying `sigGen` fields and byte lengths.

## Runtime mapping notes

The observed public-key length of `1952` bytes and signature length of `3309`
bytes match the isolated `cryptography==48.0.0` ML-DSA-65 runtime observations.

This suggests that `sigVer` vector-format execution may be feasible with raw
public-key and signature APIs.

This does not prove official vector compatibility yet.

## Evaluation classification

| Area | Result |
| --- | --- |
| Official source family identified | PASS |
| FIPS204 revision identified | PASS |
| ML-DSA-65 coverage identified | PASS |
| `sigVer` prompt fields identified | PASS |
| `sigVer` expected pass/fail labels identified | PASS |
| `sigGen` prompt and expected fields identified | PASS |
| Raw public-key length mapping | PASS |
| Raw signature length mapping | PASS |
| Vector execution | NOT TESTED |
| Official compatibility | NOT TESTED |
| Repository dependency adoption | NOT APPROVED |

Overall result: PARTIAL.

The vector format appears suitable for later isolated compatibility testing, but
official compatibility remains unproven until vector execution is explicitly
approved and recorded.

## Limitations

This inspection did not execute vector cases.

This inspection did not verify repository history, signed releases, maintainer
identity, or external provenance for the downloaded JSON files.

The inspected files were not copied into the repository.

This result is not a validation claim for `cryptography`, ML-DSA, or the
repository verifier.

## Not implemented

This inspection did not implement:

- official vector execution;
- repository dependency adoption;
- package installation in the repository environment;
- requirements or lockfile changes;
- verifier source changes;
- schema changes;
- example passport updates;
- real signature verification;
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

Decide whether to run an isolated `/tmp` ML-DSA-65 `sigVer` compatibility test
against the inspected NIST ACVP-Server FIPS204 JSON files.
