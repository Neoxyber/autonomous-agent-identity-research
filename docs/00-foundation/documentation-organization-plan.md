# Documentation Organization Plan

## Purpose

This document records the planned organization model for the repository
documentation.

The goal is to make the research easier to navigate as the project grows, while
preserving file history, public-document stability, and the chronological
evidence trail.

This is an organization plan only. It does not move files, rename files, change
references, change source code, change tests, adopt dependencies, or change
verifier behavior.

## Current state

The `docs/` directory currently contains foundation documents, research models,
canonicalization research, signature-verification research, standards
positioning, references, and threat-boundary material at the same directory
level.

This was acceptable while the repository was small, but the canonicalization and
signature-verification chains now need clearer reader navigation.

The evidence directory already contains chronological research logs and should
remain unchanged.

`docs/references.md` is the central reference register and should remain at the
docs root.

## Organization principles

The documentation structure should follow these principles:

1. Keep `docs/references.md` at the docs root.
2. Keep evidence files unchanged.
3. Keep specs files unchanged.
4. Keep public filenames stable where practical.
5. Avoid renaming files only to add sequence numbers.
6. Use folder-level README files for reading order.
7. Group documents by research area.
8. Move files only with `git mv`.
9. Update links in the same commit as any file move.
10. Keep each migration small and reviewable.
11. Add future folders only when they reduce confusion.

## Proposed future docs folders

The future `docs/` structure should be:

- `docs/README.md`
- `docs/00-foundation/`
- `docs/10-models/`
- `docs/20-threat-boundaries/`
- `docs/30-canonicalization/`
- `docs/40-signature-verification/`
- `docs/50-standards-positioning/`
- `docs/references.md`

The folder numbers are for reader navigation only. Individual document filenames
do not need numeric prefixes.

## Files that should stay where they are

These files and directories should not move in the first documentation
migration:

- `docs/references.md`
- `evidence/research-log.md`
- `evidence/research-log-archive-001.md`
- `evidence/research-log-archive-002.md`
- `specs/`

## Proposed file grouping

Foundation documents should move to `docs/00-foundation/`:

- `principles.md`
- `problem-statement.md`
- `research-questions.md`
- `scope.md`
- `limitations.md`
- `evaluation-method.md`

Research model documents should move to `docs/10-models/`:

- `identity-layer.md`
- `permission-model.md`
- `human-oversight-model.md`
- `revocation-model.md`
- `decentralized-verification.md`
- `audit-model.md`
- `post-quantum-readiness.md`

Threat and trust-boundary documents should move to
`docs/20-threat-boundaries/`:

- `agent-passport-threat-model-and-trust-boundaries.md`

Canonicalization documents should move to `docs/30-canonicalization/`.

Signature-verification documents should move to
`docs/40-signature-verification/`.

Standards-positioning documents should move to
`docs/50-standards-positioning/`:

- `standards-positioning.md`

## Long-term growth

The documentation structure should remain expandable as the research grows.

Future research areas may receive new numbered folders when there is enough
material to justify them. Examples may include revocation status evidence, human
approval and audit evidence, gateway and MCP integration, post-quantum
experiments, deployment research, or other autonomous-agent identity topics.

New folders should be created only when they reduce confusion. The project
should avoid empty or speculative folders.

The goal is to help researchers, students, security experts, and contributors
understand the research path, reproduce evidence, review decisions, and improve
the work without needing to reconstruct the project history from commit logs.

## Migration order

The migration should happen in stages:

1. Add this organization plan.
2. Add `docs/README.md` as the central documentation map.
3. Add folder README files without moving documents.
4. Run a link-impact check.
5. Move foundation and model documents first.
6. Move canonicalization documents.
7. Move signature-verification documents.
8. Move standards-positioning after link updates are clear.
9. Keep `docs/references.md` at the docs root.
10. Keep evidence and specs unchanged.

## Link-update rule

Any file move must update references in the same commit.

Before moving files, check references across:

- `README.md`
- `ROADMAP.md`
- `docs/`
- `specs/`
- `evidence/`
- `CITATION.cff`
- `SECURITY.md`

The migration should avoid leaving broken links or ambiguous reading paths.

## Evidence handling

Evidence logs should remain in `evidence/`.

The active evidence log and archives should not be moved into topic folders at
this stage because they are chronological audit records, not topic documents.

Future evidence scaling can be handled with an `evidence/README.md` if needed,
but the current evidence files should remain unchanged.

## Non-goals

This document does not:

- move documentation files;
- rename documentation files;
- move `docs/references.md`;
- move evidence files;
- move specs files;
- add numeric prefixes to existing filenames;
- update references;
- change source code;
- change tests;
- adopt dependencies;
- change verifier behavior;
- implement real signature verification;
- create a passport-verifier `ALLOW` path.

## Next step

Add a central `docs/README.md` that gives readers a clear map of the research
areas and the recommended reading order before moving any files.
