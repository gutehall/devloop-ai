#!/usr/bin/env python3
"""Update Linear issue state. Usage: ai-status LIN-123 "In Progress" """
import sys

from linear_utils import get_issue_by_key, set_issue_state


def usage():
    print('Usage: ai-status LIN-123 "In Progress"')
    sys.exit(1)


if len(sys.argv) < 3:
    usage()

identifier = sys.argv[1].upper()
target_state_name = " ".join(sys.argv[2:])

issue = get_issue_by_key(identifier)
if not issue:
    print(f"Could not find issue {identifier}")
    sys.exit(1)

print(f"Current state: {issue['state']['name']}")

set_issue_state(issue, target_state_name)
