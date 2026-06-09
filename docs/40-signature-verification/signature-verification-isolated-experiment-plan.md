# Signature Verification Isolated Experiment Plan

## Purpose

This document defines the first isolated experiment plan for ML-DSA runtime
evaluation.

The goal is to evaluate candidate runtime support, key encoding, signature
encoding, and failure behavior before any repository dependency adoption or
signature-verification implementation.

This is planning only. It does not install packages, run experiments, change
requirements or lockfiles, change verifier source, change schema, add real
signature material, run test vectors, or create a passport-verifier `ALLOW` path.

## Current boundary

The repository has planning documents for signature verification and signature
runtime research.

Real signature verification is still not implemented.

The verifier currently prepares canonical passport payload bytes, records
`signature_input_prepared`, checks supported signature algorithm metadata, records
`signature_verification_not_implemented`, returns `DENY`, and cannot return
`ALLOW`.

## Experiment location

Any future runtime experiment must run outside the repository environment.

The preferred temporary location is:

`$AAID_SIGNATURE_SANDBOX/mldsa-runtime-eval`

The experiment must not install packages into the repository environment.

The experiment must not write generated keys, signatures, downloaded packages,
logs, or scripts into the repository unless sanitized documentation output is
explicitly approved.

## Candidate order

The first candidate order is:

1. Python `cryptography` ML-DSA API and backend availability.
2. Open Quantum Safe `liboqs` and suitable language bindings.
3. Other maintained ML-DSA-capable libraries only after separate source,
   license, maintenance, dependency, and security review.

Candidate evaluation does not mean adoption.

## Allowed experiment actions

A future isolated experiment may:

1. create a temporary workspace under `$AAID_SIGNATURE_SANDBOX`;
2. create an isolated package environment inside that workspace;
3. inspect package metadata and versions;
4. check whether ML-DSA-65 APIs are available;
5. check backend or native-library requirements;
6. generate disposable research keys only inside the signature sandbox;
7. sign disposable test messages only inside the signature sandbox;
8. verify disposable signatures only inside the signature sandbox;
9. test malformed public-key and signature handling;
10. record sanitized findings for later documentation review.

## Disallowed experiment actions

A future isolated experiment must not:

1. install packages into the repository environment;
2. modify repository requirements or lockfiles;
3. import candidate libraries from repository source code;
4. copy candidate source into the repository;
5. modify verifier source;
6. modify schema files;
7. modify example passport files;
8. add real keys or signatures to the repository;
9. run production credentials or real agent data;
10. create any passport-verifier `ALLOW` path.

## Evidence to capture

A future isolated experiment should capture:

1. operating system and Python version;
2. temporary environment path;
3. candidate name and version;
4. package source and artifact source;
5. dependency and backend requirements;
6. whether ML-DSA-65 is available;
7. accepted public-key byte format;
8. accepted signature byte format;
9. observed public-key size;
10. observed signature size;
11. signing and verification behavior for disposable inputs;
12. failure behavior for modified messages;
13. failure behavior for malformed public keys;
14. failure behavior for malformed signatures;
15. exception types and whether they can map to `DENY`;
16. limitations and unanswered questions.

## Result categories

Results should use the repository evaluation categories:

- PASS
- FAIL
- PARTIAL
- BLOCKED
- NEEDS_RESEARCH

A candidate may pass one category and remain blocked for adoption.

## Stop conditions

The experiment should stop if:

1. the candidate cannot be installed or inspected safely in the signature sandbox;
2. the candidate requires repository dependency changes;
3. ML-DSA-65 support is unavailable in the observed runtime;
4. backend requirements are unclear;
5. accepted key or signature encoding is unclear;
6. test-vector compatibility cannot be evaluated;
7. errors cannot be mapped safely to fail-closed behavior;
8. security-relevant behavior requires responsible disclosure.

## Responsible disclosure

If a security-relevant library or tool issue is observed, the finding should be
reproduced in isolation, minimized, and handled through responsible disclosure
before public technical details are recorded.

Public documentation should avoid exploit-style detail until maintainers have
been notified when appropriate.

## Non-goals

This document does not cover:

- package execution;
- package installation in the repository;
- dependency adoption;
- requirements or lockfile changes;
- verifier source changes;
- schema changes;
- example passport updates;
- real signature verification;
- signing-key generation in the repository;
- permanent runtime integration;
- test-vector execution in the repository;
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

Review this plan before approving any isolated signature-sandbox runtime
experiment.
