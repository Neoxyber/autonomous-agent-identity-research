# Contributing

## Purpose

This repository is a research-first project.

The goal is to develop a clear, testable, and well-documented identity model for autonomous AI agents. Contributions should improve the research, specifications, implementation, tests, evidence, or documentation.

## Contribution principles

Contributions should follow these principles:

1. Keep the work clear and focused.

2. Prefer small changes over large mixed changes.

3. Separate research claims from implementation code.

4. Keep references in docs/references.md.

5. Do not add citations, legal claims, or research references inside implementation files.

6. Record meaningful research progress in evidence/research-log.md.

7. Be honest about limitations and unresolved questions.

## Repository discipline

The repository should grow in stages.

Do not add implementation before the relevant research model is documented.

Do not add deployment files before the reference implementation is tested.

Do not add large generated files, recordings, screenshots, credentials, keys, or private data.

Do not create new folders unless they contain meaningful work.

## Document contributions

Research documents should be written in clear, direct language.

Avoid marketing language, exaggerated claims, and unsupported statements.

A good research document should explain:

1. What problem is being addressed.

2. Why the problem matters.

3. What the proposed model or decision is.

4. What is not yet solved.

5. Which related references apply.

## Reference policy

All external references should be recorded in docs/references.md.

References should remain marked as Pending review until checked against the original publisher or official source.

Final research claims should rely only on references marked as Verified.

## Implementation contributions

Implementation code should be treated as a reference implementation.

Code should be simple, testable, and connected to the research model.

Code comments should explain behaviour, not legal claims or research citations.

## Testing contributions

Tests should be added with clear purpose.

Important tests should later be connected to Empirical Testing Logs.

Priority test areas include:

1. Offline passport verification.

2. Passport tamper detection.

3. Allowed action enforcement.

4. Prohibited action denial.

5. Human approval decision flow.

6. Revocation enforcement.

7. Audit event generation.

## Security

Do not commit secrets, private keys, credentials, access tokens, database dumps, or private identity material.

Security issues should be reported privately to:

security@aixybertech.com

## Pull requests

A pull request should explain:

1. What changed.

2. Why it changed.

3. Which files were affected.

4. Whether the change affects research, specifications, implementation, tests, or evidence.

5. Any limitations or follow-up work.
