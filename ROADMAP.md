# Roadmap

## Purpose

This roadmap defines the technical research path for the Autonomous Agent Identity Research repository.

The README explains the wider QSAG research direction. This roadmap focuses on the Layer 1 work: agent identity and action-decision evidence.

The roadmap may change as the research develops. Changes should be based on evidence, tests, standards review, and community or industry feedback.

## Current focus

The current research focus is:

Agent identity and action-decision evidence.

The central technical question is:

What must be checked before an autonomous AI agent action is trusted?

The current verifier remains fail-closed. It does not return `ALLOW`.

## Current technical baseline

The repository currently includes research and tests for:

1. agent passport structure;
2. schema validation;
3. duplicate JSON key rejection;
4. canonical payload preparation;
5. payload hash checks;
6. issuer trust input boundaries;
7. revocation freshness input boundaries;
8. lifecycle and expiry checks;
9. proof and key binding checks;
10. signature planning and isolated ML-DSA research;
11. local authorization, approval, audit, and enforcement composition models;
12. automated tests.

The following areas are not implemented yet:

1. real signature verification;
2. cryptographic runtime dependency adoption;
3. issuer trust registry;
4. live revocation service;
5. production policy engine;
6. audit storage;
7. gateway enforcement;
8. cloud deployment;
9. MCP or external integration;
10. verifier `ALLOW` behavior.

## Technical principle

Identity alone is not enough to trust an autonomous agent action.

A signature alone is not enough to authorize an action.

The research will continue toward a verifier model where protected actions depend on valid evidence. That evidence may include identity, issuer trust, key validity, signature proof, lifecycle status, revocation freshness, permission scope, approval requirements, and audit context.

The default posture remains fail closed.

## Stage 1: Verifier boundary review

This stage will review the existing verifier and tests to understand where future signature verification may connect.

The research will examine:

1. how the verifier prepares canonical payload bytes;
2. how the selected key is identified;
3. how proof metadata is selected and checked;
4. how unsupported or malformed proof metadata fails closed;
5. which checks already exist;
6. which adapter-interface tests may be missing;
7. how the verifier continues to avoid `ALLOW`.

This stage will not adopt dependencies, import a cryptographic runtime, change requirements, change lockfiles, or implement real signature verification.

Research output:

This stage should produce a short finding on the verifier boundary, missing adapter-interface tests, unresolved questions, and whether the next stage is ready, blocked, or needs more research.

## Stage 2: Signature adapter-interface tests

This stage will test the future signature verification boundary without adding real cryptography.

The research will use fake or stub verification behavior to test:

1. unsupported signature profile failure;
2. unsupported algorithm failure;
3. malformed public-key value failure;
4. malformed signature value failure;
5. wrong public-key length failure;
6. wrong signature length failure;
7. runtime-unavailable failure;
8. invalid-signature failure;
9. runtime-exception fail-closed behavior;
10. verified-signature result without action authorization;
11. continued prevention of accidental verifier `ALLOW`.

Research output:

This stage should show whether fake or stub adapter tests can cover the future signature boundary without importing a cryptographic runtime, and whether any boundary assumptions need to change.

## Stage 3: Proof-profile alignment

This stage will research how future signatures should be represented and verified.

The research will evaluate:

1. whether the future proof profile should align with JOSE/COSE;
2. how RFC 9964 affects ML-DSA signature representation;
3. whether signatures should verify over canonical JSON bytes or standard signed-data bytes;
4. how the current canonicalization path fits the long-term direction;
5. which public-key format should be accepted;
6. which signature format should be accepted;
7. which unsupported modes must fail closed.

Research output:

This stage should record proof-profile options, unresolved questions, standards-alignment considerations, and whether a direction is selected, deferred, or blocked.

## Stage 4: Dependency adoption review

This stage will research whether a cryptographic runtime can be adopted responsibly.

The research will review:

1. candidate runtime support for the selected proof profile;
2. package source and release artifacts;
3. license and attribution requirements;
4. maintenance and security posture;
5. version-pinning approach;
6. rollback approach;
7. impact on requirements and lockfiles;
8. handling of test keys, signatures, and generated materials.

Research output:

This stage should record whether dependency adoption is justified, blocked, or deferred, with the reasons and rollback considerations.

## Stage 5: Real signature verification

This stage will research the first real signature verification path only after proof-profile and dependency decisions are complete.

The research will test:

1. public-key decoding;
2. signature decoding;
3. public-key length validation;
4. signature length validation;
5. supported proof-profile checks;
6. verification over selected signed bytes;
7. invalid-signature failure;
8. runtime-error failure;
9. unsupported-mode failure;
10. modified-payload failure;
11. wrong-key failure;
12. preservation of existing verifier checks.

Research output:

This stage should show whether the selected signature path verifies valid cases and fails closed for invalid, malformed, unsupported, or runtime-error cases. Signature validity remains separate from action authorization.

## Stage 6: Action-decision evidence

This stage will connect verified identity evidence to action-decision evidence.

The research will define the minimum evidence needed for decisions such as denial, approval required, review required, and future allowed outcomes.

Evidence areas include:

1. agent identity;
2. operator or controller binding;
3. issuer trust;
4. key validity;
5. signature result;
6. lifecycle status;
7. revocation freshness;
8. requested action;
9. permission scope;
10. prohibition match;
11. approval requirement;
12. approval validation;
13. audit context;
14. final decision reason.

Research output:

This stage should clarify which evidence fields are needed for action decisions, which fields are unnecessary, and which parts remain unresolved.

## Stage 7: Dummy cross-organization scenarios

This stage will test Layer 1 with simulated organizations and dummy agents.

The research will use only dummy data. It will not use real users, real organizations, real secrets, production credentials, live systems, or external execution.

Example scenarios include:

1. valid identity but expired passport;
2. valid signature but revoked agent;
3. valid signature but stale revocation evidence;
4. valid signature but prohibited action;
5. approval-required action without approval;
6. approval cannot override prohibition;
7. malformed signature;
8. unsupported algorithm;
9. missing issuer trust;
10. changed payload after signing;
11. wrong key for valid signature;
12. suspended or compromised agent status.

Research output:

This stage should show how the verifier behaves in dummy cross-organization scenarios and identify any gaps before later gateway research.

## Deferred research

The following areas are important but deferred until Layer 1 is clearer and better tested:

1. agent behavior evidence;
2. runtime drift detection;
3. delegation and multi-agent chains;
4. child-agent scope narrowing;
5. gateway enforcement;
6. MCP, A2A, cloud, and workflow integration;
7. live demo deployment;
8. audit storage;
9. transparency logs;
10. real multi-organization deployment.

Deferred work may become future QSAG layers or future repositories.

## Evidence and research records

Evidence records support the research timeline and help readers understand why technical decisions were made.

The evidence log is reserved for meaningful milestones, such as new technical behavior, new tests, isolated experiment results, dependency decisions, proof-profile decisions, security-relevant findings, important failures, and blocked research results.

Small wording updates, navigation changes, and routine documentation cleanup do not normally require evidence-log entries unless they change a research boundary.

Detailed experiment evidence should remain in focused result documents, while the evidence log should stay concise and chronological.

## Simplification and review

The repository will grow as the research continues.

Some evidence logs are already long, and some documents may need to be reviewed again as the research direction becomes clearer. This is expected for a research project in a fast-moving field.

The project will periodically review existing documents and classify them as:

1. keep;
2. update;
3. merge;
4. defer;
5. archive.

The goal is to make the research easier to understand, not larger for its own sake.

The roadmap may change as the research develops. Guidance, review, and contribution from the community, academia, standards bodies, and industry are welcome.

## QSAG layers

The wider QSAG research direction is layered.

This repository covers Layer 1.

```text
QSAG Research Program
│
├── Layer 1: Agent Identity and Action-Decision Evidence
│   Current repository
│   Studies identity, authority evidence, fail-closed verification, signatures,
│   revocation freshness, approval requirements, and audit context.
│
├── Layer 2: Agent Behavior Evidence
│   Future work
│   Studies declared purpose, observed action requests, drift, and escalation.
│
├── Layer 3: Delegation and Multi-Agent Chains
│   Future work
│   Studies parent and child agents, delegated authority, scope narrowing,
│   and chain evidence.
│
├── Layer 4: Gateway Enforcement
│   Future work
│   Studies how a gateway denies, allows, or requires approval before tools,
│   APIs, MCP, workflows, or cloud calls.
│
├── Layer 5: Audit and Evidence Replay
│   Future work
│   Studies replayable decision records, tamper evidence, and
│   privacy-minimized audit.
│
└── Layer 6: Post-Quantum Migration
    Cross-cutting work
    Studies ML-DSA, SLH-DSA, algorithm agility, key rotation,
    and long-term evidence.

```
