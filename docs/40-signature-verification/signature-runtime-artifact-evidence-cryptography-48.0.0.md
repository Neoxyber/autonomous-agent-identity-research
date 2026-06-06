# Signature Runtime Artifact Evidence: cryptography 48.0.0

## Purpose

This document records isolated package artifact evidence for Python
`cryptography` version `48.0.0`.

The evidence was collected outside the repository environment in a temporary
directory.

This is package artifact evidence only. It does not adopt a dependency, install
packages into the repository environment, change requirements or lockfiles,
change verifier source, change schema, implement real signature verification, or
create a passport-verifier `ALLOW` path.

## Environment

Repository state before the artifact evidence run:

- repository path: `~/projects/autonomous-agent-identity-research`
- repository commit: `91418e0`
- repository virtual environment: `.venv`
- isolated artifact path: `/tmp/aaid-cryptography-48-artifact-evidence`
- isolated virtual environment: `/tmp/aaid-cryptography-48-artifact-evidence/.venv`
- Python version: `3.12.3`
- pip version after upgrade: `26.1.2`

The artifact inspection was performed only in the isolated `/tmp` environment.

## Downloaded artifacts

The isolated run downloaded these artifacts:

- `cryptography-48.0.0-cp311-abi3-manylinux_2_34_x86_64.whl`
- `cryptography-48.0.0.tar.gz`

No artifact was copied into the repository.

## Artifact hashes

Observed SHA-256 hashes:

| Artifact | SHA-256 |
| --- | --- |
| `cryptography-48.0.0.tar.gz` | `5c3932f4436d1cccb036cb0eaef46e6e2db91035166f1ad6505c3c9d5a635920` |
| `cryptography-48.0.0-cp311-abi3-manylinux_2_34_x86_64.whl` | `bd72e68b06bb1e96913f97dd4901119bc17f39d4586a5adf2d3e47bc2b9d58b5` |

Result: PASS for local artifact hash capture.

## Wheel metadata

Observed wheel:

`cryptography-48.0.0-cp311-abi3-manylinux_2_34_x86_64.whl`

Selected wheel metadata:

- name: `cryptography`
- version: `48.0.0`
- summary: `cryptography is a package which provides cryptographic recipes and primitives to Python developers.`
- author email: `The Python Cryptographic Authority and individual contributors <cryptography-dev@python.org>`
- license expression: `Apache-2.0 OR BSD-3-Clause`
- requires Python: `>=3.9, !=3.9.0, !=3.9.1`
- normal runtime dependency observed for CPython: `cffi>=2.0.0`
- optional extra observed: `bcrypt>=3.1.5 ; extra == 'ssh'`
- wheel generator: `maturin (1.13.1)`
- wheel tag: `cp311-abi3-manylinux_2_34_x86_64`
- pure Python wheel: no

Observed wheel license files:

- `LICENSE`
- `LICENSE.APACHE`
- `LICENSE.BSD`

Result: PASS for wheel metadata and license-file presence capture.

## Source distribution metadata

Observed source distribution:

`cryptography-48.0.0.tar.gz`

Selected source-distribution files:

- `PKG-INFO`
- `LICENSE`
- `LICENSE.APACHE`
- `LICENSE.BSD`
- `pyproject.toml`

Selected source-distribution metadata matched the wheel metadata for package
name, version, license expression, Python requirement, runtime dependency, and
project URLs.

Result: PASS for source-distribution metadata and license-file presence capture.

## Repository environment check

After the artifact evidence run, the repository virtual environment did not have
`cryptography` installed.

Observed result:

`repo_venv_cryptography: not installed`

Result: PASS for repository environment non-adoption check.

## Evaluation classification

| Area | Result |
| --- | --- |
| Isolated artifact directory | PASS |
| Wheel artifact captured in `/tmp` | PASS |
| Source distribution captured in `/tmp` | PASS |
| SHA-256 hashes captured | PASS |
| Wheel metadata inspected | PASS |
| Source-distribution metadata inspected | PASS |
| License expression captured | PASS |
| License files observed | PASS |
| Runtime dependency surface captured | PARTIAL |
| Build/provenance verification | NOT TESTED |
| Vulnerability/security advisory review | NOT TESTED |
| Repository dependency adoption | NOT APPROVED |

Overall result: PARTIAL.

The artifact evidence is useful for later adoption review, but adoption readiness
remains partial until provenance, vulnerability posture, dependency-risk review,
official test-vector compatibility, encoding decision, and verifier integration
planning are completed.

## Limitations

The run captured artifact hashes and metadata, but it did not verify artifact
signatures, Sigstore attestations, maintainer identity, reproducible build
properties, vulnerability databases, or long-term maintenance suitability.

The source-distribution download prepared build metadata inside the isolated
temporary environment. This did not modify the repository environment.

This result is not a security audit of `cryptography`.

## Not implemented

This evaluation did not implement:

- repository dependency adoption;
- package installation in the repository environment;
- requirements or lockfile changes;
- verifier source changes;
- schema changes;
- example passport updates;
- official test-vector execution;
- real passport signature verification;
- signing-key generation in the repository;
- permanent runtime integration;
- issuer trust registry;
- signed revocation evidence;
- authorization policy changes;
- approval enforcement changes;
- audit storage;
- gateway, MCP, Civo, Supabase, or cloud integration;
- production readiness;
- legal compliance;
- certification;
- passport-verifier `ALLOW` path.

## Next step

Review official ML-DSA test-vector compatibility, provenance options, and
dependency-risk evidence before any repository dependency adoption or verifier
integration proposal.
