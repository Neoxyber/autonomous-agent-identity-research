# Signature Verification Runtime Research

## Purpose

This document defines how the project will evaluate runtime support for real
passport signature verification before any implementation proposal.

The focus is ML-DSA-65 as the first passport signature research target.

This is research planning only. It does not adopt a dependency, install a
package, change requirements or lockfiles, change verifier source, change schema,
add real signature material, run test vectors, or create a passport-verifier
`ALLOW` path.

## Current boundary

The repository now has a focused signature-verification planning document.

Real signature verification is still not implemented.

The verifier currently prepares canonical passport payload bytes, records
`signature_input_prepared`, checks supported signature algorithm metadata, records
`signature_verification_not_implemented`, returns `DENY`, and cannot return
`ALLOW`.

The current repository has no adopted cryptographic dependency for real passport
signature verification.

## Research question

The next research question is:

Which ML-DSA runtime path, key encoding, signature encoding, and test-vector
source are suitable for fail-closed autonomous-agent passport signature
verification?

A suitable answer must be based on evidence, not package popularity alone.

## Standards basis

ML-DSA-65 remains the first passport signature research target.

SLH-DSA remains a backup signature-family research direction.

ML-KEM is not a passport signature algorithm and remains future work for secure
key establishment.

The project must not implement post-quantum cryptographic primitives from
scratch.

## Candidate runtime paths

The first runtime paths to evaluate are:

1. Python `cryptography` ML-DSA support.
2. Open Quantum Safe `liboqs` and appropriate language bindings.
3. Other maintained ML-DSA-capable libraries only after source, license,
   maintenance, dependency, and security review.

Candidate evaluation does not mean adoption.

A candidate may be useful for isolated research even if it is not suitable for
repository dependency adoption.

## Runtime-support questions

Each candidate must answer:

1. Does it support ML-DSA-65?
2. Does it support verification without requiring custom cryptography?
3. Which backend or native library is required?
4. Can public keys be imported from bytes?
5. Can signatures be verified from bytes?
6. What exact key and signature byte formats are accepted?
7. Does it expose raw public-key bytes and raw signature bytes?
8. Does it fail cleanly for malformed keys and signatures?
9. Does it raise exceptions that can be mapped to fail-closed verifier checks?
10. Does behavior differ by platform, backend, or build configuration?

## Encoding questions

The current schema includes `public_key_b64u` and `signature_b64u`.

The initial planning position is unpadded base64url encoding of raw ML-DSA-65
public-key bytes and raw ML-DSA-65 signature bytes.

This remains a hypothesis until candidate libraries and test-vector sources are
reviewed.

The research must record whether a candidate expects raw bytes, standardized
containers, library-specific serialization, or another proof format.

## Test-vector questions

Real signature verification must not be implemented until test-vector sources are
reviewed and recorded.

The project should prefer final-version ML-DSA-65 vectors or validation-style
test material from official or authoritative sources.

The research should avoid relying on draft-era vectors unless the limitation is
explicitly recorded.

Self-generated key and signature examples may be useful later, but they should
not be the only evidence for implementation readiness.

## Evidence matrix

Each candidate runtime path should be recorded with these categories:

| Area | Result | Evidence needed |
| --- | --- | --- |
| Source identity | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL | Official source or repository identity checked |
| License and attribution | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL | License signal and attribution requirements reviewed |
| Maintenance risk | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL | Release activity, issues, security posture, and support status reviewed |
| Dependency surface | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL | Runtime and build dependencies understood |
| Backend support | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL | Required backend or native library identified |
| ML-DSA-65 support | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL | Key generation, signing, or verification support checked |
| Key encoding | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL | Accepted public-key byte format recorded |
| Signature encoding | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL | Accepted signature byte format recorded |
| Test-vector compatibility | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL | Candidate checked against selected vectors |
| Fail-closed behavior | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL | Malformed input and exception behavior recorded |
| Adoption readiness | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL | Decision based on all earlier evidence |

## Evaluation rules

Candidate evaluation must run outside the repository environment unless a later
decision explicitly approves repository dependency adoption.

Temporary tools, downloaded artifacts, generated keys, scripts, logs, and test
outputs should stay outside the repository unless a specific sanitized result is
approved for documentation.

The repository must not accidentally adopt a candidate through requirements,
lockfiles, imports, copied source, generated artifacts, or example data.

## Security and disclosure boundary

The research may find library bugs, unsafe defaults, unclear documentation,
backend differences, malformed-input failures, or encoding ambiguity.

Security-relevant findings should be reproduced in an isolated environment,
minimized, and handled through responsible disclosure before public technical
details are recorded.

Public evidence should avoid exploit-style detail until maintainers have been
notified when appropriate.

## Findings useful to industry

The most useful findings are likely to be negative or boundary findings:

1. malformed public key fails cleanly;
2. malformed signature fails cleanly;
3. wrong key fails;
4. wrong algorithm fails;
5. modified payload fails;
6. modified signature fails;
7. unsupported backend is detected clearly;
8. library exceptions can be mapped to `DENY`;
9. key and signature sizes are recorded;
10. valid signature does not create `ALLOW` by itself.

## Non-goals

This document does not cover:

- package installation in the repository;
- dependency adoption;
- requirements or lockfile changes;
- source changes;
- schema changes;
- example passport updates;
- real signature verification;
- signing-key generation in the repository;
- test-vector execution;
- permanent runtime integration;
- issuer trust registry;
- signed revocation evidence;
- authorization policy changes;
- approval enforcement changes;
- audit storage;
- gateway, MCP, Civo, Supabase, or cloud integration;
- production readiness;
- legal or compliance conclusions;
- certification.

## Next step

Review candidate sources and exact reference entries before running any isolated
runtime experiment.
