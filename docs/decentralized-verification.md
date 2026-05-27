# Decentralized Verification Model

## Purpose

This document defines the first decentralized verification model for autonomous agent identity.

The goal is to make agent passports verifiable outside one central runtime system while still allowing governed services for registration, revocation, and trust status.

## Core position

The system should be decentralized where useful and centralized where necessary.

Decentralized verification does not mean that every part of the system must use blockchain.

The first goal is portable verification. A verifier should be able to inspect an agent passport, verify signatures, check expiry, understand issuer trust, and evaluate available status evidence without depending unnecessarily on one live gateway.

## What decentralized verification means

For this research, decentralized verification means:

1. Agent passports can be verified outside the issuing service.

2. Verification material can be resolved from portable or public trust records.

3. Revocation evidence can be checked online when available and partially offline when needed.

4. Important evidence can be signed, hashed, timestamped, or anchored for later review.

5. The system avoids unnecessary single points of trust.

## What must be verifiable

A verifier should be able to check:

1. Agent identity.

2. Issuer identity.

3. Operator binding.

4. Public keys.

5. Passport signature.

6. Passport expiry.

7. Permission and prohibition references.

8. Revocation or lifecycle status.

9. Policy version.

10. Audit or evidence references.

## Verification modes

The model supports three verification modes.

### Offline verification

Offline verification checks the passport structure, signatures, public keys, expiry, hashes, and cached or signed status evidence.

Offline verification is useful when the verifier cannot contact the issuing service.

Offline verification may not know the latest revocation state unless fresh status evidence or a signed revocation list is available.

### Online verification

Online verification checks live issuer status, revocation status, key rotation status, and current trust information.

Online verification is useful when live network access is available.

### Hybrid verification

Hybrid verification combines local verification with online checks.

A verifier may accept the passport structure and signature offline, then strengthen the decision with live revocation or issuer checks when available.

## Trust material

The identity model should support more than one way to resolve trust material.

Examples include:

1. A published issuer public key.

2. A signed issuer metadata file.

3. A decentralized identifier document.

4. A trusted issuer registry.

5. A transparency log or signed statement service.

6. A signed revocation or status list.

The first implementation should start simple and avoid unnecessary infrastructure.

## DID research direction

Decentralized identifiers may be useful for resolving verification material.

DID support is a research direction, not a first-version dependency.

The first implementation should support portable verification using signed passports, issuer public keys, signed issuer metadata, and signed status evidence.

Later research should evaluate did:web because it can use an existing domain as a trust anchor.

Later research should also evaluate did:key because it can support simple key-derived identifiers for offline verification.

The project should not depend on a blockchain-based DID method until the identity, revocation, audit, and verification models have been tested.

## Revocation and status

Revocation is a key part of decentralized verification.

The model should support:

1. Online status endpoint.

2. Signed revocation list.

3. Cached status record.

4. Short-lived passport.

5. Offline warning mode.

A verifier should record which revocation evidence was available at the time of verification.

## Evidence anchoring

Evidence anchoring can help prove that a passport, revocation list, policy version, or audit summary existed before a certain point in time.

The system should anchor hashes, not private data.

Examples of evidence that may be hashed and anchored include:

1. Agent passport hash.

2. Revocation list hash.

3. Policy version hash.

4. Audit summary hash.

5. Issuer metadata hash.

## Bitcoin timestamping research

Bitcoin timestamping is considered only as an evidence anchoring mechanism.

The system should not place agent passports, personal data, secrets, or operational details on a public blockchain.

Future research may test OpenTimestamps or similar timestamping methods to anchor hashes of passports, revocation lists, policy versions, or audit summaries.

This can help prove that a document or state existed before a certain point in time without exposing the underlying content.

## Blockchain boundary

Blockchain is optional for this research.

The first implementation should not require running a blockchain, issuing a token, paying transaction fees, or storing sensitive data on-chain.

Blockchain-based anchoring, decentralized registries, or transparency mechanisms may be researched later if funding, testing time, and security review are available.

## Implementation direction

The first practical implementation should be simple.

It should test whether the system can:

1. Create an agent passport.

2. Canonicalize the passport.

3. Sign the passport.

4. Verify the passport offline.

5. Detect passport tampering.

6. Check expiry.

7. Check a signed or cached revocation status.

8. Record what verification evidence was available.

Later research can add decentralized identifiers, transparency services, timestamp proofs, and multi-organization verification.

## Research and testing direction

The research should record what passes, what fails, and what needs improvement.

Future tests should evaluate:

1. Offline passport verification.

2. Online revocation checks.

3. Signed revocation list verification.

4. Timestamp proof verification.

5. Key rotation handling.

6. Issuer metadata verification.

7. did:web verification.

8. did:key verification.

9. Verification under network failure.

10. Multi-organization verification.

## Current boundary

This document defines the initial decentralized verification model.

It does not define the final DID method, registry, transparency service, blockchain anchoring system, timestamping provider, or implementation. Those will be developed later through specifications, reference implementation, controlled tests, and recorded evaluation results.
