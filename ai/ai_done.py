#!/usr/bin/env python3
"""Mark current branch's issue as Done."""
import os
import re
import subprocess
import sys

AI_DIR = os.path.dirname(__file__)


def main():
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    ).decode().strip()

    m = re.search(r"([a-z]+-\d+)", branch, re.IGNORECASE)
    if not m:
        print("Branch name must contain issue key (e.g. lin-123)")
        sys.exit(1)

    issue_key = m.group(1).upper()
    ai_status = os.path.join(AI_DIR, "ai_status.py")
    result = subprocess.run([sys.executable, ai_status, issue_key, "Done"])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
