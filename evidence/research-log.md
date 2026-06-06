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
