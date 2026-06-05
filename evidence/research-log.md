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
