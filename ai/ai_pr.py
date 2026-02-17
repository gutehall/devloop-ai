#!/usr/bin/env python3
import os, re, subprocess, sys, json, urllib.request

API = os.environ.get("LINEAR_API_KEY")
if not API:
    sys.exit("Missing LINEAR_API_KEY")

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

diffstat = subprocess.check_output(
    ["git", "diff", "--stat", "origin/main...HEAD"]
).decode()

body = f"""## Summary
Implements {issue['identifier']}: {issue['title']}

## Changes
{diffstat}

Closes {issue['identifier']}
"""

p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
p.communicate(body.encode("utf-8"))

print("PR description copied to clipboard.")
