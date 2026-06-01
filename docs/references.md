# References

## Purpose

This file is the central reference register for the repository.

All external sources used by the research should be recorded here before they are relied on in research documents. The purpose is to keep references easy to verify, review, update, and replace.

URLs are added only after a source has been checked against the original publisher or official source.

Research documents may refer to reference identifiers from this file. Implementation files should not contain citations, legal claims, or research references. Code comments should explain code behaviour only.

## Status definitions

Pending review means the source has been identified but has not yet been fully checked.

Verified means the source has been checked against the original publisher or official source.

Replaced means the source was previously used but has been superseded by a newer version.

Retired means the source is no longer used by this repository.

## Reference register

| ID | Topic | Source | Publisher | Status | Accessed | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| REF-001 | Decentralized identifiers | W3C DID Core | W3C | Pending review | Not recorded | Used for decentralized identifier research |
| REF-002 | Verifiable credentials | W3C Verifiable Credentials Data Model | W3C | Pending review | Not recorded | Used for agent passport research |
| REF-003 | Post-quantum digital signatures | FIPS 204 ML-DSA | NIST | Pending review | Not recorded | Used for primary passport signature research |
| REF-004 | Hash-based post-quantum signatures | FIPS 205 SLH-DSA | NIST | Pending review | Not recorded | Used for backup passport signature research |
| REF-005 | Post-quantum key establishment | FIPS 203 ML-KEM | NIST | Pending review | Not recorded | Used for future secure key exchange research |
| REF-006 | Digital identity guidance | NIST SP 800-63 series | NIST | Pending review | Not recorded | Used for operator identity assurance research |
| REF-007 | AI governance | EU AI Act | European Union | Pending review | Not recorded | Used for risk, transparency, and accountability mapping |
| REF-008 | Agentic AI security risks | OWASP Top 10 for Agentic Applications | OWASP | Pending review | Not recorded | Used for threat model research |
| REF-009 | Agent identity governance | Agent Identity Governance Framework | Cloud Security Alliance | Pending review | Not recorded | Used for industry identity governance research |
| REF-010 | Workload identity | SPIFFE and SPIRE | SPIFFE | Pending review | Not recorded | Used for runtime identity research |
| REF-011 | Proof of possession | OAuth DPoP | IETF | Pending review | Not recorded | Used for action request proof research |
| REF-012 | Software supply chain integrity | SLSA | OpenSSF | Pending review | Not recorded | Used for future supply chain binding |
| REF-013 | JSON canonicalization | RFC 8785 JSON Canonicalization Scheme | IETF | Pending review | Not recorded | Used for canonicalization compatibility research |
| REF-014 | RFC 8785 candidate implementation | rfc8785 / trailofbits/rfc8785.py | Trail of Bits | Pending review | Not recorded | Source identity and declared license checked in `docs/canonicalization-evaluation-results-ref014-rfc8785-0.1.4.md`; adoption and functional conformance remain unverified |
| REF-015 | RFC 8785 candidate implementation | jcs Python package / titusz jcs | titusz | Pending review | Not recorded | Isolated evaluation recorded in `docs/canonicalization-evaluation-results-ref015-jcs-0.2.1.md`; source identity and declared license checked, but standalone source license file was not present; adoption and full conformance remain unverified |
| REF-016 | JSON Canonicalization reference implementation and test vectors | cyberphone/json-canonicalization | Anders Rundgren / cyberphone | Pending review | Not recorded | Used for RFC 8785/JCS reference vectors and comparison |
| REF-017 | Alternative canonical JSON implementation | canonicaljson | Matrix.org | Pending review | Not recorded | Used as excluded comparison because it targets Matrix canonical JSON rather than RFC 8785/JCS |
| REF-018 | Legacy/low-maintenance JCS candidate | json-canonical | AnasMK | Pending review | Not recorded | Used as excluded or low-priority comparison candidate |
| REF-019 | Incomplete JSON canonicalization candidate | jsoncanon | sveinugu | Pending review | Not recorded | Used as excluded comparison because floating-point support appears incomplete |

## Use policy

New references should be added to this file before they are used in research documents.

References should remain marked as Pending review until checked from the original publisher or official source.

Final research claims should rely only on references marked as Verified.

Implementation files should not contain citations or legal claims.

If a reference is replaced by a newer source, the old entry should be marked as Replaced rather than deleted.

If a reference is no longer used, it should be marked as Retired rather than deleted.
