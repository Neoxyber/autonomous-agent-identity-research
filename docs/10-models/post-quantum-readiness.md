# Post-Quantum Readiness Model

## Purpose

This document defines the first post-quantum readiness model for autonomous agent identity.

The model explains how the project will prepare agent identity, verification, revocation, and audit evidence for long-term cryptographic change.

## Core position

Post-quantum readiness is a design requirement, not a marketing claim.

Autonomous agent identities may need to remain verifiable for many years. The identity layer should therefore be able to support post-quantum signatures, key rotation, algorithm migration, and cryptographic agility.

The project will not implement cryptographic algorithms from scratch.

The project will use respected and maintained cryptographic libraries for research and testing.

## Initial algorithm direction

The first research direction is:

1. ML-DSA as the primary candidate for signing agent passports.

2. SLH-DSA as an independent backup signature family.

3. ML-KEM as a future candidate for secure key establishment.

4. Hybrid transition support where classical and post-quantum mechanisms need to coexist.

5. Cryptographic agility so algorithms, parameter sets, proof formats, and key material can change over time.

## Agent passport signatures

Agent passports need signatures so verifiers can detect tampering and confirm issuer authority.

The first research implementation should evaluate ML-DSA for passport signing and verification.

The research should record:

1. Key generation behaviour.

2. Signature size.

3. Verification time.

4. Passport payload size.

5. Failure when a signed field is modified.

6. Failure when an unsupported algorithm is used.

7. Failure when a signature is missing or invalid.

## Backup signature family

The model should support an independent backup signature family.

SLH-DSA is treated as the first backup candidate because it is a hash-based signature family and gives algorithm diversity.

The project should research whether a passport should support:

1. A primary signature only.

2. A backup signature only for high-risk passports.

3. Dual signatures during migration.

4. Separate signatures for identity, policy, and revocation evidence.

The first model should not assume that every passport must always carry every possible signature.

## ML-KEM direction

ML-KEM is not a passport signature algorithm.

It is considered for future secure key establishment between agents, gateways, verifiers, and supporting services.

The first research phase should focus on signatures for identity verification. ML-KEM experiments should come later when secure channels, key exchange, or encrypted transport are in scope.

## Hybrid transition

The transition to post-quantum cryptography will not happen everywhere at the same time.

The model should support hybrid transition where needed.

Hybrid transition may include:

1. Classical and post-quantum verification during migration.

2. Dual-signature passports.

3. Policy rules that define acceptable algorithms.

4. Key rotation from classical keys to post-quantum keys.

5. Verifier behaviour for older passports.

Hybrid mode should be tested, not assumed.

## Cryptographic agility

Cryptographic agility is mandatory.

The system should be able to change:

1. Algorithms.

2. Parameter sets.

3. Key identifiers.

4. Proof formats.

5. Signature containers.

6. Verification policies.

7. Rotation rules.

The system should not permanently bind the identity model to one algorithm, library, parameter set, or proof format.

## Library direction

The project should use respected cryptographic libraries for research and testing.

The first research library direction is Open Quantum Safe, including liboqs and its language bindings where appropriate.

The purpose is controlled experimentation, not a production security claim.

The project should not use unknown or unmaintained cryptographic packages for core research results.

The project should not write custom implementations of ML-DSA, SLH-DSA, ML-KEM, or any other cryptographic primitive.

## Verification evidence

Post-quantum verification should produce audit evidence.

The audit record should be able to capture:

1. Algorithm used.

2. Parameter set.

3. Key identifier.

4. Signature identifier.

5. Verification result.

6. Verification time.

7. Passport hash.

8. Policy hash.

9. Failure reason, if verification fails.

This helps later review, migration planning, and performance evaluation.

## Key rotation

The model should support key rotation.

Key rotation may be required because of:

1. Scheduled lifecycle management.

2. Algorithm migration.

3. Key compromise.

4. Operator change.

5. Issuer policy change.

6. Research test condition.

A rotated agent or issuer should clearly indicate which key material is current and which key material is retired.

## What the project should test

The first post-quantum tests should evaluate:

1. ML-DSA key generation.

2. ML-DSA passport signing.

3. ML-DSA passport verification.

4. SLH-DSA backup signing.

5. SLH-DSA backup verification.

6. Dual-signature passport verification.

7. Signature size comparison.

8. Verification latency.

9. Passport payload size.

10. Key rotation.

11. Algorithm migration.

12. Failure when a signature is modified.

13. Failure when passport claims are modified.

14. Failure when the verifier does not support the algorithm.

15. ML-KEM experiments when secure key establishment becomes in scope.

## EU and long-term transition note

This model is designed to support long-term cryptographic migration and post-quantum readiness.

It does not claim legal compliance, production readiness, or final standardization.

Post-quantum migration requires legal, technical, operational, and security review. The project will treat post-quantum readiness as a research and testing requirement and will record what passes, what fails, what is costly, and what needs improvement.

## Current boundary

This document defines the initial post-quantum readiness model.

It does not define the final proof suite, signature container, key management system, secure channel design, deployment architecture, or production cryptographic policy. Those will be developed later through specifications, reference implementation, controlled tests, and recorded evaluation results.
