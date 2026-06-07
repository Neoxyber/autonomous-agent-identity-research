# Audit Model

## Purpose

This document defines the audit model for autonomous-agent identity.

Audit evidence explains what an agent requested, what evidence was available,
which decision was made, and why that decision was made.

This model may change as the research develops and as standards, tests, and
review feedback improve the project.

## Why it matters

Autonomous agents may act quickly, repeatedly, and across systems.

Without audit evidence, it becomes difficult to understand which agent requested
an action, which operator was responsible, which checks passed or failed, and
why a decision was returned.

The gap is:

How can autonomous-agent action decisions be reviewed later without collecting
unnecessary sensitive data?

## Core rule

Audit evidence should support review, accountability, human oversight,
revocation analysis, incident response, and research evaluation.

Audit evidence should be useful, but minimized.

The project should prefer identifiers, references, hashes, scopes, timestamps,
decision reasons, and check results over raw sensitive content.

## Audit scope

The audit model focuses on three areas:

1. action-decision evidence;
2. lifecycle and revocation evidence;
3. human oversight evidence.

### Action-decision evidence

Action-decision evidence should help explain:

1. which agent requested an action;
2. which operator or controller was responsible;
3. which passport or evidence was presented;
4. which issuer and trust boundary applied;
5. which action and resource scope were requested;
6. which checks passed or failed;
7. which decision was returned;
8. why the decision was returned.

### Lifecycle and revocation evidence

Lifecycle and revocation evidence should help explain:

1. which lifecycle state was known;
2. which revocation or status evidence was available;
3. whether status evidence was fresh enough;
4. whether the agent was active, suspended, revoked, expired, compromised, or
   retired;
5. why trust continued or failed closed.

### Human oversight evidence

Human oversight evidence should help explain:

1. whether approval or review was required;
2. who approved, denied, reviewed, or escalated the decision;
3. what action and resource scope the approval covered;
4. when the oversight decision was made;
5. whether approval evidence was bound to the same decision context.

## Minimum useful fields

Audit evidence may include:

1. event identifier;
2. event type;
3. timestamp or caller-provided occurrence time;
4. agent identifier;
5. operator or controller identifier;
6. issuer identifier;
7. passport identifier or hash;
8. requested action;
9. resource scope;
10. lifecycle status;
11. revocation reference or status summary;
12. verification decision;
13. authorization decision;
14. composed decision;
15. decision reason;
16. check results;
17. approval or review reference, if applicable.

Not every field is required for every event. Future schemas should define
required and optional fields for each event type.

## Data minimization

Audit evidence should avoid storing unnecessary personal data, secrets,
credentials, private prompts, sensitive documents, full tool outputs, or full
operational content.

When possible, audit evidence should record references, hashes, identifiers,
scopes, and decision reasons instead of raw content.

Audit minimization is part of the research because autonomous agents may create
many events at high speed. More audit data is not automatically better if it
makes review harder or increases privacy and security risk.

## Tamper evidence

Future audit research may study tamper evidence.

Possible mechanisms include hashes, event chaining, signed summaries, signed
audit batches, timestamping, or external anchoring.

These mechanisms are future research only. The current local audit preparation
boundary does not store, hash, chain, sign, transmit, or persist audit events.

## Current boundary

The repository includes local audit event preparation.

The current audit builder is deterministic and in-memory. It prepares limited
audit evidence from already-produced verification, authorization, and composed
decision results.

It does not store audit records, write files, use a database, transmit events,
hash events, sign events, chain events, call gateways, execute tools, or create a
passport verifier `ALLOW` path.

Current audit research does not define a final audit schema, storage system,
retention policy, transparency service, timestamping provider, user interface, or
production audit process.

## Future work

Future audit research may include:

1. event schemas for different decision types;
2. tamper-evident audit summaries;
3. audit minimization tests;
4. approval and revocation evidence links;
5. replayable decision records;
6. cross-organization dummy audit scenarios;
7. retention and deletion policy research;
8. later gateway and storage integration.

These areas should be researched in small steps and recorded through tests,
focused evidence, and review.
