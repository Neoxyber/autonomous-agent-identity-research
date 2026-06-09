# Signature Test-Vector Compatibility Plan

## Purpose

This document defines the first compatibility plan for ML-DSA test-vector
evidence.

The goal is to decide how official or authoritative ML-DSA-65 test-vector
material should be reviewed before any repository dependency adoption, verifier
integration, or real signature-verification implementation.

This is planning only. It does not download test vectors, execute test vectors,
adopt a dependency, install packages into the repository environment, change
requirements or lockfiles, change verifier source, change schema, add real
passport signature material, or create a passport-verifier `ALLOW` path.

## Current boundary

The repository has recorded isolated runtime behavior for Python
`cryptography==48.0.0`.

The candidate showed ML-DSA-65 API availability, disposable key generation,
signing, verification, raw public-key export/import, and expected failure
behavior for modified or malformed inputs.

That result remains PARTIAL because official test-vector compatibility has not
been tested.

## Source boundary

The project should prefer final-version ML-DSA material from NIST CAVP / ACVP
sources.

Draft-era or intermediate post-quantum vectors must not be treated as final
ML-DSA compatibility evidence unless the limitation is explicitly recorded.

Self-generated signatures are useful for runtime smoke testing, but they are not
sufficient evidence for implementation readiness.

## Candidate vector source

The first source family to review is NIST CAVP / ACVP ML-DSA JSON material.

The planned source review should identify:

1. exact repository or publisher location;
2. exact vector file names;
3. whether vectors target FIPS 204 final ML-DSA;
4. whether vectors include ML-DSA-65;
5. whether vectors cover signature generation;
6. whether vectors cover signature verification;
7. whether vectors include context or external-interface cases;
8. whether vectors include invalid signature cases;
9. whether vectors include public-key or signature encoding expectations;
10. whether vectors can be used with the candidate Python runtime without
    modifying repository source.

## Compatibility questions

Before execution, the project must answer:

1. What message bytes are signed?
2. What public-key bytes are provided?
3. What signature bytes are expected?
4. How are seeds, messages, public keys, and signatures encoded in JSON?
5. Does the vector set include ML-DSA-65 only, or multiple parameter sets?
6. Does the vector set use deterministic test seeds or externally computed
   values?
7. Does the vector format map cleanly to `cryptography` raw public-key and
   signature APIs?
8. Are invalid vectors expected to fail with `InvalidSignature`, `ValueError`,
   or another mapped failure?
9. Can failures be recorded as fail-closed verifier checks later?
10. Does any test require API behavior not exposed by the candidate runtime?

## Planned compatibility categories

Future compatibility review should use these categories:

| Area | Result |
| --- | --- |
| Source identity | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL |
| Final-vector status | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL |
| ML-DSA-65 coverage | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL |
| Signature-verification coverage | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL |
| Encoding clarity | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL |
| Runtime API compatibility | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL |
| Negative-vector behavior | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL |
| Adoption readiness | PASS, PARTIAL, BLOCKED, NEEDS_RESEARCH, or FAIL |

A candidate may pass runtime testing and still remain blocked on official
test-vector compatibility.

## Isolated execution rule

If vector execution is approved later, it must run outside the repository
environment first.

The preferred temporary location is:

`$AAID_SIGNATURE_SANDBOX/mldsa-vector-eval`

The repository virtual environment must not receive package installs, generated
keys, generated signatures, downloaded vectors, scripts, logs, or copied
artifacts unless a sanitized result is explicitly approved for documentation.

## Evidence to capture later

If vector review or vector execution is approved later, record:

1. source location;
2. access date;
3. file names;
4. hash of downloaded vector files if applicable;
5. vector set type;
6. parameter set;
7. number of relevant ML-DSA-65 cases;
8. valid and invalid case counts;
9. encoding assumptions;
10. runtime version;
11. pass/fail counts;
12. exception mapping;
13. limitations;
14. result category;
15. next step.

## Stop conditions

Stop the compatibility work if:

1. the vector source is not clearly official or authoritative;
2. the vector set appears draft-era or mismatched to FIPS 204 final ML-DSA;
3. ML-DSA-65 cases cannot be identified;
4. key or signature encodings are unclear;
5. the candidate runtime cannot import the required key or signature format;
6. vector execution would require repository dependency adoption;
7. results cannot be mapped to fail-closed verifier behavior;
8. security-relevant findings require responsible disclosure.

## Non-goals

This document does not cover:

- downloading official vectors into the repository;
- executing official vectors;
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
- legal or compliance conclusions;
- certification;
- passport-verifier `ALLOW` path.

## Next step

Review exact NIST CAVP / ACVP ML-DSA vector files and decide whether an
isolated signature-sandbox vector-format inspection should be approved.
