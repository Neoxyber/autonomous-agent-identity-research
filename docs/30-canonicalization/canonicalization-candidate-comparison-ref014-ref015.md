# Canonicalization Candidate Comparison: REF-014 and REF-015

## Purpose

This document compares the current isolated evidence for two RFC 8785 / JSON
Canonicalization Scheme candidate implementations:

- REF-014: `rfc8785 / trailofbits/rfc8785.py`, version `0.1.4`.
- REF-015: `jcs Python package / titusz jcs`, version `0.2.1`.

The purpose is to compare evidence collected so far and identify the next review
gate. This document does not adopt a dependency or select a candidate.

## Current boundary

This comparison is evidence review only. It does not:

- Adopt REF-014 or REF-015.
- Select a canonicalization dependency.
- Replace the repository canonicalizer.
- Claim full RFC 8785/JCS conformance.
- Claim legal compatibility.
- Unblock real signature verification.
- Start issuer trust, revocation, policy, gateway, audit, cloud, or deployment
  work.

## Evidence sources

| Reference | Result record |
| --- | --- |
| REF-014 | `docs/30-canonicalization/canonicalization-evaluation-results-ref014-rfc8785-0.1.4.md` |
| REF-015 | `docs/30-canonicalization/canonicalization-evaluation-results-ref015-jcs-0.2.1.md` |
| REF-016 | Staged `cyberphone/json-canonicalization` vectors under `/tmp` |

## Summary comparison

| Area | REF-014 | REF-015 |
| --- | --- | --- |
| Package | `rfc8785` | `jcs` |
| Version evaluated | `0.1.4` | `0.2.1` |
| Source | `trailofbits/rfc8785.py` | `titusz/jcs` |
| Implementation relationship | Independent candidate | Port of cyberphone lineage |
| Runtime dependency surface observed | No third-party runtime dependencies | No third-party runtime dependencies |
| Source/license signal | Source identity and declared license checked | Source identity and declared license checked |
| License concern | Apache-2.0 signals checked | Apache-2.0 declared, but no standalone source license file found |
| Broader inline result | 19 PASS / 7 NEEDS_RESEARCH | 25 PASS / 6 NEEDS_RESEARCH |
| REF-016 staged vectors | 6 PASS | 6 PASS |
| Independence from REF-016 | Stronger | Weaker because of shared cyberphone lineage |
| Adoption status | Not adopted | Not adopted |
| Full conformance status | Not claimed | Not claimed |

## REF-014 evidence assessment

REF-014 has stronger independence as candidate evidence because it is not a
cyberphone-lineage port. It passed the staged REF-016 vectors and the isolated
broader inline coverage exercised so far.

Its remaining open work includes number-serialization boundaries, duplicate-key
parse-layer policy, broader RFC 8785/JCS conformance, build provenance, legal
compatibility, and any later adoption review.

## REF-015 evidence assessment

REF-015 passed the same broad categories of checks used in the isolated
comparison and matched the staged REF-016 vectors. It is useful as differential
comparison evidence and as a cyberphone-lineage behavior reference.

However, its agreement with REF-016 is not fully independent corroboration
because REF-015 is a port of cyberphone/json-canonicalization. The pinned source
tree also did not contain a standalone root license file, so the Apache-2.0
license signal remains declared metadata rather than a checked standalone source
license file.

## Shared open items

Both candidates still require separate review for:

- Full RFC 8785/JCS conformance.
- Full I-JSON validation boundaries.
- Bounded number-serialization reference-vector coverage.
- Duplicate-key parse-layer policy.
- Build provenance and package artifact provenance.
- Legal compatibility and attribution completeness.
- Dependency adoption suitability.
- Real signature verification integration.

## Current interpretation

The current evidence supports keeping both candidates under review. REF-014 is
the stronger adoption candidate on independence grounds, while REF-015 remains a
useful comparison candidate and cyberphone-lineage cross-check.

This interpretation is not a selection decision. The repository should continue
to treat both candidates as Pending review until the remaining gates are
completed or explicitly deferred.

## Recommended next gate

Before any adoption discussion, run or explicitly defer a bounded
number-serialization reference-vector gate. That gate should focus on cases that
remain open in both records, including negative zero, exponent formatting,
small decimal forms, large exponent forms, and oversized integer-domain behavior.

If that gate is run, it should follow the existing discipline:

- Use `/tmp` only.
- Pin source/vector provenance.
- Avoid repository dependency adoption.
- Use explicit PASS / FAIL / BLOCKED / NEEDS_RESEARCH result categories.
- Record observed output without inventing expected constants.
- Keep signature verification blocked.

## Non-goals

This comparison does not cover:

- Selecting REF-014 or REF-015.
- Adding either dependency to project requirements.
- Replacing canonicalization code.
- Verifying build provenance.
- Completing a legal review.
- Implementing real signatures.
- Implementing post-quantum signing.
- Implementing issuer trust, revocation, policy, audit, gateway, cloud, or
  deployment behavior.
