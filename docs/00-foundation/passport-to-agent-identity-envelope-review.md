# Passport to Agent Identity Envelope Review

## Purpose

This document reviews the repository's early use of `agent passport` and records why `Agent Identity Envelope` is the stronger long-term research term.

The review is part of the foundation work for autonomous agent identity research. It helps clarify the model before later layers become harder to rename or restructure.

## Context

The internet already contains large amounts of automated activity. Much of this activity comes from bots. Bots crawl pages, index websites, scrape content, monitor systems, submit forms, test credentials, or perform repeated narrow tasks.

Autonomous AI agents are different.

An autonomous agent can plan, reason, use tools, communicate with systems, hold context, request access, delegate work, and act across digital environments. In the future, one person may use separate agents for travel, finance, shopping, research, health support, business administration, and personal scheduling. A company may use agents for procurement, customer support, reporting, compliance checks, cloud operations, and security monitoring.

As AI systems become more capable, the question is no longer only whether traffic is human or automated.

The deeper question becomes:

Which agent is acting, under whose authority, with what permission, at what risk, and with what evidence?

This is the research area of the repository.

## Why passport was used

The project began with a simple security idea:

No verified identity, no trusted action.

At the start, the closest familiar human comparison was a passport. A passport links identity to an issuer, validity period, and trust decision across different places.

That made `agent passport` useful as an early research metaphor. It helped give structure to an unclear problem and made the first model easier to reason about.

The term supported the early questions:

Who is the agent?

Who operates it?

Who issued its identity?

Is it still valid?

What can it do?

What evidence supports the decision?

This early wording helped the project move from an idea into documents, schema work, verifier boundaries, tests, and evidence logs.

## Why the model has moved beyond passport

The research has now expanded beyond the original metaphor.

The current model is not only an identity record. It carries verification and decision context around an autonomous agent.

The model now includes:

Agent identity.

Operator binding.

Issuer trust.

Lifecycle state.

Expiration.

Revocation.

Permissions.

Prohibitions.

Human approval.

Approval validation.

Audit evidence.

Proof metadata.

Payload hashes.

Key references.

Canonicalization.

Future signature verification.

Post-quantum readiness.

Fail-closed verification behavior.

A passport mainly points to human identity, government issuance, citizenship, nationality, travel, and legal documents.

That is not the direction of this research.

The repository is researching technical identity and decision boundaries for autonomous systems. The term `passport` helped at the beginning, but it now narrows the meaning of the model.

## Research direction

The better long-term term is:

`Agent Identity Envelope`

Short form:

`AIE`

The wider project framing remains:

`Autonomous Agent Identity Research`

`Agent Identity Envelope` fits the current model more accurately.

This is a research working term. It is not presented as a formal standard term,
an originality claim, or a replacement for existing identity, credential,
authorization, workload identity, or policy-envelope work.

`Agent` identifies the autonomous system.

`Identity` aligns with the emerging industry direction around agent identity, agent authentication, workload identity, credentials, authorization, and agent-to-agent trust.

`Envelope` describes a portable technical container. It can hold identity, trust, permission, status, proof, approval, and audit information without implying a human passport or government document.

The term gives the research room to grow.

An Agent Identity Envelope can later be mapped toward verifiable credentials, workload identity, delegated authorization, policy systems, revocation evidence, audit trails, post-quantum signatures, and agent-to-agent trust models.

The goal is not to replace those areas.

The goal is to research what evidence is needed before an autonomous agent is trusted to act.

## Why this matters long term

Autonomous systems may eventually operate at a scale and speed far beyond normal human activity.

If agents can buy goods, book services, move data, manage systems, negotiate tasks, call APIs, and interact with other agents, then identity alone is not enough.

A system needs to know:

Which agent is this?

Who is accountable for it?

Which issuer is trusted?

Which key is valid?

Which actions are allowed?

Which actions are prohibited?

Is the agent revoked, expired, suspended, or compromised?

Does this action need human approval?

What evidence is recorded for review?

This research treats identity as the first gate, not the whole system.

The long-term direction is:

No verified identity.

No trusted permission.

No approved action.

No silent execution.

## Migration position

This document records the research direction only.

It does not rename files, schemas, source code, tests, examples, or historical evidence.

Older evidence can keep the term `agent passport` because that was the working term at the time. Newer research can explain that `agent passport` was the early name and `Agent Identity Envelope` is the preferred future term.

The repository now contains substantial use of the passport term across schemas, source files, tests, examples, documentation, and evidence. The current test baseline gives the project a stable point to measure the size of the change before more layers are added.

This is the right time to review the active terminology. If the term remains in place while signature verification, issuer trust, revocation freshness, permission evaluation, approval validation, audit evidence, agent-to-agent trust, federation, and standards mapping expand, the migration becomes harder to review and easier to misunderstand.

The next step after this review is a migration inventory. That inventory can separate active model terminology from historical evidence. Active terminology can move toward `Agent Identity Envelope`. Historical evidence can keep the wording used at the time so the research record remains accurate.

The goal is not to erase the earlier work. The goal is to move the active model toward a clearer long-term foundation while keeping the evidence record clean.

The migration can happen later as a controlled technical step.

The migration needs to preserve current behavior:

Verifier paths remain fail-closed.

Tests remain meaningful.

Historical evidence remains understandable.

No unrelated feature work is mixed into the rename.

No dependency adoption is mixed into the rename.

No real signature verification is added during the rename.

## Research roadmap after this review

With the test-review sweep complete, the next direction is to record this terminology review, then decide whether a controlled migration plan is ready.

After the terminology work, the research can continue through the main layers:

Canonicalization readiness.

Signature verification planning and implementation.

Issuer trust.

Revocation freshness.

Permission evaluation.

Human approval validation.

Audit evidence.

Agent-to-agent trust.

Federation and standards mapping.

Post-quantum readiness.

Each layer continues the same fail-closed principle:

When required evidence cannot be verified, the result is denial or review, not permission by default.

## Conclusion

`Agent passport` was a useful early research metaphor.

It helped start the work when the problem was still forming.

The model has now become broader than a passport. It carries identity, trust, permissions, proof material, revocation, approval, audit, and decision evidence.

`Agent Identity Envelope` is the better research term for the next phase.

It is more technical, more neutral, more aligned with autonomous agent identity, and easier to connect with future industry work.

## Current status

Preferred research term: `Agent Identity Envelope`

Short form: `AIE`

Earlier working term: `agent passport`

Project framing: `Autonomous Agent Identity Research`

Migration status: not started

Next step: review this document, then decide whether to record the terminology review before preparing a controlled migration plan.
