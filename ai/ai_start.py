#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys

from cursor_utils import CURSOR_FAST_PROMPT, build_cursor_payload
from linear_utils import gql, set_issue_state, slug
from platform_utils import copy_to_clipboard, open_cursor, run_cursor_agent

READY_STATE = os.environ.get("LINEAR_READY_STATE", "Ready for build")
IN_PROGRESS_STATE = os.environ.get("LINEAR_IN_PROGRESS_STATE", "In Progress")
PROMPT_DIR = os.path.join(os.path.dirname(__file__), "..", "prompt")


def load_prompt(name: str) -> str | None:
    """Load prompt from file. Tries cursor_<name>.md then <name>.md."""
    for candidate in (f"cursor_{name}", name):
        path = os.path.join(PROMPT_DIR, f"{candidate}.md")
        if os.path.isfile(path):
            with open(path) as f:
                return f.read()
    return None


def create_or_checkout_branch(issue: dict) -> str:
    """Create branch or checkout if it already exists. Returns branch name."""
    branch = f"{issue['identifier'].lower()}-{slug(issue['title'])}"
    if subprocess.run(["git", "checkout", "-b", branch], stderr=subprocess.DEVNULL).returncode != 0:
        subprocess.check_call(["git", "checkout", branch])
    return branch


def main() -> None:
    parser = argparse.ArgumentParser(description="Pick issue, create branch, open Cursor")
    parser.add_argument("--prompt", help="Prompt mode (e.g. velocity, bugfix, refactor)")
    parser.add_argument("--agent", action="store_true", help="Run Cursor agent CLI instead of opening editor (skips paste)")
    parser.add_argument("--no-status", action="store_true", help="Do not set Linear status to In Progress")
    parser.add_argument("choice", nargs="?", type=str, help="Issue number to select (e.g. 5) — skips interactive prompt")
    args = parser.parse_args()

    if not os.environ.get("LINEAR_API_KEY"):
        print("Missing LINEAR_API_KEY env var")
        sys.exit(1)

    prompt_text = CURSOR_FAST_PROMPT
    if args.prompt:
        loaded = load_prompt(args.prompt)
        if loaded:
            prompt_text = loaded
        else:
            print(f"Prompt '{args.prompt}' not found, using default.")

    query = """
    query Issues($filter: IssueFilter) {
      issues(first: 25, filter: $filter) {
        nodes {
          id
          identifier
          title
          description
          url
          team { id name }
        }
      }
    }
    """
    variables = {"filter": {"state": {"name": {"eq": READY_STATE}}}}
    data = gql(query, variables)
    issues = data.get("data", {}).get("issues", {}).get("nodes", [])

    if not issues:
        print("No issues found.")
        sys.exit(0)

    for i, it in enumerate(issues, 1):
        print(f"{i}. {it['identifier']} — {it['title']}")

    choice_raw = args.choice if args.choice is not None else input("Select issue #: ")
    choice_clean = "".join(choice_raw.split()).strip() or choice_raw.strip()
    try:
        choice_idx = int(choice_clean)
        if not (1 <= choice_idx <= len(issues)):
            raise ValueError("out of range")
    except (ValueError, TypeError):
        recv = repr(choice_raw[:50]) if choice_raw else "(empty)"
        print(f"Invalid selection: got {recv}. Enter a number from 1 to {len(issues)}.")
        sys.exit(1)

    issue = issues[choice_idx - 1]
    branch = create_or_checkout_branch(issue)

    if not args.no_status:
        set_issue_state(issue, IN_PROGRESS_STATE)

    payload = build_cursor_payload(issue, prompt_text)
    if copy_to_clipboard(payload):
        print("Prompt copied to clipboard.")
    else:
        print("Could not copy to clipboard. Paste manually:")
        print(payload[:200] + "..." if len(payload) > 200 else payload)

    if args.agent and run_cursor_agent(payload, "."):
        print("Started Cursor agent CLI.")
    else:
        open_cursor(".")
        if args.agent:
            print("Cursor agent CLI not found. Opened Cursor editor — paste (⌘V) to implement.")

    print("Branch created:", branch)


if __name__ == "__main__":
    main()
