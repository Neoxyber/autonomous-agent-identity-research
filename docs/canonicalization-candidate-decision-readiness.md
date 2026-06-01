# Canonicalization Candidate Research Assessment

## Purpose

This document summarizes the current research evidence for RFC 8785 / JSON
Canonicalization Scheme candidate selection.

It asks whether the repository has enough evidence to move from candidate
evaluation into a reviewed candidate decision record. It does not adopt a
dependency, select a candidate, replace the canonicalizer, or unblock real
signature verification.

## Research question

Can the project begin drafting a canonicalization candidate decision record, or
is more candidate testing required before decision planning is useful?

The question is limited to decision readiness. It is not a production-readiness,
legal-readiness, dependency-adoption, or signature-verification question.

## Method

The assessment is based on repository evidence collected through isolated,
approval-gated evaluation steps:

- candidate references and comparison matrix;
- isolated REF-014 evaluation;
- isolated REF-015 evaluation;
- REF-016 reference-vector comparison;
- side-by-side REF-014 / REF-015 comparison;
- bounded RFC 8785 / ECMA-262 number-serialization gate;
- duplicate-key parse-layer and payload-domain boundary review.

The evaluations were kept outside the repository runtime environment unless a
separate documentation record was explicitly committed. Candidate packages were
not added to project requirements, and no verifier behavior was changed.

## Evidence summary

| Evidence area | Current finding |
| --- | --- |
| REF-014 behavior | Strong isolated evidence across known-answer, broader, REF-016, and number gates |
| REF-015 behavior | Useful comparison evidence, including REF-016 and number gates |
| REF-016 vectors | Useful reference vectors, but REF-015 shares cyberphone lineage |
| Number serialization | Bounded gate completed with no FAIL results |
| Duplicate keys | Raw JSON parser rejects duplicate member names and has focused tests |
| Numeric payload domain | Current schema has no `number` or `integer` typed fields |
| Non-finite values | Current helper fails closed through `allow_nan=False` |
| Signature verification | Still blocked |
| Dependency adoption | Not performed |

## Candidate comparison finding

REF-014 currently has the stronger research position for provisional integration
planning.

The reasons are:

- REF-014 is independent from the REF-016 cyberphone vector lineage.
- REF-014 matched staged REF-016 vectors in isolated comparison.
- REF-014 matched the bounded number oracle for asserted in-domain rows.
- REF-014 fails closed on values beyond its safe-integer domain.
- REF-014 has a clearer source and declared-license signal than REF-015.

REF-015 remains useful as comparison evidence and as a cyberphone-lineage
cross-check. Its REF-016 agreement is less independent because it shares
cyberphone lineage, and its unsafe-integer behavior remains an input-domain
research concern.

## Integer-domain finding

The bounded number gate produced two REF-014 `BLOCKED` results for `2**53` and
`2**53 + 1`. These are not ordinary output mismatches. They show that REF-014
raises `IntegerDomainError` outside its safe-integer domain.

This fail-closed behavior is relevant to security review. It supports treating
REF-014 as stricter on ambiguous numeric domains, while still requiring a clear
payload-domain policy before adoption.

## Parse-layer and payload-domain finding

Duplicate JSON object member names are a raw JSON text concern. The repository
already includes a parser helper that rejects duplicate member names before
normal parsing collapses them into mappings.

The current passport schema does not expose numeric typed fields, which reduces
the current profile's exposure to unsafe integer and ambiguous number-domain
behavior. Future schema versions should not add numeric payload fields without a
separate numeric-domain policy.

## Readiness assessment

The current evidence is sufficient to draft a candidate decision record for
review.

The appropriate decision-record outcome is not adoption. The appropriate outcome
is:

`REF-014 is recommended for provisional integration planning; no dependency
adoption yet.`

This means the next record may identify REF-014 as the leading candidate for
planning, while keeping all adoption, provenance, legal, and verifier-integration
blockers active.

## Remaining blockers before adoption

Before dependency adoption or canonicalizer replacement, the project still
requires:

- explicit approval of a candidate decision record;
- package artifact and build provenance review;
- legal compatibility and attribution review;
- maintenance and vulnerability-risk review;
- verifier entry-point policy for raw JSON versus parsed mappings;
- duplicate-key rejection before canonicalization when raw JSON is accepted;
- schema validation before canonicalization;
- numeric-domain policy for future payload fields;
- implementation tests before runtime behavior changes;
- continued blocking of real signature verification until integration is
  complete.

## Research limitations

This assessment does not establish full RFC 8785/JCS conformance, legal
compatibility, production readiness, package provenance, long-term maintenance
suitability, or post-quantum signature readiness.

## Current research recommendation

Use this assessment as the current canonicalization decision-readiness record.
REF-014 is the leading candidate for provisional integration planning only.
REF-015 remains comparison evidence.

A separate adoption decision record should wait until the remaining provenance,
legal, dependency-risk, and verifier-boundary blockers are resolved.

This assessment does not authorize requirements changes, canonicalizer
replacement, verifier changes, Pending review status changes, real signature
verification, or post-quantum signing work.

## Next step

Prepare a REF-014 provisional integration plan. The plan should define required
tests, provenance checks, legal/attribution checks, dependency-risk checks, and
verifier-boundary changes before any adoption proposal.
