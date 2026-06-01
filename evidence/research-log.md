# Research Log

## Purpose

This file records the chronological progress of the autonomous agent identity research project.

The research log is used to track meaningful project steps, not every small edit. It records what changed, why it changed, which files were affected, and what the next step is.

Detailed design decisions will be recorded separately in Research Decision Records when the project reaches that stage. Empirical tests and benchmark results will be recorded separately in Empirical Testing Logs when implementation and testing begin.

## Archive note

Entries 001 to 021 are preserved unchanged in evidence/research-log-archive-001.md. This active log continues the same entry numbering and format from Entry 022 onward.

## Entry 022

Date: 2026-05-30

Type: Research planning

Summary: Updated the research roadmap.

Files:
Updated `ROADMAP.md`; updated this evidence log.

Result:
The roadmap now defines the project as standards-aligned autonomous agent identity research and orders the next work around standards positioning, canonicalization closure, signature verification, issuer trust, revocation, permission evaluation, human oversight, audit evidence, post-quantum research, and a local dummy demo.

Tests:
158 tests passed.

Not implemented:
source code changes, schema changes, dependency adoption, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Align the README with the current research stage.

## Entry 023

Date: 2026-05-30

Type: Research documentation

Summary: Aligned README with the current research stage.

Files:
Updated `README.md`; updated this evidence log.

Result:
The README now describes the repository as standards-aligned autonomous agent identity research and reflects the current state of the project, including the existing research models, schema, reference implementation foundation, fail-closed verifier pipeline, and tests. It avoids production-readiness, legal-compliance, standards-compliance, and replacement-of-standards claims.

Tests:
158 tests passed.

Not implemented:
source code changes, schema changes, dependency adoption, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Add a concise standards-positioning map.

## Entry 024

Date: 2026-05-30

Type: Research positioning

Summary: Added standards positioning map.

Files:
Created `docs/standards-positioning.md`; updated this evidence log.

Result:
The new document positions the agent passport as a standards-aligned research envelope rather than a replacement for existing identity standards. It maps project concepts to related external areas such as verifiable credentials, decentralized identifiers, workload identity, delegated authority, agentic identity and access management, agent security risks, and post-quantum signatures while preserving clear non-claims and open research questions.

Tests:
158 tests passed.

Not implemented:
source code changes, schema changes, dependency adoption, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Close canonicalization through external conformance tests.

## Entry 025

Date: 2026-05-31

Type: Canonicalization conformance

Summary: Added RFC 8785 target vector test.

Files:
Created `tests/test_passport_canonicalization_rfc8785_vectors.py`; updated this evidence log.

Result:
The new test adds an external RFC 8785/JCS known-answer vector as the first canonicalization conformance step. It records external conformance evidence before dependency adoption. This does not adopt a canonicalization dependency, does not claim full RFC 8785/JCS compatibility, and does not unblock real signature verification by itself.

Tests:
159 tests passed.

Not implemented:
dependency adoption, full RFC 8785/JCS compatibility, duplicate-key rejection, full I-JSON validation, canonicalization package evaluation, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Add canonicalization failure-boundary tests before evaluating or adopting a canonicalization dependency.

## Entry 026

Date: 2026-05-31

Type: Canonicalization failure boundary

Summary: Rejected non-finite canonicalization numbers.

Files:
Updated `src/aaid/canonicalization.py`; updated `tests/test_passport_canonicalization_rfc8785_vectors.py`; updated this evidence log.

Result:
The canonicalization helper now rejects `NaN`, `Infinity`, and `-Infinity` by using the standard JSON serializer's fail-closed behavior for non-finite numbers. The tests add a parametrized boundary check for all three values. This closes one JCS-related failure boundary before dependency adoption while preserving the existing research-helper boundary and avoiding any full RFC 8785/JCS compatibility claim.

Tests:
162 tests passed.

Not implemented:
dependency adoption, full RFC 8785/JCS compatibility, duplicate-key rejection, full I-JSON validation, canonicalization package evaluation, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Study and test the duplicate-key parsing boundary before evaluating or adopting a canonicalization dependency.

## Entry 027

Date: 2026-05-31

Type: Canonicalization parsing boundary

Summary: Added duplicate-key JSON parsing boundary.

Files:
Created `src/aaid/json_parsing.py`; created `tests/test_passport_json_parsing.py`; updated this evidence log.

Result:
The new raw JSON parsing helper rejects duplicate JSON object member names before normal parsing collapses them into a Python mapping. The helper uses the Python standard library only and detects duplicate keys in top-level objects, nested objects, and objects inside arrays. This creates a tested parsing boundary before canonicalization input is trusted, while preserving current verifier and canonicalization behavior.

Tests:
168 tests passed.

Not implemented:
verifier integration, canonicalization behavior changes, dependency adoption, full RFC 8785/JCS compatibility, full I-JSON validation, canonicalization package evaluation, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Decide where the duplicate-key parsing boundary should enter the verifier pipeline before evaluating or adopting a canonicalization dependency.

## Entry 028

Date: 2026-05-31

Type: Canonicalization compatibility boundary

Summary: Documented UTF-16 canonicalization ordering boundary.

Files:
Updated `tests/test_passport_canonicalization_rfc8785_vectors.py`; updated this evidence log.

Result:
The new boundary test records a JCS key-ordering edge case where the current helper's Python code-point ordering differs from RFC 8785/JCS UTF-16 code-unit ordering for non-BMP object member names. This documents a concrete compatibility limitation before dependency adoption. It does not change canonicalization behavior, does not claim full RFC 8785/JCS compatibility, and does not unblock real signature verification.

Tests:
169 tests passed.

Not implemented:
canonicalization behavior changes, dependency adoption, full RFC 8785/JCS compatibility, full I-JSON validation, canonicalization package evaluation, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Continue canonicalization closure by adding number-serialization boundary tests or by preparing a candidate implementation evaluation step.

## Entry 029

Date: 2026-05-31

Type: Canonicalization compatibility boundary

Summary: Documented number serialization boundary.

Files:
Updated `tests/test_passport_canonicalization_rfc8785_vectors.py`; updated this evidence log.

Result:
The new boundary test records a finite-number serialization edge case where the current helper's Python float serialization differs from RFC 8785/JCS ECMAScript number serialization. The test uses `1e16` as a deliberately selected float value: the current helper emits exponential notation, while the JCS expected form is positional digits. This documents another concrete compatibility limitation before dependency adoption. It does not change canonicalization behavior, does not claim full RFC 8785/JCS compatibility, and does not unblock real signature verification.

Tests:
170 tests passed.

Not implemented:
canonicalization behavior changes, dependency adoption, full RFC 8785/JCS compatibility, full I-JSON validation, canonicalization package evaluation, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Begin candidate RFC 8785/JCS implementation evaluation before adopting any canonicalization dependency.

## Entry 030

Date: 2026-05-31

Type: Reference management

Summary: Added RFC 8785 reference entry.

Files:
Updated `docs/references.md`; updated this evidence log.

Result:
The central reference register now includes `REF-013` for RFC 8785 JSON Canonicalization Scheme. The reference is marked `Pending review`, consistent with the repository policy that new references remain under review until checked against the original publisher or official source. No implementation file was changed, and no RFC 8785/JCS compatibility claim was added.

Tests:
170 tests passed.

Not implemented:
reference verification, canonicalization behavior changes, dependency adoption, full RFC 8785/JCS compatibility, full I-JSON validation, canonicalization package evaluation, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Begin candidate RFC 8785/JCS implementation evaluation before adopting any canonicalization dependency.

## Entry 031

Date: 2026-05-31

Type: Reference management

Summary: Added canonicalization candidate references.

Files:
Updated `docs/references.md`; updated this evidence log.

Result:
The central reference register now includes pending-review references for candidate RFC 8785/JCS implementations and comparison sources. The additions include `rfc8785`, `jcs`, the `cyberphone/json-canonicalization` reference and vector source, and excluded or lower-priority comparison candidates. All new entries remain marked `Pending review`. No dependency was adopted, no package was evaluated in the repository, and no candidate was selected.

Tests:
170 tests passed.

Not implemented:
reference verification, package installation, dependency adoption, canonicalization behavior changes, full RFC 8785/JCS compatibility, full I-JSON validation, canonicalization package evaluation results, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Create a candidate canonicalization evaluation matrix before running any isolated package evaluation.

## Entry 032

Date: 2026-05-31

Type: Canonicalization evaluation planning

Summary: Added canonicalization candidate matrix.

Files:
Created `docs/canonicalization-candidate-matrix.md`; updated this evidence log.

Result:
The new matrix compares pending-review canonicalization candidates and reference sources before isolated evaluation or dependency adoption. It records candidate roles, initial evaluation priority, reasons for inclusion, known risks, evaluation use, required evaluation checks, proposed evaluation order, non-goals, and the next step. The document preserves the current boundary: no dependency is adopted, no candidate is selected or verified, no full RFC 8785/JCS compatibility is claimed, and real signature verification remains blocked.

Tests:
170 tests passed.

Not implemented:
package installation, package execution, dependency adoption, candidate selection, candidate verification, canonicalizer replacement, full RFC 8785/JCS compatibility, full I-JSON validation, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Create an isolated canonicalization candidate evaluation plan before running or installing candidate packages.

## Entry 033

Date: 2026-05-31

Type: Canonicalization evaluation planning

Summary: Added isolated canonicalization evaluation plan.

Files:
Created `docs/canonicalization-isolated-evaluation-plan.md`; updated this evidence log.

Result:
The new plan defines how canonicalization candidates should be evaluated in an isolated environment before package execution, dependency adoption, or verifier changes. It records candidate scope, isolation requirements, evaluation inputs, evaluation outputs, result categories, proposed evaluation order, safety controls, non-goals, and the next step. The plan preserves the current boundary: no package is installed or executed, no dependency is adopted, no candidate is selected or verified, no canonicalizer is replaced, no full RFC 8785/JCS compatibility is claimed, and real signature verification remains blocked.

Tests:
170 tests passed.

Not implemented:
package installation, package execution, dependency adoption, candidate selection, candidate verification, canonicalizer replacement, full RFC 8785/JCS compatibility, full I-JSON validation, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Decide whether to run an isolated canonicalization candidate evaluation with explicit approval, or first create an evaluation results template.

## Entry 034

Date: 2026-05-31

Type: Canonicalization evaluation planning

Summary: Added canonicalization evaluation results template.

Files:
Created `docs/canonicalization-evaluation-results-template.md`; updated this evidence log.

Result:
The new template defines how future isolated canonicalization candidate evaluation results should be recorded. It standardizes candidate records, vector result tables, environment records, result status values, review checklist items, non-goals, and the next step. The template records no live candidate results and preserves the current boundary: no package is installed or executed, no dependency is adopted, no candidate is selected or verified, no canonicalizer is replaced, no full RFC 8785/JCS compatibility is claimed, and real signature verification remains blocked.

Tests:
170 tests passed.

Not implemented:
package installation, package execution, live candidate evaluation results, dependency adoption, candidate selection, candidate verification, canonicalizer replacement, full RFC 8785/JCS compatibility, full I-JSON validation, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Decide whether to run an isolated canonicalization candidate evaluation with explicit approval.

## Entry 035

Date: 2026-05-31

Type: Canonicalization candidate evaluation

Summary: Recorded isolated REF-014 evaluation results.

Files:
Created `docs/canonicalization-evaluation-results-ref014-rfc8785-0.1.4.md`; updated this evidence log.

Result:
The new results document records an isolated evaluation of `REF-014` using `rfc8785==0.1.4` in a temporary environment outside the repository. The candidate passed the exercised small inline checks for the RFC 8785 known-answer vector, `1e16` number serialization, UTF-16 non-BMP key ordering, non-finite number rejection, and a synthetic minimal passport-like payload. Duplicate-key handling remains a separate parse-layer concern and is recorded as `NEEDS_RESEARCH`. The result is evidence only: it does not adopt the dependency, does not select or verify the candidate, does not claim full RFC 8785/JCS conformance, does not replace the canonicalizer, and does not unblock real signature verification.

Tests:
170 tests passed.

Not implemented:
dependency adoption, candidate selection, candidate verification, canonicalizer replacement, full RFC 8785/JCS compatibility, full I-JSON validation, broad cyberphone vector evaluation, malformed input coverage, empty object and array coverage, size/depth stress testing, license verification, maintenance verification, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Verify the candidate license and original source, then decide whether to run broader isolated vector coverage before any adoption discussion.

## Entry 036

Date: 2026-05-31

Type: Reference verification

Summary: Recorded REF-014 source and declared license check.

Files:
Updated `docs/canonicalization-evaluation-results-ref014-rfc8785-0.1.4.md`; updated `docs/references.md`; updated this evidence log.

Result:
The REF-014 evaluation results document now includes a compact source and declared license check based on official package and source pages. The note records that the `rfc8785` package and `trailofbits/rfc8785.py` source identity were checked, that version `0.1.4` and the project documentation location were observed, and that the declared license signals indicate Apache Software License / Apache-2.0. The central reference register keeps REF-014 as `Pending review` while noting that source identity and declared license were checked and that adoption and functional conformance remain unverified. This preserves the boundary: the dependency is not adopted, the candidate is not selected, full RFC 8785/JCS conformance is not claimed, legal compatibility is not claimed, and real signature verification remains blocked.

Tests:
170 tests passed.

Not implemented:
dependency adoption, candidate selection, candidate verification, canonicalizer replacement, build provenance verification, legal compatibility review, full RFC 8785/JCS compatibility, full I-JSON validation, broad cyberphone vector evaluation, malformed input coverage, empty object and array coverage, size/depth stress testing, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Continue broader isolated canonicalization vector testing before any adoption discussion.

## Entry 037

Date: 2026-05-31

Type: Canonicalization candidate evaluation

Summary: Recorded broader isolated REF-014 vector coverage.

Files:
Updated `docs/canonicalization-evaluation-results-ref014-rfc8785-0.1.4.md`; updated this evidence log.

Result:
The REF-014 evaluation results document now records a broader isolated vector suite for `rfc8785==0.1.4`. The suite was created and executed under `/tmp/aaid-canonicalization-eval-rfc8785` using the isolated temporary environment only. The script and captured output remained outside the repository. The broader run recorded 26 checks total: 19 `PASS` checks and 7 `NEEDS_RESEARCH` checks, with no `FAIL`, `PARTIAL`, or `BLOCKED` results. The passing checks covered exact-output vectors, property checks, and rejection checks. Deferred items remain open for negative-zero review, standalone exponent-number forms, oversized integer-domain behavior, duplicate-key parse-layer policy, cyberphone reference vectors, and broader RFC 8785/JCS conformance. This is candidate evidence only: the dependency is not adopted, the candidate is not selected, full RFC 8785/JCS conformance is not claimed, legal compatibility and safety are not claimed, and real signature verification remains blocked.

Tests:
170 tests passed.

Not implemented:
dependency adoption, candidate selection, candidate verification, canonicalizer replacement, build provenance verification, legal compatibility review, full RFC 8785/JCS compatibility, full I-JSON validation, cyberphone reference-vector coverage, REF-015 comparison, malformed input coverage beyond the exercised rejection checks, full size/depth stress testing, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Decide whether to run official/reference-vector coverage, including cyberphone vectors, or compare REF-015 using the same isolated evaluation discipline.

## Entry 038

Date: 2026-05-31

Type: Canonicalization reference-vector evaluation

Summary: Recorded REF-016 reference-vector comparison for REF-014.

Files:
Updated `docs/canonicalization-evaluation-results-ref014-rfc8785-0.1.4.md`; updated this evidence log.

Result:
The REF-014 evaluation results document now records a comparison against staged REF-016 `cyberphone/json-canonicalization` reference vectors. The REF-016 files were staged outside the repository under `/tmp/aaid-canonicalization-eval-rfc8785/ref016-vectors` and pinned to commit `19d51d7fe467d4706a3ff08adf8a748f29fc21e0`. The comparison used `rfc8785==0.1.4` in the isolated temporary environment only. Six staged vectors were compared: `arrays`, `french`, `structures`, `unicode`, `values`, and `weird`. Observed canonical bytes matched both the staged `output/*.json` bytes and normalized `outhex/*.txt` expected hex for all six vectors. The run recorded 6 `PASS` vectors and no `FAIL`, `NEEDS_RESEARCH`, or `BLOCKED` results. No cyberphone implementation code was executed. This is reference-vector evidence only: the dependency is not adopted, the candidate is not selected, full RFC 8785/JCS conformance is not claimed, legal compatibility and safety are not claimed, and real signature verification remains blocked.

Tests:
170 tests passed.

Not implemented:
dependency adoption, candidate selection, candidate verification, canonicalizer replacement, build provenance verification, legal compatibility review, full RFC 8785/JCS compatibility, full I-JSON validation, broad ES6 number-vector coverage, REF-015 comparison, duplicate-key parse-layer policy, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Decide whether to compare REF-015 using the same isolated evaluation discipline, or run a separate bounded number-serialization reference-vector gate.

## Entry 039

Date: 2026-06-01

Type: Canonicalization candidate evaluation

Summary: Recorded REF-015 isolated evaluation results.

Files:
Added `docs/canonicalization-evaluation-results-ref015-jcs-0.2.1.md`; updated `docs/references.md`; updated this evidence log.

Result:
The REF-015 evaluation results document records isolated staging and evaluation of `jcs==0.2.1` under `/tmp/aaid-canonicalization-eval-jcs`. REF-015 was evaluated as a comparison candidate only. The run used the temporary environment, did not modify repository source, tests, requirements, or lockfiles, and did not adopt or select the dependency. The evaluation recorded 31 checks total: 25 `PASS` checks and 6 `NEEDS_RESEARCH` checks, with no `FAIL` or `BLOCKED` results. Exact-output, property, rejection, and staged REF-016 vector checks passed. Deferred items remain open for negative-zero behavior, standalone exponent-number forms, oversized integer-domain behavior, duplicate-key parse-layer policy, and broader RFC 8785/JCS conformance. The REF-016 agreement is port-fidelity evidence because REF-015 shares cyberphone lineage with the REF-016 vectors, not fully independent corroboration. Source identity and declared license signals were checked, but the pinned source tree did not contain a standalone root license file; legal compatibility and attribution completeness remain unverified. The central reference register now points REF-015 to the isolated evaluation results while keeping adoption and full conformance unverified.

Tests:
170 tests passed.

Not implemented:
dependency adoption, candidate selection, candidate verification, canonicalizer replacement, build provenance verification, legal compatibility review, attribution completeness review, full RFC 8785/JCS compatibility, full I-JSON validation, broad ES6 number-vector coverage, bounded number-serialization reference gate, side-by-side REF-014 versus REF-015 decision record, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Compare REF-014 and REF-015 evidence side by side and decide whether a separate bounded number-serialization reference-vector gate is needed before any adoption discussion.

## Entry 040

Date: 2026-06-01

Type: Canonicalization candidate comparison

Summary: Compared REF-014 and REF-015 canonicalization candidate evidence.

Files:
Added `docs/canonicalization-candidate-comparison-ref014-ref015.md`; updated this evidence log.

Result:
The comparison document now records a side-by-side review of the current isolated evidence for REF-014 `rfc8785==0.1.4` and REF-015 `jcs==0.2.1`. REF-014 remains stronger on independence grounds because it is not a cyberphone-lineage port. REF-015 remains useful as differential comparison evidence and as a cyberphone-lineage cross-check, but its agreement with REF-016 vectors is port-fidelity evidence rather than fully independent corroboration. Both candidates remain Pending review. No candidate is adopted or selected, no canonicalizer is replaced, full RFC 8785/JCS conformance is not claimed, legal compatibility is not claimed, and real signature verification remains blocked. The comparison identifies bounded number-serialization reference-vector coverage as the recommended next gate before any adoption discussion.

Tests:
170 tests passed.

Not implemented:
dependency adoption, candidate selection, canonicalizer replacement, build provenance verification, legal compatibility review, attribution completeness review, full RFC 8785/JCS compatibility, full I-JSON validation, bounded number-serialization reference-vector gate, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Plan the bounded number-serialization reference-vector gate, or explicitly defer it with rationale before any adoption discussion.

## Entry 041

Date: 2026-06-01

Type: Canonicalization number-serialization evaluation

Summary: Recorded bounded number-serialization gate for REF-014 and REF-015.

Files:
Added `docs/canonicalization-number-serialization-gate-ref014-ref015.md`; updated this evidence log.

Result:
The number-serialization gate document records a bounded RFC 8785 / ECMA-262 number-token comparison for REF-014 `rfc8785==0.1.4` and REF-015 `jcs==0.2.1`. The oracle table was generated deterministically under `/tmp/aaid-canonicalization-eval-numbers`, validated as strict JSON, and hashed before execution. The oracle SHA-256 was `c0b08f3e3a6c5004cb302228938382973e8606abc5d1bc7d9b698ce8a08e95eb`. The captured output SHA-256 was `7d478f0ab8fcca491c68167ef3d1f8fb8459f2166c301840f549135a81b4cde5`. The run evaluated 14 bounded vectors across 2 candidates, producing 28 candidate results: 25 `PASS`, 2 `BLOCKED`, 1 `NEEDS_RESEARCH`, and 0 `FAIL`. Both candidates matched the asserted RFC 8785 / ECMA-262 number tokens for negative zero, decimal/exponent formatting, threshold values, `1e16`, and `2**53 - 1`. REF-014 blocked `2**53` and `2**53 + 1` with safe-integer domain enforcement. REF-015 emitted `9007199254740992` for `2**53` and observed `9007199254740992` for `2**53 + 1`, leaving the unsafe-integer input-layer behavior as `NEEDS_RESEARCH`. No candidate is adopted or selected, no canonicalizer is replaced, full RFC 8785/JCS conformance is not claimed, legal compatibility is not claimed, and real signature verification remains blocked.

Tests:
170 tests passed.

Not implemented:
dependency adoption, candidate selection, canonicalizer replacement, build provenance verification, legal compatibility review, attribution completeness review, full RFC 8785/JCS compatibility, full I-JSON validation policy, duplicate-key parse-layer policy, package artifact provenance, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Decide whether to write a canonicalization candidate decision record, or run another explicitly bounded gate for duplicate-key parse-layer policy and payload-domain validation before any adoption discussion.

## Entry 042

Date: 2026-06-01

Type: Canonicalization parse and payload-domain review

Summary: Recorded parse-layer and payload-domain boundary gate.

Files:
Added `docs/canonicalization-parse-and-payload-domain-gate.md`; updated this evidence log.

Result:
The parse and payload-domain gate document records the current repository boundary for duplicate-key parsing and numeric payload-domain exposure before any canonicalization candidate adoption decision. The repository already includes `src/aaid/json_parsing.py`, which parses raw JSON text using an `object_pairs_hook` and fails closed on duplicate object member names, including nested objects and objects inside arrays. Focused tests in `tests/test_passport_json_parsing.py` cover valid parsing, top-level duplicate rejection, nested duplicate rejection, duplicate keys inside array objects, sibling object key reuse, and malformed JSON. Schema inspection found no `number` or `integer` typed fields in the current passport schema, reducing current exposure to ambiguous JSON number-domain behavior. The current canonicalization helper also uses `allow_nan=False`, so non-finite numbers fail closed. This is parse-layer and payload-domain evidence only: it does not adopt or select a canonicalization candidate, does not replace the canonicalizer, does not claim full RFC 8785/JCS or full I-JSON conformance, does not claim legal compatibility, and does not unblock real signature verification.

Tests:
170 tests passed.

Not implemented:
dependency adoption, candidate selection, canonicalizer replacement, full RFC 8785/JCS compatibility, full I-JSON conformance, verifier raw-JSON entry point integration, schema-level numeric-domain policy for future numeric fields, unsafe integer rejection policy, build provenance verification, legal compatibility review, attribution completeness review, package artifact provenance, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Decide whether the parse-layer and payload-domain evidence is sufficient to draft a canonicalization candidate decision record, or whether verifier API integration should first require raw JSON parsing through the duplicate-key rejecting helper.

## Entry 043

Date: 2026-06-01

Type: Canonicalization candidate research assessment

Summary: Assessed canonicalization candidate decision readiness.

Files:
Added `docs/canonicalization-candidate-decision-readiness.md`; updated this evidence log.

Result:
The decision-readiness research assessment summarizes the current RFC 8785 / JSON Canonicalization Scheme candidate evidence. It records that the repository has enough evidence to draft a candidate decision record for review, but not enough to adopt a dependency, replace the canonicalizer, or unblock real signature verification. The assessment identifies REF-014 `rfc8785==0.1.4` as the stronger candidate for provisional integration planning because it is independent from the REF-016 cyberphone vector lineage, matched staged REF-016 vectors, matched the bounded number oracle for asserted in-domain rows, failed closed outside its safe-integer domain, and has a clearer source and declared-license signal than REF-015. REF-015 `jcs==0.2.1` remains useful as comparison evidence and as a cyberphone-lineage cross-check, but its REF-016 agreement is less independent and its unsafe-integer behavior remains an input-domain research concern. The assessment preserves the research boundary: no dependency is adopted, no candidate is selected, no canonicalizer is replaced, references remain Pending review, full RFC 8785/JCS conformance is not claimed, legal compatibility is not claimed, and real signature verification remains blocked.

Tests:
170 tests passed.

Not implemented:
dependency adoption, candidate selection, canonicalizer replacement, package installation in the repository environment, package artifact provenance review, build provenance verification, legal compatibility review, attribution completeness review, maintenance and vulnerability-risk review, verifier raw-JSON entry-point integration, schema-level numeric-domain policy for future numeric fields, unsafe integer rejection policy, full RFC 8785/JCS conformance, full I-JSON conformance, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Draft a canonicalization candidate decision record for review. The decision record should recommend REF-014 for provisional integration planning only, keep REF-015 as comparison evidence, and list the remaining blockers before adoption.
