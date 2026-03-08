#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

from platform_utils import copy_to_clipboard

API = os.environ.get("LINEAR_API_KEY")
if not API:
    sys.exit("Missing LINEAR_API_KEY")


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


def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    auth = API if API.startswith("Bearer ") or API.startswith("lin_api_") else f"Bearer {API}"
    req = urllib.request.Request(
        "https://api.linear.app/graphql",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": auth,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else str(e)
        sys.exit(f"Linear API error {e.code}: {body}")

parser = argparse.ArgumentParser(description="Generate PR description from branch and Linear issue")
parser.add_argument("--issue", help="Override: issue key (e.g. FIN-587) instead of from branch")
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

m = re.match(r"^([A-Za-z]+)-(\d+)$", issue_key)
if not m:
    sys.exit(f"Invalid issue key format: {issue_key} (expected e.g. FIN-587)")
team_key, issue_num = m.group(1).upper(), int(m.group(2))

query = """
query IssueByTeamAndNumber($teamKey: String!, $number: Float!) {
  issues(filter: { team: { key: { eq: $teamKey } }, number: { eq: $number } }, first: 1) {
    nodes {
      identifier
      title
    }
  }
}
"""
data = gql(query, {"teamKey": team_key, "number": float(issue_num)})
nodes = data.get("data", {}).get("issues", {}).get("nodes", [])
if not nodes:
    sys.exit(f"Issue {issue_key} not found in Linear")
issue = nodes[0]

base = get_base_branch()

# Stage, commit, and push
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(
    ["git", "commit", "-m", f"{issue['identifier']}: {issue['title']}"],
)  # may fail if nothing to commit
subprocess.run(["git", "push"], check=True)

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
