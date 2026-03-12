#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys

from cursor_utils import build_cursor_payload
from linear_utils import gql, set_issue_state, slug
from platform_utils import copy_to_clipboard, open_cursor as _open_cursor, run_cursor_agent

READY_STATE = os.environ.get("LINEAR_READY_STATE", "Ready for build")
IN_PROGRESS_STATE = os.environ.get("LINEAR_IN_PROGRESS_STATE", "In Progress")

if not os.environ.get("LINEAR_API_KEY"):
    print("Missing LINEAR_API_KEY env var")
    sys.exit(1)


def sh(cmd: list[str]) -> str:
    return subprocess.check_output(cmd).decode("utf-8", errors="replace").strip()

def run(cmd: list[str]) -> None:
    subprocess.check_call(cmd)

def ensure_clean_worktree():
    status = sh(["git", "status", "--porcelain"])
    if status:
        print("Working tree is not clean. Commit/stash your changes before running ai-go.\n")
        print(status)
        sys.exit(1)

def git_pull_rebase():
    # Equivalent to "git pull --rebase" on current branch
    run(["git", "pull", "--rebase"])

def fetch_ready_issues():
    query = """
    query Issues($filter: IssueFilter) {
      issues(first: 25, filter: $filter, orderBy: updatedAt) {
        nodes {
          id
          identifier
          title
          description
          url
          state { name }
          team { id name }
        }
      }
    }
    """
    variables = {"filter": {"state": {"name": {"eq": READY_STATE}}}}
    data = gql(query, variables)
    return data.get("data", {}).get("issues", {}).get("nodes", []) or []

def pick_issue(issues):
    import re
    for i, it in enumerate(issues, 1):
        print(f"{i}. {it['identifier']} — {it['title']}")
    choice_raw = input("\nSelect issue #: ").strip()
    m = re.search(r"\d+", choice_raw)
    if not m or not (1 <= int(m.group(0)) <= len(issues)):
        print(f"Invalid selection (enter a number from 1 to {len(issues)})")
        sys.exit(1)
    return issues[int(m.group(0)) - 1]

def create_or_checkout_branch(issue):
    """Create branch if it doesn't exist, else checkout existing (resume work)."""
    branch = f"{issue['identifier'].lower()}-{slug(issue['title'])}"
    if subprocess.run(["git", "checkout", "-b", branch], stderr=subprocess.DEVNULL).returncode != 0:
        subprocess.check_call(["git", "checkout", branch])
    return branch


def copy_cursor_payload(issue):
    payload = build_cursor_payload(issue)
    if not copy_to_clipboard(payload):
        print("Could not copy to clipboard. Paste manually:")
        print(payload[:200] + "..." if len(payload) > 200 else payload)

def open_cursor():
    _open_cursor(".")

def main():
    ap = argparse.ArgumentParser(description="ai-go: pull, pick Linear issue, branch, open Cursor, copy prompt.")
    ap.add_argument("--no-pull", action="store_true", help="Do not run git pull --rebase")
    ap.add_argument("--no-status", action="store_true", help=f"Do not set Linear status to {IN_PROGRESS_STATE}")
    ap.add_argument("--agent", action="store_true", help="Run Cursor agent CLI instead of opening editor (skips paste)")
    args = ap.parse_args()

    ensure_clean_worktree()

    if not args.no_pull:
        print("→ git pull --rebase")
        git_pull_rebase()

    print(f"\n→ Fetching Linear issues in state: {READY_STATE}")
    issues = fetch_ready_issues()
    if not issues:
        print(f"No issues found in '{READY_STATE}'.")
        sys.exit(0)

    issue = pick_issue(issues)

    print("\n→ Creating branch")
    branch = create_or_checkout_branch(issue)

    if not args.no_status:
        print(f'\n→ Setting Linear status to "{IN_PROGRESS_STATE}"')
        set_issue_state(issue, IN_PROGRESS_STATE)

    print("\n→ Copying Cursor prompt + issue to clipboard")
    copy_cursor_payload(issue)

    print("\n→ Opening Cursor")
    full_payload = build_cursor_payload(issue)
    if args.agent and run_cursor_agent(full_payload, "."):
        print("Started Cursor agent CLI.")
    else:
        open_cursor()
        if args.agent:
            print("Cursor agent CLI not found. Opened Cursor editor — paste (Ctrl+V / Cmd+V) to implement.")

    print("\n✅ Done")
    print(f"Branch: {branch}")
    print("Next: In Cursor chat, paste (Ctrl+V / Cmd+V) and start implementing.")

if __name__ == "__main__":
    main()