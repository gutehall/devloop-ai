#!/usr/bin/env python3
import json, os, re, subprocess, sys, urllib.request

API = os.environ.get("LINEAR_API_KEY")
READY_STATE = os.environ.get("LINEAR_READY_STATE", "Ready for build")

if not API:
    print("Missing LINEAR_API_KEY env var")
    sys.exit(1)

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

query = """
query Issues($filter: IssueFilter) {
  issues(first: 25, filter: $filter) {
    nodes {
      id
      identifier
      title
      description
      url
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

payload = f"{CURSOR_FAST_PROMPT}\n\nTitle: {issue['title']}\n\n{issue.get('description','')}"
p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
p.communicate(payload.encode("utf-8"))

subprocess.Popen(["open", "-a", "Cursor", "."])

print("Branch created:", branch)
print("Prompt copied to clipboard.")
