# Post-Quantum Readiness Model

## Purpose

This document explains where post-quantum readiness fits in the autonomous
agent identity research.

Post-quantum readiness is a cross-cutting research direction. It affects agent
identity evidence, signatures, key rotation, long-term audit evidence, and future
migration planning.

This model may change as the research develops and as standards, tests, and
review feedback improve the project.

## Why it matters

Autonomous agents may eventually operate in large numbers, across many systems,
at machine speed.

If agent identity evidence is expected to remain verifiable over time, the
research must consider cryptographic migration early. A passport, signature,
revocation record, approval record, or audit record may need to be reviewed long
after it was created.

The gap is not only choosing a post-quantum algorithm.

The gap is:

How can autonomous-agent identity evidence remain verifiable, reviewable, and
migratable when cryptographic algorithms, libraries, proof formats, and threat
models change?

## Fit in the roadmap

Post-quantum readiness supports QSAG Layer 1:

Agent identity and action-decision evidence.

It connects to the current roadmap through:

1. proof and key metadata;
2. signed-byte and canonicalization research;
3. future signature verification;
4. key validity and key rotation;
5. long-term audit evidence;
6. proof-profile alignment;
7. dependency adoption review;
8. failure handling for unsupported algorithms or proof formats.

Post-quantum work is also cross-cutting because it may affect later QSAG layers,
including gateway enforcement, delegation, evidence replay, and long-term
migration.

## Current boundary

This repository does not implement real signature verification.

It does not adopt a cryptographic runtime dependency, generate production keys,
define a production key-management system, or claim post-quantum security.

The current technical focus remains verifier-boundary research and future
signature adapter-interface tests. Any real signature path requires proof-profile
decisions, dependency review, test-vector evidence, encoding decisions, and
fail-closed verifier integration.

## Current research direction

The current post-quantum signature research direction is:

1. ML-DSA-65 as the first passport signature research target;
2. SLH-DSA as an independent backup signature-family direction;
3. ML-KEM as future key-establishment research, not a passport signature
   algorithm;
4. algorithm agility so the model is not permanently tied to one algorithm,
   parameter set, proof format, or library;
5. migration planning so old and new evidence can be handled safely during
   transition periods.

Hybrid or multi-signature approaches may be researched later, but they should
not be assumed until tested.

## Runtime and vector evidence

Runtime and vector research is evidence-gathering, not adoption.

Candidate runtime paths include:

1. Python `cryptography` ML-DSA support;
2. Open Quantum Safe `liboqs` and appropriate bindings;
3. other maintained ML-DSA-capable runtimes only after source, license,
   maintenance, dependency, and security review.

Current research has recorded isolated ML-DSA-65 runtime and test-vector work.
That evidence helps decide whether a future verifier integration is practical,
but it does not approve dependency adoption or real signature verification.

NIST/ACVP-style vector material is important because future signature work should
be tested against authoritative or well-understood vectors before it is trusted.

## What future research should test

Future post-quantum research may test:

1. supported proof profiles;
2. public-key encoding;
3. signature encoding;
4. signed-byte selection;
5. valid and invalid ML-DSA verification cases;
6. unsupported-algorithm failure;
7. malformed-key failure;
8. malformed-signature failure;
9. wrong-key failure;
10. modified-payload failure;
11. runtime-unavailable failure;
12. runtime-exception fail-closed behavior;
13. key rotation and algorithm migration;
14. audit evidence for signature results.

These tests should use dummy data and isolated environments until the project
records a separate adoption decision.

## Future work

Future post-quantum readiness work may include:

1. proof-profile alignment with signed-data standards;
2. dependency adoption review;
3. expanded NIST/ACVP vector compatibility;
4. SLH-DSA backup-profile research;
5. hybrid migration research;
6. long-term evidence replay;
7. key rotation and retirement policy;
8. migration guidance for later QSAG layers.

These areas should be researched in small steps and recorded through tests,
focused evidence, and review.

## Non-goals

This document does not define:

1. a production cryptographic policy;
2. a final proof suite;
3. a final signature container;
4. a key-management system;
5. a secure-channel design;
6. dependency adoption;
7. real signature verification;
8. production post-quantum security;
9. legal, compliance, or certification readiness.

The model should remain narrow, testable, and aligned with the README, ROADMAP,
tests, and evidence records.
