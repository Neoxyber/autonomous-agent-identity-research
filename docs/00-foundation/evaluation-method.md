# Evaluation Method

## Purpose

This document defines the first evaluation method for autonomous agent identity research.

The evaluation method explains how the project will test the research models, record results, and identify what needs improvement before implementation expands.

## Core position

Research claims should be tested.

The project should record what passes, what fails, what is unclear, what is blocked, and what needs more research.

Results should be recorded as evidence, not hidden in implementation notes.

## Evaluation scope

The first evaluation scope includes:

1. Agent passport verification.

2. Permission evaluation.

3. Human oversight decisions.

4. Revocation and lifecycle checks.

5. Decentralized verification evidence.

6. Audit evidence.

7. Post-quantum readiness.

8. Documentation security.

## Result categories

Each evaluation should use clear result categories.

1. PASS

2. FAIL

3. PARTIAL

4. BLOCKED

5. NEEDS_RESEARCH

PASS means the test met the expected result.

FAIL means the test did not meet the expected result.

PARTIAL means the result worked in some conditions but not all.

BLOCKED means the test could not be completed because a dependency, implementation, library, or environment was missing.

NEEDS_RESEARCH means the result raised a question that needs further study before implementation continues.

## Evidence record

Each evaluation should record:

1. Test name.

2. Test purpose.

3. Date.

4. Model area tested.

5. Input used.

6. Expected result.

7. Actual result.

8. Result category.

9. Evidence location.

10. Limitations.

11. Follow-up work.

The evidence should be clear enough for another reviewer to understand what was tested and why the result was recorded.

## First tests

The first tests should be simple and controlled.

Initial tests include:

1. Create a sample agent passport.

2. Verify a valid passport offline.

3. Reject a modified passport.

4. Deny a prohibited action.

5. Allow an explicitly permitted action.

6. Require human approval for an approval-required action.

7. Require human review for an uncertain action.

8. Deny action from a revoked agent.

9. Record an audit event for each decision.

10. Record what needs improvement.

## Verification tests

Verification tests should check whether the system can verify identity evidence.

Examples include:

1. Passport structure validation.

2. Signature verification.

3. Expiry check.

4. Issuer key check.

5. Passport hash check.

6. Offline verification.

7. Online status check when available.

8. Tamper detection.

## Permission tests

Permission tests should check whether the permission model behaves correctly.

Examples include:

1. Allowed action returns ALLOW.

2. Prohibited action returns DENY.

3. Approval-required action returns REQUIRE_HUMAN_APPROVAL.

4. Unknown action returns DENY or REQUIRE_HUMAN_REVIEW depending on policy.

5. Revoked agent cannot act.

6. Expired agent cannot act.

## Human oversight tests

Human oversight tests should check whether approval and review are handled correctly.

Examples include:

1. Approval is specific to an action.

2. Approval expires.

3. Approval cannot override prohibited actions.

4. Approval cannot allow a revoked or compromised agent to act.

5. Human review produces audit evidence.

6. Escalation can be recorded.

7. Emergency stop or pause behaviour can be recorded.

## Revocation tests

Revocation tests should check whether lifecycle status is enforced.

Examples include:

1. Active agent can be evaluated normally.

2. Suspended agent is denied.

3. Revoked agent is denied.

4. Expired agent is denied.

5. Compromised agent is denied.

6. Rotated key material is handled correctly.

7. Emergency stop behaviour is recorded.

## Decentralized verification tests

Decentralized verification tests should check whether verification can work without depending only on one central service.

Examples include:

1. Offline passport verification.

2. Signed issuer metadata verification.

3. Signed revocation list verification.

4. did:web verification research.

5. did:key verification research.

6. Timestamp proof research.

7. Verification under network failure.

8. Multi-organization verification.

## Audit tests

Audit tests should check whether decisions produce useful evidence.

Examples include:

1. Allowed action creates audit evidence.

2. Denied action creates audit evidence.

3. Human oversight creates audit evidence.

4. Revocation creates audit evidence.

5. Tampered audit evidence can be detected.

6. Audit evidence avoids unnecessary sensitive data.

7. Audit evidence explains the decision clearly enough for review.

## Post-quantum tests

Post-quantum tests should check whether the identity model can support long-term cryptographic migration.

Examples include:

1. ML-DSA key generation.

2. ML-DSA passport signing.

3. ML-DSA passport verification.

4. SLH-DSA backup signing.

5. SLH-DSA backup verification.

6. Dual-signature passport verification.

7. Signature size comparison.

8. Verification latency.

9. Passport payload size.

10. Key rotation.

11. Algorithm migration.

12. Failure when a signature is modified.

13. Failure when passport claims are modified.

14. Failure when the verifier does not support the algorithm.

15. ML-KEM experiments when secure key establishment becomes in scope.

## Documentation security tests

Documentation is part of the attack surface.

Future evaluation should include checks for:

1. Hidden Unicode characters.

2. Suspicious shell command patterns.

3. Embedded scripts.

4. Secrets in documents.

5. Unsafe links.

6. Misleading instructions.

The project should prefer reputable security tools where possible and use small custom checks only where needed.

## Recording results

Detailed test results should later be recorded in Empirical Testing Logs.

The research log records project progress.

Empirical Testing Logs record test method, evidence, result, limitation, and follow-up work.

## Implementation boundary

Implementation should begin only after the core research model has enough structure to test.

The first implementation should be minimal.

It should create, sign, verify, revoke, and evaluate an agent passport in a controlled research setting before adding databases, deployment, user interfaces, or production infrastructure.

## Current boundary

This document defines the initial evaluation method.

It does not define the final test framework, CI pipeline, benchmark suite, deployment environment, or implementation. Those will be developed later through specifications, reference implementation, controlled tests, and recorded evaluation results.
