# Evaluation Method

## Purpose

This document explains how the research uses tests and evidence.

The goal is simple: learn carefully, record what happened, find mistakes, and
improve the work over time.

Evaluation is not a finished benchmark or security assessment. It is the way
this research stays testable and easier to review.

## Research approach

The research uses small steps.

Each meaningful step records:

1. what was tested or reviewed;
2. what passed;
3. what failed;
4. what worked only partly;
5. what was blocked;
6. what still needs more research.

This helps future work connect to earlier work instead of guessing why a
decision was made.

## Result categories

Research and test results use these categories:

| Category | Meaning |
|---|---|
| PASS | The test or review met the expected result. |
| FAIL | The test or review did not meet the expected result. |
| PARTIAL | The result worked in some conditions but not all. |
| BLOCKED | The work could not continue because something was missing. |
| NEEDS_RESEARCH | The result raised a question that needs more study. |

`PARTIAL`, `BLOCKED`, and `NEEDS_RESEARCH` are useful results. They show what is
still unclear and what needs better tests or review.

## Evidence records

The research uses two kinds of evidence records.

The research log records meaningful milestones in chronological order. It is for
short summaries, important results, tests run, limitations, and next steps.

Focused result documents record deeper experiment detail when a topic needs more
space. These documents can include the test purpose, input, expected result,
observed result, environment, limitation, and follow-up work.

This keeps the evidence log readable while still preserving technical detail.

## Current evaluation focus

The current focus is QSAG Layer 1:

Agent identity and action-decision evidence.

The main test areas are:

1. fail-closed verifier behavior;
2. malformed and duplicate-key JSON handling;
3. schema, time, and lifecycle validation;
4. issuer trust and revocation freshness boundaries;
5. proof selection and proof/key binding;
6. canonical payload preparation and payload-hash consistency;
7. signature adapter-interface planning;
8. authorization, approval, audit, and enforcement composition;
9. sensitive-data minimization;
10. dummy cross-organization scenarios.

The passport verifier cannot return `ALLOW` until signature, trust, revocation,
permission, approval, audit, and enforcement gates are intentionally connected
and tested.

## Negative testing

Negative tests are important because they show how the verifier behaves when
something is wrong or unclear.

Useful negative tests cover malformed, missing, stale, mismatched, unsupported,
expired, revoked, compromised, and ambiguous evidence.

The expected direction is fail closed, not silent acceptance.

## Data and isolation

Research tests use dummy data unless a later recorded decision explains another
approach.

The repository is not intended to contain real users, real organization secrets,
private keys, production credentials, live agent logs, or confidential
operational data.

Package, vector, and runtime experiments run outside the repository environment
unless a later decision records why repository changes are needed. Temporary
experiment files are summarized in evidence documents instead of copied into the
repository.

## Documentation review

Documentation is part of the research.

Review looks for:

1. outdated wording;
2. repeated explanations;
3. unsafe commands;
4. hidden assumptions;
5. wording that sounds more complete than the evidence supports;
6. broken links;
7. mismatch with README, ROADMAP, tests, or evidence records.

The aim is to keep the research understandable as it grows.

## Current boundary

This document describes the evaluation discipline used by the research today.

It can change as testing improves, mistakes are found, and the research direction
becomes clearer.

Small wording cleanup does not need an evidence-log entry unless it changes a
research boundary.
