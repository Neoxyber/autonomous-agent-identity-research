# REF-014 Provisional Integration Research Plan

## Purpose

This document defines the research and planning work required before any proposal
to adopt REF-014 `rfc8785==0.1.4` as the repository canonicalization
implementation.

It is not an adoption plan and does not authorize package installation,
requirements changes, canonicalizer replacement, verifier changes, or real
signature verification.

## Research basis

The project is building an agent passport research model where stable canonical
JSON bytes are required before trusted signatures can be meaningful. The current
long-term target is RFC 8785 / JSON Canonicalization Scheme.

The current research evidence identifies REF-014 as the leading candidate for
provisional integration planning. This position is based on isolated evaluation,
reference-vector comparison, bounded number-serialization checks, and
parse-layer/payload-domain review.

The broader 2026 and 2027 security environment supports an evidence-first
approach. Agentic systems require clear identity, privilege, tool-use, and
supply-chain boundaries. Product-like software also requires stronger provenance,
vulnerability-handling, and dependency-review discipline. Post-quantum signature
standards should inform future algorithm agility, but they do not remove the
need to first stabilize canonical bytes and verifier semantics.

## Current repository boundary

The repository currently has:

- a local research canonicalization helper in `src/aaid/canonicalization.py`;
- a raw JSON parser helper in `src/aaid/json_parsing.py` that rejects duplicate
  object member names;
- verifier logic that accepts an already parsed envelope object;
- schema validation before payload-hash comparison;
- signature-input preparation through the shared canonicalization helper;
- real signature verification blocked and fail-closed;
- no runtime dependency on REF-014 or REF-015;
- no package adoption, lockfile, or requirements change.

## Planning position

REF-014 is the leading candidate for provisional integration planning only.
This does not mean adoption, runtime selection, full RFC 8785/JCS conformance,
license compatibility, package provenance, or signature-readiness.

REF-015 remains comparison evidence and a cyberphone-lineage cross-check.

## Required provenance review

Before any adoption proposal, the project should record the exact package
version, source repository and release correspondence, package artifact hashes,
source-to-artifact traceability, generated/build-file status, native-build
status, transitive dependencies, and package-index expectations.

## P0 provenance evidence collected

A first isolated provenance pass was run under
`/tmp/aaid-ref014-provenance-review`.

Findings:
PyPI and GitHub release artifacts matched byte-for-byte for the evaluated wheel
and source distribution. The wheel SHA-256 was
`520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`; the source
distribution SHA-256 was
`e545841329fe0eee4f6a3b44e7034343100c12b4ec566dc06ca9735681deb4da`. The wheel
was `py3-none-any`, pure Python, with no native extensions observed. Normal
runtime dependency surface remained empty. PyPI release metadata reported no
index-hosted provenance field. GitHub release assets included Sigstore bundles;
bundle metadata referenced Rekor `hashedrekord` entries containing the expected
artifact hashes and certificate hints for `trailofbits/rfc8785.py`,
`refs/tags/v0.1.4`, `https://token.actions.githubusercontent.com`, and
`release.yml@refs/tags/v0.1.4`.

Status at P0:
This was provenance evidence only. At P0, cryptographic Sigstore verification,
Rekor inclusion verification, certificate-chain verification, expected issuer
policy, and expected workflow identity policy remained pending. The procedure
for that cryptographic verification, with acceptance criteria, was recorded in
`docs/canonicalization-ref014-provenance-verification-plan.md`.

## P1 cryptographic provenance verification result

A second isolated provenance pass was run under
`/tmp/aaid-ref014-provenance-verify`, using a separate verifier environment at
`/tmp/aaid-ref014-tools/.venv`.

Result:
PASS. The pinned wheel and source distribution were downloaded from the GitHub
release assets and their SHA-256 digests matched the values already recorded in
this plan. Sigstore 4.3.0 verified both artifacts offline against their release
bundles, using the fixed OIDC issuer
`https://token.actions.githubusercontent.com` and the fixed workflow identity
`https://github.com/trailofbits/rfc8785.py/.github/workflows/release.yml@refs/tags/v0.1.4`.

Tooling:
The verifier environment used Python 3.12.3, pip 26.1.2, and Sigstore 4.3.0.
Relevant verifier packages included `sigstore==4.3.0`,
`sigstore-models==0.0.6`, `sigstore-rekor-types==0.0.18`, `tuf==7.0.0`,
`securesystemslib==1.4.0`, `cryptography==48.0.0`, and `rfc8785==0.1.4`
inside the isolated verifier environment only.

Artifact digests:
The wheel digest matched
`520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`. The
source distribution digest matched
`e545841329fe0eee4f6a3b44e7034343100c12b4ec566dc06ca9735681deb4da`.

Status:
This is artifact provenance evidence only. It does not adopt REF-014, does not
promote REF-014 to Verified, does not install REF-014 into the repository, does
not change requirements or lockfiles, does not replace the current
canonicalization helper, does not migrate golden vectors, and does not unblock
real signature verification by itself.

## Required license and attribution review

Before any adoption proposal, the project should record declared package
license, source license file status, copyright and attribution requirements,
metadata/source-license agreement, required documentation attribution, and
whether license compatibility remains pending review.

Legal compatibility should not be claimed until reviewed through appropriate
license resources.

## Required dependency-risk review

Before any adoption proposal, the project should record dependency tree,
supported Python versions, maintenance and release activity, vulnerability
signals, maintainer/source trust considerations, unsupported-domain behavior,
update/rollback expectations, and whether the dependency can be isolated behind
a small internal boundary.

## P1 license and dependency-risk evidence collected

A first isolated license/attribution and dependency-risk pass inspected the wheel
and source distribution staged under `/tmp/aaid-ref014-provenance-review`.

Findings:
The wheel includes `rfc8785-0.1.4.dist-info/LICENSE`; the source distribution
includes `LICENSE`, `PKG-INFO`, `README.md`, and `pyproject.toml`. The included
license text is Apache License, Version 2.0. The wheel and source distribution
license files were identical, with SHA-256 digest
`0d542e0c8804e39aa7f37eb00da5a762149dc682d7829451287e11b938e94594`. No
`NOTICE` file was found in the inspected wheel, source distribution, or exact
GitHub `v0.1.4` tag metadata.

Package metadata includes the Apache Software License classifier,
`pyproject.toml` declares `license = { file = "LICENSE" }`, and author metadata
identifies Trail of Bits. The README/PKG-INFO states that parts are adapted from
Andrew Rundgren's reference implementation, also described as Apache License,
Version 2.0. `pyproject.toml` declares `dependencies = []`; observed
`Requires-Dist` entries are optional extras for development, documentation,
lint, and tests.

Status:
This is license/attribution and dependency-risk evidence only. License compatibility
and attribution completeness remain pending review. No adoption, package
installation, requirements change, or runtime behavior change is authorized.

## P2 maintenance-risk evidence collected

A maintenance-risk pass observed that REF-014 `rfc8785==0.1.4` declares
`Requires-Python >=3.8`, has no normal runtime dependencies, and is marked
`Development Status :: 4 - Beta`. Observed `Requires-Dist` entries were optional
extras for development, documentation, lint, and tests.

Repository metadata showed that `trailofbits/rfc8785.py` was not archived, not a
fork, not a mirror, not private, not empty, and had GitHub security policy
support enabled. The default branch was `main`, primary language was Python, the
repository had issues enabled, and metadata showed activity in May 2026. GitHub
repository license metadata returned `null`, while artifact license evidence is
recorded separately in the P1 section.

Tags and releases were observed from `v0.0.1` through `v0.1.4`. The evaluated
release `v0.1.4` was created and published on 2024-09-27, was not a draft, and
was not a prerelease. The release assets included the pinned wheel, source
distribution, and corresponding Sigstore bundles. The open issue query found no
open issues excluding pull requests. One open pull request related to mypy
settings was observed. The GitHub security-advisory query returned no entries.

Status:
PARTIAL. This is dependency and maintenance-risk evidence only. The normal
runtime dependency surface is low and no obvious repository blocking signal was
observed, but the package is marked beta, the latest release is from 2024, GitHub
repository license metadata is null, and long-term maintenance suitability,
vulnerability posture, adoption readiness, and operational readiness remain
unproven.

## Required verifier-boundary decisions

Before replacing the canonicalization helper, the project should decide:

- whether public verifier entry points accept raw JSON text or parsed mappings;
- whether raw JSON input must pass through duplicate-key rejection first;
- whether parsed mappings are trusted only after caller-side parsing guarantees
  are documented;
- whether schema validation always happens before canonicalization;
- how canonicalization failures are represented in `VerificationResult`;
- whether unsafe integer and future numeric payload-domain failures are schema
  failures, parse failures, or canonicalization failures.

## P3 verifier-boundary evidence collected

A first verifier-boundary pass inspected the current parser, canonicalization
helper, verifier, and related tests.

Findings:
The raw JSON duplicate-key helper exists separately in `src/aaid/json_parsing.py`
and rejects duplicate object member names before JSON objects collapse into
parsed mappings. The current verifier entry point `verify_passport_envelope()`
accepts an already parsed envelope object, not raw JSON text. Schema validation
runs before payload-hash comparison. Payload-hash verification and future
signature-input preparation both use the shared canonicalization helper over the
`passport` object only, excluding the envelope wrapper and `proofs`. Unsupported
canonicalization fails closed before signature input preparation. Real signature
verification remains unimplemented and fails closed.

Status:
The verifier entry-point boundary is recorded. `verify_passport_json()` is the
raw JSON entry point and parses input with `parse_json_no_duplicate_keys()`
before schema validation, so raw JSON duplicate-key rejection runs before
canonicalization-dependent checks. `verify_passport_envelope()` is the
parsed-envelope entry point and assumes callers provide already parsed,
duplicate-key-safe mappings. This section does not authorize verifier changes or
runtime behavior changes.

## P4 numeric-domain policy evidence collected

The current passport payload profile remains numeric-field-free. Existing
canonicalization and threat-model documents already record that future numeric
payload fields require a separate schema and canonicalization decision before
canonicalizer adoption, golden-vector migration, or signature-verification
planning.

Result:
PASS for the current numeric-field-free passport profile. The schema inspection
found no `number` or `integer` typed fields in the current passport profile.
Repository current-profile evidence records fail-closed handling for non-finite
values. REF-014's unsafe-integer blocking behavior is treated as input-domain
enforcement, not as an ordinary canonical byte mismatch.

Status:
This is current-profile numeric-domain evidence only. It does not approve future
numeric payload fields, implement numeric-domain enforcement, adopt REF-014,
replace the canonicalizer, migrate golden vectors, or unblock real signature
verification. Future numeric payload fields remain blocked until explicit schema
bounds, accepted numeric domains, and failure semantics are recorded.

## Required integration-test planning

Future integration tests should be planned before any runtime change. Executing
REF-014-based tests requires separate adoption approval and is not authorized by
this plan.

Planned categories:

1. REF-014 produces expected canonical bytes for the minimal passport.
2. The minimal passport payload hash is intentionally migrated or preserved with
   explanation.
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

## Golden vector migration

Replacing the helper may change the minimal passport canonical byte output or
payload hash. Any change must be treated as an intentional migration, not
incidental drift.

Current helper evidence:
The current helper canonicalizes the minimal passport to 1628 bytes. The current
SHA-256 payload hash is
`b85a7ddfefccb9582bf6ab23dac42a968cc0b6aabfc1d29d416ea25e27bfb6bc`, which
matches the minimal example proof `payload_hash`.

Before adoption, the project must record:

- current helper canonical bytes or hash;
- REF-014 canonical bytes or hash;
- whether the minimal example changes;
- whether the existing payload hash is preserved or intentionally migrated;
- why any migration is acceptable;
- which tests pin the expected value.

Status:
This is golden-vector migration planning only. It does not execute REF-014,
adopt REF-014, replace the canonicalizer, update the minimal example, change the
payload hash, migrate golden vectors, or unblock real signature verification.

## Security interpretation

REF-014's safe-integer blocking behavior should be treated as security-relevant
input-domain enforcement, not as an ordinary mismatch. The integration plan
should preserve fail-closed handling for ambiguous or unsupported payload
domains.

The canonicalization dependency should remain behind a small internal boundary
so future algorithm-agility and post-quantum signature work can change signature
algorithms without redefining canonical payload bytes.

## Adoption blockers

REF-014 must not be adopted until these items are resolved or explicitly
deferred with rationale: build provenance, legal compatibility and attribution
completeness, integration-test execution, golden vector migration review, and
verification-result failure semantics.

## Non-goals

This plan does not cover dependency adoption, package installation,
canonicalizer replacement, real signature verification, post-quantum signing,
issuer trust, revocation, policy, audit, gateway, cloud, or external
integrations.

## Next step

Review the remaining REF-014 adoption requirements: legal compatibility and
attribution completeness, integration-test execution, golden-vector migration
review, and verification-result failure semantics.
No adoption proposal, runtime integration work, requirements change, or
canonicalizer replacement is authorized by this plan.
