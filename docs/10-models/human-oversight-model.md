# Human Oversight Model

## Purpose

This document defines the first human oversight model for autonomous agent identity.

The model explains when a human must review, approve, deny, pause, or escalate an autonomous agent action.

## Core rule

Human oversight is not only approval.

A human oversight model should support approval, denial, review, escalation, pause, and intervention.

Human approval can authorize approval-required actions.

Human approval cannot authorize prohibited actions.

Human approval cannot allow a revoked, expired, suspended, or compromised agent to act.

Human approval cannot disable audit logging.

## Oversight and approval

Approval is one form of oversight.

Oversight is broader. It includes monitoring, understanding the action, reviewing the context, intervening when needed, and stopping or escalating unsafe activity.

The system should not treat a human click as meaningful approval unless the human has enough context, authority, and time to make the decision.

## Decision outcomes

The first model uses four decision outcomes:

1. ALLOW

2. DENY

3. REQUIRE_HUMAN_APPROVAL

4. REQUIRE_HUMAN_REVIEW

REQUIRE_HUMAN_APPROVAL means the action may proceed only after an authorized human approves it.

REQUIRE_HUMAN_REVIEW means the system cannot safely decide and a human must review the case before any further decision.

## Action risk levels

Actions should be classified by risk.

1. Low-risk actions may be allowed automatically if identity and policy checks pass.

2. Medium-risk actions may require approval depending on context.

3. High-risk actions should require approval or review.

4. Prohibited actions should always be denied.

5. Unknown actions should be denied or sent to human review depending on policy.

6. Actions from revoked, expired, suspended, or compromised agents should always be denied.

## Approver requirements

An approver should be identifiable, authorized, and appropriate for the action.

The approval record should identify:

1. Who approved or reviewed the action.

2. What role or authority they had.

3. What action was reviewed.

4. What context was shown.

5. What decision was made.

6. When the decision was made.

## Approval context

Before approving an action, the human should be shown enough context to understand the decision.

The context should include:

1. Agent identity.

2. Operator identity.

3. Requested action.

4. Resource or system affected.

5. Risk level.

6. Reason approval or review is required.

7. Passport status.

8. Revocation status.

9. Expected effect of the action.

10. Audit requirement.

## Limits of approval

Approvals should be specific and limited.

An approval should not grant broad or permanent authority unless the policy explicitly supports that and the risk is acceptable.

A good approval is tied to a specific action, agent, resource scope, purpose, and time window.

## Expiry and replay protection

Human approvals should expire.

An approval should not be reusable forever. The system should prevent old approvals from being replayed for a different action, different agent, different resource, or different time period.

## Escalation

The model should support escalation when the reviewer cannot safely decide.

Escalation may be required when:

1. The action is outside normal scope.

2. The agent behaviour is unusual.

3. The requested action affects sensitive data or critical systems.

4. The verifier cannot determine whether the request is safe.

5. The policy requires more than one approver.

## Audit evidence

Human oversight decisions should produce audit evidence.

The audit record should include the agent, operator, requested action, approver, decision, reason, timestamp, approval expiry, passport reference, and policy reference.

## Research and testing direction

This model defines what the project will research and test.

The research will study how human oversight should work for autonomous agent identity, including approval, denial, review, escalation, pause, intervention, and audit evidence.

Future tests should record:

1. Which oversight decisions pass.

2. Which oversight decisions fail.

3. Which decisions require more context.

4. Which actions require stronger controls.

5. Which parts of the model need improvement.

The results should be recorded as research evidence rather than hidden inside implementation notes.

Future research will also study emergency stop and kill switch behaviour for autonomous agents, including when an agent should be paused, suspended, revoked, or prevented from continuing a workflow.

## EU alignment note

This model is designed to support human oversight concepts relevant to EU AI governance, especially for higher-risk systems.

It does not claim legal compliance. Legal compliance requires separate legal, technical, organizational, and operational review.

## Current boundary

This document defines the initial human oversight model.

It does not define the final user interface, schema, approval workflow, kill switch mechanism, or implementation. Those will be developed later through specifications, reference implementation, controlled tests, and recorded evaluation results.
