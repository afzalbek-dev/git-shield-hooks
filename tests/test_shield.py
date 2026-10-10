"""Unit tests for Git Shield."""
import os
import tempfile
import pytest
from git_shield.scanner import ShieldScanner
from git_shield.installer import install_pre_commit_hook

def test_scanner_detects_tokens():
    scanner = ShieldScanner()

    # Secret test samples
    sample_with_gh_token = "export GH_TOKEN=ghp_ABC1234567890abcdefghijklmnopqrstuv"
    findings = scanner.scan_content(sample_with_gh_token, file_path="config.sh")
    assert len(findings) == 1
    assert findings[0]["type"] == "GitHub Personal Access Token"

    sample_with_bot_token = "BOT_TOKEN = '1234567890:ABCdefGhIjkLmNoPqRsTuVwXyZ_12345678'"
    findings_bot = scanner.scan_content(sample_with_bot_token, file_path="bot.py")
    assert len(findings_bot) == 1
    assert findings_bot[0]["type"] == "Telegram Bot Token"

    # Clean text
    clean_sample = "def calculate_sum(a, b):\n    return a + b\n"
    assert len(scanner.scan_content(clean_sample, file_path="clean.py")) == 0

def test_oversized_file_detection():
    scanner = ShieldScanner(max_file_size_mb=0.001) # ~1KB limit for test
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(b"A" * 2048) # 2KB
        temp_path = tf.name

    try:
        findings = scanner.scan_file(temp_path)
        assert len(findings) >= 1
        assert any(f["type"] == "Oversized File" for f in findings)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_install_pre_commit_hook():
    with tempfile.TemporaryDirectory() as td:
        # Without .git
        assert install_pre_commit_hook(td) is False

        # With .git
        os.makedirs(os.path.join(td, ".git"))
        assert install_pre_commit_hook(td) is True
        hook_file = os.path.join(td, ".git", "hooks", "pre-commit")
        assert os.path.exists(hook_file)
        assert os.access(hook_file, os.X_OK)
