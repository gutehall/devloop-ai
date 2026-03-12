#!/usr/bin/env python3
"""Update Linear issue state. Usage: ai-status LIN-123 "In Progress" """
import argparse
import sys

from linear_utils import get_issue_by_key, set_issue_state


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update Linear issue state.",
        epilog='Example: ai-status LIN-123 "In Progress"',
    )
    parser.add_argument("identifier", help="Issue key (e.g. LIN-123)")
    parser.add_argument("state", nargs="+", help='Target state name (e.g. "In Progress")')
    args = parser.parse_args()

    identifier = args.identifier.upper()
    target_state_name = " ".join(args.state)

    issue = get_issue_by_key(identifier)
    if not issue:
        print(f"Could not find issue {identifier}")
        sys.exit(1)

    print(f"Current state: {issue['state']['name']}")

    set_issue_state(issue, target_state_name)


if __name__ == "__main__":
    main()
