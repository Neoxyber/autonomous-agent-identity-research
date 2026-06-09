# Canonicalization Number Serialization Gate: REF-014 and REF-015

## Purpose

This document records a bounded number-serialization gate for the current
RFC 8785 / JSON Canonicalization Scheme candidate implementations:

- REF-014: `rfc8785==0.1.4`.
- REF-015: `jcs==0.2.1`.

The gate compares each candidate against a small oracle table derived from
RFC 8785 and ECMA-262 number serialization references. Neither candidate is
treated as the oracle.

## Current boundary

This is bounded candidate evidence only. It does not:

- Adopt REF-014 or REF-015.
- Select a canonicalization dependency.
- Replace the repository canonicalizer.
- State full RFC 8785/JCS conformance.
- State legal compatibility, safety, or production readiness.
- Unblock real signature verification.

## Oracle and execution record

| Field | Value |
| --- | --- |
| Oracle path | `$AAID_NUMERIC_GATE_SANDBOX/number-oracle.json` |
| Oracle SHA-256 | `c0b08f3e3a6c5004cb302228938382973e8606abc5d1bc7d9b698ce8a08e95eb` |
| Output path | `$AAID_NUMERIC_GATE_SANDBOX/observed-output-number-oracle-ref014-ref015.txt` |
| Output SHA-256 | `7d478f0ab8fcca491c68167ef3d1f8fb8459f2166c301840f549135a81b4cde5` |
| Vectors | 14 |
| Candidates | 2 |
| Candidate results | 28 |
| Repository files changed by execution | None |

The oracle table was staged in a temporary virtual environment outside the
repository and validated as strict JSON before execution. The cyberphone 100M
ES6 number test file was excluded from this gate.

## Result summary

| Status | Count |
| --- | ---: |
| PASS | 25 |
| BLOCKED | 2 |
| NEEDS_RESEARCH | 1 |
| FAIL | 0 |
| Total | 28 |

The run recorded no `FAIL` results.

## Asserted number rows

Both candidates matched the expected token for these asserted rows:

- `-0.0` -> `0`
- `0.002` -> `0.002`
- `1e-27` -> `1e-27`
- `1e30` -> `1e+30`
- `333333333.33333329` -> `333333333.3333333`
- `4.50` -> `4.5`
- `10^16` -> `10000000000000000`
- `9,007,199,254,740,991 (2^53 - 1)` -> `9007199254740991`
- `1e20` -> `100000000000000000000`
- `1e21` -> `1e+21`
- `1e-6` -> `0.000001`
- `1e-7` -> `1e-7`

## Integer-domain observations

The `9,007,199,254,740,992 (2^53)` row produced different candidate behavior:

| Candidate | Input | Result | Observation |
| --- | --- | --- | --- |
| REF-014 | `9,007,199,254,740,992 (2^53)` | BLOCKED | Raised `IntegerDomainError` for exceeding the safe integer domain |
| REF-015 | `9,007,199,254,740,992 (2^53)` | PASS | Emitted `9007199254740992` |

The `9,007,199,254,740,993 (2^53 + 1)` observe row also produced different
candidate behavior:

| Candidate | Input | Result | Observation |
| --- | --- | --- | --- |
| REF-014 | `9,007,199,254,740,993 (2^53 + 1)` | BLOCKED | Raised `IntegerDomainError` for exceeding the safe integer domain |
| REF-015 | `9,007,199,254,740,993 (2^53 + 1)` | NEEDS_RESEARCH | Emitted `9007199254740992`; this records a silent precision-loss concern for unconstrained numeric payloads |

These results should be interpreted as input-domain behavior, not as a simple
byte mismatch. REF-014 enforces a stricter safe-integer boundary. REF-015 accepts
the Python input and, for the `2^53 + 1` observe row, emits the same token as
`2^53`. This is a silent precision-loss concern for any future unconstrained
numeric payload field.

## Current interpretation

This gate reduces uncertainty around negative zero, exponent formatting,
small decimal forms, large exponent forms, and common threshold rows.

REF-014 remains stronger on independence grounds and demonstrates stricter
integer-domain enforcement. REF-015 remains useful as differential comparison
evidence and matched the asserted number tokens in this bounded gate, while its
unsafe-integer behavior remains `NEEDS_RESEARCH` and requires an explicit
numeric-domain policy before any adoption discussion.

This document does not select a candidate. Both candidates remain Pending review.

## Remaining open items

Separate review is still required for:

- Full RFC 8785/JCS conformance.
- Full I-JSON validation policy.
- Duplicate-key parse-layer policy.
- Package artifact and build provenance.
- Legal compatibility and attribution completeness.
- Dependency adoption suitability.
- Real signature verification integration.

## Next step

The next step is to decide whether to write a canonicalization candidate
decision record, or to run another explicitly bounded gate for duplicate-key
parse-layer policy and payload-domain validation before any adoption discussion.
