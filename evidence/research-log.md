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
