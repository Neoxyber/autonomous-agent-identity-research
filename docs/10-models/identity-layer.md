# Identity Layer Model

## Purpose

This document defines the identity-layer model for autonomous agents.

The identity layer exists to make autonomous-agent actions visible, verifiable,
permission-scoped, revocable, and auditable.

This model may change as the research develops and as standards, tests, and
review feedback improve the project.

## Core question

The identity layer supports one verifier-side question:

What must be checked before an autonomous AI agent action is trusted?

Identity alone is not enough to authorize an action. A verifier also needs
evidence about issuer trust, lifecycle status, revocation freshness, permission
scope, approval requirements, proof material, and audit context.

## Current boundary

This is a research model.

It does not define a final protocol, production service, compliance framework,
deployment architecture, or completed signature-verification system.

The current verifier remains fail-closed. Real signature verification,
dependency adoption, live issuer registry, live revocation service, production
policy engine, audit storage, gateway enforcement, and verifier `ALLOW` behavior
are not implemented.

## Core entities

### Agent

An agent is an autonomous or semi-autonomous software actor that can reason,
select actions, call tools, access services, or execute workflow steps.

An agent may use human accounts, service accounts, workloads, devices, or
applications, but it should have its own identity when it acts with autonomy.

### Operator

An operator is the responsible party for an agent.

The operator may be a person, organization, legal entity, research group, system
owner, or other accountable controller. The identity model should make
responsibility explicit while avoiding unnecessary exposure of personal or
sensitive information.

### Issuer

An issuer is the party that issues identity evidence for the agent.

The verifier should not treat every issuer as trusted. Issuer trust must be
configured, checked, and recorded as a separate boundary.

### Verifier

A verifier checks identity and action-decision evidence before a protected
action is trusted.

A verifier may later be part of a gateway, service, workflow engine, policy
engine, registry, identity provider, security monitor, or receiving
organization. Gateway and production integration remain future work.

## Agent passport research envelope

The current repository uses an agent passport as a research envelope.

The passport helps study which evidence may need to travel together for
autonomous-agent verification.

The envelope may contain:

1. agent identifier;
2. operator reference;
3. issuer reference;
4. declared purpose;
5. risk class;
6. lifecycle status;
7. issue and expiry times;
8. public-key metadata;
9. permission and prohibition references;
10. approval requirements;
11. revocation reference;
12. proof metadata;
13. payload hash;
14. audit-relevant references.

The passport is not permanent authority. It must be checked against current
trust, lifecycle, revocation, permission, approval, and audit boundaries before a
decision is made.

Future work should map this research envelope to existing or emerging standards
where appropriate.

## Lifecycle states

Current schema lifecycle states are:

1. active;
2. suspended;
3. revoked;
4. expired;
5. compromised;
6. retired.

Only `active` allows verification to continue. Other lifecycle states fail
closed.

Rotation is treated as a transition or reason, not as a `lifecycle_status`
value. Pending review is handled outside `lifecycle_status` unless a later
schema decision changes that boundary.

## Action-decision evidence

The identity layer is connected to action decisions.

Before a protected action is trusted, the verifier should be able to evaluate:

1. which agent is acting;
2. who is responsible for the agent;
3. which issuer is trusted for the agent;
4. which proof and key metadata are selected;
5. whether the passport is within its validity window;
6. whether lifecycle status allows verification;
7. whether revocation evidence is available and fresh enough;
8. whether the requested action is explicitly prohibited;
9. whether the requested action is within allowed scope;
10. whether human approval is required and valid;
11. what decision and reason should be recorded.

Detailed permission, approval, revocation, audit, decentralized verification,
and post-quantum models are maintained in their own documents.

## Decision outcomes

The wider research model uses these decision outcomes:

1. `DENY`;
2. `REQUIRE_HUMAN_APPROVAL`;
3. `REQUIRE_HUMAN_REVIEW`;
4. future `ALLOW`.

The current passport verifier does not return `ALLOW`.

A future allowed outcome should require the relevant signature, trust,
revocation, permission, approval, audit, and enforcement gates to be
intentionally connected and tested.

## Verification direction

The current technical direction is verifier-boundary research.

The verifier should continue to fail closed for malformed, missing, stale,
mismatched, unsupported, expired, revoked, compromised, or ambiguous evidence.

Future signature verification should be added only after proof-profile,
dependency, canonicalization-boundary, and verifier-integration decisions are
complete.

## Audit direction

Identity decisions should produce enough evidence for later review without
collecting unnecessary sensitive data.

Audit evidence should help explain:

1. which agent acted or requested action;
2. which operator was responsible;
3. which passport or evidence was presented;
4. which action was requested;
5. which checks passed or failed;
6. which decision was returned;
7. why the decision was made.

Detailed audit rules are maintained in the audit model and evidence documents.

## Future work

Future identity-layer work may include:

1. mapping the passport envelope to existing identity, credential, or signed-data
   formats;
2. stronger issuer trust models;
3. signed revocation or status evidence;
4. multi-organization dummy scenarios;
5. delegation and child-agent scope narrowing;
6. runtime and behavior evidence;
7. gateway enforcement integration;
8. standards-alignment review.

These areas should be researched in small steps and recorded through tests,
focused evidence, and review.

## Non-goals

This document does not define:

1. a final schema;
2. a wire protocol;
3. a production implementation;
4. a legal or compliance framework;
5. real signature verification;
6. gateway enforcement;
7. cloud deployment;
8. live multi-organization operation.

The model should remain narrow, testable, and aligned with the README, ROADMAP,
tests, and evidence records.
