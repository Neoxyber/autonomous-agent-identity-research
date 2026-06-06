# Isolated Canonicalization Candidate Evaluation Plan

## Purpose

This document defines the planned isolated evaluation process for canonicalization
candidates before any package execution, dependency adoption, or verifier change.

It is a plan only. It does not install, execute, select, or adopt any package.
It builds on `docs/30-canonicalization/canonicalization-candidate-matrix.md` and
`specs/canonicalization-candidate-evaluation.md`, which list the candidates and
define the evaluation framework. Its goal is to describe how a later evaluation
would run safely and what it would record, so that any adoption decision is based
on reviewed evidence rather than assumption.

## Current boundary

This document does not change the current state. Specifically:

- No package is installed.
- No package is executed.
- No dependency is adopted.
- No candidate is selected.
- No candidate is verified.
- No canonicalizer is replaced.
- No full RFC 8785/JCS compatibility is claimed for any candidate or for the
  current helper.
- Real signature verification remains blocked, and the verifier remains
  fail-closed.

All candidate findings remain Pending review until checked against the original
publisher or official source.

## Candidate scope

The candidates are listed by reference ID only. Roles describe how a candidate
could be used in a later evaluation; they do not select or adopt any candidate.

- REF-014 as primary evaluation candidate.
- REF-015 as comparison candidate.
- REF-016 as reference / vector source.
- REF-017 to REF-019 as comparison or exclusion candidates unless a later need
  arises.

Every finding for these references remains Pending review.

## Isolation requirements

A later evaluation must be isolated from the project source and from the
repository's dependency state. The following requirements apply:

- Use a separate temporary virtual environment or container.
- Make no modification to project requirements.
- Add no dependency to the repository.
- Add no imports from candidate packages inside `src/`.
- Do not replace `canonicalize_passport_payload`.
- Do not integrate any candidate into the verifier.
- Make no network calls during test execution unless explicitly approved.
- Use no secrets or credentials.
- Keep evaluation artifacts separate from the project's research and source code.
- Record results only after review, not by assumption.

## Evaluation inputs

The planned evaluation uses the following input categories:

- RFC 8785 known-answer vectors.
- cyberphone reference vectors.
- Current repository boundary vectors.
- The `1e16` number serialization boundary.
- The UTF-16 non-BMP object key ordering boundary.
- Non-finite number rejection (`NaN`, `Infinity`, `-Infinity`).
- The duplicate-key raw JSON parsing boundary.
- A minimal passport payload vector.
- Malformed JSON and malformed input behavior.
- Empty object and empty array.
- Nested object and array ordering.
- Size and depth stress cases, kept bounded and safe.

## Evaluation outputs

Each candidate evaluation must record:

- Candidate reference ID.
- Package or source name.
- Version or commit tested.
- Install method used in isolation.
- Python version.
- Operating system and environment summary.
- Dependency tree or dependency count.
- Test vector results.
- Pass / fail / partial / blocked status per the result categories below.
- Observed failure behavior.
- License and maintenance notes.
- Risks and unresolved questions.
- Recommendation for the next review step.

## Result categories

Each result is recorded using one of the following categories:

- PASS
- FAIL
- PARTIAL
- BLOCKED
- NEEDS_RESEARCH

PASS in isolated evaluation does not mean adoption. Adoption requires a separate
review and explicit approval. A PASS records only that a candidate met the stated
checks in the isolated environment for the inputs tested.

## Proposed evaluation order

This order is a proposal for a later, separate step. It does not authorize
installation, execution, or adoption.

1. Confirm oracle vectors.
2. Prepare an isolated environment.
3. Evaluate REF-014.
4. Evaluate REF-015 as comparison.
5. Use REF-016 as a reference and vector source.
6. Compare outputs against the repository boundary vectors.
7. Record results.
8. Review results before any adoption decision.
9. Keep REF-017 to REF-019 as comparison or exclusion candidates unless a later
   need arises.

## Safety controls

The following controls apply to any later evaluation:

- No automatic package adoption.
- No package execution without explicit approval.
- No dependency lockfile or requirements change.
- No canonicalizer replacement during evaluation.
- No signature verification changes.
- No policy, revocation, gateway, cloud, or deployment work.
- All results treated as evidence, not as selection.

## Non-goals

This document does not cover:

- Dependency adoption.
- Package installation in this step.
- Package execution in this step.
- Real signature verification.
- Post-quantum signing.
- Issuer trust.
- Revocation enforcement.
- Policy engine work.
- Gateway work.
- Cloud or deployment work.
- Production readiness.
- Legal or compliance claims.

## Next step

The next step after this plan is to decide whether to run an isolated evaluation
with explicit approval. That decision is a separate step and is not dependency
adoption.
