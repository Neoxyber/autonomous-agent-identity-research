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
legal compatibility, package provenance, or signature-readiness.

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

- PyPI and GitHub release artifacts matched byte-for-byte for the evaluated
  wheel and source distribution.
- Wheel SHA-256:
  `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`.
- Source distribution SHA-256:
  `e545841329fe0eee4f6a3b44e7034343100c12b4ec566dc06ca9735681deb4da`.
- The wheel is `py3-none-any`, pure Python, and no native extensions were
  observed.
- Runtime dependency surface remains empty for normal installation; dependency
  metadata observed only optional development, documentation, lint, and test
  extras.
- PyPI release metadata reported no index-hosted provenance field for the
  release files.
- GitHub release assets include Sigstore bundle files for the wheel, source
  distribution, and source archives.
- Sigstore bundle metadata referenced Rekor `hashedrekord` entries whose decoded
  bodies contained the expected artifact SHA-256 values.
- Certificate hints referenced
  `trailofbits/rfc8785.py`, `refs/tags/v0.1.4`,
  `https://token.actions.githubusercontent.com`, and the release workflow
  `release.yml@refs/tags/v0.1.4`.

Status:
This is provenance evidence only. Cryptographic Sigstore verification, Rekor
inclusion verification, certificate-chain verification, expected issuer policy,
and expected workflow identity policy remain pending. Provenance must not be
claimed as verified yet.

## Required legal and attribution review

Before any adoption proposal, the project should record declared package
license, source license file status, copyright and attribution requirements,
metadata/source-license agreement, required documentation attribution, and
whether legal compatibility remains pending user or legal review.

Legal compatibility should not be claimed until reviewed through appropriate
legal resources.

## Required dependency-risk review

Before any adoption proposal, the project should record dependency tree,
supported Python versions, maintenance and release activity, vulnerability
signals, maintainer/source trust considerations, unsupported-domain behavior,
update/rollback expectations, and whether the dependency can be isolated behind
a small internal boundary.

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
legal/attribution review, dependency and maintenance risk, verifier raw-JSON
boundary, schema-before-canonicalization rule, unsafe integer and future numeric
payload-domain policy, integration tests, golden vector migration review, and
verification-result failure semantics.

## Non-goals

This plan does not cover dependency adoption, package installation,
canonicalizer replacement, real signature verification, post-quantum signing,
issuer trust, revocation, policy, audit, gateway, cloud, or external
integrations.

## Next step

Perform REF-014 provenance, legal/attribution, dependency-risk, and
verifier-boundary review before any adoption proposal or runtime integration
branch.
