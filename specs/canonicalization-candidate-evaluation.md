# Canonicalization Candidate Evaluation

## Purpose

This document defines how canonicalization implementations or alternatives will
be evaluated before any of them is adopted.

It is a planning artifact. It does not adopt a dependency, evaluate a specific
package, or change the verifier. It prepares the evaluation framework that a
later step will use.

## Scope

This framework applies to the canonical byte form used for hashing and, later,
for trusted signature verification of the passport payload.

It covers candidate selection, acceptance criteria, the compatibility test plan,
and the evaluation process. It does not cover signing algorithms, issuer trust,
revocation, or policy, which are separate concerns.

The chosen canonical form should remain signature-algorithm-agnostic, so future
classical or post-quantum signature changes do not require redefining the
canonical payload.

Real signature verification is currently blocked because it is not implemented
yet, and the verifier remains fail-closed. It stays blocked until a
canonicalization path is evaluated, selected, and reviewed.

## Candidate categories

1. RFC 8785 / JSON Canonicalization Scheme-compatible implementations, as the
   preferred long-term direction.
2. The current constrained-profile helper, kept as a fallback path for the
   current research passport profile only.
3. Alternative deterministic encodings, such as deterministic CBOR, considered
   as research comparison only and not as a first-version target.

## Acceptance criteria

A candidate is acceptable for further evaluation only if it has:

1. A license suitable for open research use.
2. A maintained source or a stable reference implementation.
3. A small dependency surface.
4. Deterministic byte output for equal inputs.
5. Explicit, documented failure behaviour.
6. No silent fallback on invalid inputs.
7. Compatibility with the passport payload boundary, covering the passport
   object only and excluding detached proof metadata.
8. Reproducible tests that another reviewer can run.

## Required compatibility tests

Each candidate is measured against a shared test plan that covers:

1. RFC 8785 / JCS known answer vectors.
2. I-JSON input constraints.
3. Duplicate object member key rejection or explicit parser-level handling.
4. Number serialization behaviour.
5. String escaping and control characters.
6. Unicode and UTF-16 object member ordering.
7. Nested object member ordering.
8. Array order preservation.
9. Booleans and null.
10. A minimal passport vector.
11. Cross-implementation differential comparison.
12. Malformed input failure behaviour.
13. Large and deeply nested input limits.
14. Empty object and empty array edge cases.

## Evaluation process

1. Record candidate references as under review in docs/references.md in a later
   step.
2. Create the compatibility tests before adopting any dependency.
3. Run each candidate against the shared test plan.
4. Record pass and fail results as evidence.
5. Compare candidates against the acceptance criteria and the test results.
6. Adopt a candidate only after user review and explicit approval.

## Non-goals

This step does not:

1. Adopt a dependency.
2. Evaluate a specific package.
3. Implement real signature verification.
4. Rename the declared canonicalization scheme.
5. Enforce a constrained passport profile.
6. Add post-quantum signing.
7. Add cloud or network work.

## Next step

Design the compatibility tests described above before any candidate is adopted.
