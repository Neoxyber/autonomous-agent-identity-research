# Identity Layer Model

This document defines the first identity layer model for autonomous agents.

The model is intentionally simple. It defines what an agent identity should contain, how an agent passport should be interpreted, and how a verifier should decide whether an agent may perform an action.

This is a research model. It is not yet a protocol, schema, implementation, or compliance claim.

## Purpose

The identity layer exists to make autonomous agents visible, verifiable, accountable, permission-scoped, revocable, and auditable.

An autonomous agent should not be able to act anonymously inside a digital system. Before an agent performs a meaningful action, a verifier should be able to answer these questions.

1. Does this agent exist?

2. Does this agent have a stable identifier?

3. Who is responsible for this agent?

4. What is this agent allowed to do?

5. What is this agent prohibited from doing?

6. Does this action require human approval?

7. Is the agent active, suspended, revoked, expired, compromised, or retired?

8. Can the agent passport be verified outside the issuing system?

9. Can the action be linked to audit evidence?

## Core entities

### Agent

An agent is an autonomous or semi-autonomous software actor that can reason, select actions, call tools, access services, or execute workflow steps.

An agent is not the same as a human user, service account, device, workload, or ordinary application. It may use those systems, but it should have its own identity when it acts with autonomy.

### Operator

An operator is the responsible party for an agent.

The operator may be a person, organization, legal entity, research group, system owner, or other accountable controller. The identity layer should make responsibility explicit while avoiding unnecessary exposure of personal or sensitive information.

### Agent passport

An agent passport is a verifiable identity document for an autonomous agent.

The passport describes the agent, the operator, the agent's public keys, the agent's purpose, the agent's permissions, the agent's prohibitions, approval requirements, lifecycle status, expiry, revocation reference, verification material, and audit references.

A passport should not be treated as permanent authority. It must be checked against expiry, revocation, status, policy, and context before an action is allowed.

### Verifier

A verifier is a system that checks an agent passport and decides whether the agent may perform a requested action.

A verifier may be an API gateway, service, workflow engine, policy engine, registry, identity provider, security monitor, or receiving organization.

## Agent passport requirements

An agent passport should prove the following.

1. This agent exists.

2. This agent has a stable identifier.

3. This agent is controlled by a responsible operator.

4. This agent has public keys.

5. This agent has a declared purpose.

6. This agent has a risk class.

7. This agent is allowed to do specific actions.

8. This agent is prohibited from doing specific actions.

9. This agent may require human approval for specific actions.

10. This agent has an issue time and expiry time.

11. This agent has a lifecycle status.

12. This agent has a revocation reference.

13. This agent can be verified globally.

14. This agent can be linked to audit evidence.

## Passport fields

The first model uses these passport fields.

### Agent identifier

A stable identifier for the agent.

The identifier should be unique enough for verification, audit, revocation, and lifecycle management. It should not depend on a temporary runtime session.

### Operator identifier

A reference to the responsible operator.

The operator identifier should support accountability without requiring unnecessary disclosure of sensitive information.

### Issuer identifier

A reference to the party that issued the passport.

The issuer may be the operator, a trusted registry, a governance body, or another authorized issuer.

### Public keys

The public keys used to verify signatures, passport integrity, audit events, and future secure communication.

The model should support key rotation and multiple key types.

### Declared purpose

A short statement describing why the agent exists.

The declared purpose should help verifiers and reviewers understand the expected role of the agent.

### Risk class

A classification of the agent's expected risk level.

The risk class may influence approval requirements, monitoring, expiry duration, and audit requirements.

### Allowed actions

A list of actions the agent is explicitly allowed to perform.

An action not listed as allowed should not be allowed by default.

### Prohibited actions

A list of actions the agent is explicitly prohibited from performing.

A prohibited action should remain denied even if the agent has access to a tool, credential, or environment that could technically perform it.

### Human approval requirements

A list of actions or conditions that require human approval before execution.

Approval should be explicit, attributable, time-bound where possible, and linked to audit evidence.

### Issue time

The time when the passport was issued.

### Expiry time

The time after which the passport is no longer valid.

Expired agents should not be allowed to act.

### Lifecycle status

The current lifecycle state of the agent.

Supported statuses are the schema lifecycle_status values:

- active
- suspended
- revoked
- expired
- compromised
- retired

Only active allows verification to continue. The other statuses fail closed.

### Revocation reference

A reference used to check whether the passport or agent has been revoked.

The reference may point to a registry, revocation list, transparency log, signed status object, or other verification mechanism.

### Verification material

Information needed to verify the passport outside the issuing system.

This may include issuer keys, signature metadata, proof format, algorithm identifiers, registry references, and trust anchors.

### Audit reference

A reference used to connect the passport to audit evidence.

Audit evidence should support later review of who acted, which agent acted, which operator was responsible, what action was requested, what policy decision was made, and why the action was allowed or denied.

## Permission model

The identity layer uses explicit permission.

An agent may only perform an action when the action is within the allowed actions, the passport is valid, the lifecycle status permits action, the action is not prohibited, and any required approval has been satisfied.

Example allowed actions include:

- read public data
- summarize operator-owned documents
- call approved APIs
- generate draft reports
- classify low-risk data
- answer internal knowledge questions
- execute approved workflow steps

Allowed actions should be specific enough for enforcement. Broad permissions should be avoided where possible.

## Prohibition model

The identity layer uses explicit prohibition.

Example prohibited actions include:

- hide identity
- impersonate a human
- use shared human credentials
- access data outside scope
- delete production data
- initiate payments without approval
- modify its own permissions
- disable audit logging
- create child agents without permission
- delegate authority without a delegation credential
- call unapproved tools
- exfiltrate secrets
- bypass gateway enforcement
- operate after revocation

A prohibited action should produce a denial decision.

## Human approval model

Some actions may be too sensitive for automatic execution.

The identity layer should support a separate decision outcome for actions that require human approval. This avoids treating all risky actions as either fully allowed or fully denied.

Human approval may be required because of the action type, data sensitivity, financial impact, operational risk, legal risk, or policy context.

Approval evidence should record:

- the agent identifier
- the operator identifier
- the requested action
- the approving human or approval authority
- the approval time
- the approval scope
- the expiry of the approval, if applicable
- the reason for approval, if provided

## Decision model

The verifier should produce one of four decisions.

### ALLOW

The action is permitted.

This decision should only be returned when the passport is valid, the agent status permits action, the action is explicitly allowed, the action is not prohibited, and any required approval has been satisfied.

### DENY

The action is not permitted.

This decision should be returned when the passport is invalid, expired, revoked, suspended, compromised, unverifiable, outside scope, explicitly prohibited, or otherwise not acceptable under policy.

### REQUIRE_HUMAN_APPROVAL

The action may be permitted only after human approval.

This decision should be returned when the action is within a category that requires approval and approval has not yet been provided or verified.

### REQUIRE_HUMAN_REVIEW

The system cannot safely decide.

This decision should be returned when the action, context, evidence, or risk is unclear and a human must review the case before any further decision.

## Default policy

The default policy is default deny.

Only explicitly allowed actions are permitted.

High-risk actions require approval.

Prohibited actions are never allowed.

Revoked or expired agents cannot act.

A verifier should not infer authority from tool access alone. Possession of a credential, API key, token, or runtime capability does not mean the agent is authorized to use it.

## Lifecycle model

The identity layer must support lifecycle management.

### active

The agent passport is valid and the agent may act within its allowed scope.

### suspended

The agent is temporarily not allowed to act.

### revoked

The agent is removed from trust and must not act.

### expired

The passport is past its expiry time and must not be used for action.

### compromised

The agent, its keys, its runtime, or its operator binding may no longer be trustworthy.

### retired

The passport identity has been superseded or intentionally withdrawn and must not be used for action. A retired passport identity (lifecycle_status) is distinct from a retired public key (public_key.status), which marks superseded key material; the two apply at different scopes.

### Transition and onboarding states

Rotation and onboarding are not lifecycle_status values in the current schema.

Rotation is a transition process and a revocation or audit reason. When identity or key material is replaced, the superseded material is recorded as retired, newly issued material is active, and the rotation is captured as a reason. Key material may be rotated or replaced over time as part of cryptographic agility.

Onboarding and review happen before an identity becomes active. Operator-level onboarding is represented by operator.verification_status, including pending_review. A passport-level pending state would require a separate later schema decision; until then, an identity that has not completed onboarding has no active passport and is denied by default.

## Global verification

The agent passport should be verifiable outside the original issuing system.

A verifier should be able to check the passport identifier, issuer, signature, public keys, issue time, expiry time, lifecycle status, revocation reference, permissions, prohibitions, and approval requirements.

The model should avoid unnecessary dependence on a single central service. Central services may still be useful for registration, governance, discovery, and revocation, but the passport should be portable and inspectable where possible.

## Decentralized verification

The identity layer should support decentralized verification where possible.

This may include portable credentials, decentralized identifiers, signed status objects, transparency logs, replicated registries, or other mechanisms that allow verification across organizational boundaries.

Decentralization does not remove the need for governance. It should reduce unnecessary single points of trust while preserving accountability, revocation, and auditability.

## Post-quantum readiness

Agent passports may need to remain verifiable for many years.

The identity layer should support cryptographic agility so algorithms, parameter sets, proof formats, and key material can be rotated or replaced over time.

The current research direction is:

- ML-DSA as the primary candidate for signing agent passports
- SLH-DSA as an independent backup hash-based signature family
- ML-KEM as a future candidate for secure key establishment between agents, gateways, and verification services
- hybrid transition support where classical and post-quantum mechanisms need to coexist
- algorithm agility so the model does not depend permanently on one cryptographic choice

This repository should track future post-quantum signature candidates, but the identity model should not depend on unfinalized candidates.

## Audit evidence

Important actions should produce audit evidence.

Audit evidence should make it possible to review:

- which agent acted
- which operator was responsible
- which passport was presented
- which action was requested
- which resource or system was targeted
- which policy was evaluated
- which decision was returned
- why the action was allowed, denied, or sent for approval
- whether human approval was used
- which verifier made the decision
- when the event occurred

Audit evidence should be tamper-resistant where possible and linked to the relevant passport version.

## Initial verification flow

A verifier should perform these checks before allowing an action.

1. Receive the agent passport and requested action.

2. Verify the passport signature.

3. Check issuer trust.

4. Check issue time and expiry time.

5. Check lifecycle status.

6. Check revocation status.

7. Check operator binding.

8. Check whether the action is explicitly prohibited.

9. Check whether the action is explicitly allowed.

10. Check whether human approval is required.

11. Return ALLOW, DENY, REQUIRE_HUMAN_APPROVAL, or REQUIRE_HUMAN_REVIEW.

12. Record audit evidence.

## Boundaries

This document does not define a final schema.

This document does not define a wire protocol.

This document does not define a reference implementation.

This document does not claim legal or regulatory compliance.

This document does not solve delegation, reputation, supply-chain identity, or formal verification. Those topics may be studied later after the first identity model is stable.
