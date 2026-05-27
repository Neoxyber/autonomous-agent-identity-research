# Permission Model

## Purpose

This document defines the first permission model for autonomous agent identity.

An autonomous agent identity should not only prove who the agent is. It should also define what authority is attached to that identity.

## Core rule

The default decision is deny.

An agent should only be allowed to perform an action when the action is explicitly allowed, the agent identity is valid, the agent is not expired or revoked, and any required human approval has been completed.

## Permission categories

The model uses three categories:

1. Allowed actions.

2. Approval-required actions.

3. Prohibited actions.

## Allowed actions

Allowed actions are actions the agent may perform when all identity and policy checks pass.

Examples include:

1. Read public data.

2. Summarize operator-owned documents.

3. Call approved APIs.

4. Generate draft reports.

5. Classify low-risk data.

6. Answer internal knowledge questions.

7. Execute approved workflow steps.

Allowed actions should be specific and limited. Broad permissions such as full access, all tools, or all data should be avoided.

## Approval-required actions

Approval-required actions are actions that may be possible, but should not execute until an authorized human approves them.

Examples include:

1. Sending external communications.

2. Changing customer records.

3. Accessing sensitive internal data.

4. Making configuration changes.

5. Initiating financial or contractual steps within a defined limit.

Approval should record who approved the action, what was approved, when approval was granted, and how long the approval remains valid.

## Prohibited actions

Prohibited actions are actions the agent must not perform.

Examples include:

1. Hide its identity.

2. Impersonate a human.

3. Use shared human credentials.

4. Access data outside scope.

5. Modify its own permissions.

6. Disable audit logging.

7. Create child agents without permission.

8. Delegate authority without a delegation credential.

9. Call unapproved tools.

10. Exfiltrate secrets.

11. Bypass gateway enforcement.

12. Operate after revocation.

A prohibited action should remain denied even if the agent has technical access to a tool or environment that could perform it.

## Decision outcomes

The first model uses three decision outcomes:

1. ALLOW

2. DENY

3. REQUIRE_HUMAN_APPROVAL

Each denial or approval requirement should include a reason, such as invalid identity, expired passport, revoked agent, action outside scope, prohibited action, approval required, or approval expired.

## Relationship to the agent passport

The agent passport should include or reference the permission model that applies to the agent.

The passport should express allowed actions, approval-required actions, prohibited actions, the default decision, policy version, and audit requirement.

## Evaluation order

A gateway or verifier should evaluate a request in this order:

1. Verify the agent identity.

2. Check expiry and lifecycle status.

3. Check revocation status.

4. Check whether the action is prohibited.

5. Check whether the action is allowed.

6. Check whether human approval is required.

7. Record the decision.

8. Return ALLOW, DENY, or REQUIRE_HUMAN_APPROVAL.

## Current boundary

This document defines the initial permission model.

It does not define the final schema, policy language, user interface, or implementation. Those will be developed later through specifications, reference implementation, and controlled tests.
