# Evaluation Method

## Purpose

This document defines how the project evaluates autonomous-agent identity research.

The goal is to keep the research testable, evidence-based, and easy to review.

Detailed test evidence belongs in focused result documents, test files, or evidence-log milestones.

## Core position

Research findings should be tested and reviewed before they guide implementation.

The project should record:

1. what passed;
2. what failed;
3. what worked only partly;
4. what was blocked;
5. what still needs research.

The current repository includes automated tests. Future work should continue using small, focused tests before adding wider implementation behavior.

## Result categories

Research and test results use these categories:

| Category | Meaning |
|---|---|
| PASS | The test or review met the expected result. |
| FAIL | The test or review did not meet the expected result. |
| PARTIAL | The result worked in some conditions but not all. |
| BLOCKED | The work could not continue because a dependency, decision, environment, or implementation was missing. |
| NEEDS_RESEARCH | The result raised a question that needs more study before implementation continues. |

A PARTIAL or BLOCKED result is useful when it explains what still needs to be understood.

## Evidence discipline

The project uses two levels of evidence.

The research log records meaningful milestones. A milestone entry should usually record the date, type, summary, affected files, result, tests or checks run, important limitations, not-implemented areas, and next step.

Focused result documents may record deeper experiment detail. When useful, they should include the test purpose, input or scenario, expected result, observed result, result category, environment, limitations, and follow-up work.

This separation keeps the research log chronological and readable while allowing technical experiments to remain detailed.

As the research matures, the evidence format, test records, and result documents may be improved. The goal is to keep them aligned with the README, ROADMAP, tests, industry expectations, and reviewer needs while making the work easier to understand.

## Current evaluation focus

The current evaluation focus is QSAG Layer 1:

Agent identity and action-decision evidence.

The most important test areas are:

1. fail-closed verifier behavior;
2. malformed and duplicate-key JSON rejection;
3. schema and lifecycle validation;
4. issuer trust and revocation freshness boundaries;
5. proof selection and proof/key binding;
6. canonical payload preparation and payload-hash consistency;
7. signature adapter-interface planning;
8. authorization, approval, audit, and enforcement composition boundaries;
9. sensitive-data minimization in audit and approval evidence;
10. dummy cross-organization scenarios.

The verifier should not return `ALLOW` until the required signature, trust, revocation, policy, audit, and enforcement gates are intentionally connected and tested.

## Negative testing

Negative tests are central to this project.

The project should test malformed, missing, stale, mismatched, unsupported, expired, revoked, compromised, and ambiguous evidence.

Useful negative tests show that unsafe or unclear inputs fail closed instead of being silently accepted.

## Data and isolation rules

Research tests should use dummy data only unless a later decision explicitly justifies another approach.

The repository should not include real users, real organization secrets, private keys, production credentials, live agent logs, or confidential operational data.

Isolated package, vector, and runtime experiments should run outside the repository environment unless separately approved. Temporary experiment files should be summarized in evidence documents instead of being copied into the repository.

Mistakes and incomplete assumptions can happen during research. Community, academic, standards, and industry review are welcome so that issues can be found, corrected, and recorded responsibly.

## Documentation and review

Documentation is part of the research surface.

Documentation should be reviewed for:

1. outdated statements;
2. repeated explanations;
3. unsafe commands;
4. hidden assumptions;
5. unsupported production, compliance, or certification language;
6. broken links;
7. mismatch with README, ROADMAP, tests, or evidence records.

The goal is to keep the project understandable as it grows.

## Current boundary

This document defines evaluation discipline for the research project.

It does not define a final benchmark suite, production certification process, compliance process, deployment test plan, or complete security assessment.

The evaluation method may change as the research matures, but changes should keep the project narrow, evidence-based, and reviewable.
