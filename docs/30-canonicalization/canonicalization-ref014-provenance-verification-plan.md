# REF-014 Provenance Verification Plan

## Purpose

This document defines the provenance checks required before REF-014
`rfc8785==0.1.4` can be proposed as the repository canonicalization
implementation.

This is planning only. It does not approve verification execution, package
installation, dependency adoption, requirements changes, lockfile changes,
canonicalizer replacement, golden-vector migration, or real signature
verification.

## Prior evidence

The provisional integration plan recorded an initial review of REF-014 artifact
metadata, hashes, release evidence, and declared package information. That review
did not complete cryptographic provenance verification.

This document records the procedure required before provenance can be treated as
established.

## Pinned inputs

Package: `rfc8785==0.1.4`.

Source: `trailofbits/rfc8785.py`, tag `v0.1.4`.

Artifacts:

- wheel: `rfc8785-0.1.4-py3-none-any.whl`
- wheel SHA-256:
  `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`
- source distribution: `rfc8785-0.1.4.tar.gz`
- source distribution SHA-256:
  `e545841329fe0eee4f6a3b44e7034343100c12b4ec566dc06ca9735681deb4da`

Release evidence: GitHub release Sigstore bundles for the wheel and source
distribution.

## Verification procedure

These steps are executed later, only after separate approval.

### V0. Record verifier and trust material

Record the verifier tool, exact tool version, and Sigstore trusted root material
used for the run. This includes the Fulcio root, Rekor public key, and any
transparency-log trust material used by the verifier.

Later verification steps must use this recorded trust material. Unrecorded trust
material fetched during the run is not sufficient.

### V1. Recompute artifact digests

Recompute the SHA-256 digest of the wheel and source distribution. Each digest
must match the pinned value in this document.

### V2. Verify Sigstore signatures

Verify each artifact's Sigstore bundle signature against the corresponding
artifact digest.

### V3. Verify Rekor inclusion

Verify the transparency-log inclusion proof and signed entry timestamp using the
Rekor public key recorded in V0. The Rekor entry must bind the recorded artifact
digest.

### V4. Verify the Fulcio certificate chain

Verify the signing certificate chain using the Fulcio root recorded in V0.
Certificate validity is assessed at signing time using the embedded signed
certificate timestamp.

### V5. Verify the OIDC issuer

The certificate OIDC issuer must equal:

`https://token.actions.githubusercontent.com`

### V6. Verify the workflow identity

The expected certificate identity must be fixed before verification. The bundle
identity is evidence to compare against that fixed value; it is not the source of
the expected value.

Expected identity:

`https://github.com/trailofbits/rfc8785.py/.github/workflows/release.yml@refs/tags/v0.1.4`

The expected repository, workflow, and tag remain fixed before verification.
Verification fails closed if the bundle identity does not match the expected
identity.

### V7. Record source-to-artifact correspondence

Record whether the verified identity binds the artifact build to source tag
`v0.1.4` and the release workflow. If reproducible-build re-derivation is
attempted, record the result.

## Tooling

Verification should use a maintained Sigstore verifier, such as the Sigstore
Python tool or `cosign verify-blob`, in an isolated environment outside this
repository.

The execution record must include the verifier tool name and version, trusted
root material, artifact names and digests, verified OIDC issuer, verified
certificate identity, Rekor result, and Fulcio certificate-chain result.

This document names tooling for planning only. It does not install or execute
any tool.

## Acceptance criteria

Provenance is established only when all of the following are true:

1. V0 records the verifier tool, exact version, and trusted root material.
2. V1 through V6 pass.
3. V7 is recorded.
4. Fulcio and Rekor trust material come from the V0 recorded trust root.
5. The verified certificate identity matches the identity fixed in V6.

Any failure fails closed. REF-014 remains `Pending review`, and adoption remains
blocked. A partial result is recorded as PARTIAL with explicit named gaps.

## Recording

Results are recorded using the project result categories: PASS, FAIL, PARTIAL,
BLOCKED, and NEEDS_RESEARCH.

Results should be recorded in the provisional integration plan provenance
section and in a new research-log entry. REF-014 remains `Pending review` until a
separate adoption decision record is approved.

## Out of scope

This document does not cover execution of this procedure, package installation,
dependency adoption, requirements or lockfile changes, canonicalizer replacement,
numeric-domain enforcement, golden-vector migration, real signature verification,
license or attribution sign-off, or dependency and maintenance-risk sign-off.

## Next step

Request explicit approval before executing this plan in an isolated environment.
After a passing provenance result, proceed to license and attribution review,
dependency and maintenance-risk review, and then a separate adoption decision.
