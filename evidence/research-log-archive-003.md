# Research Log

## Purpose

This file records the chronological progress of the autonomous agent identity research project.

The research log is used to track meaningful project steps, not every small edit. It records what changed, why it changed, which files were affected, and what the next step is.

Detailed design decisions will be recorded separately in Research Decision Records when the project reaches that stage. Empirical tests and benchmark results will be recorded separately in Empirical Testing Logs when implementation and testing begin.

## Archive note

Entries 001 to 021 are preserved unchanged in `evidence/research-log-archive-001.md`.

Entries 022 to 083 are preserved unchanged in `evidence/research-log-archive-002.md`.

This active log continues the same entry numbering and format from Entry 084 onward.

## Entry 084

Date: 2026-06-05

Type: Canonicalization candidate provenance verification

Summary: Recorded REF-014 artifact provenance verification.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
REF-014 `rfc8785==0.1.4` artifact provenance verification passed for the pinned wheel and source distribution in an isolated `/tmp` environment.

The isolated verifier environment was created outside the repository at `/tmp/aaid-ref014-tools/.venv`. The run used Python 3.12.3, pip 26.1.2, and Sigstore 4.3.0. Relevant verifier packages included `sigstore==4.3.0`, `sigstore-models==0.0.6`, `sigstore-rekor-types==0.0.18`, `tuf==7.0.0`, `securesystemslib==1.4.0`, `cryptography==48.0.0`, and `rfc8785==0.1.4` inside the isolated verifier environment only.

The pinned release artifacts were downloaded to `/tmp/aaid-ref014-provenance-verify`. The wheel SHA-256 digest matched `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`. The source distribution SHA-256 digest matched `e545841329fe0eee4f6a3b44e7034343100c12b4ec566dc06ca9735681deb4da`.

Sigstore offline verification returned `OK` for both artifacts using their release bundles, the fixed OIDC issuer `https://token.actions.githubusercontent.com`, and the fixed workflow identity `https://github.com/trailofbits/rfc8785.py/.github/workflows/release.yml@refs/tags/v0.1.4`.

The result was recorded in `docs/canonicalization-ref014-provisional-integration-plan.md` as a P1 cryptographic provenance verification result.

This is artifact provenance evidence only. It does not adopt REF-014, does not promote REF-014 to Verified in `docs/references.md`, does not install REF-014 into the repository, does not change requirements or lockfiles, does not replace the current canonicalization helper, does not migrate golden vectors, and does not unblock real signature verification by itself.

Tests:
Not run for this evidence-only entry. No source, test, requirement, or lockfile files were changed.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, golden-vector migration, numeric-domain policy changes, integration-test migration, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Review REF-014 license and attribution, dependency and maintenance risk, verifier entry-point decisions, numeric-domain policy, integration tests, golden-vector migration review, and verification-result failure semantics before any adoption decision.

## Entry 085

Date: 2026-06-05

Type: Canonicalization candidate license evidence

Summary: Recorded REF-014 license and attribution evidence.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
REF-014 `rfc8785==0.1.4` license and attribution evidence was refined using the pinned wheel, pinned source distribution, and exact GitHub `v0.1.4` tag metadata.

The wheel included `rfc8785-0.1.4.dist-info/LICENSE`; the source distribution included `LICENSE`, `PKG-INFO`, `README.md`, and `pyproject.toml`. The wheel and source distribution license files were identical, with SHA-256 digest `0d542e0c8804e39aa7f37eb00da5a762149dc682d7829451287e11b938e94594`.

The inspected artifact metadata identified Apache License, Version 2.0 evidence through the Apache Software License classifier and `pyproject.toml` license-file declaration. Metadata identified Trail of Bits as the author contact and stated that parts of the implementation are adapted from Andrew Rundgren's Apache License 2.0 reference implementation. No `NOTICE` file was found in the inspected wheel, source distribution, or exact GitHub `v0.1.4` tag metadata.

This is license and attribution evidence only. It is not a legal opinion, does not complete legal review, does not adopt REF-014, does not promote REF-014 to Verified in `docs/references.md`, and does not approve dependency integration.

Tests:
Not run for this evidence-only entry yet. No source, test, requirement, or lockfile files were changed.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, golden-vector migration, numeric-domain policy changes, integration-test migration, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Review REF-014 dependency and maintenance risk, verifier entry-point decisions, numeric-domain policy, integration tests, golden-vector migration review, and verification-result failure semantics before any adoption decision.

## Entry 086

Date: 2026-06-05

Type: Canonicalization candidate maintenance-risk evidence

Summary: Recorded REF-014 dependency and maintenance-risk evidence.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
REF-014 `rfc8785==0.1.4` dependency and maintenance-risk evidence was reviewed and recorded as PARTIAL.

The pinned package metadata declared `Requires-Python >=3.8`, `Development Status :: 4 - Beta`, and no normal runtime dependencies. Observed `Requires-Dist` entries were optional extras for development, documentation, lint, and tests.

GitHub repository metadata for `trailofbits/rfc8785.py` showed that the repository was not archived, not a fork, not a mirror, not private, not empty, and had GitHub security policy support enabled. The default branch was `main`, the primary language was Python, issues were enabled, and metadata showed activity in May 2026.

Tags and releases were observed from `v0.0.1` through `v0.1.4`. The evaluated release `v0.1.4` was created and published on 2024-09-27, was not a draft, and was not a prerelease. The release assets included the pinned wheel, source distribution, and corresponding Sigstore bundles. The open issue query found no open issues excluding pull requests. One open pull request related to mypy settings was observed. The GitHub security-advisory query returned no entries.

This is dependency and maintenance-risk evidence only. The normal runtime dependency surface is low and no obvious repository blocking signal was observed, but the package is marked beta, the latest release is from 2024, GitHub repository license metadata is null, and long-term maintenance suitability, vulnerability posture, adoption readiness, and operational readiness remain unproven.

Tests:
Not run for this evidence-only entry yet. No source, test, requirement, or lockfile files were changed.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, golden-vector migration, numeric-domain policy changes, integration-test migration, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Review verifier entry-point decisions, numeric-domain policy, integration tests, golden-vector migration review, and verification-result failure semantics before any REF-014 adoption decision.

## Entry 087

Date: 2026-06-05

Type: Verifier boundary documentation

Summary: Recorded verifier entry-point boundary for canonicalization planning.

Files:
Updated `docs/canonicalization-parse-and-payload-domain-gate.md`, updated `docs/canonicalization-ref014-provisional-integration-plan.md`, and this evidence log.

Result:
The canonicalization planning documents now record the verifier entry-point boundary for REF-014 adoption planning.

`verify_passport_json()` is the raw JSON entry point. It parses input with `parse_json_no_duplicate_keys()` before schema validation, so duplicate-key rejection runs before canonicalization-dependent checks.

`verify_passport_envelope()` is the parsed-envelope entry point. It assumes callers provide already parsed, duplicate-key-safe mappings.

The REF-014 provisional integration plan no longer treats the verifier raw-JSON boundary as a remaining adoption blocker. Remaining REF-014 adoption blockers are build provenance, legal compatibility and attribution completeness, numeric payload-domain policy, integration tests, golden-vector migration review, and verification-result failure semantics.

This is documentation alignment only. It does not change verifier behavior, adopt REF-014, install packages, change requirements or lockfiles, replace the canonicalizer, migrate golden vectors, implement numeric-domain policy, or unblock real signature verification.

Tests:
Not run for this evidence-only entry yet. No source, test, requirement, or lockfile files were changed.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, golden-vector migration, numeric-domain policy changes, integration-test migration, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Review numeric payload-domain policy before any REF-014 adoption decision, integration-test planning, golden-vector migration review, or real signature-verification planning.

## Entry 088

Date: 2026-06-05

Type: Canonicalization candidate numeric-domain evidence

Summary: Recorded REF-014 numeric-domain evidence for the current passport profile.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
REF-014 numeric-domain evidence was recorded as PASS for the current numeric-field-free passport profile.

The current passport schema inspection found no `number` or `integer` typed fields in the current passport profile. Existing canonicalization and threat-model documents already record that future numeric payload fields require a separate schema and canonicalization decision before canonicalizer adoption, golden-vector migration, or signature-verification planning.

Repository current-profile evidence records fail-closed handling for non-finite values. REF-014's unsafe-integer blocking behavior is treated as input-domain enforcement, not as an ordinary canonical byte mismatch.

The REF-014 provisional integration plan no longer treats numeric payload-domain policy as a remaining adoption blocker for the current numeric-field-free profile. Future numeric payload fields remain blocked until explicit schema bounds, accepted numeric domains, and failure semantics are recorded.

This is current-profile numeric-domain evidence only. It does not approve future numeric payload fields, implement numeric-domain enforcement, adopt REF-014, replace the canonicalizer, migrate golden vectors, or unblock real signature verification.

Tests:
Not run for this evidence-only entry yet. No source, test, requirement, or lockfile files were changed.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, golden-vector migration, future numeric payload-field support, numeric-domain enforcement, integration-test migration, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Review integration-test planning, golden-vector migration review, and verification-result failure semantics before any REF-014 adoption decision.

## Entry 089

Date: 2026-06-05

Type: Canonicalization candidate integration-test planning

Summary: Refined REF-014 integration-test planning.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
The REF-014 provisional integration plan now refines integration-test planning without executing REF-014-based tests or authorizing runtime integration.

The planned categories now explicitly include the existing `canonical_payload_prepared` boundary, require payload-hash input and signature-input preparation to use the same canonical bytes, preserve proof exclusion from the signed payload, keep duplicate-key raw JSON behavior at the parse boundary, keep schema validation before canonicalization-dependent verification, require unsupported canonicalization and canonicalizer errors to fail closed, and keep signature verification blocked until a later phase.

The plan now aligns with the current numeric-domain milestone. Non-finite values must fail closed. Current-profile unsafe-integer behavior remains outside the passport payload domain because the current profile is numeric-field-free. Future numeric payload fields remain blocked until explicit schema bounds, accepted numeric domains, and failure semantics are recorded.

The REF-014 provisional integration plan now names the remaining adoption blocker as integration-test execution rather than generic integration tests. Executing REF-014-based tests still requires separate adoption approval and is not authorized by the plan.

This is integration-test planning only. It does not execute REF-014 tests, adopt REF-014, install packages, change requirements or lockfiles, replace the canonicalizer, migrate golden vectors, implement numeric-domain enforcement, or unblock real signature verification.

Tests:
Not run for this evidence-only entry yet. No source, test, requirement, or lockfile files were changed.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, golden-vector migration, future numeric payload-field support, numeric-domain enforcement, integration-test execution, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Review golden-vector migration and verification-result failure semantics before any REF-014 adoption decision or REF-014-based test execution.

## Entry 090

Date: 2026-06-05

Type: Canonicalization candidate golden-vector planning

Summary: Recorded REF-014 golden-vector migration planning.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
The REF-014 provisional integration plan now records golden-vector migration planning for the minimal passport example.

The current helper canonicalizes the minimal passport to 1628 bytes. The current SHA-256 payload hash is `b85a7ddfefccb9582bf6ab23dac42a968cc0b6aabfc1d29d416ea25e27bfb6bc`, which matches the minimal example proof `payload_hash`.

The plan now states that any canonicalizer replacement must treat changes to the minimal passport canonical bytes or payload hash as intentional migration, not incidental drift. Before adoption, the project must record the current helper canonical bytes or hash, the REF-014 canonical bytes or hash, whether the minimal example changes, whether the existing payload hash is preserved or intentionally migrated, why any migration is acceptable, and which tests pin the expected value.

This is golden-vector migration planning only. It does not execute REF-014, adopt REF-014, replace the canonicalizer, update the minimal example, change the payload hash, migrate golden vectors, or unblock real signature verification.

Tests:
Not run for this evidence-only entry yet. No source, test, requirement, or lockfile files were changed.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, minimal example update, payload-hash update, golden-vector migration, future numeric payload-field support, numeric-domain enforcement, integration-test execution, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Review verification-result failure semantics before any REF-014 adoption decision, REF-014-based test execution, canonicalizer replacement, golden-vector migration, or real signature-verification planning.

## Entry 091

Date: 2026-06-05

Type: Canonicalization candidate failure-semantics planning

Summary: Recorded REF-014 verification-result failure semantics.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
The REF-014 provisional integration plan now records verification-result failure semantics that any future REF-014 integration must preserve.

The plan records that canonical payload preparation failures must be represented by a failed `canonical_payload_prepared` verifier check, and verifier paths must return `VerificationResult.failed(...)` with `DENY` rather than allowing canonicalization or candidate-canonicalizer exceptions to escape.

The plan also records that later payload-hash, key-selection, signature-input, algorithm, and signature checks must not run after canonical payload preparation fails. Unsupported declared canonicalization remains a separate `signature_canonicalization_supported` failure. Payload-hash mismatch remains a separate `payload_hash_valid` failure. Real signature verification remains blocked until a later phase.

This is failure-semantics planning only. It does not execute REF-014 tests, adopt REF-014, replace the canonicalizer, change verifier source, change requirements or lockfiles, migrate golden vectors, or unblock real signature verification.

Tests:
Not run for this evidence-only entry yet. No source, test, requirement, or lockfile files were changed.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, verifier source changes, minimal example update, payload-hash update, golden-vector migration, future numeric payload-field support, numeric-domain enforcement, integration-test execution, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Review remaining REF-014 adoption blockers: build provenance, legal compatibility and attribution completeness, integration-test execution, and golden-vector migration review before any adoption decision.

## Entry 092

Date: 2026-06-05

Type: Canonicalization candidate adoption-readiness checkpoint

Summary: Recorded REF-014 adoption-readiness checkpoint.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
The REF-014 provisional integration plan now records an adoption-readiness checkpoint.

The checkpoint records that REF-014 evidence has been collected for artifact provenance, license and attribution signals, dependency and maintenance risk, verifier entry-point boundaries, current-profile numeric-domain policy, integration-test planning, golden-vector migration planning, and verification-result failure semantics.

Current readiness is recorded as PARTIAL. REF-014 is better understood, but it is not ready for adoption. Remaining blockers are intentionally narrow and must be resolved or explicitly deferred with rationale before any adoption decision.

Remaining blockers are build provenance, legal compatibility and attribution completeness, integration-test execution, and golden-vector migration review. The checkpoint also records that future research-paper evidence should distinguish artifact evidence, legal evidence, maintenance-risk evidence, behavioral verification, and adoption readiness.

This is an adoption-readiness checkpoint only. It does not adopt REF-014, execute REF-014 tests, replace the canonicalizer, change verifier source, change requirements or lockfiles, migrate golden vectors, or unblock real signature verification.

Tests:
Not run for this evidence-only entry yet. No source, test, requirement, or lockfile files were changed.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, verifier source changes, minimal example update, payload-hash update, golden-vector migration, future numeric payload-field support, numeric-domain enforcement, integration-test execution, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Review remaining REF-014 blockers carefully before any adoption decision. Do not execute REF-014-based tests or replace the canonicalizer without explicit approval.

## Entry 093

Date: 2026-06-05

Type: Canonicalization candidate build-provenance status

Summary: Recorded REF-014 build-provenance status.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
The REF-014 provisional integration plan now separates artifact provenance evidence from build provenance.

Artifact provenance evidence has been collected for the pinned wheel and source distribution, including pinned SHA-256 digests and Sigstore verification against the fixed GitHub Actions OIDC issuer and release workflow identity.

Build provenance remains unresolved. The project has not re-derived the wheel from the source tag, has not verified reproducible source-to-artifact correspondence, and has not recorded an equivalent build-reproducibility result.

Current status is PARTIAL. Artifact provenance is evidenced, but source-to-artifact build provenance is not established. Build provenance remains an adoption blocker unless it is verified or explicitly deferred with rationale in a separate adoption decision.

This is build-provenance status recording only. It does not adopt REF-014, execute REF-014 tests, rebuild artifacts, replace the canonicalizer, change verifier source, change requirements or lockfiles, migrate golden vectors, or unblock real signature verification.

Tests:
Not run for this evidence-only entry yet. No source, test, requirement, or lockfile files were changed.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, verifier source changes, artifact rebuild, reproducible-build verification, minimal example update, payload-hash update, golden-vector migration, future numeric payload-field support, numeric-domain enforcement, integration-test execution, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Review legal compatibility and attribution completeness before any REF-014 adoption decision, REF-014-based test execution, canonicalizer replacement, or golden-vector migration.

## Entry 094

Date: 2026-06-05

Type: Canonicalization candidate golden-vector comparison

Summary: Recorded REF-014 minimal passport golden-vector comparison.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
An isolated REF-014 golden-vector comparison was run for the minimal passport example.

The first attempt used the isolated REF-014 verifier environment directly and failed because that environment did not include the repository dependency `jsonschema`. This was an environment issue, not a canonicalization mismatch.

The corrected attempt used the repository virtual environment and added only the isolated REF-014 site-packages path for importing `rfc8785`.

REF-014 produced 1628 canonical bytes for the minimal passport, matching the current helper byte-for-byte. The REF-014 SHA-256 payload hash was `b85a7ddfefccb9582bf6ab23dac42a968cc0b6aabfc1d29d416ea25e27bfb6bc`, matching the current helper hash and the minimal example proof `payload_hash`.

No golden-vector migration is required for the current minimal passport example. Any future canonicalizer replacement must still pin this expected value in tests before adoption.

Earlier REF-014 entries already recorded artifact provenance, Apache-2.0 license and attribution evidence, dependency and maintenance-risk evidence, build-provenance status, verifier-boundary evidence, numeric-domain evidence, and verification-result failure semantics.

This is isolated comparison evidence only. It does not adopt REF-014, install REF-014 into the repository, change requirements or lockfiles, replace the canonicalizer, change verifier source, execute REF-014 verifier integration tests, migrate golden vectors, or unblock real signature verification.

Tests:
Repository baseline before the comparison passed with 594 tests. Full tests should be run again before push.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, verifier source changes, artifact rebuild, reproducible-build verification, minimal example update, payload-hash update, golden-vector migration, future numeric payload-field support, numeric-domain enforcement, REF-014 verifier integration-test execution, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Review whether to run REF-014 verifier integration-test execution in isolation or defer REF-014 adoption before moving to real signature-verification planning.

## Entry 095

Date: 2026-06-05

Type: Canonicalization candidate verifier integration execution

Summary: Recorded isolated REF-014 verifier integration execution.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
An isolated REF-014 verifier integration execution was run without editing repository source, tests, requirements, or lockfiles. The script monkeypatched the verifier canonicalization boundary in memory so REF-014 supplied canonical bytes and payload hashes during the run.

The first attempt failed because the test script expected unsupported proof canonicalization to reach `signature_canonicalization_supported`; the mutated value was instead rejected earlier at schema validation. The corrected execution treated this as schema-gated fail-closed behavior.

The corrected execution passed. It verified REF-014 byte/hash parity, the verifier DENY invariant, raw JSON duplicate-key parse boundary, schema-before-canonicalization behavior, payload-hash behavior, proof exclusion, signature-input reuse, and candidate-canonicalizer error failure semantics. Unsupported canonicalization mutation was handled at `schema_valid`.

Earlier REF-014 entries already recorded artifact provenance, Apache-2.0 license and attribution evidence, dependency and maintenance-risk evidence, build-provenance status, verifier-boundary evidence, numeric-domain evidence, golden-vector comparison, and verification-result failure semantics.

This is isolated verifier integration execution evidence only. It does not adopt REF-014, install REF-014 into the repository, change requirements or lockfiles, replace the canonicalizer, change verifier source, migrate golden vectors, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
Repository baseline before the isolated execution passed with 594 tests. Full tests should be run again before push.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, verifier source changes, artifact rebuild, reproducible-build verification, minimal example update, payload-hash update, golden-vector migration, future numeric payload-field support, numeric-domain enforcement, permanent REF-014 verifier integration tests, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Decide whether to defer REF-014 adoption and move to real signature-verification planning, or first record an explicit REF-014 adoption/defer decision.

## Entry 096

Date: 2026-06-05

Type: Canonicalization candidate adoption decision

Summary: Deferred REF-014 adoption after isolated evidence collection.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md` and this evidence log.

Result:
REF-014 adoption remains deferred. The collected evidence is sufficient to inform future canonicalizer adoption, but the repository will not replace the current helper, add REF-014 as a dependency, update requirements or lockfiles, or promote REF-014 to Verified without a separate adoption decision.

Real signature-verification planning may proceed while runtime canonicalizer adoption remains separate.

This decision follows earlier REF-014 evidence covering artifact provenance, Apache-2.0 license and attribution evidence, dependency and maintenance-risk evidence, build-provenance status, verifier-boundary evidence, numeric-domain evidence, golden-vector comparison, and isolated verifier integration execution.

This is an adoption-deferral decision only. It does not adopt REF-014, install REF-014 into the repository, change requirements or lockfiles, replace the canonicalizer, change verifier source, migrate golden vectors, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
Not run for this evidence-only entry yet. No source, test, requirement, or lockfile files were changed.

Not implemented:
dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, verifier source changes, artifact rebuild, reproducible-build verification, minimal example update, payload-hash update, golden-vector migration, future numeric payload-field support, numeric-domain enforcement, permanent REF-014 verifier integration tests, real signature verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Begin real signature-verification planning while keeping canonicalizer adoption separate.

## Entry 097

Date: 2026-06-06

Type: Signature verification planning boundary

Summary: Recorded real signature-verification planning boundary.

Files:
Updated `docs/agent-passport-threat-model-and-trust-boundaries.md` and this evidence log.

Result:
The threat model now records that real signature-verification planning may proceed after the REF-014 adoption deferral decision while runtime canonicalizer adoption remains separate.

The first signature-verification design is constrained to the already prepared canonical passport payload bytes, proof exclusion from the signed input, selected public key after key selection and key validity checks, exact `proof.verification_method` to key `kid` binding, explicit algorithm allowlisting, and fail-closed handling for unsupported algorithms, malformed keys, malformed signatures, unsupported encodings, and verifier-library errors.

ML-DSA-65 remains the current research target for the first passport signature path. A future implementation should not write custom cryptography and should use a reviewed library only after dependency, runtime-support, encoding, test-vector, and rollback decisions are recorded.

This is planning-boundary evidence only. It does not implement signature verification, add dependencies, change requirements or lockfiles, change verifier source, adopt REF-014, replace the canonicalizer, or create a passport-verifier `ALLOW` path.

Tests:
Not run for this evidence-only entry yet. No source, test, requirement, or lockfile files were changed.

Not implemented:
signature verification, dependency adoption, package installation into the repository, requirements changes, lockfile changes, canonicalizer replacement, verifier source changes, ML-DSA runtime integration, test-vector execution, key encoding decisions, rollback handling, real cryptographic verification, reference promotion to Verified, passport-verifier `ALLOW` path, Civo, Supabase, MCP, gateway, storage, cloud deployment, or production use.

Next step:
Inspect ML-DSA runtime support, key encoding, and test-vector options before any signature-verification implementation.

## Entry 098

Date: 2026-06-06

Type: Signature verification planning

Summary: Added focused signature-verification planning document.

Files:
Added `docs/signature-verification-planning.md` and updated this evidence log.

Result:
A focused signature-verification planning document now records the first planning boundary for real passport signature verification.

The document separates signature-verification planning from canonicalization planning, post-quantum readiness, issuer trust, revocation, authorization, approval, audit, and enforcement.

It records the current repository boundary: the verifier prepares canonical passport payload bytes, excludes the envelope wrapper and detached proof material from the signed input, records `signature_verification_not_implemented`, returns `DENY`, and cannot return `ALLOW`.

The document also records the implemented gates that must run before any future signature step, the current ML-DSA-65 research direction, SLH-DSA backup direction, runtime-support boundary, unresolved key and signature encoding questions, initial raw-byte base64url encoding position, test-vector requirements, failure semantics, adapter boundary, and adoption blockers.

This is planning evidence only. It does not implement real signature verification, adopt a cryptographic dependency, install packages, change requirements or lockfiles, change verifier source, change schema, update example passport values, add signing key generation, add test-vector execution, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the planning commit.

Not implemented:
real signature verification, dependency adoption, package installation, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, ML-DSA runtime integration, signing key generation, real ML-DSA public-key or signature material, test-vector execution, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, reference promotion to Verified, or passport-verifier `ALLOW` path.

Next step:
Review candidate ML-DSA runtime support, key encoding, signature encoding, and test-vector sources before any implementation proposal.

## Entry 099

Date: 2026-06-06

Type: Signature runtime research planning

Summary: Added signature runtime research plan.

Files:
Added `docs/signature-verification-runtime-research.md` and updated this evidence log.

Result:
A focused signature runtime research plan now defines how the project will evaluate runtime support for real passport signature verification before any implementation proposal.

The plan records ML-DSA-65 as the first passport signature research target, keeps SLH-DSA as a backup signature-family direction, and keeps ML-KEM outside passport signature scope as future secure key-establishment work.

The plan defines candidate runtime paths for later review, including Python `cryptography` ML-DSA support, Open Quantum Safe `liboqs` and appropriate language bindings, and other maintained ML-DSA-capable libraries only after source, license, maintenance, dependency, and security review.

It records runtime-support questions, encoding questions, test-vector questions, an evidence matrix, isolated evaluation rules, a security and responsible-disclosure boundary, and findings that would be useful to industry.

The plan preserves the current boundary: candidate evaluation does not mean adoption, candidate experiments must run outside the repository environment unless separately approved, and the repository must not accidentally adopt a candidate through requirements, lockfiles, imports, copied source, generated artifacts, or example data.

This is runtime research planning only. It does not adopt a dependency, install packages, change requirements or lockfiles, change verifier source, change schema, add real signature material, run test vectors, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the runtime research plan commit.

Not implemented:
real signature verification, dependency adoption, package installation, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, ML-DSA runtime integration, signing key generation, real ML-DSA public-key or signature material, test-vector execution, permanent runtime integration, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, reference promotion to Verified, or passport-verifier `ALLOW` path.

Next step:
Review candidate sources and exact reference entries before running any isolated runtime experiment.

## Entry 100

Date: 2026-06-06

Type: Signature runtime reference candidates

Summary: Added signature runtime and test-vector reference candidates.

Files:
Updated `docs/references.md` and this evidence log.

Result:
The reference register now includes pending-review reference candidates for signature runtime and test-vector research.

New entries cover NIST ACVP ML-DSA validation-style material, NIST CAVP / ACVP final JSON vector location, Python `cryptography` ML-DSA documentation, pyca/cryptography backend-support boundary, Open Quantum Safe `liboqs`, Open Quantum Safe ML-DSA documentation, RFC 9881 ML-DSA X.509 algorithm identifiers, and RFC 9882 ML-DSA in CMS.

All new references remain marked `Pending review` with `Accessed` set to `Not recorded`. No reference was promoted to `Verified`.

This is reference-candidate documentation only. It does not complete source verification, approve dependency adoption, run isolated runtime experiments, install packages, change requirements or lockfiles, change verifier source, change schema, implement signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the reference-candidate commit.

Not implemented:
source verification completion, reference promotion to Verified, dependency adoption, package installation, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, ML-DSA runtime integration, signing key generation, real ML-DSA public-key or signature material, test-vector execution, permanent runtime integration, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, or passport-verifier `ALLOW` path.

Next step:
Review the exact source identity, publisher identity, access date, and relevance of the new signature runtime references before any isolated runtime experiment.

## Entry 101

Date: 2026-06-06

Type: Signature runtime source review

Summary: Recorded source review details for signature runtime references.

Files:
Updated `docs/references.md` and this evidence log.

Result:
The reference register now records access date and source-review notes for REF-020 through REF-027.

REF-020 through REF-027 cover ML-DSA validation-style JSON test planning, NIST final-vector source location, Python `cryptography` ML-DSA runtime API review, pyca/cryptography backend-support boundary review, Open Quantum Safe `liboqs`, Open Quantum Safe ML-DSA documentation, RFC 9881 ML-DSA X.509 encoding research, and RFC 9882 ML-DSA CMS encoding research.

All updated references remain marked `Pending review`. No reference was promoted to `Verified`.

This is source-review documentation only. It records source identity, publisher identity, access date, and relevance notes for later review. It does not complete source verification, approve dependency adoption, run isolated runtime experiments, install packages, change requirements or lockfiles, change verifier source, change schema, implement signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the source-review commit.

Not implemented:
source verification completion, reference promotion to Verified, dependency adoption, package installation, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, ML-DSA runtime integration, signing key generation, real ML-DSA public-key or signature material, test-vector execution, permanent runtime integration, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, or passport-verifier `ALLOW` path.

Next step:
Plan the isolated ML-DSA runtime experiment in a temporary environment before any package execution or repository dependency adoption.

## Entry 102

Date: 2026-06-06

Type: Signature runtime isolated experiment planning

Summary: Added isolated ML-DSA runtime experiment plan.

Files:
Added `docs/signature-verification-isolated-experiment-plan.md` and updated this evidence log.

Result:
A focused isolated experiment plan now defines how future ML-DSA runtime evaluation should run before any package execution, repository dependency adoption, or signature-verification implementation.

The plan records that future runtime experiments must run outside the repository environment, preferably under `/tmp/aaid-mldsa-runtime-eval`, and must not install packages into the repository virtual environment.

The plan defines candidate order, allowed experiment actions, disallowed experiment actions, evidence to capture, result categories, stop conditions, responsible-disclosure handling, non-goals, and the next review step.

The plan preserves the current boundary: real signature verification is still not implemented; the verifier still records `signature_verification_not_implemented`, returns `DENY`, and cannot return `ALLOW`.

This is experiment planning only. It does not execute packages, install dependencies, change requirements or lockfiles, change verifier source, change schema, update example passport values, generate signing keys in the repository, run test vectors, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the experiment plan commit.

Not implemented:
package execution, package installation in the repository, dependency adoption, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, real signature verification, signing-key generation in the repository, permanent runtime integration, test-vector execution in the repository, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, reference promotion to Verified, or passport-verifier `ALLOW` path.

Next step:
Review and approve the isolated `/tmp` runtime experiment command plan before any package execution.

## Entry 103

Date: 2026-06-06

Type: Signature runtime isolated evaluation

Summary: Recorded isolated cryptography ML-DSA runtime evaluation.

Files:
Added `docs/signature-runtime-evaluation-results-cryptography-48.0.0.md` and updated this evidence log.

Result:
The first isolated ML-DSA runtime evaluation was recorded for Python `cryptography` version `48.0.0`.

The evaluation ran outside the repository environment under `/tmp/aaid-mldsa-runtime-eval` using a temporary virtual environment. The package was not installed into the repository virtual environment.

The isolated runtime exposed the ML-DSA module and the `MLDSA65PrivateKey` and `MLDSA65PublicKey` classes. The observed backend signal was `OpenSSL 4.0.0 14 Apr 2026`.

Disposable ML-DSA-65 key generation, signing, verification, raw public-key export, and raw public-key import passed in the isolated environment. Observed sizes were raw public key `1952` bytes, private seed `32` bytes, and signature `3309` bytes.

Negative checks passed for modified message, modified signature, wrong context, malformed-length public keys, mutated same-length public key verification, and malformed signatures. The observed failure behavior used `InvalidSignature` or `ValueError` in the tested cases.

Overall result:
PARTIAL. The candidate showed strong isolated ML-DSA-65 runtime behavior, but adoption readiness remains partial until official test-vector compatibility, artifact provenance, dependency-risk review, encoding decision, and verifier integration planning are completed.

This is isolated runtime evidence only. It does not adopt `cryptography`, approve dependency adoption, install packages into the repository environment, change requirements or lockfiles, change verifier source, change schema, add real passport signature material, execute official test vectors, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the evaluation result commit.

Not implemented:
repository dependency adoption, package installation in the repository environment, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, official test-vector execution, artifact provenance verification, real passport signature verification, signing-key generation in the repository, permanent runtime integration, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, reference promotion to Verified, or passport-verifier `ALLOW` path.

Next step:
Review official ML-DSA test-vector compatibility and package artifact evidence before any repository dependency adoption or verifier integration proposal.

## Entry 104

Date: 2026-06-06

Type: Signature runtime artifact evidence

Summary: Recorded isolated cryptography package artifact evidence.

Files:
Added `docs/signature-runtime-artifact-evidence-cryptography-48.0.0.md` and updated this evidence log.

Result:
Isolated package artifact evidence was recorded for Python `cryptography` version `48.0.0`.

The artifact evidence run used `/tmp/aaid-cryptography-48-artifact-evidence` and a temporary virtual environment outside the repository. The package was not installed into the repository virtual environment.

The isolated run downloaded the `cryptography-48.0.0` source distribution and the `cryptography-48.0.0-cp311-abi3-manylinux_2_34_x86_64` wheel. Observed SHA-256 hashes were recorded for both artifacts.

The wheel metadata and source-distribution metadata recorded package name, version, license expression, Python requirement, runtime dependency surface, project URLs, wheel generator, wheel tag, and license-file presence.

The repository environment check confirmed `repo_venv_cryptography: not installed`.

Overall result:
PARTIAL. Artifact hashes, metadata, license signal, and dependency surface were captured, but adoption readiness remains partial until provenance verification, vulnerability/security advisory review, dependency-risk review, official test-vector compatibility, encoding decision, and verifier integration planning are completed.

This is artifact evidence only. It does not adopt `cryptography`, approve dependency adoption, install packages into the repository environment, change requirements or lockfiles, change verifier source, change schema, execute official test vectors, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the artifact evidence commit.

Not implemented:
repository dependency adoption, package installation in the repository environment, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, official test-vector execution, provenance verification, vulnerability/security advisory review, real passport signature verification, signing-key generation in the repository, permanent runtime integration, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, reference promotion to Verified, or passport-verifier `ALLOW` path.

Next step:
Review official ML-DSA test-vector compatibility, provenance options, and dependency-risk evidence before any repository dependency adoption or verifier integration proposal.

## Entry 105

Date: 2026-06-06

Type: Signature test-vector compatibility planning

Summary: Added ML-DSA test-vector compatibility plan.

Files:
Added `docs/signature-test-vector-compatibility-plan.md` and updated this evidence log.

Result:
A focused compatibility plan now defines how official or authoritative ML-DSA-65 test-vector material should be reviewed before any repository dependency adoption, verifier integration, or real signature-verification implementation.

The plan records that final-version ML-DSA material from NIST CAVP / ACVP sources should be preferred, and that draft-era or intermediate post-quantum vectors must not be treated as final ML-DSA compatibility evidence unless the limitation is explicitly recorded.

The plan records compatibility questions for message bytes, public-key bytes, signature bytes, JSON encoding, ML-DSA-65 parameter-set coverage, deterministic test material, runtime API compatibility, invalid-vector behavior, fail-closed exception mapping, and API limitations.

The plan also records planned compatibility categories, isolated execution rules, evidence to capture later, stop conditions, non-goals, and the next step.

This is test-vector compatibility planning only. It does not download official vectors, execute vectors, adopt dependencies, install packages into the repository environment, change requirements or lockfiles, change verifier source, change schema, add real passport signature material, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the compatibility plan commit.

Not implemented:
official vector download, official vector execution, repository dependency adoption, package installation in the repository environment, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, real passport signature verification, signing-key generation in the repository, permanent runtime integration, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, reference promotion to Verified, or passport-verifier `ALLOW` path.

Next step:
Review exact NIST CAVP / ACVP ML-DSA vector files and decide whether an isolated `/tmp` vector-format inspection should be approved.

## Entry 106

Date: 2026-06-06

Type: Signature test-vector format inspection

Summary: Recorded ML-DSA FIPS204 test-vector format inspection.

Files:
Added `docs/signature-test-vector-format-inspection-mldsa-fips204.md` and updated this evidence log.

Result:
An isolated format inspection was recorded for NIST ACVP-Server ML-DSA FIPS204 JSON files.

The inspection ran outside the repository under `/tmp/aaid-mldsa-vector-format`. The inspected JSON files were downloaded and inspected only under `/tmp`; no vector files were copied into the repository.

The inspected source family was `usnistgov/ACVP-Server` under `gen-val/json-files`, covering `ML-DSA-keyGen-FIPS204`, `ML-DSA-sigGen-FIPS204`, and `ML-DSA-sigVer-FIPS204`.

The inspection recorded SHA-256 hashes for the selected prompt and expected-results JSON files, confirmed top-level ML-DSA FIPS204 structure, and recorded case counts for key generation, signature generation, and signature verification.

Observed ML-DSA-65 coverage included 8 `sigGen` groups and 4 `sigVer` groups. The `sigVer` format included public keys, signatures, messages or `mu`, context where applicable, and expected `testPassed` labels. Observed ML-DSA-65 byte lengths matched the isolated `cryptography==48.0.0` runtime observations: public key `1952` bytes and signature `3309` bytes.

Overall result:
PARTIAL. The vector format appears suitable for later isolated compatibility testing, but official compatibility remains unproven until vector execution is explicitly approved and recorded.

This is format inspection only. It does not execute vectors, adopt dependencies, install packages into the repository environment, change requirements or lockfiles, change verifier source, change schema, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the format inspection commit.

Not implemented:
official vector execution, repository dependency adoption, package installation in the repository environment, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, real signature verification, permanent runtime integration, signing-key generation in the repository, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, reference promotion to Verified, or passport-verifier `ALLOW` path.

Next step:
Decide whether to run an isolated `/tmp` ML-DSA-65 `sigVer` compatibility test against the inspected NIST ACVP-Server FIPS204 JSON files.

## Entry 107

Date: 2026-06-06

Type: Signature test-vector execution result

Summary: Recorded isolated ML-DSA-65 sigVer compatibility result.

Files:
Added `docs/signature-test-vector-execution-results-cryptography-48.0.0-mldsa65-sigver.md` and updated this evidence log.

Result:
An isolated ML-DSA-65 `sigVer` compatibility result was recorded for Python `cryptography==48.0.0` against NIST ACVP-Server ML-DSA FIPS204 `sigVer` JSON files.

The test ran outside the repository under `/tmp/aaid-mldsa-sigver-compat`. The package and vector files were used only in the isolated temporary environment. No package was installed into the repository virtual environment and no vector files were copied into the repository.

The first broad external run selected two ML-DSA-65 external groups and executed 30 cases. It matched 27 cases and had 3 mismatches, all in `tgId` 4. The mismatches were expected-valid cases observed as invalid: `tcId` 48, `tcId` 49, and `tcId` 51.

Follow-up classification showed that `tgId` 4 contains test-level `hashAlg` values on all 15 cases. The first script selected external groups by group-level metadata only, so those test-level `hashAlg` cases were incorrectly treated as ordinary message-mode verification cases.

The corrected run executed only direct external ML-DSA-65 `sigVer` cases excluding test-level `hashAlg` and internal-interface cases. It executed 15 cases and matched all 15 expected `testPassed` labels.

Overall result:
PARTIAL. Direct external non-hash ML-DSA-65 `sigVer` compatibility passed for the selected subset, while test-level `hashAlg`, internal-interface, and `mu` cases remain untested or require further mapping research.

This is isolated test-vector execution evidence only. It does not adopt `cryptography`, approve dependency adoption, install packages into the repository environment, change requirements or lockfiles, change verifier source, change schema, implement real passport signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the execution-result commit.

Not implemented:
repository dependency adoption, package installation in the repository environment, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, full official vector execution, test-level `hashAlg` handling, internal-interface vector execution, `mu` interface vector execution, real passport signature verification, signing-key generation in the repository, permanent runtime integration, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, reference promotion to Verified, or passport-verifier `ALLOW` path.

Next step:
Research the correct ML-DSA `hashAlg` and internal-interface mapping before expanding official vector execution beyond direct external non-hash `sigVer` cases.

## Entry 108

Date: 2026-06-06

Type: Signature hashAlg and internal-interface mapping planning

Summary: Added ML-DSA hashAlg and internal-interface mapping plan.

Files:
Added `docs/signature-test-vector-hashalg-internal-mapping-plan.md` and updated this evidence log.

Result:
A focused mapping plan now defines the next research boundary for ML-DSA test-vector compatibility after the isolated direct external non-hash `sigVer` subset passed.

The plan records that the direct external non-hash ML-DSA-65 `sigVer` subset passed with 15 executed cases, 15 matches, and 0 mismatches, while the first broader external run produced 3 mismatches in `tgId` 4 where follow-up inspection showed test-level `hashAlg` values on all 15 cases.

The plan defines the next research question as how ACVP `hashAlg`, internal-interface, `externalMu`, and `mu` test cases should be interpreted, and whether the candidate runtime exposes the required interface clearly enough for later isolated execution.

The plan records mapping topics, source review targets, possible outcomes, non-goals, and the next step.

This is mapping research planning only. It does not execute more vectors, adopt dependencies, install packages into the repository environment, change requirements or lockfiles, change verifier source, change schema, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the mapping plan commit.

Not implemented:
additional vector execution, repository dependency adoption, package installation in the repository environment, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, real passport signature verification, full official vector compatibility, test-level `hashAlg` handling, internal-interface vector execution, `mu` interface vector execution, permanent runtime integration, signing-key generation in the repository, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, reference promotion to Verified, or passport-verifier `ALLOW` path.

Next step:
Review FIPS 204, the ACVP ML-DSA JSON specification, and the candidate runtime documentation to decide whether `hashAlg`, internal-interface, and `mu` cases can be executed safely in isolation or should remain explicitly out of scope.

## Entry 109

Date: 2026-06-06

Type: Signature hashAlg source review

Summary: Recorded ML-DSA hashAlg source-review findings.

Files:
Added `docs/signature-test-vector-hashalg-source-review.md` and updated this evidence log.

Result:
A focused source-review document now records findings for ML-DSA `hashAlg`, internal-interface, `externalMu`, and `mu` mapping before expanding isolated ML-DSA-65 `sigVer` vector execution beyond the direct external non-hash subset.

The document records the current boundary: Python `cryptography==48.0.0` passed the direct external non-hash ML-DSA-65 `sigVer` subset with 15 executed cases, 15 matches, and 0 mismatches. The earlier broader external run remains PARTIAL because 3 mismatches occurred in `tgId` 4 where follow-up inspection showed test-level `hashAlg` values on all 15 cases.

The source-review findings record that future ML-DSA compatibility work must not treat pure ML-DSA, HashML-DSA, internal-interface inputs, and `mu` inputs as interchangeable. ACVP vector fields require explicit mapping before execution, and candidate runtime documentation and issue history must be reviewed before attempting `hashAlg`, internal-interface, or `mu` cases.

The document records mapping risks, research questions, evaluation classification, non-goals, and the next step. Additional vector execution remains blocked until mapping review.

Overall result:
NEEDS_RESEARCH. Direct external non-hash ML-DSA-65 `sigVer` remains the only passing official-vector subset recorded so far. `hashAlg`, HashML-DSA runtime support, internal-interface mapping, `mu` mapping, and passport proof-profile decisions remain unresolved.

This is source review only. It does not execute more vectors, adopt dependencies, install packages into the repository environment, change requirements or lockfiles, change verifier source, change schema, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the source-review commit.

Not implemented:
additional vector execution, repository dependency adoption, package installation in the repository environment, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, real passport signature verification, full official vector compatibility, test-level `hashAlg` handling implementation, internal-interface vector execution, `mu` interface vector execution, permanent runtime integration, signing-key generation in the repository, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, reference promotion to Verified, or passport-verifier `ALLOW` path.

Next step:
Review FIPS 204 and ACVP ML-DSA mapping details more closely before deciding whether to keep passport signature verification scoped to pure direct external ML-DSA message-mode verification for the first implementation plan.

## Entry 110

Date: 2026-06-06

Type: Signature proof profile initial scope

Summary: Added initial signature proof profile scope.

Files:
Added `docs/signature-proof-profile-initial-scope.md` and updated this evidence log.

Result:
A focused profile-scope document now records the initial passport signature-verification boundary before any verifier implementation, dependency adoption, schema change, or passport-verifier `ALLOW` path.

The document scopes the first passport signature-verification profile to ML-DSA-65 pure direct external message-mode verification, with canonical passport payload bytes as the signed message. It records that context handling, raw public-key encoding, and raw signature encoding still require explicit profile decisions before implementation.

The document explicitly leaves test-level `hashAlg`, HashML-DSA, internal-interface cases, `externalMu`, `mu` input handling, reconstructed internal ML-DSA values, signing operations, generated passport test signatures, and verifier `ALLOW` behavior out of scope.

The document records required implementation preconditions, fail-closed behavior for unsupported signature modes, the narrow research position, non-goals, and the next step.

Overall result:
PARTIAL. The initial profile scope is now recorded, but real signature verification remains unimplemented and implementation preconditions remain unresolved.

This is a profile-scope decision only. It does not execute vectors, adopt dependencies, install packages into the repository environment, change requirements or lockfiles, change verifier source, change schema, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the profile-scope commit.

Not implemented:
additional vector execution, repository dependency adoption, package installation in the repository environment, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, real passport signature verification, full official vector compatibility, test-level `hashAlg` handling implementation, internal-interface vector execution, `mu` interface vector execution, permanent runtime integration, signing-key generation in the repository, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, reference promotion to Verified, or passport-verifier `ALLOW` path.

Next step:
Plan the first implementation boundary for pure direct external ML-DSA-65 message-mode verification without changing verifier behavior yet.

## Entry 111

Date: 2026-06-06

Type: Signature implementation boundary planning

Summary: Added signature verification implementation boundary plan.

Files:
Added `docs/signature-verification-implementation-boundary-plan.md` and updated this evidence log.

Result:
A focused implementation-boundary plan now defines the smallest future boundary for pure direct external ML-DSA-65 message-mode verification before changing verifier behavior.

The plan records the current boundary: the verifier already prepares canonical passport payload bytes, records `signature_input_prepared`, records `signature_verification_not_implemented`, returns `DENY`, and cannot return `ALLOW`.

The plan defines a future small internal signature-verification adapter that should accept only prepared canonical passport payload bytes, selected public-key metadata, selected proof metadata, and configured signature-profile information. The adapter must not perform parsing, canonicalization, issuer trust, revocation, authorization, approval, audit, enforcement, gateway, or MCP decisions.

The plan records the first supported profile, explicitly unsupported modes, proposed adapter result model, proposed verifier checks, fail-closed behavior, required tests, dependency blocker, non-goals, and the next step.

Overall result:
PARTIAL. The implementation boundary is now planned, but real signature verification remains unimplemented and dependency adoption remains blocked.

This is planning only. It does not adopt dependencies, install packages into the repository environment, change requirements or lockfiles, change verifier source, change schema, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the boundary-plan commit.

Not implemented:
dependency adoption, package installation in the repository environment, requirements changes, lockfile changes, verifier source changes, schema changes, example passport updates, new passport signatures, real signature verification, signing-key generation, full official vector compatibility, test-level `hashAlg` handling, internal-interface vector execution, `mu` interface vector execution, issuer trust registry, signed revocation evidence, authorization policy changes, approval enforcement changes, audit storage, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, or passport-verifier `ALLOW` path.

Next step:
Review this boundary against the existing verifier code and tests before deciding whether to create adapter-interface tests without importing a cryptographic runtime.

## Entry 112

Date: 2026-06-06

Type: Documentation organization planning

Summary: Added documentation organization plan.

Files:
Added `docs/documentation-organization-plan.md` and updated this evidence log.

Result:
A focused documentation organization plan now records how the repository documentation should be organized as the research grows.

The plan keeps `docs/references.md` at the docs root, keeps evidence files unchanged, keeps specs unchanged, avoids numeric prefixes on existing filenames, and recommends folder-level README files for reading order.

The plan proposes future topic folders for foundation documents, research models, threat boundaries, canonicalization, signature verification, and standards positioning. It also records that future folders should be added only when they reduce confusion and have enough material to justify them.

The plan records a staged migration order: add the organization plan, add a central `docs/README.md`, add folder README files without moving documents, run a link-impact check, then move topic documents in small reviewable stages using `git mv` with link updates in the same commit.

This is organization planning only. It does not move files, rename files, update references, change source code, change tests, change specs, adopt dependencies, change verifier behavior, implement real signature verification, or create a passport-verifier `ALLOW` path.

Tests:
`python -m pytest -q` passed with 594 tests after the organization-plan commit.

Not implemented:
documentation file moves, documentation file renames, `docs/references.md` move, evidence file moves, specs moves, numeric filename prefixes, reference updates, source changes, test changes, dependency adoption, verifier behavior changes, real signature verification, folder README files, central docs README, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, or passport-verifier `ALLOW` path.

Next step:
Add a central `docs/README.md` that gives readers a clear map of the research areas and the recommended reading order before moving any files.

## Entry 113

Date: 2026-06-06

Type: Documentation file organization

Summary: Organized documentation files into topic folders.

Files:
Added `docs/README.md`, moved topic documentation files into docs topic folders, updated internal documentation path references, and updated this evidence log.

Result:
The documentation directory is now organized around a central index and topic folders.

The docs root now contains only:

- `docs/README.md`
- `docs/references.md`

Topic documentation was moved into:

- `docs/00-foundation/`
- `docs/10-models/`
- `docs/20-threat-boundaries/`
- `docs/30-canonicalization/`
- `docs/40-signature-verification/`
- `docs/50-standards-positioning/`

The documentation organization plan was moved into `docs/00-foundation/` so the docs root remains focused on the central index and reference register.

`docs/references.md` remains at the docs root. Evidence files remain unchanged. Specs remain unchanged.

Internal documentation path references were updated in the same migration commit. A markdown link check found no broken markdown links after the move.

This is documentation organization only. It does not change source code, tests, specs, evidence structure, dependencies, verifier behavior, real signature verification, or passport-verifier `ALLOW` behavior.

Tests:
`python -m pytest -q` passed with 594 tests after the documentation organization commit.

Not implemented:
source changes, test changes, spec moves, evidence file moves, reference-register move, dependency adoption, verifier behavior changes, real signature verification, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, or passport-verifier `ALLOW` path.

Next step:
Run final tests and push the documentation organization milestone.
