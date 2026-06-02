# REF-014 Provenance Verification Plan

## Purpose

This document defines the cryptographic provenance verification procedure that must
be completed and recorded before any proposal to adopt REF-014 `rfc8785==0.1.4` as
the repository canonicalization implementation.

It is planning only. It does not authorize execution of the verification, package
installation, requirements or lockfile changes, canonicalizer replacement,
golden-vector migration, dependency adoption, or real signature verification.

## Relationship to prior evidence

The provisional integration plan recorded a first provenance pass that observed,
but did not cryptographically verify, the REF-014 artifacts. This document specifies
how that cryptographic verification will be performed and what must hold for it to pass.

## Inputs (pinned)

- Package: `rfc8785==0.1.4` (PyPI).
- Source: `trailofbits/rfc8785.py`, tag `v0.1.4`.
- Wheel `rfc8785-0.1.4-py3-none-any.whl` SHA-256:
  `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`.
- Source distribution `rfc8785-0.1.4.tar.gz` SHA-256:
  `e545841329fe0eee4f6a3b44e7034343100c12b4ec566dc06ca9735681deb4da`.
- GitHub release Sigstore bundles for the wheel and source distribution.

## Verification steps (to be executed later, under separate approval)

V0. Trusted root and tooling pinning: before any other step, record the verifier
tool, its exact version, and the Sigstore trusted-root / TUF material used for
verification. All certificate and transparency-log trust material used below — the
Fulcio root, the Rekor public key, and any other Sigstore trust anchors — must come
from this recorded trusted root used by the verifier, not from material fetched ad
hoc at verification time.

V1. Artifact digest pinning: recompute the SHA-256 of the wheel and source
distribution; each must equal the recorded digest above.

V2. Sigstore signature verification: verify each artifact's Sigstore bundle signature
over the artifact digest.

V3. Rekor inclusion verification: verify the transparency-log inclusion proof and
signed entry timestamp against the Rekor public key taken from the V0 recorded
trusted root; the log entry must bind the recorded artifact digest.

V4. Fulcio certificate-chain verification: verify the signing certificate chains to
the Fulcio root taken from the V0 recorded trusted root, with validity established at
signing time via the embedded signed certificate timestamp.

V5. Issuer-identity policy: the certificate OIDC issuer must equal
`https://token.actions.githubusercontent.com`.

V6. Workflow-identity policy: the expected certificate identity (SAN) must be pinned
before verification, from the expected publisher and release-workflow policy. It is
never taken from the bundle being checked; the bundle's SAN is evidence to compare
against the pinned expected value, not the source of that value. The pinned expected
identity for this artifact is the GitHub Actions release-workflow identity
`https://github.com/trailofbits/rfc8785.py/.github/workflows/release.yml@refs/tags/v0.1.4`,
with repository `trailofbits/rfc8785.py` and ref `refs/tags/v0.1.4`. Only the exact
string format is reconciled against the verifier tool's expected form at execution
time; the expected value itself is fixed in advance. Verification fails closed if the
bundle SAN does not equal the pinned expected identity.

V7. Source-to-artifact correspondence: confirm the verified identity binds the
artifact build to the source tag `v0.1.4` release workflow. Record whether a
reproducible-build re-derivation from source is feasible and, if attempted, its result.

## Tooling (named for the later isolated run; not installed or run now)

The verification will use a maintained Sigstore verifier — for example the `sigstore`
Python tool (`sigstore verify identity --cert-identity <expected> --cert-oidc-issuer
https://token.actions.githubusercontent.com ...`) or `cosign verify-blob` with
`--certificate-identity` and `--certificate-oidc-issuer`. It will run in an isolated
environment outside this repository. The verifier tool, its exact version, and the
Sigstore trusted-root / TUF material used are recorded at execution time (see V0), and
the Fulcio root, Rekor key, and any other transparency-log trust material must come
from that recorded trusted root.

## Acceptance criteria

Provenance is established only if the V0 trusted-root and tooling material is recorded,
V1 through V6 all pass, and V7 is recorded. The Fulcio root, Rekor key, and any other
transparency-log trust material used by V3 and V4 must come from the V0 recorded
trusted root, and the V6 bundle SAN must equal the expected identity pinned in advance.
Any failure fails closed: provenance is not established, REF-014 remains
`Pending review`, and adoption remains blocked. A partial result is recorded as
PARTIAL with explicit named gaps.

## Recording

Results are recorded using the project result categories (PASS, FAIL, PARTIAL,
BLOCKED, NEEDS_RESEARCH) in the provisional integration plan provenance section and a
new research-log entry. REF-014 stays `Pending review` until a separate adoption
decision record is approved.

## Out of scope / remains blocked

Execution of this plan (requires separate approval), license and attribution review,
dependency and maintenance-risk sign-off, dependency adoption, package installation,
requirements or lockfile changes, canonicalizer replacement, numeric-domain
enforcement, golden-vector migration, and real signature verification.

## Next step

Request explicit approval to execute this plan in an isolated environment. On a
passing result, proceed to the license/attribution review record and the
dependency/maintenance-risk sign-off, then a separate adoption decision record.
