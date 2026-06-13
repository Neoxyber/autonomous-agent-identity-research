# Reading Notes

## Purpose

This folder stores short research notes for standards, papers, and industry sources that may affect the autonomous agent identity research model.

The purpose is to avoid rereading the same sources repeatedly and to record what each source teaches the repository.

These notes are research inputs, not adoption decisions.

## Scope

Reading notes may cover:

1. identity standards
2. authorization standards
3. verifiable credentials
4. decentralized identifiers
5. workload identity
6. agent identity work
7. agent security papers
8. revocation and lifecycle status
9. audit and decision evidence
10. post-quantum signature representation
11. Zero Trust Architecture
12. non-human identity governance

## Folder structure

Use:

1. `standards/` for official standards, specifications, RFCs, W3C documents, NIST documents, OpenID work, IETF drafts, SPIFFE, and related protocol work
2. `papers/` for academic papers, preprints, surveys, and technical research papers
3. `industry/` for OWASP, CSA, vendor reports, ecosystem notes, and practitioner guidance

## Note rules

Each note must be written in the repository's own words.

Do not store full papers, full standards, PDFs, screenshots, datasets, or long copied passages in this repository.

Short quotes may be used only when needed.

Each note records:

1. what the source is
2. why it matters
3. what maps to this research
4. what does not map
5. what remains unclear
6. whether the source suggests a future architecture change
7. whether the source needs a reference entry

A reading note does not mean the repository adopts the source.

A reading note does not mean the repository states compliance with the source.

A reading note does not approve implementation, dependency adoption, signature verification, schema changes, or an `ALLOW` path.

## Reference handling

Important sources belong in `docs/references.md`.

New sources start as reference candidates with `Pending review` status.

A source can be useful even when the repository does not adopt its approach.

## Public review

Public review is welcome.

Reviewers can help by checking:

1. whether a note accurately summarizes the source
2. whether the source is official, draft, academic, industry, or background material
3. whether the mapping to this research is too strong, too weak, or unclear
4. whether adoption boundaries are clear
5. whether important open questions are missing
6. whether a source needs an entry in `docs/references.md`

Review comments are most useful when they point to a specific source section, standard clause, paper section, or repository note.

Reading notes do not replace source documents.

Reading notes do not approve standards adoption, implementation, dependency changes, schema changes, signature verification, or verifier `ALLOW` behavior.

## Current boundary

This folder supports research reading only.

It does not change source code, schemas, examples, tests, verifier behavior, proof formats, dependency policy, or repository terminology.
