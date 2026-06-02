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

## Entry 044

Date: 2026-06-01

Type: Canonicalization decision-readiness clarification

Summary: Clarified the canonicalization readiness next step.

Files:
Updated `docs/canonicalization-candidate-decision-readiness.md`; updated this evidence log.

Result:
The decision-readiness research assessment now avoids creating a separate near-duplicate candidate decision record at this stage. It records that the assessment itself is the current canonicalization decision-readiness record, identifies REF-014 as the leading candidate for provisional integration planning only, and keeps REF-015 as comparison evidence. The next step is now a REF-014 provisional integration plan covering required tests, provenance checks, legal/attribution checks, dependency-risk checks, and verifier-boundary changes before any adoption proposal. This preserves the boundary: no dependency is adopted, no candidate is selected for adoption, no canonicalizer is replaced, references remain Pending review, real signature verification remains blocked, and post-quantum signing work is not started.

Tests:
170 tests passed.

Not implemented:
dependency adoption, candidate adoption decision record, canonicalizer replacement, package installation in the repository environment, package artifact provenance review, build provenance verification, legal compatibility review, attribution completeness review, maintenance and vulnerability-risk review, verifier raw-JSON entry-point integration, schema-level numeric-domain policy for future numeric fields, unsafe integer rejection policy, full RFC 8785/JCS conformance, full I-JSON conformance, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Prepare a REF-014 provisional integration plan before any adoption proposal.

## Entry 045

Date: 2026-06-01

Type: Canonicalization provisional integration planning

Summary: Planned REF-014 provisional integration requirements.

Files:
Added `docs/canonicalization-ref014-provisional-integration-plan.md`; updated this evidence log.

Result:
The REF-014 provisional integration research plan records the required planning work before any proposal to adopt REF-014 `rfc8785==0.1.4` as the repository canonicalization implementation. The plan is explicitly not an adoption plan: it does not authorize package installation, requirements changes, canonicalizer replacement, verifier changes, or real signature verification. It records the current repository boundary, including the local research canonicalization helper, the duplicate-key raw JSON parser helper, schema validation before payload-hash comparison, signature-input preparation through the shared helper, and fail-closed real signature verification. The plan identifies required provenance review, legal and attribution review, dependency-risk review, verifier-boundary decisions, integration tests, golden vector migration review, and adoption blockers. It treats REF-014 safe-integer blocking as security-relevant input-domain enforcement and keeps post-quantum work limited to future algorithm-agility considerations. No dependency is adopted, no runtime behavior changes, references remain Pending review, legal compatibility is not claimed, and real signature verification remains blocked.

Tests:
170 tests passed.

Not implemented:
dependency adoption, package installation in the repository environment, requirements changes, canonicalizer replacement, verifier behavior changes, package artifact provenance review, build provenance verification, legal compatibility review, attribution completeness review, maintenance and vulnerability-risk review, verifier raw-JSON entry-point integration, schema-level numeric-domain policy for future numeric fields, unsafe integer rejection policy, golden vector migration, full RFC 8785/JCS conformance, full I-JSON conformance, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Perform REF-014 provenance, legal/attribution, dependency-risk, and verifier-boundary review before any adoption proposal or runtime integration branch.

## Entry 046

Date: 2026-06-01

Type: REF-014 provenance evidence

Summary: Recorded first REF-014 provenance evidence pass.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md`; updated this evidence log.

Result:
The REF-014 provisional integration plan now records P0 provenance evidence collected under `/tmp/aaid-ref014-provenance-review`. The PyPI and GitHub release artifacts matched byte-for-byte for the evaluated wheel and source distribution. The wheel SHA-256 was `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`; the source distribution SHA-256 was `e545841329fe0eee4f6a3b44e7034343100c12b4ec566dc06ca9735681deb4da`. The wheel was observed as `py3-none-any`, pure Python, with no native extensions and no normal runtime dependency surface beyond optional development, documentation, lint, and test extras. PyPI release metadata reported no index-hosted provenance field. GitHub release assets included Sigstore bundle files for the wheel, source distribution, and source archives. The Sigstore bundle metadata referenced Rekor `hashedrekord` entries whose decoded bodies contained the expected artifact SHA-256 values, and certificate hints referenced `trailofbits/rfc8785.py`, `refs/tags/v0.1.4`, `https://token.actions.githubusercontent.com`, and the release workflow `release.yml@refs/tags/v0.1.4`. This is provenance evidence only: cryptographic Sigstore verification, Rekor inclusion verification, certificate-chain verification, expected issuer policy, and expected workflow identity policy remain pending. Provenance is not claimed as verified.

Tests:
170 tests passed.

Not implemented:
dependency adoption, package installation in the repository environment, requirements changes, canonicalizer replacement, verifier behavior changes, cryptographic Sigstore verification, Rekor inclusion verification, certificate-chain verification, expected issuer policy, expected workflow identity policy, legal compatibility review, attribution completeness review, maintenance and vulnerability-risk review, verifier raw-JSON entry-point integration, schema-level numeric-domain policy for future numeric fields, unsafe integer rejection policy, golden vector migration, full RFC 8785/JCS conformance, full I-JSON conformance, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Perform REF-014 legal/attribution review and dependency-risk review, while keeping provenance verification pending until Sigstore/Rekor/certificate/issuer/workflow checks are explicitly verified.

## Entry 047

Date: 2026-06-01

Type: REF-014 legal and dependency-risk evidence

Summary: Recorded first REF-014 legal/attribution and dependency-risk evidence pass.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md`; updated this evidence log.

Result:
The REF-014 provisional integration plan now records P1 legal/attribution and dependency-risk evidence collected from the wheel and source distribution staged under `/tmp/aaid-ref014-provenance-review`. The wheel includes `rfc8785-0.1.4.dist-info/LICENSE`; the source distribution includes `LICENSE`, `PKG-INFO`, `README.md`, and `pyproject.toml`. The included license text is Apache License, Version 2.0. Package metadata includes the Apache Software License classifier, `pyproject.toml` declares `license = { file = "LICENSE" }`, and author metadata identifies Trail of Bits. The README/PKG-INFO states that parts are adapted from Andrew Rundgren's reference implementation, also described as Apache License, Version 2.0. `pyproject.toml` declares `dependencies = []`; observed `Requires-Dist` entries are optional extras for development, documentation, lint, and tests. This is legal/attribution and dependency-risk evidence only. Legal compatibility and attribution completeness remain pending review. No adoption, package installation, requirements change, or runtime behavior change is authorized.

Tests:
170 tests passed.

Not implemented:
dependency adoption, package installation in the repository environment, requirements changes, canonicalizer replacement, verifier behavior changes, legal compatibility determination, attribution completeness determination, legal review, cryptographic Sigstore verification, Rekor inclusion verification, certificate-chain verification, expected issuer policy, expected workflow identity policy, maintenance and vulnerability-risk review, verifier raw-JSON entry-point integration, schema-level numeric-domain policy for future numeric fields, unsafe integer rejection policy, golden vector migration, full RFC 8785/JCS conformance, full I-JSON conformance, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Continue REF-014 dependency and maintenance-risk review, then review verifier-boundary integration requirements before any adoption proposal.

## Entry 048

Date: 2026-06-01

Type: REF-014 maintenance-risk evidence

Summary: Recorded first REF-014 maintenance-risk evidence pass.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md`; updated this evidence log.

Result:
The REF-014 provisional integration plan now records P2 maintenance-risk evidence. The reviewed REF-014 package `rfc8785==0.1.4` declares `Requires-Python >=3.8`, has no normal runtime dependencies, and is marked `Development Status :: 4 - Beta`. The GitHub repository was observed as not archived, not disabled, and not a fork. Tags and releases were observed from `v0.0.1` through `v0.1.4`; the evaluated release was published on 2024-09-27. Repository metadata showed recent activity in May 2026. The open issue query found no open issues excluding pull requests and one open pull request related to mypy settings. This is maintenance-risk evidence only. It does not establish long-term maintenance suitability, vulnerability posture, adoption readiness, or production readiness.

Tests:
170 tests passed.

Not implemented:
dependency adoption, package installation in the repository environment, requirements changes, canonicalizer replacement, verifier behavior changes, legal compatibility determination, attribution completeness determination, legal review, cryptographic Sigstore verification, Rekor inclusion verification, certificate-chain verification, expected issuer policy, expected workflow identity policy, long-term maintenance suitability determination, vulnerability posture determination, verifier raw-JSON entry-point integration, schema-level numeric-domain policy for future numeric fields, unsafe integer rejection policy, golden vector migration, full RFC 8785/JCS conformance, full I-JSON conformance, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Review verifier-boundary integration requirements before any adoption proposal, while keeping provenance, legal compatibility, attribution completeness, and long-term maintenance suitability pending.

## Entry 049

Date: 2026-06-01

Type: Verifier-boundary evidence

Summary: Recorded first verifier-boundary evidence pass.

Files:
Updated `docs/canonicalization-ref014-provisional-integration-plan.md`; updated this evidence log.

Result:
The REF-014 provisional integration plan now records P3 verifier-boundary evidence. The current raw JSON duplicate-key helper exists separately in `src/aaid/json_parsing.py` and rejects duplicate object member names before JSON objects collapse into parsed mappings. The current verifier entry point `verify_passport_envelope()` accepts an already parsed envelope object, not raw JSON text. Schema validation runs before payload-hash comparison. Payload-hash verification and future signature-input preparation both use the shared canonicalization helper over the `passport` object only, excluding the envelope wrapper and `proofs`. Unsupported canonicalization fails closed before signature input preparation. Real signature verification remains unimplemented and fails closed. Before any REF-014 adoption proposal, the project should decide whether to add a raw JSON verifier entry point that calls `parse_json_no_duplicate_keys()` before schema validation, or document that parsed mappings are accepted only with caller-side duplicate-key parsing guarantees. No verifier changes or runtime behavior changes were authorized.

Tests:
170 tests passed.

Not implemented:
dependency adoption, package installation in the repository environment, requirements changes, canonicalizer replacement, verifier behavior changes, raw JSON verifier entry point, duplicate-key parsing integration into the verifier entry point, legal compatibility determination, attribution completeness determination, legal review, cryptographic Sigstore verification, Rekor inclusion verification, certificate-chain verification, expected issuer policy, expected workflow identity policy, long-term maintenance suitability determination, vulnerability posture determination, schema-level numeric-domain policy for future numeric fields, unsafe integer rejection policy, golden vector migration, full RFC 8785/JCS conformance, full I-JSON conformance, real signature verification, post-quantum signing, issuer trust, revocation enforcement, policy evaluation, audit implementation, gateway logic, cloud deployment, or external integrations.

Next step:
Prepare a threat model and trust-boundary research document before any adoption proposal or implementation change. The document should position the project as interoperable research for autonomous-agent identity and control, not as a replacement for existing identity, credential, supply-chain, or post-quantum standards.

## Entry 050

Date: 2026-06-01

Type: Threat model and trust boundaries

Summary: Added agent passport threat model and trust-boundary research document.

Files:
Added `docs/agent-passport-threat-model-and-trust-boundaries.md`; updated this evidence log.

Result:
The project now records a focused threat model and trust-boundary document for the agent passport research model. The document positions the passport as an interoperable research envelope for autonomous-agent identity and control, not as a replacement for verifiable credentials, decentralized identifiers, workload identity, OAuth/OIDC, Sigstore, SLSA, SCITT, MCP, post-quantum standards, or other existing ecosystems. It records the core security question, future proof goals, what a passport does not prove by itself, assets, trust boundaries, attacker model, current fail-closed behavior, known gaps, interoperability posture, 2026 and 2027 research implications, reviewer questions, reviewer-critical open risks, non-goals, and the next boundary decision. The document makes clear that a valid passport is not unlimited authority and that issuer trust, lifecycle, revocation, permission policy, human oversight, and audit evidence remain future gates.

Tests:
170 tests passed.

Not implemented:
dependency adoption, package installation in the repository environment, requirements changes, canonicalizer replacement, verifier behavior changes, raw JSON verifier entry point, duplicate-key parsing integration into the verifier entry point, real signature verification, issuer trust registry, trust anchor model, key rotation enforcement, expiration enforcement, lifecycle enforcement, revocation checking, permission and policy evaluation, human approval or review enforcement, audit evidence implementation, cryptographic provenance verification for dependencies, legal compatibility determination, post-quantum signing, cloud deployment, or external integrations.

Next step:
Use the threat model to decide the raw JSON verifier boundary before any implementation change. The next research decision should determine whether the public verifier API accepts raw JSON text, parsed mappings, or both with explicit trust guarantees.

## Entry 051

Date: 2026-06-01

Type: Verifier-boundary research decision

Summary: Recorded raw JSON verifier-boundary decision.

Files:
Updated `docs/agent-passport-threat-model-and-trust-boundaries.md`; updated this evidence log.

Result:
The threat model now records that untrusted raw JSON should enter through `verify_passport_json(text: str)` and be parsed with `parse_json_no_duplicate_keys()` before schema validation, canonicalization, payload-hash comparison, or signature processing. The parsed-object boundary, `verify_passport_envelope(envelope: object)`, may remain for internal or caller-trusted mappings when duplicate-key parsing guarantees are provided. This records the API boundary only and does not change verifier behavior.

Tests:
170 tests passed.

Not implemented:
raw JSON verifier entry point, duplicate-key parsing integration into the public verifier boundary, verifier behavior changes, dependency adoption, canonicalizer replacement, real signature verification, issuer trust, revocation checking, permission and policy evaluation, human oversight, audit evidence implementation, post-quantum signing, cloud deployment, or external integrations.

Next step:
Implement or plan the raw JSON verifier entry point as the next small verifier-boundary step.

## Entry 052

Date: 2026-06-01

Type: Verifier-boundary implementation

Summary: Added raw JSON verifier entry point.

Files:
Updated `src/aaid/passport_verifier.py`, `src/aaid/__init__.py`, `tests/test_passport_verifier_signature_abstraction.py`, and added `tests/test_passport_verifier_raw_json.py`; updated this evidence log.

Result:
The verifier now exposes `verify_passport_json(text: str)` as the raw JSON boundary for untrusted input. It parses with `parse_json_no_duplicate_keys()` before schema validation, canonicalization, payload-hash comparison, or signature processing. Malformed JSON and duplicate object member names fail closed with a `raw_json_parsed` check. Successful raw JSON parsing prepends a passed `raw_json_parsed` check and delegates to the existing parsed-object verifier. The existing `verify_passport_envelope(envelope: object)` behavior remains available and unchanged.

Tests:
181 tests passed.

Not implemented:
dependency adoption, requirements changes, canonicalizer replacement, real signature verification, issuer trust, revocation checking, permission and policy evaluation, human oversight, audit evidence implementation, post-quantum signing, cloud deployment, or external integrations.

Next step:
Review whether the next small verifier step should address expiration, lifecycle, or another fail-closed trust boundary before any canonicalizer adoption or signature implementation.

## Entry 053

Date: 2026-06-02

Type: Verifier-boundary research decision

Summary: Recorded expiration and lifecycle verifier-boundary decision.

Files:
Updated `docs/agent-passport-threat-model-and-trust-boundaries.md`; updated this evidence log.

Result:
The threat model now records the planned expiration and lifecycle verifier boundary. The next verifier checks should be `passport_time_valid` and `lifecycle_status_allows_verification`, running after `schema_valid` and before `proof_selected`. The decision records strict UTC `Z` timestamp handling, inclusive `issued_at`, exclusive `expires_at`, fail-closed timestamp behavior, active-only lifecycle continuation, and future deterministic UTC `now` injection. This records a research decision only and does not implement expiration or lifecycle enforcement.

Tests:
181 tests passed.

Not implemented:
expiration enforcement, lifecycle enforcement, issuer trust, revocation checking, permission and policy evaluation, human oversight, audit evidence implementation, signatures, post-quantum signing, dependency adoption, requirements changes, canonicalizer replacement, cloud deployment, or external integrations.

Next step:
Plan, implement, and test the expiration and lifecycle verifier boundary as the next small verifier step.

## Entry 054

Date: 2026-06-02

Type: Verifier-boundary implementation

Summary: Added passport expiration and lifecycle validity checks.

Files:
Updated `src/aaid/passport_verifier.py`, added `tests/_support.py`, added `tests/test_passport_verifier_expiration_lifecycle.py`, and updated existing verifier tests for deterministic `now` injection; updated this evidence log.

Result:
The verifier now records `passport_time_valid` and `lifecycle_status_allows_verification` after `schema_valid` and before `proof_selected`. Passport timestamps are checked as strict UTC `Z` values, `issued_at` is treated as inclusive, and `expires_at` is treated as exclusive. Malformed timestamps, non-strict timestamp forms, inverted validity windows, not-yet-valid passports, expired passports, and non-active lifecycle statuses fail closed before proof selection, payload-hash comparison, key selection, canonicalization metadata checks, signature-input preparation, or future signature verification. The raw JSON verifier now forwards deterministic `now` into the parsed-object verifier after duplicate-key-safe parsing. Existing verifier tests now inject a fixed UTC `now` where they intentionally exercise checks beyond schema validation.

Tests:
225 tests passed.

Not implemented:
issuer trust, revocation checking, permission and policy evaluation, human oversight, audit evidence implementation, real signature verification, post-quantum signing, dependency adoption, requirements changes, canonicalizer replacement, cloud deployment, or external integrations.

Next step:
Review the next verifier trust boundary before adding issuer trust, revocation, policy evaluation, canonicalizer adoption, or signature verification.

## Entry 055

Date: 2026-06-02

Type: Verifier-boundary research decision

Summary: Recorded issuer trust and revocation ordering decision.

Files:
Updated `docs/agent-passport-threat-model-and-trust-boundaries.md`; updated this evidence log.

Result:
The threat model now records that issuer trust should be decided before revocation or freshness checks. A revocation result is useful only when the verifier knows which issuer, registry, trust anchor, or status authority is allowed to provide that result. The document also updates current fail-closed behavior to include passport validity-window failure and non-active lifecycle status, removes stale expiration and lifecycle enforcement from current gaps, and updates the next step toward planning the smallest issuer-trust verifier boundary. This records a research decision only and does not implement issuer trust or revocation checking.

Tests:
225 tests passed.

Not implemented:
issuer trust, revocation checking, network lookup, permission and policy evaluation, human oversight, audit evidence implementation, real signature verification, post-quantum signing, dependency adoption, requirements changes, canonicalizer replacement, cloud deployment, or external integrations.

Next step:
Plan the smallest issuer-trust verifier boundary before revocation, policy evaluation, canonicalizer adoption, or signature verification.

## Entry 056

Date: 2026-06-02

Type: Example vector alignment

Summary: Aligned minimal example issuer identifier.

Files:
Updated `specs/examples/agent-passport.minimal.json` and `tests/test_passport_canonicalization_conformance.py`; updated this evidence log.

Result:
The minimal example issuer identifier was changed from `urn:aaid:issuer:aixyber-research-issuer` to `urn:aaid:issuer:aixybertech-issuer`. Because `issuer_id` is part of the canonicalized passport payload, the example proof `payload_hash` and the frozen canonical SHA-256 golden vector were re-pinned from `c8548cbedf9be9a378d0b48ddc7f070c5597230cf9f9ada715f0802eb1c8089c` to `b85a7ddfefccb9582bf6ab23dac42a968cc0b6aabfc1d29d416ea25e27bfb6bc`. This was a fixture and vector alignment only and did not change verifier behavior.

Tests:
225 tests passed.

Not implemented:
issuer trust, revocation checking, network lookup, permission and policy evaluation, human oversight, audit evidence implementation, real signature verification, post-quantum signing, dependency adoption, requirements changes, canonicalizer replacement, cloud deployment, or external integrations.

Next step:
Resume the issuer-trust verifier-boundary implementation using `urn:aaid:issuer:aixybertech-issuer` as the configured example issuer.

## Entry 057

Date: 2026-06-02

Type: Verifier-boundary implementation

Summary: Added caller-provided issuer trust check.

Files:
Updated `src/aaid/passport_verifier.py`, `tests/_support.py`, added `tests/test_passport_verifier_issuer_trust.py`, updated existing verifier tests for explicit issuer-trust injection, updated `docs/agent-passport-threat-model-and-trust-boundaries.md`, and updated this evidence log.

Result:
The verifier now supports caller-provided issuer trust configuration through keyword-only `trusted_issuers` on `verify_passport_envelope(..., now=None, trusted_issuers=None)` and `verify_passport_json(..., now=None, trusted_issuers=None)`. The raw JSON verifier forwards `trusted_issuers` after duplicate-key-safe parsing. The new `issuer_trusted` check runs after `lifecycle_status_allows_verification` and before `proof_selected`. It fails closed when issuer trust is not configured, when the trust configuration is a string, bytes, bytearray, or mapping, or when the passport `issuer_id` is not explicitly configured as trusted. It passes only when the issuer identifier is explicitly present in the caller-provided trusted issuer collection. This boundary performs no registry lookup, network lookup, revocation checking, signature verification, policy evaluation, audit storage, or external issuer verification. The verifier still cannot return `ALLOW` because real signature verification remains intentionally not implemented.

Tests:
244 tests passed.

Not implemented:
revocation checking, freshness evidence, issuer registry or external trust-anchor model, network lookup, permission and policy evaluation, human oversight, audit evidence implementation, real signature verification, post-quantum signing, dependency adoption, requirements changes, canonicalizer replacement, cloud deployment, or external integrations.

Next step:
Plan the revocation and freshness verifier boundary before policy evaluation, canonicalizer adoption, or signature verification.

## Entry 058

Date: 2026-06-02

Type: Security-review test evidence

Summary: Strengthened never-allow verifier step tests.

Files:
Updated `tests/test_passport_verifier_proof_selection.py`, `tests/test_passport_verifier_payload_hash.py`, `tests/test_passport_verifier_key_selection.py`, `tests/test_passport_verifier_canonicalization_scheme.py`, `tests/test_passport_verifier_signature_input.py`, and `tests/test_passport_verifier_signature_abstraction.py`; updated this evidence log.

Result:
A read-only security review found that six `*_step_never_returns_allow` sweeps could short-circuit at `issuer_trusted` without proving they reached the verifier step named by the test. The tests now inject `VALID_NOW` and `TRUSTED_ISSUERS` for the valid trusted example, assert the named step is reached, and still assert the verifier never returns `ALLOW`. This is a behavior-neutral test-evidence fix only and does not change verifier behavior.

Tests:
244 tests passed.

Not implemented:
revocation checking, freshness evidence, lifecycle vocabulary alignment, key expiration enforcement, proof-selection hardening, signature verification, permission and policy evaluation, human oversight, audit evidence implementation, post-quantum signing, dependency adoption, requirements changes, canonicalizer replacement, cloud deployment, or external integrations.

Next step:
Review lifecycle vocabulary alignment before recording the revocation and freshness verifier-boundary decision.

## Entry 059

Date: 2026-06-02

Type: Documentation alignment decision

Summary: Aligned lifecycle vocabulary prose to the committed schema enum.

Files:
Updated `docs/identity-layer.md`, `docs/revocation-model.md`, `docs/agent-passport-threat-model-and-trust-boundaries.md`, and this evidence log.

Result:
The lifecycle prose now aligns with the committed schema and verifier vocabulary: `active`, `suspended`, `revoked`, `expired`, `compromised`, and `retired`. `active` remains the only lifecycle status that allows verification to continue. `rotated` is documented as a transition process and revocation or audit reason, not as a current `lifecycle_status` value. `pending_verification` is documented as an onboarding or review state outside the current lifecycle enum. This is documentation alignment only and does not change the schema, verifier behavior, tests, examples, or the verifier's fail-closed behavior.

Tests:
244 tests passed.

Not implemented:
lifecycle vocabulary alignment of deferred forward-looking documents (`ROADMAP.md:119,125`, `docs/research-questions.md:41`, `docs/scope.md:45`), schema additions for `rotated` or `pending_verification`, passport-level pending state, lifecycle transition enforcement, revocation checking, freshness evidence, key expiration enforcement, operator verification enforcement, real signature verification, permission and policy evaluation, human oversight, audit evidence implementation, post-quantum signing, dependency adoption, requirements changes, canonicalizer replacement, cloud deployment, or external integrations.

Next step:
Record the revocation and freshness verifier-boundary decision.

## Entry 060

Date: 2026-06-02

Type: Verifier-boundary research decision

Summary: Recorded revocation and freshness verifier-boundary decision.

Files:
Updated `docs/agent-passport-threat-model-and-trust-boundaries.md` and this evidence log.

Result:
Recorded the planned revocation and freshness checks: `revocation_status_checked`, `revocation_status_fresh`, and `passport_not_revoked`. The checks should run after `issuer_trusted` and before `proof_selected`. The decision records caller-provided in-memory status evidence, exact binding to `status_reference`, `passport_id`, and `status_authority`, strict UTC freshness, and `active` as the only status that allows the chain to continue. The decision also records fail-closed handling for missing, mismatched, stale, malformed, unknown, or non-active status evidence.

Tests:
244 tests passed.

Not implemented:
revocation checking, freshness checking, network lookup, registry lookup, signed status evidence, replay or rollback protection, schema changes, real signature verification, permission and policy evaluation, human oversight, audit evidence implementation, dependency adoption, canonicalizer replacement, cloud deployment, or external integrations.

Next step:
Implement caller-provided revocation and freshness checks after review.

## Entry 061

Date: 2026-06-02

Type: Verifier-boundary implementation

Summary: Added caller-provided revocation and freshness checks.

Files:
Updated `src/aaid/passport_verifier.py`, `tests/_support.py`, added `tests/test_passport_verifier_revocation_freshness.py`, and updated existing verifier tests for explicit fresh status evidence; updated this evidence log.

Result:
The verifier now records `revocation_status_checked`, `revocation_status_fresh`, and `passport_not_revoked` after `issuer_trusted` and before `proof_selected`. The raw JSON verifier forwards caller-provided `revocation_status` after duplicate-key-safe parsing. Status evidence must bind by exact string equality to the passport `status_reference`, `passport_id`, and issuer through `status_authority`, and the authority must be configured as trusted. Freshness uses strict UTC `Z` timestamps with injected deterministic `now` and requires `produced_at <= now < valid_until`. Only `status == "active"` allows the chain to continue. Missing, malformed, mismatched, stale, future-dated, inverted-window, unknown, or non-active status evidence fails closed. Issuer-trust handling was also hardened so non-iterable trust configuration fails closed instead of raising.

Tests:
351 tests passed.

Not implemented:
network lookup, registry lookup, signed status evidence, cryptographic verification of status evidence, replay or rollback protection beyond the freshness window, schema changes, real signature verification, permission and policy evaluation, human oversight, audit evidence implementation, dependency adoption, requirements changes, canonicalizer replacement, cloud deployment, MCP integration, post-quantum signing, or external integrations.

Next step:
Review the next verifier boundary before policy evaluation, canonicalizer adoption, key-validity expansion, or real signature verification.

## Entry 062

Date: 2026-06-02

Type: Verifier-boundary research decision

Summary: Recorded selected-key validity and verification-method binding decision.

Files:
Updated `docs/agent-passport-threat-model-and-trust-boundaries.md` and this evidence log.

Result:
Recorded the next verifier boundary decision for selected-key validity and proof binding. The planned check should run after `verification_key_selected` and before signature-input preparation or signature-algorithm checks. The selected key should fail closed when it is not yet valid, expired, malformed, or not bound to the proof `verification_method`. Key `created_at` should be inclusive, optional `not_after` should be exclusive, and the check should use strict UTC `Z` timestamps with injected deterministic `now`. The proof `verification_method` should match the selected key `kid` by exact string equality.

Tests:
351 tests passed.

Not implemented:
selected-key time-validity enforcement, verification-method binding enforcement, proof-selection hardening, canonicalizer replacement, dependency adoption, real signature verification, signed status evidence, policy evaluation, human oversight, audit evidence implementation, cloud deployment, MCP integration, post-quantum signing, or external integrations.

Next step:
Implement selected-key validity and verification-method binding after review.

## Entry 063

Date: 2026-06-02

Type: Verifier-boundary implementation

Summary: Added selected-key validity and verification-method binding checks.

Files:
Updated `src/aaid/passport_verifier.py`, added `tests/test_passport_verifier_key_validity.py`, and updated this evidence log.

Result:
The verifier now records `verification_key_valid_for_proof` after `verification_key_selected` and before signature-stage checks. The check requires the selected key `created_at` value to be a strict UTC `Z` timestamp and treats it as inclusive. Optional `not_after` is strict UTC `Z` when present and is treated as exclusive. The check uses the already resolved injected deterministic `now` and fails closed for missing, malformed, non-strict, future-created, expired, or inverted key validity windows. It also binds `proof.verification_method` to the selected key `kid` by exact string equality. This adds selected-key time validity and proof/key self-consistency only; it does not perform cryptographic verification.

Tests:
395 tests passed.

Not implemented:
real signature verification, proof-selection hardening, canonicalizer replacement, dependency adoption, signed status evidence, network lookup, registry lookup, replay or rollback protection beyond the freshness window, permission and policy evaluation, human oversight, audit evidence implementation, cloud deployment, MCP integration, post-quantum signing, or external integrations.

Next step:
Review proof-selection hardening and canonicalization conformance before signature-verification planning.

## Entry 064

Date: 2026-06-02

Type: Verifier-boundary research decision

Summary: Recorded proof-selection hardening and downgrade-policy decision.

Files:
Updated `docs/agent-passport-threat-model-and-trust-boundaries.md` and this evidence log.

Result:
Recorded the next verifier boundary decision for proof-selection hardening. The current verifier selects the first proof only, which remains acceptable while the verifier cannot return `ALLOW`, but should not become a real signature-verification trust model. The planned boundary should fail closed when more than one proof is present and should run before `proof_selected`. This prevents multi-proof envelopes from continuing before a long-term proof-selection policy exists.

Tests:
395 tests passed.

Not implemented:
proof-selection hardening, multi-proof policy, hybrid-signature proof selection, post-quantum proof selection, canonicalizer replacement, dependency adoption, real signature verification, signed status evidence, policy evaluation, human oversight, audit evidence implementation, cloud deployment, MCP integration, post-quantum signing, or external integrations.

Next step:
Implement proof-selection hardening after review.

## Entry 065

Date: 2026-06-02

Type: Verifier-boundary implementation

Summary: Added proof-selection hardening.

Files:
Updated `src/aaid/passport_verifier.py`, added `tests/test_passport_verifier_proof_selection_hardening.py`, updated existing proof-selection and payload-hash tests for fail-closed multi-proof behavior, and updated this evidence log.

Result:
The verifier now records `proof_count_allowed` before `proof_selected`. The check passes only when exactly one proof is present and fails closed when more than one proof is present. Multi-proof envelopes no longer reach `proof_selected`, `payload_hash_valid`, key selection, key-validity checks, canonicalization checks, signature-input preparation, signature-algorithm checks, or signature verification. Existing missing, non-sequence, and empty proof structural checks remain earlier and unchanged. This removes first-proof-only behavior as a future trust boundary while keeping long-term multi-proof, hybrid-signature, and post-quantum proof-selection policy deferred.

Tests:
409 tests passed.

Not implemented:
multi-proof policy, hybrid-signature proof selection, post-quantum proof selection, canonicalizer replacement, dependency adoption, real signature verification, signed status evidence, network lookup, registry lookup, permission and policy evaluation, human oversight, audit evidence implementation, cloud deployment, MCP integration, post-quantum signing, or external integrations.

Next step:
Review canonicalization conformance and dependency adoption before signature-verification planning.

