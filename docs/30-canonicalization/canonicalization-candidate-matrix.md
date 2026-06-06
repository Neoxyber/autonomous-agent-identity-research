# Canonicalization Candidate Matrix

## Purpose

This document compares candidate canonicalization sources before any isolated
evaluation and before any dependency is adopted.

It is a planning artifact. It does not install, execute, evaluate, select, or
endorse any candidate. It records why each candidate is listed, what is already
known about it, and how it could be used in a later, separate evaluation step.
It builds on `specs/canonicalization-resolution.md` and
`specs/canonicalization-candidate-evaluation.md`, which define the resolution
options and the evaluation framework.

## Current boundary

This document does not change the current state. Specifically:

- No dependency is adopted.
- No candidate is selected.
- No candidate is verified.
- No full RFC 8785/JCS compatibility is claimed for any candidate or for the
  current helper.
- Real signature verification remains blocked, and the verifier remains
  fail-closed.

All candidate findings below are recorded as Pending review until checked
against the original publisher or official source.

## Evaluation context

The following evidence already exists in the repository and frames the
comparison. It is summarized here, not extended:

- An RFC 8785/JCS known-answer vector is exercised as an external conformance
  reference point.
- Non-finite numbers (`NaN`, `Infinity`, `-Infinity`) are rejected.
- Duplicate object member keys are rejected at a raw JSON parsing boundary,
  before normal parsing would collapse them.
- A UTF-16 ordering boundary is documented: the current helper's code-point
  ordering differs from JCS UTF-16 code-unit ordering for non-BMP object member
  names.
- A number serialization boundary is documented: for the selected value `1e16`,
  the current helper emits exponential notation, while the JCS form is
  positional digits.

These items describe known boundaries and limitations. They do not establish
full RFC 8785/JCS compatibility and do not unblock real signature verification.

## Candidate matrix

All entries are Pending review. Roles and priorities describe how a candidate
could be used in a later evaluation; they do not select or adopt any candidate.

| Reference | Role | Initial priority | Reason for inclusion | Known risks | Evaluation use |
| --- | --- | --- | --- | --- | --- |
| REF-014 `rfc8785 / trailofbits/rfc8785.py` | Primary evaluation candidate | High | Targets RFC 8785; maintained source under a recognized publisher (Pending review) | Behavior, dependency surface, and license unconfirmed in this repository (Pending review) | Measure against shared known-answer and boundary vectors in a later isolated step |
| REF-015 `jcs Python package / titusz jcs` | Comparison candidate | Medium | Independent RFC 8785/JCS-oriented implementation usable for differential comparison (Pending review) | Maintenance status, dependency surface, and license unconfirmed (Pending review) | Compare outputs against REF-014 and the reference vectors |
| REF-016 `cyberphone/json-canonicalization` | Reference / vector source | Medium | Widely cited reference implementation and source of test vectors (Pending review) | Used as a vector and reference source, not as an adoption target; vector scope unconfirmed (Pending review) | Provide reference vectors and cross-checks for other candidates |
| REF-017 `canonicaljson` | Comparison / exclusion candidate | Low | Listed to document a non-matching canonicalization target | Reported to target Matrix canonical JSON rather than RFC 8785/JCS (Pending review) | Differential comparison only; not an adoption candidate |
| REF-018 `json-canonical` | Comparison / exclusion candidate | Low | Listed to document a legacy / low-maintenance option | Maintenance level appears low; suitability unconfirmed (Pending review) | Differential comparison only; not an adoption candidate |
| REF-019 `jsoncanon` | Comparison / exclusion candidate | Low | Listed to document an apparently incomplete option | Floating-point support appears incomplete (Pending review) | Differential comparison only; not an adoption candidate |

## Required evaluation checks

A later isolated evaluation should measure each candidate against a shared set of
checks. At minimum:

- RFC 8785 known-answer vectors.
- cyberphone reference vectors.
- Number serialization behavior, including the `1e16` case.
- UTF-16 object member key ordering, including non-BMP names.
- Non-finite number rejection.
- Duplicate object member key strategy.
- A minimal passport vector.
- Malformed input behavior.
- Dependency surface.
- Maintenance and license review.
- Size and depth limits.

These checks define what a later evaluation would record as evidence. This
document does not run them.

## Proposed evaluation order

This order is a proposal for a later, separate step. It does not authorize
installation, execution, or adoption.

1. Build or confirm oracle vectors first.
2. Evaluate REF-014 in an isolated environment.
3. Evaluate REF-015 as comparison.
4. Use REF-016 as a vector and reference source.
5. Keep REF-017 to REF-019 as comparison or exclusion candidates unless a later
   need arises.

## Non-goals

This document does not cover:

- Dependency adoption.
- Package installation.
- Package execution.
- Real signature verification.
- Post-quantum signing.
- Issuer trust.
- Revocation enforcement.
- Policy engine work.
- Gateway work.
- Cloud or deployment work.

## Next step

The next step after this matrix is to design an isolated evaluation plan for the
listed candidates. That plan is a separate step and does not adopt a dependency.
