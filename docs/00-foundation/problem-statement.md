# Problem Statement

Autonomous agents are becoming able to use tools, access services, make decisions, and request actions across digital systems.

This creates an identity and action-trust problem.

Most identity systems were designed around humans, service accounts, applications, workloads, or devices. Autonomous agents do not fit neatly into one category. They may act repeatedly, use multiple tools, make chained decisions, and cross organizational boundaries.

When an autonomous agent acts without clear identity and action-decision evidence, these questions become difficult to answer:

1. Which agent requested the action?
2. Who was responsible for the agent?
3. Which issuer or trust boundary applied?
4. Was the agent active, expired, revoked, suspended, compromised, or retired?
5. Was revocation or status evidence fresh enough?
6. Was the action within permission scope?
7. Was the action explicitly prohibited?
8. Did the action require human approval or review?
9. Which proof, key, and payload evidence was checked?
10. Can the decision be reviewed later without exposing unnecessary sensitive data?

These questions matter because autonomous agents may act at machine speed and may create security, operational, governance, and accountability consequences.

This research studies QSAG Layer 1:

Agent identity and action-decision evidence.

The work starts with one verifier-side question:

What must be checked before an autonomous AI agent action is trusted?

The current focus is not deployment, product design, cloud infrastructure, or a live gateway. The current focus is a narrow, testable, fail-closed identity and evidence model that can improve through research, tests, and review.
