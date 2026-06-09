# Signature Runtime Evaluation Results: cryptography 48.0.0

## Purpose

This document records the first isolated ML-DSA runtime evaluation result for
Python `cryptography`.

The evaluation was run outside the repository environment in a temporary
signature runtime workspace.

This is isolated runtime evidence only. It does not adopt a dependency, install
packages into the repository environment, change requirements or lockfiles,
change verifier source, change schema, add real passport signature material,
execute official test vectors, implement real signature verification, or create a
passport-verifier `ALLOW` path.

## Environment

Repository state before the isolated test:

- repository path: `$AAID_PROJECT_ROOT`
- repository commit: `03a6d09`
- repository virtual environment: `.venv`
- isolated experiment workspace: `$AAID_SIGNATURE_SANDBOX/mldsa-runtime-eval`
- isolated virtual environment: `$AAID_SIGNATURE_SANDBOX/mldsa-runtime-eval/.venv`
- Python version: `3.12.3`
- pip version after upgrade: `26.1.2`

The package was installed and executed only in the isolated signature runtime
workspace.

## Candidate

Candidate:

- package: `cryptography`
- observed version: `48.0.0`
- observed runtime dependency: `cffi==2.0.0`
- observed transitive dependency: `pycparser==3.0`
- observed backend signal: `OpenSSL 4.0.0 14 Apr 2026`

## Availability result

The isolated runtime exposed the ML-DSA module.

Observed ML-DSA names included:

- `MLDSA44PrivateKey`
- `MLDSA44PublicKey`
- `MLDSA65PrivateKey`
- `MLDSA65PublicKey`
- `MLDSA87PrivateKey`
- `MLDSA87PublicKey`

Observed ML-DSA-65 attributes:

- `MLDSA65PrivateKey`: available
- `MLDSA65PublicKey`: available

Result: PASS for ML-DSA-65 API availability in the isolated environment.

## Disposable sign and verify result

A disposable ML-DSA-65 key pair was generated inside the isolated signature
runtime workspace.

Observed values:

- private key type: `MLDSA65PrivateKey`
- public key type: `MLDSA65PublicKey`
- raw public key length: `1952`
- private seed length: `32`
- signature length: `3309`

A disposable message was signed with a context value.

The valid signature verified successfully.

Result: PASS for disposable ML-DSA-65 sign and verify behavior.

## Negative behavior result

The isolated runtime returned expected failure behavior for modified inputs:

- modified message: `InvalidSignature`
- modified signature: `InvalidSignature`
- wrong context: `InvalidSignature`

Result: PASS for modified message, modified signature, and wrong-context
rejection.

## Raw public key import result

The raw public key bytes were exported and imported again.

The imported public key verified the disposable signature successfully.

Result: PASS for raw public-key export and import behavior.

## Malformed public key behavior

Malformed public-key import behavior:

- empty public key: rejected with `ValueError`
- short public key: rejected with `ValueError`
- long public key: rejected with `ValueError`
- mutated same-length public key: imported, but verification failed with
  `InvalidSignature`

Result: PASS for malformed-length public-key rejection and same-length mutated
key verification failure.

## Malformed signature behavior

Malformed signature verification behavior:

- empty signature: `InvalidSignature`
- short signature: `InvalidSignature`
- long signature: `InvalidSignature`

Result: PASS for malformed signature rejection.

## Evaluation classification

| Evaluation area | Result | Finding / boundary observation |
| --- | --- | --- |
| Isolated install outside repository | PASS | Installed only in `$AAID_SIGNATURE_SANDBOX`. |
| ML-DSA module availability | PASS | Runtime exposed ML-DSA classes. |
| ML-DSA-65 API availability | PASS | `MLDSA65PrivateKey` and `MLDSA65PublicKey` were available. |
| Disposable key generation | PASS | Disposable ML-DSA-65 key pair generated in isolation. |
| Disposable signing | PASS | Disposable message and context were signed in isolation. |
| Disposable verification | PASS | Valid disposable signature verified successfully. |
| Raw public-key export/import | PASS | Exported public key bytes imported and verified successfully. |
| Modified message failure | PASS | Modified message raised `InvalidSignature`. |
| Modified signature failure | PASS | Modified signature raised `InvalidSignature`. |
| Wrong context failure | PASS | Wrong context raised `InvalidSignature`. |
| Malformed public-key behavior | PASS | Malformed lengths raised `ValueError`; same-length mutation failed verification. |
| Malformed signature behavior | PASS | Malformed signatures raised `InvalidSignature`. |
| Official test-vector compatibility | NOT TESTED | Deferred to official vector compatibility work. |
| Artifact provenance or hash verification | NOT TESTED | Deferred to package artifact/provenance review. |
| Repository dependency adoption | NOT APPROVED | Repository environment remained unchanged. |
| Verifier integration readiness | PARTIAL | Runtime behavior is useful, but adapter design and official vectors remain open. |

Overall result: PARTIAL.

The candidate showed strong isolated ML-DSA-65 runtime behavior, but adoption
readiness remains partial until official test-vector compatibility, artifact
provenance, dependency-risk review, encoding decision, and verifier integration
planning are completed.

## Security notes

No runtime behavior in this isolated run changed the repository safety boundary.

The observed failure behavior is useful for future fail-closed mapping because
invalid signatures and malformed signatures produced verification failures
rather than successful verification.

This result is not a security audit of `cryptography`.

## Not implemented

This evaluation did not implement:

- repository dependency adoption;
- package installation in the repository environment;
- requirements or lockfile changes;
- verifier source changes;
- schema changes;
- example passport updates;
- official test-vector execution;
- artifact provenance verification;
- real passport signature verification;
- signing-key generation in the repository;
- permanent runtime integration;
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

Review official ML-DSA test-vector compatibility and package artifact evidence
before any repository dependency adoption or verifier integration proposal.
