#!/usr/bin/env python3
"""Stage, commit, push, and create PR from branch and Linear issue."""
import argparse
import os
import re
import subprocess
import sys

from linear_utils import get_issue_by_key, set_issue_state, slug
from platform_utils import copy_to_clipboard

# Strip bracket-paste escape sequences (^[[200~, ^[[201~) and other junk from argv
# Some terminals (e.g. Warp) emit these when pasting commands
def _sanitize_argv() -> None:
    for i, arg in enumerate(sys.argv):
        cleaned = re.sub(r"\x1b\[2?0?[01]~", "", arg)  # \e[200~, \e[201~, \e[20~, \e[21~
        cleaned = re.sub(r"^\^P", "", cleaned)  # Leading ^P from some paste flows
        sys.argv[i] = cleaned.strip()


_sanitize_argv()

DONE_STATE = os.environ.get("LINEAR_DONE_STATE", "Done")


def get_base_branch() -> str:
    """Get base branch for diff (origin/main, origin/master, or LINEAR_MAIN_BRANCH)."""
    if base := os.environ.get("LINEAR_MAIN_BRANCH"):
        return base
    try:
        default = subprocess.check_output(
            ["git", "config", "--get", "init.defaultBranch"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if default:
            return f"origin/{default}"
    except subprocess.CalledProcessError:
        pass
    return "origin/main"


def is_base_branch(branch: str, base: str) -> bool:
    """Check if current branch is the base (e.g. main)."""
    local_base = base.replace("origin/", "") if base.startswith("origin/") else base
    return branch == local_base


parser = argparse.ArgumentParser(description="Stage, commit, push, and create PR from branch and Linear issue")
parser.add_argument("--issue", help="Override: issue key (e.g. FIN-587) instead of from branch")
parser.add_argument("--no-create", action="store_true", help="Skip creating PR via gh (only copy to clipboard)")
parser.add_argument("--skip-commit", action="store_true", help="Skip stage/commit/push (already committed, just create PR)")
parser.add_argument("--no-status", action="store_true", help=f"Do not set Linear issue to {DONE_STATE}")
args = parser.parse_args()

branch = subprocess.check_output(
    ["git", "rev-parse", "--abbrev-ref", "HEAD"]
).decode().strip()

if args.issue:
    issue_key = args.issue.upper()
else:
    m = re.search(r"([a-z]+-\d+)", branch, re.IGNORECASE)
    if not m:
        sys.exit("Branch name must contain issue key (e.g. lin-123) or use --issue FIN-587")
    issue_key = m.group(1).upper()

if not re.match(r"^[A-Za-z]+-\d+$", issue_key):
    sys.exit(f"Invalid issue key format: {issue_key} (expected e.g. FIN-587)")

issue = get_issue_by_key(issue_key)
if not issue:
    sys.exit(f"Issue {issue_key} not found in Linear")

base = get_base_branch()

# Create branch if on base (e.g. main)
created_branch = False
if is_base_branch(branch, base) and not args.skip_commit:
    new_branch = f"{issue['identifier'].lower()}-{slug(issue['title'])}"
    subprocess.run(["git", "checkout", "-b", new_branch], check=True)
    branch = new_branch
    created_branch = True

# Stage, commit, and push (unless --skip-commit)
if not args.skip_commit:
    subprocess.run(["git", "add", "-A"], check=True)
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    if status:
        subprocess.run(
            ["git", "commit", "-m", f"{issue['identifier']}: {issue['title']}"],
            check=True,
        )
        # Always use -u for first push (branch created by ai-start has no upstream yet)
        subprocess.run(["git", "push", "-u", "origin", branch], check=True)
    else:
        print("Nothing to commit (working tree clean, no staged changes).")
        print("PR description will be generated from existing commits.")
        print("If you meant to commit first, do so and run ai-pr again (or use --skip-commit).")

diffstat = subprocess.check_output(
    ["git", "diff", "--stat", f"{base}...HEAD"]
).decode()

body = f"""## Summary
Implements {issue['identifier']}: {issue['title']}

## What changed
{diffstat}

## Why
{issue['title']}

## Testing & Validation
- [ ] Run tests locally
- [ ] CI passes

## Linked issues
Closes {issue['identifier']}

## Known limitations & risks
_None_
"""

if copy_to_clipboard(body):
    print("PR description copied to clipboard.")
else:
    print("Could not copy to clipboard. Paste manually:")
    print(body[:300] + "..." if len(body) > 300 else body)

# Create PR via GitHub CLI
pr_created = False
if not args.no_create:
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
        result = subprocess.run(["gh", "pr", "create", "--body", body])
        pr_created = result.returncode == 0
        if pr_created and not args.no_status:
            set_issue_state(issue, DONE_STATE)
        sys.exit(result.returncode)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GitHub CLI (gh) not found. Install: https://cli.github.com/")
        print("PR description is in clipboard. Create PR manually or run with --no-create")
        sys.exit(1)
else:
    if not args.no_status:
        set_issue_state(issue, DONE_STATE)
