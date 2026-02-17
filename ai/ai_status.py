#!/usr/bin/env python3
import json
import os
import sys
import urllib.request

API = os.environ.get("LINEAR_API_KEY")

if not API:
    print("Missing LINEAR_API_KEY env var")
    sys.exit(1)

def gql(query: str, variables=None):
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

def usage():
    print('Usage: ai-status LIN-123 "In Progress"')
    sys.exit(1)

if len(sys.argv) < 3:
    usage()

identifier = sys.argv[1].upper()
target_state_name = " ".join(sys.argv[2:])

# 1️⃣ Fetch issue (get issue ID + team ID)
query_issue = """
query IssueByIdentifier($identifier: String!) {
  issue(identifier: $identifier) {
    id
    team { id name }
    state { id name }
  }
}
"""

data = gql(query_issue, {"identifier": identifier})
issue = data.get("data", {}).get("issue")

if not issue:
    print(f"Could not find issue {identifier}")
    sys.exit(1)

issue_id = issue["id"]
team_id = issue["team"]["id"]

print(f"Current state: {issue['state']['name']}")

# 2️⃣ Fetch all states for the team
query_states = """
query TeamStates($teamId: String!) {
  team(id: $teamId) {
    states {
      nodes {
        id
        name
      }
    }
  }
}
"""

data_states = gql(query_states, {"teamId": team_id})
states = data_states.get("data", {}).get("team", {}).get("states", {}).get("nodes", [])

# 3️⃣ Find matching state
match = None
for state in states:
    if state["name"].lower() == target_state_name.lower():
        match = state
        break

if not match:
    print(f'State "{target_state_name}" not found.')
    print("Available states:")
    for s in states:
        print(f"- {s['name']}")
    sys.exit(1)

state_id = match["id"]

# 4️⃣ Update issue state
mutation = """
mutation UpdateIssue($id: String!, $stateId: String!) {
  issueUpdate(id: $id, input: { stateId: $stateId }) {
    success
  }
}
"""

result = gql(mutation, {"id": issue_id, "stateId": state_id})
success = result.get("data", {}).get("issueUpdate", {}).get("success")

if success:
    print(f"✅ Updated {identifier} → {match['name']}")
else:
    print("❌ Failed to update issue")
