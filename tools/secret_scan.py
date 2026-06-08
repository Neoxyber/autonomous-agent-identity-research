#!/usr/bin/env python3
"""Strict local secret and public-risk scanner.

This scanner is intentionally local, deterministic, and stdlib-only.

It is designed for the research repository's current rule:

- use dummy data only;
- do not commit real secrets, private keys, credentials, tokens, private paths,
  live logs, personal data, or confidential operational data;
- keep isolated experiment artifacts outside the repository;
- record only the minimum useful evidence.

The scanner is not a replacement for GitHub secret scanning, push protection,
Gitleaks, or careful human review. It is an early fail-closed guard for commits.
"""

from __future__ import annotations

import argparse
import math
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


MAX_TEXT_BYTES = 750_000

SKIP_DIR_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
}

SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".tgz",
    ".whl",
    ".pyc",
    ".sqlite",
    ".db",
}

# Intentional dummy/test-only values used in this repository to prove no-leak
# behavior. These exact values are allowed; real secrets with similar names are
# not allowed.
ALLOWLIST_EXACT_TOKENS = {
    "SIGSECRET",
    "TOKENSECRET",
    "MFASECRET",
    "DOCSECRET",
    "BIOSECRET",
    "TOPSECRET",
}

ALLOWLIST_LINE_FRAGMENTS = {
    "Use no secrets or credentials.",
    "Do not commit secrets, private keys, credentials",
    "not intended to contain real users",
    "not use real users, real organizations, real secrets",
    "run production credentials or real agent data",
    "private key type: `MLDSA65PrivateKey`",
    "secret key: `4032` bytes",
    "repository path: `~/projects/autonomous-agent-identity-research`",
    "isolated experiment path: `/tmp/",
    "isolated virtual environment: `/tmp/",
    "isolated test path: `/tmp/",
    "isolated inspection path: `/tmp/",
    "isolated artifact path: `/tmp/",
    "isolated installation path: `/tmp/",
    "PRIVATE_REMOTE_RE = re.compile(",
}

PUBLIC_EVIDENCE_CONTEXT = (
    "sha-256",
    "sha256",
    "digest",
    "hash",
    "commit",
    "artifact",
    "wheel",
    "source distribution",
    "nist",
    "acvp",
    "github.com",
    "pypi",
    "sigstore",
    "rekor",
    "fulcio",
    "oidc",
    "token.actions.githubusercontent.com",
    "expectedresults.json",
    "prompt.json",
    "ml-dsa",
    "mldsa",
    "ref-",
)

SECRET_CONTEXT_WORDS = (
    "password",
    "passwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "access_key",
    "client_secret",
    "private_key",
    "private-key",
    "credential",
    "credentials",
    "bearer",
)

@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str
    message: str
    text: str


PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN (?:RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----|"
    r"-----END (?:RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"
)

KNOWN_SECRET_RES = {
    "aws_access_key": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "github_token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{30,}\b"),
    "github_fine_grained_pat": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "gitlab_token": re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    "openai_style_key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "google_api_key": re.compile(r"\bAIza[A-Za-z0-9_-]{20,}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
}

ASSIGNMENT_RE = re.compile(
    r"(?i)\b(password|passwd|secret|token|api[_-]?key|access[_-]?key|"
    r"client[_-]?secret|private[_-]?key|credential|credentials)\b"
    r"\s*[:=]\s*['\"]?([^'\"\s`#]{8,})"
)

URL_WITH_CREDENTIALS_RE = re.compile(
    r"\b(?:https?|ssh|git)://[^/\s:@]+:[^/\s:@]+@"
)

LOCAL_PRIVATE_PATH_RE = re.compile(
    r"(?<![`A-Za-z0-9_./-])(?:/home/[A-Za-z0-9_.-]+|/Users/[A-Za-z0-9_.-]+|"
    r"C:\\\\Users\\\\[A-Za-z0-9_.-]+)"
)

PRIVATE_REMOTE_RE = re.compile(r"\b(?:git@|ssh://)")
PRIVATE_IP_RE = re.compile(
    r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})\b"
)

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(?:\+?\d[\d .()/-]{8,}\d)\b")

HIGH_ENTROPY_RE = re.compile(r"[A-Za-z0-9_/\+=.-]{32,}")


def _repo_root() -> Path:
    out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
    return Path(out.strip())


def _git_files(args: list[str]) -> list[Path]:
    out = subprocess.check_output(args, text=False)
    return [Path(p.decode()) for p in out.split(b"\0") if p]


def staged_files() -> list[Path]:
    return _git_files([
        "git",
        "diff",
        "--cached",
        "--name-only",
        "--diff-filter=ACMRT",
        "-z",
    ])


def tracked_files() -> list[Path]:
    return _git_files(["git", "ls-files", "-z"])


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIR_PARTS:
        return True
    if path.suffix.lower() in SKIP_SUFFIXES:
        return True
    return False


def read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None

    if len(data) > MAX_TEXT_BYTES:
        return None

    if b"\x00" in data:
        return None

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return data.decode("utf-8", errors="replace")
        except Exception:
            return None


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    counts = {char: value.count(char) for char in set(value)}
    return -sum((count / len(value)) * math.log2(count / len(value)) for count in counts.values())


def has_public_evidence_context(line: str) -> bool:
    lower = line.lower()
    return any(fragment in lower for fragment in PUBLIC_EVIDENCE_CONTEXT)


def has_secret_context(line: str) -> bool:
    lower = line.lower()
    return any(word in lower for word in SECRET_CONTEXT_WORDS)


def is_allowlisted_line(line: str) -> bool:
    if any(fragment in line for fragment in ALLOWLIST_LINE_FRAGMENTS):
        return True
    tokens = set(re.findall(r"[A-Za-z0-9_]+", line))
    return bool(tokens & ALLOWLIST_EXACT_TOKENS)


def redacted(line: str) -> str:
    line = line.strip()
    if len(line) <= 180:
        return line
    return line[:177] + "..."


def add(findings: list[Finding], path: Path, line_no: int, rule: str, message: str, line: str) -> None:
    findings.append(
        Finding(
            path=str(path),
            line=line_no,
            rule=rule,
            message=message,
            text=redacted(line),
        )
    )


def scan_text(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []

    for line_no, line in enumerate(text.splitlines(), 1):
        if is_allowlisted_line(line):
            continue

        if PRIVATE_KEY_RE.search(line):
            add(findings, path, line_no, "private-key-block", "private key block marker found", line)

        for name, pattern in KNOWN_SECRET_RES.items():
            if pattern.search(line):
                add(findings, path, line_no, name, "known secret/token pattern found", line)

        if URL_WITH_CREDENTIALS_RE.search(line):
            add(findings, path, line_no, "url-embedded-credentials", "URL appears to contain credentials", line)

        match = ASSIGNMENT_RE.search(line)
        if match:
            candidate_value = match.group(2)
            if candidate_value not in ALLOWLIST_EXACT_TOKENS and not has_public_evidence_context(line):
                add(findings, path, line_no, "secret-assignment", "secret-like assignment found", line)

        if LOCAL_PRIVATE_PATH_RE.search(line):
            add(findings, path, line_no, "private-local-path", "private local user path found", line)

        if PRIVATE_REMOTE_RE.search(line):
            add(findings, path, line_no, "private-remote", "SSH/private remote pattern found", line)

        if PRIVATE_IP_RE.search(line):
            add(findings, path, line_no, "private-ip", "private/internal IP address found", line)

        # Avoid blocking the public SECURITY contact or project metadata unless it
        # appears in a data-like context. This catches accidental lists of personal
        # data without treating a public contact address as a leak.
        if EMAIL_RE.search(line) and re.search(r"(?i)\b(customer|client|user|operator|personal data|dataset|log)\b", line):
            add(findings, path, line_no, "email-in-data-context", "email address appears in data context", line)

        if PHONE_RE.search(line) and re.search(r"(?i)\b(customer|client|user|operator|personal data|phone)\b", line):
            add(findings, path, line_no, "phone-in-data-context", "phone number appears in data context", line)

        for token in HIGH_ENTROPY_RE.findall(line):
            if token in ALLOWLIST_EXACT_TOKENS:
                continue
            entropy = shannon_entropy(token)
            if entropy < 3.9:
                continue
            if has_public_evidence_context(line):
                continue
            if has_secret_context(line):
                add(
                    findings,
                    path,
                    line_no,
                    "high-entropy-secret-context",
                    "high-entropy token in secret-like context",
                    line,
                )

    return findings


def scan_paths(paths: Iterable[Path], root: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    root = root or Path.cwd()

    for path in sorted(set(paths)):
        if should_skip(path):
            continue
        full_path = path if path.is_absolute() else root / path
        if not full_path.exists() or not full_path.is_file():
            continue
        text = read_text(full_path)
        if text is None:
            continue
        display_path = path if not path.is_absolute() else Path(os.path.relpath(path, root))
        findings.extend(scan_text(display_path, text))

    return findings


def print_findings(findings: list[Finding]) -> None:
    for item in findings:
        print(f"{item.path}:{item.line}: {item.rule}: {item.message}")
        print(f"    {item.text}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Strict local secret/public-risk scanner")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--staged", action="store_true", help="scan staged files")
    mode.add_argument("--all", action="store_true", help="scan all tracked files")
    mode.add_argument("--path", action="append", default=[], help="scan a path; can be repeated")
    args = parser.parse_args(argv)

    root = _repo_root() if (args.staged or args.all) else Path.cwd()

    if args.all:
        paths = tracked_files()
    elif args.path:
        paths = [Path(p) for p in args.path]
    else:
        paths = staged_files()

    findings = scan_paths(paths, root=root)

    if findings:
        print("\nSECRET/PUBLIC-RISK SCAN FAILED\n")
        print_findings(findings)
        print(
            "\nRemove the risky data, replace it with dummy data, or keep the "
            "experiment artifact outside the repository. Do not bypass this "
            "scanner for real secrets or personal/confidential data.\n"
        )
        return 1

    print("Secret/public-risk scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
