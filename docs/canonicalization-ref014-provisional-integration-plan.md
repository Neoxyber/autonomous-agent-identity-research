# REF-014 Provisional Integration Research Plan

## Purpose

This document records the research evidence and remaining decisions for REF-014
`rfc8785==0.1.4` as a candidate canonicalization implementation.

It is a research checkpoint, not an adoption decision. REF-014 is not installed
in the repository, not selected as the canonicalizer, and not used by the
verifier.

## Repository boundary

The repository currently uses a local research canonicalization helper in
`src/aaid/canonicalization.py`. Raw JSON input can enter through
`verify_passport_json()`, which rejects duplicate object member names before
schema validation. `verify_passport_envelope()` accepts already parsed,
duplicate-key-safe mappings.

Schema validation runs before canonicalization-dependent checks. Real signature
verification remains blocked and fail-closed.

No REF-014 runtime dependency, package adoption, requirements change, lockfile
change, canonicalizer replacement, golden-vector migration, or signature
verification change has been made.

## Research position

REF-014 is the leading candidate for provisional integration planning based on
isolated evaluation, reference-vector comparison, bounded number-serialization
checks, parse-layer review, artifact provenance evidence, and verifier failure
semantics.

This position does not claim full RFC 8785/JCS conformance, production
readiness, legal compatibility, or adoption readiness.

## Evidence collected

### Artifact provenance

The pinned wheel and source distribution were reviewed in isolated `/tmp`
environments.

Pinned artifacts:

- wheel: `rfc8785-0.1.4-py3-none-any.whl`
- wheel SHA-256:
  `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`
- source distribution: `rfc8785-0.1.4.tar.gz`
- source distribution SHA-256:
  `e545841329fe0eee4f6a3b44e7034343100c12b4ec566dc06ca9735681deb4da`

PyPI and GitHub release artifacts matched byte-for-byte for the evaluated wheel
and source distribution. The wheel was `py3-none-any`, pure Python, with no
native extensions observed. Normal runtime dependency surface was empty.

Sigstore 4.3.0 verified both pinned artifacts offline against their release
bundles using the fixed OIDC issuer
`https://token.actions.githubusercontent.com` and the fixed workflow identity
`https://github.com/trailofbits/rfc8785.py/.github/workflows/release.yml@refs/tags/v0.1.4`.

### Build provenance

Artifact provenance is evidenced, but source-to-artifact build provenance is not
established. The project has not re-derived the wheel from the source tag,
verified reproducible source-to-artifact correspondence, or recorded an
equivalent build-reproducibility result.

Build provenance remains an adoption blocker unless verified or explicitly
deferred with rationale in a separate adoption decision.

### License and attribution evidence

The wheel includes `rfc8785-0.1.4.dist-info/LICENSE`. The source distribution
includes `LICENSE`, `PKG-INFO`, `README.md`, and `pyproject.toml`.

The wheel and source distribution license files were identical, with SHA-256
digest:

`0d542e0c8804e39aa7f37eb00da5a762149dc682d7829451287e11b938e94594`

Package metadata includes the Apache Software License classifier.
`pyproject.toml` declares `license = { file = "LICENSE" }`. Author metadata
identifies Trail of Bits. README/PKG-INFO attribution records that parts are
adapted from Andrew Rundgren's reference implementation, also described as
Apache License, Version 2.0.

No `NOTICE` file was found in the inspected wheel, source distribution, or exact
GitHub `v0.1.4` tag metadata.

This is license and attribution evidence only. It is not legal advice or a legal
opinion. Any future adoption or redistribution should preserve the Apache-2.0
license text and recorded attribution evidence.

### Dependency and maintenance risk

REF-014 `rfc8785==0.1.4` declares `Requires-Python >=3.8`, has no normal runtime
dependencies, and is marked `Development Status :: 4 - Beta`. Observed
`Requires-Dist` entries were optional extras for development, documentation,
lint, and tests.

Repository metadata showed that `trailofbits/rfc8785.py` was not archived, not a
fork, not a mirror, not private, and not empty. The default branch was `main`,
primary language was Python, issues were enabled, and metadata showed activity
in May 2026. The evaluated release `v0.1.4` was created and published on
2024-09-27. One open pull request related to mypy settings was observed. The
GitHub security-advisory query returned no entries.

Status: PARTIAL. The runtime dependency surface is low and no immediate blocking
repository signal was observed, but long-term maintenance suitability,
vulnerability posture, and adoption readiness remain unproven.

### Verifier entry-point boundary

`verify_passport_json()` is the raw JSON entry point and parses input with
duplicate-key rejection before schema validation. `verify_passport_envelope()` is
the parsed-envelope entry point and assumes callers provide already parsed,
duplicate-key-safe mappings.

Payload-hash verification and future signature-input preparation use the shared
canonicalization helper over the `passport` object only, excluding the envelope
wrapper and `proofs`.

### Numeric-domain policy

The current passport payload profile is numeric-field-free. Schema inspection
found no `number` or `integer` typed fields in the current passport profile.
Repository evidence records fail-closed handling for non-finite values.

REF-014's unsafe-integer blocking behavior is treated as input-domain
enforcement, not as an ordinary canonical byte mismatch. Future numeric payload
fields remain blocked until explicit schema bounds, accepted numeric domains,
and failure semantics are recorded.

### Integration-test planning

REF-014-based tests have not been executed against the repository verifier.
Executing them requires a separate explicit approval.

Planned categories before runtime integration:

1. REF-014 produces expected canonical bytes for the minimal passport.
2. The minimal passport payload hash is preserved or intentionally migrated.
3. Object order remains irrelevant.
4. Array order remains significant.
5. Proof material remains excluded from the signed payload.
6. Payload-hash input and signature-input preparation use the same canonical
   bytes, including the existing `canonical_payload_prepared` boundary.
7. Non-finite values fail closed.
8. Current-profile unsafe-integer behavior remains outside the passport payload
   domain because the current profile is numeric-field-free.
9. Future numeric payload fields remain blocked until explicit schema bounds,
   accepted numeric domains, and failure semantics are recorded.
10. Duplicate-key raw JSON behavior remains enforced at the parse boundary.
11. Schema validation still runs before canonicalization-dependent verification.
12. Unsupported canonicalization fails closed.
13. Canonicalization and candidate-canonicalizer errors become failed verifier
    checks and `DENY` results, not unhandled exceptions.
14. Signature verification remains blocked until a later phase.

### Golden-vector migration planning

The current helper canonicalizes the minimal passport to 1628 bytes. The current
SHA-256 payload hash is:

`b85a7ddfefccb9582bf6ab23dac42a968cc0b6aabfc1d29d416ea25e27bfb6bc`

This hash matches the minimal example proof `payload_hash`.

Any future canonicalizer replacement must treat changes to the minimal passport
canonical bytes or payload hash as intentional migration, not incidental drift.
Before adoption, the project must record:

- current helper canonical bytes or hash;
- REF-014 canonical bytes or hash;
- whether the minimal example changes;
- whether the existing payload hash is preserved or intentionally migrated;
- why any migration is acceptable;
- which tests pin the expected value.

### Verification-result failure semantics

A future REF-014 integration must preserve the current verifier failure
semantics:

- canonical payload preparation failures are represented by a failed
  `canonical_payload_prepared` verifier check;
- verifier paths return `VerificationResult.failed(...)` with `DENY` rather than
  allowing canonicalization or candidate-canonicalizer exceptions to escape;
- later payload-hash, key-selection, signature-input, algorithm, and signature
  checks do not run after canonical payload preparation fails;
- unsupported declared canonicalization remains a separate
  `signature_canonicalization_supported` failure;
- payload-hash mismatch remains a separate `payload_hash_valid` failure;
- real signature verification remains blocked until a later phase.

## Adoption-readiness checkpoint

Current readiness: PARTIAL.

REF-014 is better understood, but it is not ready for adoption. Remaining
blockers are intentionally narrow and must be resolved or explicitly deferred
with rationale before any adoption decision.

Remaining blockers:

- build provenance, unless source-to-artifact reproducibility is verified or
  explicitly deferred;
- attribution-handling decision for any future adoption or redistribution;
- integration-test execution;
- golden-vector migration review.

Research-paper note: this checkpoint records the decision method, not an
adoption result. Future research evidence should distinguish artifact evidence,
license and attribution evidence, maintenance-risk evidence, behavioral
verification, and adoption readiness.

## Non-goals

This plan does not cover dependency adoption, package installation,
requirements changes, lockfile changes, canonicalizer replacement, real
signature verification, post-quantum signing, issuer trust, revocation, policy,
audit, gateway, cloud, or external integrations.

## Next step

Pause before any REF-014 execution. The next step should be an explicit decision
on whether to run REF-014 integration-test execution in isolation, continue
golden-vector migration review, or defer REF-014 adoption.
