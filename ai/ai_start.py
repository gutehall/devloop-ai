#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

from linear_utils import gql, set_issue_state, slug
from platform_utils import copy_to_clipboard, open_cursor, run_cursor_agent

READY_STATE = os.environ.get("LINEAR_READY_STATE", "Ready for build")
IN_PROGRESS_STATE = os.environ.get("LINEAR_IN_PROGRESS_STATE", "In Progress")
PROMPT_DIR = os.path.join(os.path.dirname(__file__), "..", "prompt")

CURSOR_FAST_PROMPT = """You are implementing this issue.

Primary goal:
Deliver a working, minimal solution that satisfies acceptance criteria.

Rules:
- Do not refactor unrelated code.
- Do not redesign architecture.
- Keep changes small and focused.
- Follow existing patterns.
- Prefer simple solutions over clever ones.
- Stop if scope expands.
"""


def load_prompt(name: str) -> str | None:
    """Load prompt from file. Tries cursor_<name>.md then <name>.md."""
    for candidate in (f"cursor_{name}", name):
        path = os.path.join(PROMPT_DIR, f"{candidate}.md")
        if os.path.isfile(path):
            with open(path) as f:
                return f.read()
    return None


# Parse args
parser = argparse.ArgumentParser(description="Pick issue, create branch, open Cursor")
parser.add_argument("--prompt", help="Prompt mode (e.g. velocity, bugfix, refactor)")
parser.add_argument("--agent", action="store_true", help="Run Cursor agent CLI instead of opening editor (skips paste)")
parser.add_argument("--no-status", action="store_true", help="Do not set Linear status to In Progress")
args = parser.parse_args()

prompt_text = CURSOR_FAST_PROMPT
if args.prompt:
    loaded = load_prompt(args.prompt)
    if loaded:
        prompt_text = loaded
    else:
        print(f"Prompt '{args.prompt}' not found, using default.")

if not os.environ.get("LINEAR_API_KEY"):
    print("Missing LINEAR_API_KEY env var")
    sys.exit(1)

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

choice = input("Select issue #: ").strip()
if not choice.isdigit() or not (1 <= int(choice) <= len(issues)):
    print("Invalid selection")
    sys.exit(1)

issue = issues[int(choice) - 1]

branch = f"{issue['identifier'].lower()}-{slug(issue['title'])}"
subprocess.check_call(["git", "checkout", "-b", branch])

if not args.no_status:
    set_issue_state(issue, IN_PROGRESS_STATE)

payload = f"{prompt_text}\n\nTitle: {issue['title']}\n\n{issue.get('description','')}"
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
