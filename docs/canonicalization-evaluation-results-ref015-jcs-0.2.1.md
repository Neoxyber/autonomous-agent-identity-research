# REF-015 Canonicalization Evaluation Results: jcs 0.2.1

## Purpose

This document records isolated evaluation results for REF-015, the `jcs`
Python package / `titusz/jcs`, version `0.2.1`.

REF-015 is evaluated as a comparison candidate for RFC 8785 / JSON
Canonicalization Scheme research. This record is candidate evidence only.

## Current boundary

This record does not adopt a dependency, does not select a candidate, does not
replace the repository canonicalizer, and does not unblock real signature
verification.

Specifically:

- REF-015 was staged and evaluated in `/tmp` only.
- Repository source, tests, requirements, and lockfiles were not changed.
- The candidate is not adopted.
- The candidate is not selected.
- Full RFC 8785/JCS conformance is not claimed.
- Legal compatibility is not claimed.
- Safety or production readiness is not claimed.
- Real signature verification remains blocked.

## Candidate result record

| Field | Value |
| --- | --- |
| Reference | REF-015 |
| Package | `jcs` |
| Source | `titusz/jcs` |
| Version evaluated | `0.2.1` |
| Source pin | `6e4c7b57e027a99bc75eb65d5b2d30203263c07c` |
| Temporary environment | `/tmp/aaid-canonicalization-eval-jcs/venv` |
| Runtime dependency surface | No third-party runtime dependencies observed |
| Public API observed | `canonicalize`, `ntoj` |
| Function signature observed | `canonicalize(obj, utf8=True)` |
| Output mode used | Default `utf8=True`, bytes output |
| Evaluation script | `/tmp/aaid-canonicalization-eval-jcs/compare_ref015_vectors.py` |
| Captured output | `/tmp/aaid-canonicalization-eval-jcs/observed-output-ref015-comparison.txt` |

## Source and declared license check

The REF-015 package was installed only in the temporary `/tmp` environment.
Observed package metadata reported `jcs==0.2.1`, home page
`https://github.com/titusz/jcs`, and declared license `Apache-2.0`.

The pinned source tree did not contain a standalone root `LICENSE`,
`LICENSE.txt`, or `COPYING` file. The source-side declaration observed in
`pyproject.toml` was `license = "Apache-2.0"`, with
`version = "0.2.1"` and `python = ">=3.6.2"`.

This is a source identity and declared-license signal only. It does not verify
legal compatibility, attribution completeness, package provenance, or adoption
suitability.

## Evaluation summary

The isolated evaluation exercised 31 checks:

| Group | PASS | NEEDS_RESEARCH | FAIL | BLOCKED |
| --- | ---: | ---: | ---: | ---: |
| Exact-output checks | 10 | 0 | 0 | 0 |
| Property checks | 5 | 0 | 0 | 0 |
| Rejection checks | 4 | 0 | 0 | 0 |
| Deferred checks | 0 | 6 | 0 | 0 |
| REF-016 reference vectors | 6 | 0 | 0 | 0 |
| Total | 25 | 6 | 0 | 0 |

The run recorded 25 `PASS` checks and 6 `NEEDS_RESEARCH` checks, with no
`FAIL` or `BLOCKED` results.

## Exact-output and property coverage

The exact-output checks covered the recorded known-answer vector, `1e16`,
UTF-16 non-BMP key ordering, empty object, empty array, object key ordering,
nested object ordering, array order preservation, booleans/null, and zero
integer serialization.

The property checks covered control-character escaping, Unicode/non-ASCII
output, bounded depth, bounded size, and repeated deterministic output.

The rejection checks covered non-finite numbers, non-string object keys, `set`,
and `decimal.Decimal`.

## REF-016 vector comparison

The evaluation compared REF-015 output against staged REF-016
`cyberphone/json-canonicalization` vectors pinned at
`19d51d7fe467d4706a3ff08adf8a748f29fc21e0`.

| Vector | Byte output | Hex output | Result |
| --- | --- | --- | --- |
| `arrays` | Match | Match | PASS |
| `french` | Match | Match | PASS |
| `structures` | Match | Match | PASS |
| `unicode` | Match | Match | PASS |
| `values` | Match | Match | PASS |
| `weird` | Match | Match | PASS |

REF-015 is a port of `cyberphone/json-canonicalization`, the same lineage as
the REF-016 vectors. Therefore, REF-016 agreement is port-fidelity evidence and
not fully independent corroboration.

## Deferred items

The following items remain `NEEDS_RESEARCH`:

- Negative zero behavior.
- Standalone small decimal and exponent-number forms.
- Large exponent-number behavior.
- Oversized integer-domain behavior.
- Duplicate-key parse-layer policy.
- Broader RFC 8785/JCS conformance.

These deferred items are not failures in this record. They remain separate
review tasks before any adoption or verifier change can be discussed.

## Environment record

- Python: 3.12.3.
- Platform: Linux WSL2.
- Temporary environment path: `/tmp/aaid-canonicalization-eval-jcs/venv`.
- Installation command: `python -m pip install "jcs==0.2.1"` in the temporary
  environment only.
- `pip freeze`: `jcs==0.2.1`.
- Network use during setup: yes, for package installation and source metadata
  inspection.
- Network use during evaluation: none.
- Repository files changed by evaluation: none.
- Temporary files retained under `/tmp` for review.

## Non-goals

This record does not cover:

- Dependency adoption.
- Candidate selection.
- Canonicalizer replacement.
- Build provenance verification.
- Legal compatibility review.
- Full RFC 8785/JCS conformance.
- Full I-JSON validation.
- Broad ES6 number-vector coverage.
- Real signature verification.
- Post-quantum signing.
- Issuer trust.
- Revocation enforcement.
- Policy, gateway, audit, cloud, or deployment work.

## Next step

The next step is to compare REF-014 and REF-015 evidence side by side and decide
whether a separate bounded number-serialization reference-vector gate is needed.
Any adoption decision remains separate and requires explicit approval.
