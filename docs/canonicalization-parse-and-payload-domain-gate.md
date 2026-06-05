# Canonicalization Parse and Payload Domain Gate

## Purpose

This document records the current repository boundary for duplicate-key parsing
and payload-domain validation before any canonicalization candidate adoption
decision.

The gate follows the bounded canonicalization evidence already collected for
REF-014 and REF-015. It does not select a candidate, adopt a dependency, replace
the canonicalizer, or unblock real signature verification.

## Current boundary

The current repository separates three concerns:

1. Raw JSON parsing.
2. Schema and payload-domain validation.
3. Canonical byte generation.

Duplicate JSON object member names can only be detected at the raw JSON text
parsing boundary. After ordinary JSON parsing collapses object members into a
mapping, duplicate names cannot be reliably recovered from the parsed object.

## Current repository evidence

The repository already includes a raw JSON parsing helper:

- `src/aaid/json_parsing.py`

The helper parses raw JSON text with an `object_pairs_hook` and fails closed on
duplicate object member names, including nested objects and objects inside
arrays.

The repository also includes focused parser tests:

- `tests/test_passport_json_parsing.py`

Those tests cover:

- valid JSON without duplicate keys;
- top-level duplicate-key rejection;
- nested duplicate-key rejection;
- duplicate keys inside objects within arrays;
- allowing the same key name in separate sibling objects;
- malformed JSON surfacing through the `ValueError` family.

This is parse-layer evidence only. It is not canonicalization, schema
validation, full I-JSON conformance, or full RFC 8785/JCS conformance.

## Numeric payload-domain observation

The current passport schema inspection found no `number` or `integer` typed
fields. That materially reduces the current passport profile's exposure to
ambiguous JSON number-domain behavior.

The current canonicalization helper also uses JSON serialization with
`allow_nan=False`, so non-finite values such as `NaN`, `Infinity`, and
`-Infinity` fail closed instead of emitting non-conformant JSON tokens.

The bounded number-serialization gate remains candidate evidence only. It does
not mean that future schema versions may safely add arbitrary numeric fields
without separate payload-domain validation.

## Current interpretation

The duplicate-key parse-layer boundary is already implemented and tested for the
research helper. The current schema avoids numeric typed fields, so unsafe
integer-domain behavior is not presently exposed by the declared passport
profile.

This supports the recorded verifier entry-point boundary.
`verify_passport_json()` is the raw JSON entry point and handles duplicate-key
rejection before schema validation. `verify_passport_envelope()` is the
parsed-envelope entry point and assumes callers provide already parsed,
duplicate-key-safe mappings.

## Required constraints before adoption

Before any canonicalization dependency is adopted or real signature verification
is enabled, the project should explicitly decide:

- whether verifier APIs accept raw JSON text or parsed Python mappings;
- where duplicate-key rejection is enforced;
- whether schema validation must run before canonicalization;
- whether future numeric payload fields are forbidden, constrained, or rejected
  outside a safe profile;
- whether unsafe integers are rejected at schema validation, raw parsing, or
  canonicalization;
- how parse, schema, canonicalization, and signature-input failures are reported
  in the verification result model.

## Non-goals

This document does not cover:

- dependency adoption;
- candidate selection;
- canonicalizer replacement;
- full RFC 8785/JCS conformance;
- full I-JSON conformance;
- legal compatibility review;
- build or package provenance;
- real signature verification;
- post-quantum signing;
- issuer trust;
- revocation;
- policy, audit, gateway, cloud, or deployment work.

## Next step

The next step is to decide whether the current parse-layer and payload-domain
evidence is sufficient to draft a canonicalization candidate decision record, or
whether verifier API integration should first require raw JSON parsing through
the duplicate-key rejecting helper.
