# Security Policy

## Purpose

This repository contains research and a future reference implementation for autonomous agent identity.

The project is experimental. It should not be treated as production security software.

## Supported status

The repository is currently in the research foundation stage.

There is no production release and no supported production deployment.

## Reporting security issues

If you find a security issue in this repository, please report it privately before opening a public issue.

Contact:

security@aixybertech.com

Please include:

1. A clear description of the issue.

2. The affected file, document, or implementation area.

3. Steps to reproduce the issue if implementation code is involved.

4. Any possible impact.

5. Any suggested fix or mitigation.

## Sensitive material

Do not commit secrets, private keys, credentials, access tokens, service account files, database dumps, or private identity material to this repository.

The repository includes a .gitignore file that excludes common secret and private key formats, but contributors are still responsible for reviewing their changes before committing.

## Cryptographic research notice

The cryptographic material in this repository is for research and evaluation.

Future implementation work may include post-quantum signature experiments, passport verification, key rotation, and revocation testing. These should be treated as experimental until independently reviewed.

## Legal and compliance notice

This repository does not claim legal compliance, production readiness, or formal certification.

Research documents may discuss regulatory and governance requirements, but those discussions are not legal advice.

## Responsible use

The purpose of this research is to improve accountability, verification, permission control, revocation, and auditability for autonomous agents.

The project should not be used to hide agent activity, impersonate users, bypass access control, or weaken audit trails.

## Local secret and public-risk scan

A local secret and public-risk scan has been added as an additional research
safety guard.

This is an early layer. It will improve over time as the research continues,
and additional safety layers will be reviewed and added through small,
careful changes.
