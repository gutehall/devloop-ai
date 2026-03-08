#!/usr/bin/env python3
import os
import re
import subprocess
import sys
import json
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

branch = subprocess.check_output(
    ["git", "rev-parse", "--abbrev-ref", "HEAD"]
).decode().strip()

m = re.search(r"([a-z]+-\d+)", branch, re.IGNORECASE)
if not m:
    sys.exit("Branch name must contain issue key (e.g. lin-123)")

issue_key = m.group(1).upper()

query = """
query Issue($identifier: String!) {
  issue(identifier: $identifier) {
    identifier
    title
  }
}
"""

issue = gql(query, {"identifier": issue_key})["data"]["issue"]

base = get_base_branch()
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
