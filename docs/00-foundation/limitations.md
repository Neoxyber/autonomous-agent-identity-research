# Limitations

## Purpose

This document records the current limitations of the autonomous agent identity research.

The purpose is to keep the project honest, reviewable, and clear about what has been defined, what has not been implemented, and what still needs research and testing.

## Research-stage work

This repository is currently in the research model stage.

The documents define initial models for identity, permissions, human oversight, revocation, decentralized verification, audit evidence, post-quantum readiness, and evaluation.

The repository does not yet provide a production system.

## No production readiness claim

This project does not currently claim production readiness.

The current work should not be used as a production identity service, authorization gateway, compliance system, revocation registry, audit system, or post-quantum security product.

A production system would require implementation, testing, security review, operational controls, incident response processes, deployment hardening, and independent review.

## No legal compliance claim

This repository does not claim compliance with the EU AI Act, GDPR, UK law, cybersecurity regulation, financial regulation, healthcare regulation, or any other legal framework.

The research may discuss concepts that are relevant to governance, traceability, human oversight, logging, accountability, and post-quantum transition.

Legal compliance requires separate legal, technical, organizational, and operational review.

## No final standardization claim

The models in this repository are not standards.

They are research models intended to be tested, refined, and compared with relevant standards, guidance, and industry practice.

Future work may change field names, decision outcomes, schemas, algorithms, verification methods, and implementation details.

## No custom cryptography

The project will not design or implement custom cryptographic algorithms.

Post-quantum research should use respected and maintained cryptographic libraries.

Any cryptographic experiment in this repository should be treated as research until reviewed and tested.

## Post-quantum uncertainty

Post-quantum readiness is a design goal, not a guarantee.

The project currently treats ML-DSA, SLH-DSA, and ML-KEM as research candidates based on current post-quantum standardization direction.

Algorithm choices, parameter sets, proof formats, libraries, and deployment guidance may change over time.

The system must remain cryptographically agile.

## Canonicalization compatibility limit

The declared canonicalization scheme names the JSON Canonicalization Scheme as the long-term target, but the current research helper is not a complete independent RFC 8785 implementation.

The current canonicalization tests document the helper's deterministic behaviour for the current research passport profile only. They do not establish full RFC 8785 or JSON Canonicalization Scheme compliance.

Real signature verification is blocked until this canonicalization compatibility is resolved. The decision is recorded in specs/canonicalization.md.

## DID and decentralized verification limits

DID support is a research direction, not a first-version dependency.

The project may evaluate did:web and did:key first because they are practical for early testing.

The project does not currently depend on a blockchain-based DID method.

Blockchain anchoring, transparency services, and decentralized registries require further funding, testing, security review, and operational design.

## Blockchain boundary

Blockchain is not treated as a required foundation.

The project may research timestamping or anchoring hashes of passports, policies, revocation lists, or audit summaries.

The project should not place agent passports, secrets, personal data, private documents, or operational details on a public blockchain.

## Human oversight limits

The human oversight model is an initial research model.

It does not define the final user interface, approver workflow, escalation process, training requirement, organizational role model, or kill switch implementation.

Future research must test whether humans are given enough context, authority, and time to make meaningful decisions.

## Revocation limits

The revocation model does not yet define the final registry, status endpoint, signed revocation list format, cache policy, or offline freshness rules.

Offline verification may not know the latest revocation state unless fresh evidence is available.

This limitation must be tested and documented.

## Audit limits

The audit model does not yet define the final schema, storage system, retention policy, access control model, evidence export format, or tamper-evidence mechanism.

Audit evidence must avoid unnecessary sensitive data.

Retention rules require legal and operational review.

## Evaluation limits

The evaluation method defines how tests should be recorded, but the tests have not yet been implemented.

Future results may show that some parts of the model are incomplete, too complex, too expensive, too slow, or unsuitable for certain environments.

Failures should be recorded and used to improve the model.

## Documentation security limits

Documentation can contain mistakes, outdated assumptions, hidden characters, unsafe commands, or misleading instructions.

Future work should add documentation security checks using reputable tools where possible and small custom checks where necessary.

Documentation should be treated as part of the attack surface.

## Implementation boundary

Implementation should begin only after the core research model has enough structure to test.

The first implementation should be minimal and should focus on creating, signing, verifying, revoking, and evaluating an agent passport in a controlled research setting.

Databases, deployment, user interfaces, production infrastructure, and commercial service features should come later.

## Current boundary

This document records the current known limitations.

It should be updated as the research model, specifications, implementation, tests, and evidence records evolve.
