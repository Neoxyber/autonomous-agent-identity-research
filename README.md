# Autonomous Agent Identity Research

## Purpose

This research is the first layer of the wider Quantum-Secure Autonomous Gateway direction.

I am starting with autonomous AI agent identity because every bigger question depends on it. Before thinking about gateways, approvals, audit trails, cloud systems, or enforcement, I want to understand one thing clearly:

**Who is this agent, who is responsible for it, and why should it be allowed to act?**

The core rule is simple:

**No verified identity and authority evidence, no protected action.**

Identity alone is not enough, but it is the first foundation I want to understand. The rest can grow from there.

## Learning is part of this journey

My curiosity keeps pushing me to explore more, try different ideas, and understand what is coming next in technology. I started this research because I want to understand autonomous systems, AI agents that can take actions, and the future where AI may become more intelligent than humans.

I am still learning. I can be wrong, I can make mistakes, and some architecture decisions may change with time. But I want to keep going, keep testing, keep improving, and keep sharing the journey openly.

Some people may say this is too hard or impossible to do alone. Maybe they are right. But I still want to try, see how far I can go, and learn as much as I can along the way.

Instead of spending my time only on games, parties, or distractions, I want to explore hard problems and build something useful. I hope this research can also bring curious people alongside me, so we can learn, question, and improve together.

## Why this matters

AI agents are becoming more capable. They can plan, call tools, use software, connect systems, and act faster than humans can review every step.

That creates a hard question:

**Before an autonomous agent touches a protected system, what must be checked?**

This research explores that question through small, testable steps. It looks at identity, authority, permission scope, lifecycle status, revocation, approval evidence, signatures, canonicalization, and audit records.

The goal is not to pretend the answer is finished. The goal is to learn carefully, test ideas, find mistakes, and improve the model over time.

## QSAG Layer 1

This repository focuses on Layer 1:

**Agent Identity and Action-Decision Evidence**

This layer studies what a verifier needs before an autonomous agent is allowed to perform a protected action.

The wider QSAG direction may later include gateways, cloud systems, policy enforcement, storage, and integrations. This repository stays focused on the first layer.

## Agent passport

The current research uses an **agent passport** as a test envelope.

It is not a final standard. It is a way to explore what information may need to travel together when an autonomous agent requests action.

The passport helps test:

- agent identity;
- operator binding;
- issuer trust assumptions;
- lifecycle status;
- permissions and prohibitions;
- approval requirements;
- revocation freshness;
- payload hash checks;
- proof metadata;
- audit-relevant decision data.

Future work can map this envelope to existing identity, workload, credential, and signed-data standards where appropriate.

## Current status

The repository currently includes:

- research models for identity, permissions, oversight, revocation, decentralized verification, audit evidence, and post-quantum readiness;
- an initial agent passport schema and example;
- deterministic canonicalization helpers for the current profile;
- payload hash checks;
- verifier pipeline checks;
- fail-closed verifier behavior;
- raw JSON parsing with duplicate-key rejection;
- lifecycle and expiry checks;
- issuer trust and revocation freshness boundaries;
- proof selection and key binding checks;
- canonical payload preparation;
- signature verification planning and isolated ML-DSA research;
- a local secret and public-risk scan;
- automated tests.

The local verifier remains fail-closed.

Real signature verification, dependency adoption, issuer trust registry, live revocation service, production policy engine, audit storage, gateway logic, cloud deployment, and external integrations are not implemented.

## What this research should produce

This research should produce:

- a clear model for autonomous agent identity and action decisions;
- fail-closed verifier behavior;
- negative tests for unsafe or unclear evidence;
- proof and key binding checks;
- canonicalization and signed-byte research;
- signature proof-profile research;
- audit-minimization rules;
- dummy cross-organization verification scenarios.

The strongest contribution is a small, testable verifier-side model for deciding when an autonomous agent action should not be trusted.

## What this repository does not do

This repository does not currently build:

- a production gateway;
- a commercial identity service;
- an MCP replacement;
- a full policy language;
- a live multi-organization network;
- a production revocation service;
- a cryptographic library;
- a real-agent execution system;
- a cloud deployment;
- a compliance framework.

MCP, A2A, APIs, workflow engines, cloud platforms, and future agent protocols are treated as integration layers, not trust foundations.

## Documentation

Start with:

- `docs/README.md`

External references are maintained in:

- `docs/references.md`

The staged research direction is maintained in:

- `ROADMAP.md`

Evidence logs are maintained in:

- `evidence/`

## Current focus

The current focus is signature verification boundary review.

The next technical step is to inspect the existing verifier and tests against the signature implementation-boundary plan, then define the smallest signature adapter-interface tests without importing a cryptographic runtime.

## Research discipline

This research should stay narrow, testable, and evidence-based.

From this point:

- `docs/README.md` is the living documentation index;
- `docs/references.md` is the source register;
- `evidence/research-log.md` records short milestone entries only;
- detailed experiment evidence belongs in focused result documents;
- no broad documents should be added unless they reduce confusion;
- dependency adoption requires a separate decision;
- real signature verification requires proof-profile and adoption decisions;
- legal, compliance, certification, and production wording should be avoided unless a specific document needs careful boundary language.

## Community input

This research direction may change as AI agents, identity standards, post-quantum cryptography, and gateway security continue to move.

Useful feedback includes:

- threat-model review;
- standards mapping;
- negative test cases;
- verifier failure cases;
- revocation and approval evidence review;
- audit-minimization review;
- post-quantum proof-profile review;
- cross-organization dummy scenarios.

The goal is to keep learning in public, improve carefully, and stay honest about what has and has not been proven.

## Final question

This repository is useful if it keeps asking one question clearly:

**What must be checked before an autonomous AI agent action is trusted?**
