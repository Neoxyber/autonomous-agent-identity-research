"""Tests for the local secret and public-risk scanner CLI.

The scanner is a local pre-commit guard for this research repository. These
tests use temporary files and constructed dummy values only; they do not place
real credentials, personal data, private keys, or live operational data in the
repository.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tools" / "secret_scan.py"


def run_scan(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--path", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def write_sample(tmp_path: Path, filename: str, content: str) -> Path:
    sample = tmp_path / filename
    sample.write_text(content, encoding="utf-8")
    return sample


def assert_scan_passes(path: Path) -> None:
    result = run_scan(path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Secret/public-risk scan passed." in result.stdout


def assert_scan_fails(path: Path, rule: str) -> None:
    result = run_scan(path)

    assert result.returncode == 1
    assert "SECRET/PUBLIC-RISK SCAN FAILED" in result.stdout
    assert rule in result.stdout


@pytest.mark.parametrize(
    ("filename", "content"),
    [
        (
            "clean.md",
            "Research tests use dummy data.\n"
            "Temporary experiments run outside the repository.\n"
            "SHA-256 evidence may be summarized without copying raw artifacts.\n",
        ),
        (
            "dummy.py",
            'PLANTED_SECRETS = ["SIGSECRET", "TOKENSECRET", "TOPSECRET"]\n',
        ),
        (
            "evidence.md",
            "Artifact SHA-256: "
            "bd72e68b06bb1e96913f97dd4901119bc17f39d4586a5adf2d3e47bc2b9d58b5\n",
        ),
        (
            "authorization.py",
            "decision = authorize_action(passport, dict(ACT), "
            "unknown_action=REQUIRE_HUMAN_REVIEW)\n"
            "def test_checked_helper_passes_when_bound_and_authority_trusted():\n"
            "    pass\n",
        ),
        (
            "public-contact.md",
            "Security contact: security@aixybertech.com\n",
        ),
    ],
    ids=[
        "clean-research-text",
        "dummy-no-leak-fixtures",
        "public-sha256-evidence",
        "authorization-words",
        "public-contact-email",
    ],
)
def test_clean_or_allowlisted_inputs_pass(
    tmp_path: Path,
    filename: str,
    content: str,
) -> None:
    assert_scan_passes(write_sample(tmp_path, filename, content))


@pytest.mark.parametrize(
    ("filename", "content", "rule"),
    [
        (
            "bad.pem",
            "-----BEGIN " + "PRIVATE KEY-----\nabc\n"
            "-----END " + "PRIVATE KEY-----\n",
            "private-key-block",
        ),
        (
            "bad.env",
            "OPENAI_" + "API_KEY=sk-" + "abcdefghijklmnop"
            "qrstuvwxyz123456\n",
            "openai_style_key",
        ),
        (
            "bad.txt",
            "pass" + 'word = "correct-horse-battery-staple"\n',
            "secret-assignment",
        ),
        (
            "bad-path.md",
            "The output was stored in /" + "home/alice/private-run.\n",
            "private-local-path",
        ),
        (
            "bad-url.txt",
            "remote = https" + "://user:pass" + "@example.com/repo.git\n",
            "url-embedded-credentials",
        ),
        (
            "bad-remote.txt",
            "origin = " + "git" + "@github.com:example/private-repo.git\n",
            "private-remote",
        ),
        (
            "bad-ip.log",
            "Internal endpoint " + "10" + ".0.0.5 responded.\n",
            "private-ip",
        ),
        (
            "bad-email.csv",
            "operator email: " + "alice" + "@example.com\n",
            "email-in-data-context",
        ),
        (
            "bad-phone.csv",
            "customer phone: "
            + "+44 "
            + "7700"
            + " 900"
            + "123\n",
            "phone-in-data-context",
        ),
        (
            "bad-entropy.txt",
            "secret material "
            + "AbCdEfGhIjKlMnOp"
            + "QrStUvWxYz123456"
            + "7890abcd\n",
            "high-entropy-secret-context",
        ),
    ],
    ids=[
        "private-key-block",
        "known-openai-style-key",
        "secret-assignment",
        "private-local-path",
        "url-embedded-credentials",
        "private-remote",
        "private-ip",
        "email-data-context",
        "phone-data-context",
        "high-entropy-secret-context",
    ],
)
def test_risky_inputs_fail_closed(
    tmp_path: Path,
    filename: str,
    content: str,
    rule: str,
) -> None:
    assert_scan_fails(write_sample(tmp_path, filename, content), rule)


def test_cli_help_lists_scan_modes() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0
    assert "--staged" in result.stdout
    assert "--all" in result.stdout
    assert "--path" in result.stdout
