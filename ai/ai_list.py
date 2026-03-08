#!/usr/bin/env python3
"""List Linear issues. Default: Ready for build."""
import argparse
import os
import sys

from linear_utils import gql, set_issue_state

READY_STATE = os.environ.get("LINEAR_READY_STATE", "Ready for build")
PLANNED_STATE = os.environ.get("LINEAR_PLANNED_STATE", "Planned")


def get_viewer_id() -> str:
    q = """
    query Viewer {
      viewer { id }
    }
    """
    data = gql(q)
    return data.get("data", {}).get("viewer", {}).get("id", "")


def _parse_selection(choice: str, n: int) -> list[int]:
    """Parse '1,3,5' or '1-3' into list of 1-based indices. Returns [] if invalid."""
    choice = choice.strip()
    if not choice:
        return []
    indices = []
    for part in choice.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            try:
                lo, hi = int(a.strip()), int(b.strip())
                if 1 <= lo <= hi <= n:
                    indices.extend(range(lo, hi + 1))
                else:
                    return []
            except ValueError:
                return []
        else:
            try:
                i = int(part)
                if 1 <= i <= n:
                    indices.append(i)
                else:
                    return []
            except ValueError:
                return []
    return sorted(set(indices))


def main():
    parser = argparse.ArgumentParser(description="List Linear issues")
    parser.add_argument("--state", default=READY_STATE, help=f"Filter by state (default: {READY_STATE})")
    parser.add_argument("--mine", action="store_true", help="Only issues assigned to me")
    parser.add_argument("--limit", type=int, default=25, help="Max issues to show (default: 25)")
    parser.add_argument(
        "--move-to-ready",
        action="store_true",
        help="After listing, prompt to move selected issues to Ready for build (use with --state Planned)",
    )
    args = parser.parse_args()

    if args.move_to_ready and args.state == READY_STATE:
        args.state = PLANNED_STATE

    filter_parts = {"state": {"name": {"eq": args.state}}}

    if args.mine:
        viewer_id = get_viewer_id()
        if not viewer_id:
            print("Could not get current user")
            sys.exit(1)
        filter_parts["assignee"] = {"id": {"eq": viewer_id}}

    fields = "identifier title state { name } assignee { name }"
    if args.move_to_ready:
        fields += " id team { id name }"

    query = f"""
    query Issues($filter: IssueFilter, $first: Int!) {{
      issues(first: $first, filter: $filter) {{
        nodes {{ {fields} }}
      }}
    }}
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

    if args.move_to_ready:
        print(f"\nMove which to '{READY_STATE}'? (e.g. 1,3,5 or 1-3, or Enter to skip)")
        choice = input("Selection: ").strip()
        indices = _parse_selection(choice, len(issues))
        if indices:
            for i in indices:
                issue = issues[i - 1]
                print(f"\n→ {issue['identifier']} …")
                set_issue_state(issue, READY_STATE, _exit_on_fail=False)
        elif choice:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
