# Decentralized Verification Model

## Purpose

This document explains where decentralized verification fits in the autonomous
agent identity research.

Decentralized verification is not the current implementation focus. It is a
future research direction that becomes important when agent identity evidence
needs to be checked across organizations, systems, gateways, and trust domains.

This model may change as the research develops and as standards, tests, and
review feedback improve the project.

## Why it matters

Autonomous agents may act across more than one system or organization.

A verifier should not always need to depend on one live central service to
understand basic identity evidence. Some evidence should be portable,
inspectable, and reviewable across trust boundaries.

The research gap is not blockchain or decentralization for its own sake.

The gap is:

How can another organization verify enough agent identity and action-decision
evidence to make a fail-closed decision?

## Fit in the roadmap

Decentralized verification supports QSAG Layer 1:

Agent identity and action-decision evidence.

It connects to the current roadmap through:

1. portable agent identity evidence;
2. issuer trust boundaries;
3. public-key and proof metadata;
4. lifecycle and expiry checks;
5. revocation freshness evidence;
6. audit and decision evidence;
7. future cross-organization dummy scenarios.

The current repository does not implement a live decentralized registry,
blockchain system, DID method, transparency service, or multi-organization
deployment.

## What should be portable

Future decentralized verification research may study how a verifier can inspect
or resolve:

1. agent identity;
2. issuer identity;
3. operator or controller reference;
4. public-key metadata;
5. proof metadata;
6. lifecycle status;
7. expiry and validity windows;
8. revocation or status evidence;
9. permission and prohibition references;
10. audit or decision evidence references.

Portable evidence must still fail closed when it is missing, stale, malformed,
unsupported, or untrusted.

## Trust boundary

Decentralized verification does not remove trust decisions.

A verifier still needs to know:

1. which issuer is trusted;
2. which key is valid;
3. which proof format is supported;
4. whether status evidence is fresh enough;
5. whether the action is within scope;
6. whether approval or review is required;
7. what evidence should be recorded.

A valid portable credential or signed object should not automatically authorize
an action.

## Possible future mechanisms

Future research may evaluate:

1. signed issuer metadata;
2. signed status or revocation evidence;
3. portable credential formats;
4. decentralized identifiers such as practical DID methods;
5. transparency logs;
6. timestamp or hash anchoring;
7. replicated registries;
8. cross-organization verifier scenarios.

Blockchain-based anchoring is optional future research only. The project should
not place agent passports, secrets, personal data, private documents, or
operational details on a public blockchain.

## Current boundary

This document defines a future research model.

It does not define a final DID method, registry, transparency service,
blockchain anchoring system, timestamping provider, production trust network, or
implementation.

Current Layer 1 work should stay focused on fail-closed verifier semantics,
signature-boundary research, evidence minimization, and dummy-data-only
cross-organization scenarios.
