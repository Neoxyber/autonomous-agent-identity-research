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

Status:
This is provenance evidence only. Cryptographic Sigstore verification, Rekor
inclusion verification, certificate-chain verification, expected issuer policy,
and expected workflow identity policy remain pending.

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
license text is Apache License, Version 2.0. Package metadata includes the
Apache Software License classifier, `pyproject.toml` declares
`license = { file = "LICENSE" }`, and author metadata identifies Trail of Bits.
The README/PKG-INFO states that parts are adapted from Andrew Rundgren's
reference implementation, also described as Apache License, Version 2.0.
`pyproject.toml` declares `dependencies = []`; observed `Requires-Dist` entries
are optional extras for development, documentation, lint, and tests.

Status:
This is license/attribution and dependency-risk evidence only. License compatibility
and attribution completeness remain pending review. No adoption, package
installation, requirements change, or runtime behavior change is authorized.

## P2 maintenance-risk evidence collected

A first maintenance-risk pass observed that REF-014 `rfc8785==0.1.4` declares
`Requires-Python >=3.8`, has no normal runtime dependencies, and is marked
`Development Status :: 4 - Beta`. The GitHub repository was not archived,
disabled, or a fork. Tags and releases were observed from `v0.0.1` through
`v0.1.4`; the evaluated release was published on 2024-09-27. Repository metadata
showed recent activity in May 2026. The open issue query found no open issues
excluding pull requests and one open pull request related to mypy settings.

Status:
This is maintenance-risk evidence only. It does not establish long-term
maintenance suitability, vulnerability posture, adoption readiness, or operational
readiness.

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
Before any REF-014 adoption proposal, the project should decide whether to add a
raw JSON verifier entry point that calls `parse_json_no_duplicate_keys()` before
schema validation, or document that parsed mappings are accepted only with
caller-side duplicate-key parsing guarantees. This section does not authorize
verifier changes or runtime behavior changes.

## Required integration tests

A future integration branch should add tests before or with any runtime change:

- REF-014 produces expected canonical bytes for the minimal passport;
- the minimal passport payload hash is intentionally migrated or preserved with
  explanation;
- object order remains irrelevant;
- array order remains significant;
- proof material remains excluded from the signed payload;
- non-finite numbers fail closed;
- unsafe integer-domain behavior is tested and documented;
- duplicate-key raw JSON behavior remains enforced at the parse boundary;
- schema validation still runs before canonicalization-dependent verification;
- unsupported canonicalization fails closed;
- signature verification remains blocked until a later phase.

## Golden vector migration

Replacing the helper may change the minimal passport canonical byte output or
payload hash. Any change should be treated as an intentional migration, not
incidental drift.

Before adoption, the project should record:

- old helper canonical bytes or hash;
- REF-014 canonical bytes or hash;
- whether the minimal example changes;
- why the migration is acceptable;
- which tests pin the new expected value.

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
deferred with rationale: package artifact provenance, build provenance,
license/attribution review, dependency and maintenance risk, verifier raw-JSON
boundary, schema-before-canonicalization rule, unsafe integer and future numeric
payload-domain policy, integration tests, golden vector migration review, and
verification-result failure semantics.

## Non-goals

This plan does not cover dependency adoption, package installation,
canonicalizer replacement, real signature verification, post-quantum signing,
issuer trust, revocation, policy, audit, gateway, cloud, or external
integrations.

## Next step

Review the remaining REF-014 adoption requirements: cryptographic provenance
verification, license/attribution review, dependency and maintenance-risk
review, verifier entry-point decisions, numeric-domain policy, integration
tests, golden-vector migration review, and verification-result failure semantics.
No adoption proposal, runtime integration work, requirements change, or
canonicalizer replacement is authorized by this plan.
