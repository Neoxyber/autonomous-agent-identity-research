# Permission Model

## Purpose

This document defines the permission model for autonomous-agent identity.

Identity says which agent is acting. Permission says what that agent is allowed
to request.

This model may change as the research develops and as standards, tests, and
review feedback improve the project.

## Why it matters

Autonomous agents may call tools, access services, request data, or trigger
workflow steps at high speed.

A valid identity is not enough. An agent may be real, signed, active, and still
not authorized for a specific action.

The gap is:

How can a verifier decide whether an autonomous-agent action request is within
scope, needs approval, requires review, or must be denied?

## Core rule

The default decision is deny.

An action should continue only when the required identity, trust, lifecycle,
revocation, permission, approval, audit, and enforcement conditions are
intentionally checked.

Permission must not be inferred from tool access, credentials, API tokens,
runtime capability, or network reachability.

## Permission categories

The model uses three action categories:

1. allowed actions;
2. approval-required actions;
3. prohibited actions.

### Allowed actions

Allowed actions are actions the agent may request when all required checks pass.

Allowed actions should be specific and limited. Broad permissions such as all
tools, all data, full access, or administrator access should be avoided unless a
later policy model explicitly justifies them.

### Approval-required actions

Approval-required actions are actions that may be possible, but should not
continue without valid human approval evidence.

Approval should be specific to the agent, action, resource scope, purpose, and
time window where possible.

Approval evidence does not override identity failure, revocation, expiry,
compromise, prohibited actions, or missing trust evidence.

### Prohibited actions

Prohibited actions are actions the agent must not perform.

Examples include:

1. hiding its identity;
2. impersonating a human;
3. using shared human credentials;
4. accessing data outside scope;
5. modifying its own permissions;
6. disabling audit evidence;
7. creating child agents without authority;
8. delegating authority without evidence;
9. calling unapproved tools;
10. exfiltrating secrets;
11. bypassing future enforcement controls;
12. operating after revocation.

A prohibited action should remain denied even if the agent has technical access
to a tool or environment that could perform it.

## Decision outcomes

The permission model uses these decision outcomes:

1. `DENY`;
2. `REQUIRE_HUMAN_APPROVAL`;
3. `REQUIRE_HUMAN_REVIEW`;
4. `ALLOW` inside the local authorization model only.

The passport verifier currently does not return `ALLOW`.

A local authorization result of `ALLOW` does not authorize execution by itself.
Future end-to-end allow behavior requires the required signature, issuer trust,
revocation freshness, permission, approval, audit, and enforcement gates to be
connected and tested.

## Evaluation order

A permission decision should evaluate a request in this order:

1. reject malformed request or permission data;
2. confirm the default decision is `DENY`;
3. check prohibited actions first;
4. check approval-required actions;
5. check explicitly allowed actions;
6. apply the unknown-action policy;
7. record the decision reason.

Prohibited actions should take priority over allowed or approval-required
actions.

Unknown actions should fail closed to `DENY` unless a later policy explicitly
routes them to `REQUIRE_HUMAN_REVIEW`.

## Relationship to the agent passport

The agent passport may include or reference permission evidence.

That evidence may include:

1. allowed actions;
2. approval-required actions;
3. prohibited actions;
4. default decision;
5. unknown-action policy;
6. policy identifier;
7. policy version;
8. audit requirement.

The passport is not permanent authority. Permission evidence must be evaluated
with current identity, lifecycle, revocation, trust, approval, and audit context.

## Current boundary

The repository includes a local deterministic authorization evaluator.

That evaluator is separate from passport verification, approval validation, audit
preparation, enforcement composition, gateway behavior, and tool execution.

Current permission research does not define a final policy language, production
policy engine, user interface, gateway integration, storage system, or live
multi-organization enforcement model.

## Future work

Future permission research may include:

1. richer policy language;
2. delegation and child-agent scope narrowing;
3. approval expiry and replay protection;
4. policy-version binding;
5. cross-organization dummy scenarios;
6. enforcement composition;
7. gateway integration after Layer 1 is better tested.

These areas should be researched in small steps and recorded through tests,
focused evidence, and review.
