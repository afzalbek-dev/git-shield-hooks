"""Git hooks installer for Git Shield."""
import os
import stat

HOOK_SCRIPT = """#!/usr/bin/env sh
# Git Shield Pre-Commit Security Hook
if command -v git-shield >/dev/null 2>&1; then
    git-shield scan --staged-only
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        echo "🚨 Git Shield: Commit rad etildi! Maxfiy tokenlar yoki katta fayllar aniqlandi."
        exit 1
    fi
elif python3 -m git_shield.cli >/dev/null 2>&1; then
    python3 -m git_shield.cli scan
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        echo "🚨 Git Shield: Commit rad etildi! Maxfiy tokenlar yoki katta fayllar aniqlandi."
        exit 1
    fi
fi
exit 0
"""

def install_pre_commit_hook(repo_dir: str = ".") -> bool:
    git_dir = os.path.join(repo_dir, ".git")
    if not os.path.isdir(git_dir):
        return False

    hooks_dir = os.path.join(git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    hook_path = os.path.join(hooks_dir, "pre-commit")

    with open(hook_path, "w", encoding="utf-8") as f:
        f.write(HOOK_SCRIPT)

    st = os.stat(hook_path)
    os.chmod(hook_path, st.st_mode | stat.S_IEXEC)
    return True
