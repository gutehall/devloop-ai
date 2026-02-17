#!/usr/bin/env python3
"""Create GitHub PR with clipboard content. Runs ai-pr first if clipboard empty."""
import os
import subprocess
import sys

from platform_utils import paste_from_clipboard

AI_DIR = os.path.dirname(__file__)


def main():
    # Check gh is available
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GitHub CLI (gh) required. Install: https://cli.github.com/")
        sys.exit(1)

    body = paste_from_clipboard().strip()

    if not body:
        # Run ai-pr to generate description
        ai_pr = os.path.join(AI_DIR, "ai_pr.py")
        result = subprocess.run([sys.executable, ai_pr])
        if result.returncode != 0:
            sys.exit(result.returncode)
        body = paste_from_clipboard().strip()
        if not body:
            print("ai-pr produced no output.")
            sys.exit(1)

    result = subprocess.run(
        ["gh", "pr", "create", "--body", body],
        capture_output=False,
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
