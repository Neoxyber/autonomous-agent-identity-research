# Limitations

## Purpose

This document records current limitations of the autonomous agent identity research.

The goal is to keep the research honest about what is implemented, what is planned, what is experimental, what is deferred, and what remains unresolved.

This research is expected to improve over time. Mistakes, incomplete assumptions, outdated wording, or missed issues can happen during research. Review and guidance from the community, academia, standards groups, and industry are helpful so the work can be corrected and improved responsibly.

## Research stage

This is research-stage work.

The repository contains research models, specifications, focused planning documents, deterministic local helpers, verifier-boundary checks, and automated tests.

It is not a production system.

## No production readiness

The research is not ready to be used as a production identity service, authorization gateway, revocation registry, audit system, cryptographic library, cloud deployment, or post-quantum security product.

Production use would need separate maturity work, security review, operational controls, incident response planning, deployment hardening, and independent review.

## No legal or compliance status

The research does not establish compliance with any legal, regulatory, certification, or governance framework.

It may study accountability, transparency, human oversight, logging, revocation, and long-term cryptographic migration, but legal or regulatory use needs separate professional review.

## No final standard

The models, schemas, field names, proof profiles, decision outcomes, and implementation boundaries may change as the research develops.

The research aims to build with existing standards and emerging work where appropriate. It does not claim to replace them.

## Current verifier boundary

The local verifier remains fail-closed.

Real signature verification, cryptographic runtime dependency adoption, live issuer registry, live revocation service, production policy engine, audit storage, gateway enforcement, cloud deployment, external integrations, and passport verifier `ALLOW` behavior are not implemented.

## Canonicalization boundary

The current canonicalization helper is research-stage and current-profile focused.

REF-014 adoption is deferred. Canonicalizer replacement, requirements changes, lockfile changes, golden-vector migration, and full RFC 8785/JCS conformance remain separate future decisions.

## Signature boundary

Signature planning and isolated ML-DSA research have been recorded, but real passport signature verification is not implemented.

Future signature work needs proof-profile decisions, dependency review, encoding decisions, test-vector evidence, and fail-closed verifier integration.

## Post-quantum uncertainty

Post-quantum readiness is a research direction, not a security assurance.

ML-DSA, SLH-DSA, ML-KEM, runtime support, parameter choices, proof formats, and deployment guidance may change over time. The research needs to remain cryptographically agile.

## Decentralized verification limits

Decentralized verification is future research.

The repository does not implement a live DID method, decentralized registry, transparency service, blockchain anchoring system, or multi-organization trust network.

## Human oversight limits

Human oversight research does not define a final user interface, approval workflow, escalation process, emergency stop system, or governance process.

Approval evidence is currently local and inert. It does not execute actions, store approvals, enforce expiry, prevent replay, or create a passport verifier `ALLOW` path.

## Revocation limits

The verifier currently supports caller-provided revocation freshness evidence.

It does not perform network lookup, registry lookup, signed status verification, signed revocation-list verification, emergency stop handling, or replay protection beyond the freshness window.

## Audit limits

The audit builder is deterministic and in-memory.

It prepares limited audit evidence from already-produced results. It does not store records, write files, use a database, transmit events, hash events, sign events, chain events, call gateways, execute tools, or create a passport verifier `ALLOW` path.

## Data limits

Research tests use dummy data unless a later decision records why another approach is needed.

The repository is not intended to contain real users, real organization secrets, private keys, production credentials, live agent logs, or confidential operational data.

## Documentation limits

Documentation can become outdated as the research changes.

The research will try to keep documents short, aligned, and easy to review, but missed issues can happen. Documents need periodic review for repetition, stale statements, unsafe commands, broken links, unsupported production language, and mismatch with tests or evidence.

## Current boundary

This document can be updated when meaningful research boundaries change.

Small wording cleanup does not need an evidence-log entry unless it changes a research boundary.
