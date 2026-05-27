# Audit Model

## Purpose

This document defines the first audit model for autonomous agent identity.

The audit model explains what evidence should be recorded when an agent requests an action, when a decision is made, when human oversight is used, and when an agent lifecycle state changes.

## Core position

Audit evidence is not only for debugging.

Audit evidence supports traceability, human oversight, revocation review, incident response, research evaluation, and future compliance mapping.

The system should record enough evidence to explain what happened, why it happened, and what information was available at the time.

## Audit scope

The audit model should cover three main areas.

1. Decision audit.

2. Lifecycle audit.

3. Human oversight audit.

## Decision audit

Decision audit records important agent action requests and system decisions.

Examples include:

1. Agent requested an action.

2. Passport was verified.

3. Action was allowed.

4. Action was denied.

5. Human approval was required.

6. Human review was required.

7. Verification failed.

8. Revocation evidence was unavailable or stale.

Decision audit should record both allowed and denied actions.

## Lifecycle audit

Lifecycle audit records changes to agent identity and trust state.

Examples include:

1. Passport issued.

2. Passport renewed.

3. Passport expired.

4. Agent suspended.

5. Agent revoked.

6. Agent marked compromised.

7. Key material rotated.

8. Agent restored after suspension.

Lifecycle audit is required because identity status affects whether an agent should be trusted to act.

## Human oversight audit

Human oversight audit records human intervention.

Examples include:

1. Human approved an action.

2. Human denied an action.

3. Human requested more information.

4. Human escalated the case.

5. Human paused the agent.

6. Human triggered emergency stop.

7. Human reviewed a failed or uncertain decision.

Human oversight evidence should show who acted, what authority they had, what context they saw, and what decision they made.

## Minimum audit questions

Audit evidence should help answer these questions:

1. Which agent made the request?

2. Which operator was responsible?

3. Which passport was used?

4. Which policy was applied?

5. What action was requested?

6. What resource or system was affected?

7. What decision was made?

8. Why was the decision made?

9. Was human oversight used?

10. What lifecycle state was known at the time?

11. What revocation evidence was available?

12. What verification mode was used?

13. What failed or needs improvement?

## Initial audit fields

The initial audit model should support these fields:

1. event_id

2. event_type

3. timestamp

4. agent_id

5. operator_id

6. passport_id

7. passport_hash

8. policy_id

9. policy_hash

10. requested_action

11. resource_scope

12. decision

13. decision_reason

14. verification_mode

15. lifecycle_status

16. revocation_evidence

17. human_oversight_id

18. approver_or_reviewer_id

19. evidence_hash

20. previous_event_hash

Not every field is required for every event. The final schema will define required and optional fields later.

## Decision outcomes

The audit model should record the decision outcome.

Initial outcomes are:

1. ALLOW

2. DENY

3. REQUIRE_HUMAN_APPROVAL

4. REQUIRE_HUMAN_REVIEW

5. ERROR

The ERROR outcome is used when the system cannot complete evaluation due to missing data, verification failure, service failure, or unexpected conditions.

## Evidence available at decision time

Audit evidence should record what information was available when the decision was made.

This matters because later information may change.

For example, an agent may be revoked after an action was already evaluated. The audit record should show the status evidence that was available at the decision time.

## Tamper evidence

Audit evidence should be tamper-evident where possible.

The model should support hashing, event chaining, signed audit batches, or signed summaries.

Future research may test timestamping or anchoring hashes of audit summaries without exposing raw audit content.

## Data minimization

Audit logs should avoid storing unnecessary personal data, secrets, credentials, private prompts, sensitive documents, or full operational content.

The audit model should prefer references, hashes, identifiers, scopes, and decision reasons over raw sensitive data where possible.

## Retention

Audit retention should be based on risk, purpose, operational need, and applicable law.

This research does not define a final retention period.

Future implementation should allow retention rules to be configured and reviewed.

## Research and testing direction

The research should record what passes, what fails, and what needs improvement.

Future tests should evaluate:

1. Whether allowed actions produce audit evidence.

2. Whether denied actions produce audit evidence.

3. Whether human oversight decisions are recorded.

4. Whether revocation decisions are recorded.

5. Whether tampered audit events can be detected.

6. Whether audit evidence avoids unnecessary sensitive data.

7. Whether audit records explain the decision clearly enough for review.

## EU alignment note

This model is designed to support traceability, logging, human oversight, and record-keeping concepts relevant to EU AI governance, especially for higher-risk systems.

It does not claim legal compliance. Legal compliance requires separate legal, technical, organizational, data protection, and operational review.

## Current boundary

This document defines the initial audit model.

It does not define the final audit event schema, storage system, retention policy, transparency service, timestamping provider, user interface, or implementation. Those will be developed later through specifications, reference implementation, controlled tests, and recorded evaluation results.
