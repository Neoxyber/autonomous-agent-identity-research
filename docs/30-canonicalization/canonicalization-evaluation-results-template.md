# Canonicalization Evaluation Results Template

## Purpose

This template defines how isolated canonicalization candidate evaluation results
will be recorded later. It standardizes the fields, tables, and checklists so
that any future evaluation produces comparable, reviewable evidence.

It records no live evaluation results in this step. Every value below is a
placeholder. It builds on `docs/30-canonicalization/canonicalization-candidate-matrix.md` and
`docs/30-canonicalization/canonicalization-isolated-evaluation-plan.md`, which list the candidates
and define the planned isolated process.

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

All candidate findings recorded with this template remain Pending review until
checked against the original publisher or official source.

## Result status values

Each result is recorded using one of the following status values:

- PASS
- FAIL
- PARTIAL
- BLOCKED
- NEEDS_RESEARCH

PASS does not mean adoption. Adoption requires a separate review and explicit
approval. A PASS records only that a candidate met the stated checks in the
isolated environment for the inputs tested.

## Candidate result record

One record is completed per candidate. All values are placeholders until a later,
approved evaluation fills them in.

- Candidate reference ID: `TBD`
- Candidate name: `TBD`
- Candidate role: `TBD`
- Version or commit tested: `TBD`
- Source checked: `TBD`
- Evaluation date: `TBD`
- Evaluator: `TBD`
- Python version: `TBD`
- Operating system / environment: `TBD`
- Isolated environment method: `TBD`
- Install method: `TBD`
- Dependency count or dependency tree summary: `TBD`
- License review status: `TBD`
- Maintenance review status: `TBD`
- Overall result: `TBD`
- Summary: `TBD`
- Risks: `TBD`
- Open questions: `TBD`
- Recommended next review step: `TBD`

## Vector result table

One table is completed per candidate. Observed behavior and result values are
placeholders until a later, approved evaluation fills them in.

| Check | Input source | Expected behavior | Observed behavior | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| RFC 8785 known-answer vector | RFC 8785 known-answer vector | Match the known-answer byte output | `TBD` | `TBD` | `TBD` |
| cyberphone reference vectors | cyberphone reference vectors | Match the reference vector output | `TBD` | `TBD` | `TBD` |
| Number serialization including 1e16 | Repository boundary vector | Confirm the serialization form for the `1e16` case | `TBD` | `TBD` | `TBD` |
| UTF-16 non-BMP key ordering | Repository boundary vector | Confirm object member key ordering for non-BMP names | `TBD` | `TBD` | `TBD` |
| Non-finite number rejection | Repository boundary vector | Reject `NaN`, `Infinity`, and `-Infinity` | `TBD` | `TBD` | `TBD` |
| Duplicate-key strategy | Repository boundary vector | Apply a defined duplicate object member key strategy | `TBD` | `TBD` | `TBD` |
| Minimal passport vector | Minimal passport payload vector | Produce deterministic output for the minimal payload | `TBD` | `TBD` | `TBD` |
| Malformed input behavior | Malformed JSON / input | Fail explicitly without silent fallback | `TBD` | `TBD` | `TBD` |
| Empty object | Edge-case input | Produce defined output for an empty object | `TBD` | `TBD` | `TBD` |
| Empty array | Edge-case input | Produce defined output for an empty array | `TBD` | `TBD` | `TBD` |
| Nested object ordering | Structured input | Apply deterministic nested object member ordering | `TBD` | `TBD` | `TBD` |
| Array order preservation | Structured input | Preserve array element order | `TBD` | `TBD` | `TBD` |
| Size/depth bounded stress case | Bounded stress input | Handle bounded size and depth within defined limits | `TBD` | `TBD` | `TBD` |

## Environment record

One environment record is completed per evaluation run. All values are
placeholders. No environment is created in this step.

- Temporary environment path: `TBD`
- Package installation command used: `TBD`
- Package version source: `TBD`
- Network use during setup: `TBD`
- Network use during execution: `TBD`
- Files created outside repository: `TBD`
- Repository files changed: `TBD`
- Cleanup status: `TBD`

## Review checklist

Before any result is treated as evidence, confirm:

- [ ] Results are reproducible.
- [ ] The package was evaluated only in isolation.
- [ ] No repository dependency files changed.
- [ ] No candidate was imported from `src/`.
- [ ] No canonicalizer replacement occurred.
- [ ] No verifier integration occurred.
- [ ] Duplicate-key handling was reviewed separately from canonicalization.
- [ ] Non-finite number handling was tested.
- [ ] License and maintenance status were reviewed.
- [ ] Risks and unresolved questions were recorded.
- [ ] Adoption was not implied by test results.

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

The next step after this template is to decide whether to run an isolated
evaluation with explicit approval. That decision is a separate step and is not
dependency adoption.
