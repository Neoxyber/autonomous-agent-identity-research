# Human Oversight Model

## Purpose

This document defines the human oversight model for autonomous-agent identity.

Human oversight explains when an autonomous-agent action should require human
approval, human review, escalation, pause, or intervention.

This model may change as the research develops and as standards, tests, and
review feedback improve the project.

## Why it matters

Autonomous agents may act quickly, repeatedly, and across multiple systems.

Some actions should not continue only because an agent has identity evidence,
tool access, or a matching permission entry. A human may need to understand the
context, risk, authority, and expected effect before the action continues.

The gap is:

How can a verifier decide when an autonomous-agent action needs human approval,
human review, escalation, or intervention before it is trusted?

## Core rule

Human oversight is not only approval.

The model should support:

1. approval;
2. denial;
3. review;
4. escalation;
5. pause;
6. intervention.

Human approval can satisfy approval-required actions only when the approval is
valid, specific, and bound to the same decision context.

Human approval cannot override:

1. prohibited actions;
2. failed identity verification;
3. missing issuer trust;
4. expired passports;
5. revoked, suspended, compromised, or retired lifecycle states;
6. stale or failed revocation evidence;
7. missing audit context;
8. current enforcement boundaries.

## Approval and review

`REQUIRE_HUMAN_APPROVAL` means the action may continue only after valid approval
evidence is provided and validated.

`REQUIRE_HUMAN_REVIEW` means the system cannot safely decide and a human must
review the case before another decision is made.

A human click should not be treated as meaningful approval unless the human has
enough context, authority, and time to make the decision.

## Approval evidence

Approval evidence should be specific and limited.

It should identify or reference:

1. the agent;
2. the operator or controller;
3. the requested action;
4. the resource scope;
5. the reason approval was required;
6. the approver or approval authority;
7. the approval decision;
8. the approval time;
9. the approval expiry, if applicable;
10. the decision or audit event being approved.

Approval evidence should not grant broad or permanent authority unless a later
policy model explicitly supports that boundary.

## Context shown to humans

A reviewer or approver should be shown enough context to understand the decision.

Useful context may include:

1. agent identity;
2. operator or controller reference;
3. requested action;
4. resource or system affected;
5. risk level or reason for review;
6. lifecycle status;
7. revocation status;
8. permission category;
9. expected effect;
10. audit requirement.

The project should avoid exposing unnecessary sensitive data while still giving
the human enough information to decide responsibly.

## Current boundary

The repository includes local approval evidence preparation and approval
validation boundaries.

These boundaries are inert. They do not execute actions, store approvals,
enforce expiry, prevent replay, call gateways, call tools, or create a passport
verifier `ALLOW` path.

Current human oversight research does not define a final user interface,
approval workflow, storage system, escalation system, emergency stop mechanism,
or production governance process.

## Future work

Future human oversight research may include:

1. approval expiry enforcement;
2. replay protection;
3. multi-approver policies;
4. escalation paths;
5. emergency stop and pause behavior;
6. approval storage;
7. reviewer context minimization;
8. cross-organization dummy approval scenarios;
9. later gateway enforcement integration.

These areas should be researched in small steps and recorded through tests,
focused evidence, and review.
