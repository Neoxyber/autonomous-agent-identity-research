# Canonicalization Evaluation Results — REF-014 (rfc8785 0.1.4)

## Purpose

This document records the results of one isolated canonicalization candidate
evaluation, following the structure defined in
`docs/canonicalization-evaluation-results-template.md`. It captures observed
evidence from a temporary environment outside the repository. It does not select
or adopt the candidate and does not change the verifier.

## Current boundary

This evaluation was performed in isolation and does not change the repository
state. Specifically:

- The package was installed and executed only in a temporary virtual environment
  outside the repository.
- No repository dependency was adopted.
- No candidate is selected.
- No candidate is verified.
- No canonicalizer is replaced.
- No full RFC 8785/JCS compatibility or conformance is claimed for the candidate
  or for the current helper.
- No source, test, spec, evidence, reference, or requirements file was changed by
  this evaluation.
- The candidate was not integrated into the verifier.
- Real signature verification remains blocked, and the verifier remains
  fail-closed.

The candidate remains Pending review until checked against the original
publisher or official source.

## Result status values

Each result uses one of: PASS, FAIL, PARTIAL, BLOCKED, NEEDS_RESEARCH.

PASS does not mean adoption and does not mean full RFC 8785/JCS conformance. A
PASS records only that the candidate matched the stated expected bytes for the
specific tested vector in the isolated environment.

## Candidate result record

- Candidate reference ID: REF-014
- Candidate name: rfc8785 / trailofbits/rfc8785.py
- Candidate role: primary evaluation candidate (not selected)
- Version or commit tested: 0.1.4
- Source checked: Python package index distribution `rfc8785==0.1.4` (publisher
  Trail of Bits per package metadata); original source and license not yet
  checked against the publisher (Pending review)
- Evaluation date: 2026-05-31
- Evaluator: local operator, isolated temporary environment
- Python version: 3.12.3
- Operating system / environment: Linux 5.15.167.4-microsoft-standard-WSL2 x86_64
- Isolated environment method: temporary virtual environment at
  `/tmp/aaid-canonicalization-eval-rfc8785/venv`, outside the repository
- Install method: `python -m pip install "rfc8785==0.1.4"` into the temporary
  venv only
- Dependency count or dependency tree summary: no runtime dependencies
  (`Requires:` empty); the temporary venv contained only `pip 24.0` and
  `rfc8785 0.1.4`
- License review status: license metadata was empty in the installed
  distribution; not verified from the original source (Pending review)
- Maintenance review status: pre-1.0 release (0.1.4); maintenance not assessed
  (Pending review)
- Overall result: on the exercised checks, 5 PASS and 1 NEEDS_RESEARCH; several
  template checks were not exercised in this run. Observations only; not adoption
  and not conformance.
- Summary: For the small inline vector set tested, the candidate produced bytes
  matching the recorded expected values for the known-answer vector, the `1e16`
  number-serialization case, and the UTF-16 non-BMP key-ordering case, and it
  rejected non-finite numbers. The minimal passport-like payload produced
  deterministic, valid JSON across repeated runs. Duplicate-key handling was not
  exercised through the candidate because it is a parse-layer concern.
- Risks: narrow vector coverage; empty license metadata; pre-1.0 version;
  non-finite rejection surfaced an internal exception path
  (`rfc8785._impl.FloatDomainError`).
- Open questions: license and original source verification; behavior on broader
  and adversarial inputs; public exception contract; output stability across
  versions.
- Recommended next review step: verify license and source from the publisher,
  then exercise the broader vector set (cyberphone vectors, malformed inputs,
  empty object/array, size/depth limits, full I-JSON constraints) before any
  adoption discussion.

## Source and declared license check

The source identity and declared license for REF-014 were checked from official
package and source pages. The PyPI package page shows package `rfc8785` version
`0.1.4`, released on 2024-09-27, with Trail of Bits as the owner/author signal,
Python `>=3.8`, Development Status `4 - Beta`, and an Apache Software License
classifier. The GitHub repository page for `trailofbits/rfc8785.py` shows the
same project identity, the `v0.1.4` latest release, the project documentation
location, and an Apache-2.0 license.

This check covers source identity and declared license only. It does not verify
build provenance, legal compatibility, candidate behavior, full RFC 8785/JCS
conformance, adoption suitability, or safety. The dependency is not adopted, the
candidate is not selected, and real signature verification remains blocked.

## Vector result table

| Check | Input source | Expected behavior | Observed behavior | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| RFC 8785 known-answer vector | Inline known-answer vector (copied read-only from the repository test) | Match the recorded known-answer byte output | Output identical to the expected bytes | PASS | Incidentally exercised recursive object sorting, array order, booleans/null, control-character escaping, and non-ASCII output |
| cyberphone reference vectors | cyberphone reference vectors | Match the reference vector output | Not exercised in this run | NEEDS_RESEARCH | No external vectors downloaded in this step |
| Number serialization including 1e16 | Inline boundary vector | Confirm the serialization form for the `1e16` case | `{"n":10000000000000000}` (positional form) | PASS | Matched the expected positional form recorded for this vector; not a conformance claim |
| UTF-16 non-BMP key ordering | Inline boundary vector (U+E000 and U+10000) | Confirm object member key ordering for non-BMP names | Non-BMP key ordered first, matching the recorded UTF-16 code-unit order | PASS | Single edge-case vector; not a conformance claim |
| Non-finite number rejection | Inline boundary vector | Reject `NaN`, `Infinity`, and `-Infinity` | Each raised `rfc8785._impl.FloatDomainError` | PASS | Internal exception path observed; public contract not confirmed |
| Duplicate-key strategy | Parse-layer concern | Apply a defined duplicate object member key strategy | Not exercised through the candidate | NEEDS_RESEARCH | Parse-layer concern, out of candidate canonicalization scope |
| Minimal passport vector | Inline synthetic passport-like payload | Produce deterministic output for the minimal payload | Deterministic, sorted-key, valid JSON across two runs | PASS | Synthetic inline payload; not the repository schema example |
| Malformed input behavior | Malformed JSON / input | Fail explicitly without silent fallback | Not exercised in this run | NEEDS_RESEARCH | Deferred to broader evaluation |
| Empty object | Edge-case input | Produce defined output for an empty object | Not exercised in this run | NEEDS_RESEARCH | Deferred to broader evaluation |
| Empty array | Edge-case input | Produce defined output for an empty array | Not exercised in this run | NEEDS_RESEARCH | Deferred to broader evaluation |
| Nested object ordering | Structured input | Apply deterministic nested object member ordering | Not asserted as a standalone check | NEEDS_RESEARCH | Incidentally exercised by the known-answer vector |
| Array order preservation | Structured input | Preserve array element order | Not asserted as a standalone check | NEEDS_RESEARCH | Incidentally exercised by the known-answer vector |
| Size/depth bounded stress case | Bounded stress input | Handle bounded size and depth within defined limits | Not exercised in this run | NEEDS_RESEARCH | Deferred to broader evaluation |


## Broader isolated vector coverage

A broader isolated vector suite was run under
`/tmp/aaid-canonicalization-eval-rfc8785` using `rfc8785==0.1.4`.
The suite used inline vectors only and did not modify repository files. The
captured output was written outside the repository to
`/tmp/aaid-canonicalization-eval-rfc8785/observed-output-broader-vectors.txt`.

Summary:

| Group | PASS | NEEDS_RESEARCH | Notes |
| --- | ---: | ---: | --- |
| Exact-output checks | 10 | 0 | Known-answer vector, `1e16`, UTF-16 non-BMP key ordering, empty object, empty array, object ordering, nested ordering, array order, booleans/null, and zero integer |
| Property checks | 5 | 0 | Control-character escaping, Unicode/non-ASCII output, bounded depth, bounded size, and repeated deterministic output |
| Rejection checks | 4 | 0 | Non-finite numbers, non-string object key, `set`, and `decimal.Decimal` were rejected |
| Deferred checks | 0 | 7 | Negative zero, standalone exponent-number forms, oversized integer-domain behavior, duplicate-key parse-layer policy, cyberphone reference vectors, and broader conformance remain open |

Result:
The broader isolated run recorded 19 `PASS` checks and 7 `NEEDS_RESEARCH`
checks, with no `FAIL`, `PARTIAL`, or `BLOCKED` results. This is broader
candidate evidence only. It does not adopt the dependency, does not select the
candidate, does not verify full RFC 8785/JCS conformance, does not verify legal
compatibility or safety, and does not unblock real signature verification.

Open items:
The deferred checks remain separate work. In particular, duplicate-key handling
belongs to the JSON parse layer, cyberphone reference-vector coverage was not run
in this step, and broader RFC 8785/JCS conformance remains unverified.

## Environment record

- Temporary environment path: `/tmp/aaid-canonicalization-eval-rfc8785`
- Package installation command used: `python -m pip install "rfc8785==0.1.4"`
  (temporary venv only)
- Package version source: Python package index, version 0.1.4 (latest of the
  discovered list: 0.1.4, 0.1.3, 0.1.2, 0.1.1, 0.1.0, 0.0.3, 0.0.2, 0.0.1)
- Network use during setup: yes (version discovery and install)
- Network use during execution: none (all vectors inline)
- Files created outside repository: under `/tmp/aaid-canonicalization-eval-rfc8785`
  (venv, evaluation script, captured output, environment and dependency records)
- Repository files changed: none from the evaluation
- Cleanup status: temporary directory retained for review; removal pending
  explicit instruction

## Review checklist

- [x] Results are reproducible (the evaluation script and the pinned version are
  retained under `/tmp` for re-run).
- [x] The package was evaluated only in isolation.
- [x] No repository dependency files changed.
- [x] No candidate was imported from `src/`.
- [x] No canonicalizer replacement occurred.
- [x] No verifier integration occurred.
- [x] Duplicate-key handling was reviewed separately from canonicalization.
- [x] Non-finite number handling was tested.
- [x] Source identity and declared license were checked against official
  package and source pages; legal compatibility and build provenance remain
  out of scope.
- [x] Risks and unresolved questions were recorded.
- [x] Adoption was not implied by test results.

## Non-goals

This document does not cover:

- Dependency adoption.
- Candidate selection.
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

The next step is to decide whether to run official/reference-vector coverage,
including cyberphone vectors, and then compare REF-015 using the same isolated
evaluation discipline. Any adoption would be a separate step requiring its own
review and explicit approval; this record does not adopt or select the
candidate.
