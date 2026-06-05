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
