from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "secret_scan.py"


def run_scan(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--path", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_clean_research_text_passes(tmp_path: Path) -> None:
    sample = tmp_path / "clean.md"
    sample.write_text(
        "Research tests use dummy data.\n"
        "Temporary experiments run outside the repository.\n"
        "SHA-256 evidence may be summarized without copying raw artifacts.\n"
    )

    result = run_scan(sample)

    assert result.returncode == 0, result.stdout + result.stderr


def test_dummy_no_leak_fixture_values_are_allowed(tmp_path: Path) -> None:
    sample = tmp_path / "dummy.py"
    sample.write_text(
        'PLANTED_SECRETS = ["SIGSECRET", "TOKENSECRET", "TOPSECRET"]\n'
    )

    result = run_scan(sample)

    assert result.returncode == 0, result.stdout + result.stderr


def test_private_key_block_fails(tmp_path: Path) -> None:
    begin = "-----BEGIN " + "PRIVATE KEY-----"
    end = "-----END " + "PRIVATE KEY-----"
    sample = tmp_path / "bad.pem"
    sample.write_text(f"{begin}\nabc\n{end}\n")

    result = run_scan(sample)

    assert result.returncode == 1
    assert "private-key-block" in result.stdout


def test_known_api_key_pattern_fails(tmp_path: Path) -> None:
    key_name = "OPENAI_" + "API_KEY"
    key_value = "sk" + "-" + "abcdefghijklmnopqrstuvwxyz123456"
    sample = tmp_path / "bad.env"
    sample.write_text(f"{key_name}={key_value}\n")

    result = run_scan(sample)

    assert result.returncode == 1
    assert "openai_style_key" in result.stdout


def test_secret_assignment_fails(tmp_path: Path) -> None:
    field_name = "pass" + "word"
    sample = tmp_path / "bad.txt"
    sample.write_text(f'{field_name} = "correct-horse-battery-staple"\n')

    result = run_scan(sample)

    assert result.returncode == 1
    assert "secret-assignment" in result.stdout


def test_private_local_path_fails(tmp_path: Path) -> None:
    private_path = "/" + "home" + "/alice/private-run"
    sample = tmp_path / "bad.md"
    sample.write_text(f"The output was stored in {private_path}.\n")

    result = run_scan(sample)

    assert result.returncode == 1
    assert "private-local-path" in result.stdout


def test_public_sha256_evidence_passes(tmp_path: Path) -> None:
    sample = tmp_path / "evidence.md"
    sample.write_text(
        "Artifact SHA-256: "
        "bd72e68b06bb1e96913f97dd4901119bc17f39d4586a5adf2d3e47bc2b9d58b5\n"
    )

    result = run_scan(sample)

    assert result.returncode == 0, result.stdout + result.stderr


def test_authorization_words_do_not_trigger_secret_context(tmp_path: Path) -> None:
    sample = tmp_path / "authorization.py"
    sample.write_text(
        "decision = authorize_action(passport, dict(ACT), "
        "unknown_action=REQUIRE_HUMAN_REVIEW)\n"
        "def test_checked_helper_passes_when_bound_and_authority_trusted():\n"
        "    pass\n"
    )

    result = run_scan(sample)

    assert result.returncode == 0, result.stdout + result.stderr
