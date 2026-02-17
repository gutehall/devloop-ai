#!/usr/bin/env python3
"""List Linear issues. Default: Ready for build."""
import argparse
import json
import os
import sys
import urllib.request

API = os.environ.get("LINEAR_API_KEY")
READY_STATE = os.environ.get("LINEAR_READY_STATE", "Ready for build")

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


def get_viewer_id() -> str:
    q = """
    query Viewer {
      viewer { id }
    }
    """
    data = gql(q)
    return data.get("data", {}).get("viewer", {}).get("id", "")


def main():
    parser = argparse.ArgumentParser(description="List Linear issues")
    parser.add_argument("--state", default=READY_STATE, help=f"Filter by state (default: {READY_STATE})")
    parser.add_argument("--mine", action="store_true", help="Only issues assigned to me")
    parser.add_argument("--limit", type=int, default=25, help="Max issues to show (default: 25)")
    args = parser.parse_args()

    filter_parts = {"state": {"name": {"eq": args.state}}}

    if args.mine:
        viewer_id = get_viewer_id()
        if not viewer_id:
            print("Could not get current user")
            sys.exit(1)
        filter_parts["assignee"] = {"id": {"eq": viewer_id}}

    query = """
    query Issues($filter: IssueFilter, $first: Int!) {
      issues(first: $first, filter: $filter) {
        nodes {
          identifier
          title
          state { name }
          assignee { name }
        }
      }
    }
    """
    variables = {
        "filter": filter_parts,
        "first": args.limit,
    }
    data = gql(query, variables)
    issues = data.get("data", {}).get("issues", {}).get("nodes", [])

    if not issues:
        print("No issues found.")
        return

    print(f"Issues ({args.state}):\n")
    for i, it in enumerate(issues, 1):
        assignee = it.get("assignee") and it["assignee"].get("name") or "-"
        print(f"  {i}. {it['identifier']} — {it['title']} ({assignee})")


if __name__ == "__main__":
    main()
