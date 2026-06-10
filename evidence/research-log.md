# Research Log

## Purpose

This file records the chronological progress of the autonomous agent identity research project.

The research log is used to track meaningful project steps, not every small edit. It records what changed, why it changed, which files were affected, and what the next step is.

Detailed design decisions will be recorded separately in Research Decision Records when the project reaches that stage. Empirical tests and benchmark results will be recorded separately in Empirical Testing Logs when implementation and testing begin.

## Archive note

Entries 001 to 021 are preserved unchanged in `evidence/research-log-archive-001.md`.

Entries 022 to 083 are preserved unchanged in `evidence/research-log-archive-002.md`.

Entries 084 to 113 are preserved unchanged in `evidence/research-log-archive-003.md`.

This active log continues the same entry numbering and format from Entry 114 onward.

## Entry 114

Date: 2026-06-06

Type: Research log archive rotation

Summary: Archived the active research log after documentation organization.

Files:
Added `evidence/research-log-archive-003.md`, reset `evidence/research-log.md` for new active entries, and updated documentation references to include the new archive.

Result:
The previous active research log was archived as `evidence/research-log-archive-003.md`.

The new active research log now starts from Entry 114 so future milestones can continue with a shorter active evidence file.

The archive preserves the chronological evidence trail from Entry 084 through Entry 113, including canonicalization, signature-verification, and documentation organization milestones.

This is evidence-log maintenance only. It does not change source code, tests, specs, documentation structure, dependencies, verifier behavior, real signature verification, or passport-verifier `ALLOW` behavior.

Tests:
`python -m pytest -q` passed with 594 tests after the archive rotation.

Not implemented:
source changes, test changes, spec changes, documentation restructuring, dependency adoption, verifier behavior changes, real signature verification, gateway integration, MCP integration, Civo, Supabase, cloud deployment, production readiness, legal compliance, certification, or passport-verifier `ALLOW` path.

Next step:
Resume technical research from the signature verification implementation-boundary gate.

## Entry 115

Date: 2026-06-08

Type: Safety guard implementation

Summary: Added a local secret and public-risk scanner.

Files:
Added `tools/secret_scan.py`, `tools/install_git_hooks.sh`, and `tests/test_secret_scan.py`. Updated `SECURITY.md` to note the scanner as an additional research safety guard.

Result:
The repository now includes a stdlib-only local scanner for obvious private keys, known token patterns, secret-like assignments, embedded URL credentials, private local paths, private remotes, private IPs, and high-entropy values in secret-like context.

Tests:
`python tools/secret_scan.py --all` passed.

`python -m pytest tests/test_secret_scan.py -q` passed with 8 tests.

`python -m pytest -q` passed with 602 tests.

Markdown link check found no broken links.

Not implemented:
external secret-scanning dependency adoption, CI configuration, network scanning, GitHub settings changes, verifier behavior changes, real signature verification, gateway integration, MCP integration, Civo, Supabase, cloud deployment, or passport-verifier `ALLOW` behavior.

Next step:
Review and commit the local scanner milestone, then continue improving privacy and secret-safety layers through small reviewed changes.

## Entry 116

Date: 2026-06-10

Type: Research environment safety milestone

Summary: Established an isolated research VM for repository testing.

Files:
Updated `SECURITY.md` and `evidence/research-log.md`.

Result:
Previous research checks were already run outside the main repository where
practical. This milestone strengthens that separation by preparing a dedicated
isolated research VM for repository testing and controlled experiments.

The VM is used for read-only repository checks and controlled research
experiments outside the main development environment.

A clean baseline snapshot was taken before cloning the repository. This gives
the research process a restore point before future testing.

`SECURITY.md` now records the short public testing rule for the isolated
research VM.

This milestone records testing discipline only. It does not change source
code, tests, specs, dependencies, verifier behavior, real signature
verification, or passport-verifier `ALLOW` behavior.

Tests:
`python tools/secret_scan.py --all` passed after this edit.

`python -m pytest -q` passed with 602 tests after this edit.

Not implemented:
source changes, test changes, spec changes, dependency adoption, CI
configuration, network scanning, GitHub settings changes, verifier behavior
changes, real signature verification, gateway integration, MCP integration,
Civo, Supabase, cloud deployment, production readiness, legal compliance,
certification, or passport-verifier `ALLOW` path.

Next step:
Clone the repository read-only in the isolated research VM, install
development requirements, run the full test suite, run the local secret and
public-risk scanner, inspect repository status, and take a second
repository-baseline snapshot if checks pass.


## Entry 117

Date: 2026-06-10

Type: Isolated VM repository baseline

Summary: Verified the repository baseline in the isolated VM.

Files:
Updated `evidence/research-log.md`.

Result:
The repository was cloned in the isolated VM from the public HTTPS remote.

The lab clone was kept fetch-only by disabling its push URL.

The local scanner passed, the full test suite passed with 602 tests, and a
second VM snapshot was taken after the passing baseline.

This milestone records isolated baseline testing only. It does not change
source code, tests, specs, dependencies, verifier behavior, real signature
verification, or passport-verifier `ALLOW` behavior.

Tests:
`python tools/secret_scan.py --all` passed in the isolated VM.

`python -m pytest -q` passed with 602 tests in the isolated VM.

Not implemented:
source changes, test changes, spec changes, dependency adoption, network
scanning, GitHub settings changes, verifier behavior changes, real signature
verification, cloud deployment, production readiness, legal compliance,
certification, or passport-verifier `ALLOW` path.

Next step:
Begin read-only repository review from the isolated VM baseline.


## Entry 118

Date: 2026-06-10

Type: Dependency safety update

Summary: Updated the pinned pytest development dependency.

Files:
Updated `requirements-dev.txt`.

Result:
A CVE was found for `pytest==8.3.4`. The pinned development dependency was
updated to `pytest==9.0.3`, which includes the fix.

The update was tested first in the isolated VM, then applied in the official
development repository in commit `9510f77`.

Tests:
`python tools/secret_scan.py --all` passed.

`python -m pytest -q` passed with 602 tests.

`python -m pytest --version` reported `pytest 9.0.3`.

Not implemented:
source changes, test changes, spec changes, runtime dependency adoption,
verifier behavior changes, real signature verification, cloud deployment, or
passport-verifier `ALLOW` path.

Next step:
Continue read-only repository review and classify remaining findings.

## Entry 119

Date: 2026-06-10

Type: Test import cleanup

Summary: Cleaned up repeated test import path setup.

Files:
Added `pytest.ini`.

Updated test files to remove repeated `sys.path.insert(...)` setup.

Result:
Pytest now uses one committed test import configuration for `src` and `tests`.

This cleanup affects test import setup only. It does not change source behavior,
schema, canonicalization, verifier behavior, dependency versions, real signature
verification, or passport-verifier `ALLOW` behavior.

Tests:
`python tools/secret_scan.py --all` passed.

`python -m pytest tests/test_composition.py -q` passed with 20 tests.

`python -m pytest tests/test_passport_verifier_signature_input.py -q` passed with 15 tests.

`python -m pytest -q` passed with 602 tests.

Not implemented:
package installation, `pyproject.toml`, editable install, source changes,
dependency changes, verifier behavior changes, real signature verification,
cloud deployment, or passport-verifier `ALLOW` path.

Next step:
Push the cleanup and continue the next review step separately.

## Entry 120

Date: 2026-06-10

Type: Test configuration baseline

Summary: Tightened the pytest configuration.

Files:
Updated `pytest.ini`.

Result:
The test configuration now records the expected pytest baseline, limits default
test discovery to `tests`, keeps the explicit `src` and `tests` import paths,
and enables stricter pytest behavior for configuration, markers,
parametrization IDs, and xfail handling.

This improves the testing baseline before deeper file-by-file test and source
review. The change affects test execution configuration only. It does not
change source behavior, schema behavior, dependency versions, canonicalization,
verifier behavior, real signature verification, cloud deployment, or
passport-verifier `ALLOW` behavior.

Runtime baseline:
A full test run passed with 602 tests in about 1.3 seconds in the official
development environment. A duration run also passed and showed the slowest
tests were small local scanner and verifier-boundary tests.

Tests:
`python tools/secret_scan.py --all` passed.

`python -m pytest -q` passed with 602 tests.

`python -m pytest -q --durations=20 --durations-min=0.001` passed with 602 tests.

Not implemented:
source changes, test logic changes, package installation, editable install,
dependency changes, verifier behavior changes, real signature verification,
runtime optimization, cloud deployment, or passport-verifier `ALLOW` path.

Next step:
Continue file-by-file test and source review with security, readability,
runtime, and maintainability in mind.
