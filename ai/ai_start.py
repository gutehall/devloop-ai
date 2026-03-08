#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

from platform_utils import copy_to_clipboard, open_cursor

API = os.environ.get("LINEAR_API_KEY")
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


def gql(query, variables=None):
    req = urllib.request.Request(
        "https://api.linear.app/graphql",
        data=json.dumps({"query": query, "variables": variables or {}}).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": API,
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def slug(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:40]


def set_issue_state(issue, target_state_name: str) -> None:
    """Move issue to the given state in Linear."""
    team_id = issue["team"]["id"]
    issue_id = issue["id"]
    q_states = """
    query TeamStates($teamId: String!) {
      team(id: $teamId) {
        states { nodes { id name } }
      }
    }
    """
    data_states = gql(q_states, {"teamId": team_id})
    states = (
        data_states.get("data", {}).get("team", {}).get("states", {}).get("nodes", [])
    ) or []
    match = next((s for s in states if s["name"].lower() == target_state_name.lower()), None)
    if not match:
        print(f'Could not find state "{target_state_name}" for team {issue["team"]["name"]}.')
        print("Available states:", ", ".join(s["name"] for s in states))
        return
    mutation = """
    mutation UpdateIssue($id: String!, $stateId: String!) {
      issueUpdate(id: $id, input: { stateId: $stateId }) { success }
    }
    """
    res = gql(mutation, {"id": issue_id, "stateId": match["id"]})
    if res.get("data", {}).get("issueUpdate", {}).get("success"):
        print(f'✅ Linear status updated → {match["name"]}')
    else:
        print("❌ Failed to update Linear status")


# Parse args
parser = argparse.ArgumentParser(description="Pick issue, create branch, open Cursor")
parser.add_argument("--prompt", help="Prompt mode (e.g. velocity, bugfix, refactor)")
args = parser.parse_args()

prompt_text = CURSOR_FAST_PROMPT
if args.prompt:
    loaded = load_prompt(args.prompt)
    if loaded:
        prompt_text = loaded
    else:
        print(f"Prompt '{args.prompt}' not found, using default.")

if not API:
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

set_issue_state(issue, IN_PROGRESS_STATE)

payload = f"{prompt_text}\n\nTitle: {issue['title']}\n\n{issue.get('description','')}"
if copy_to_clipboard(payload):
    print("Prompt copied to clipboard.")
else:
    print("Could not copy to clipboard. Paste manually:")
    print(payload[:200] + "..." if len(payload) > 200 else payload)

open_cursor(".")

print("Branch created:", branch)
