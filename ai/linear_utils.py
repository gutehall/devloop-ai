"""Shared Linear API helpers. Single source for gql, slug, set_issue_state."""
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = os.environ.get("LINEAR_API_KEY")


def _auth_header() -> str:
    """Return Authorization header value with Bearer prefix if needed."""
    if not API:
        return ""
    if API.startswith("Bearer ") or API.startswith("lin_api_"):
        return API
    return f"Bearer {API}"


def gql(query: str, variables: dict | None = None) -> dict:
    """Execute Linear GraphQL query. Exits on API error."""
    if not API:
        sys.exit("Missing LINEAR_API_KEY")
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    auth = _auth_header()
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
        err_body = e.read().decode("utf-8") if e.fp else str(e)
        sys.exit(f"Linear API error {e.code}: {err_body}")


def slug(s: str) -> str:
    """Slugify for branch names."""
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:40]


def get_issue_by_key(issue_key: str) -> dict | None:
    """Fetch issue by identifier (e.g. LIN-123). Returns issue dict or None."""
    m = re.match(r"^([A-Za-z]+)-(\d+)$", issue_key.upper())
    if not m:
        return None
    team_key, issue_num = m.group(1).upper(), int(m.group(2))
    query = """
    query IssueByTeamAndNumber($teamKey: String!, $number: Float!) {
      issues(filter: { team: { key: { eq: $teamKey } }, number: { eq: $number } }, first: 1) {
        nodes {
          id
          identifier
          title
          description
          url
          state { id name }
          team { id name key }
        }
      }
    }
    """
    data = gql(query, {"teamKey": team_key, "number": float(issue_num)})
    nodes = data.get("data", {}).get("issues", {}).get("nodes", [])
    return nodes[0] if nodes else None


def get_team_states(team_id: str) -> list[dict]:
    """Fetch all workflow states for a team."""
    query = """
    query TeamStates($teamId: String!) {
      team(id: $teamId) {
        states { nodes { id name } }
      }
    }
    """
    data = gql(query, {"teamId": team_id})
    return (
        data.get("data", {}).get("team", {}).get("states", {}).get("nodes", [])
        or []
    )


def set_issue_state(
    issue_or_id: dict | str,
    target_state_name: str,
    *,
    _exit_on_fail: bool = True,
) -> bool:
    """
    Move issue to the given state in Linear.

    Args:
        issue_or_id: Issue dict with 'id' and 'team.id', or identifier string (e.g. LIN-123)
        target_state_name: Target state name (e.g. "In Progress", "Ready for build")
        _exit_on_fail: If True, sys.exit on failure. If False, return False.

    Returns:
        True on success, False on failure (only when _exit_on_fail=False).
    """
    if isinstance(issue_or_id, str):
        issue = get_issue_by_key(issue_or_id)
        if not issue:
            print(f"Could not find issue {issue_or_id}")
            if _exit_on_fail:
                sys.exit(1)
            return False
    else:
        issue = issue_or_id

    team_id = issue["team"]["id"]
    issue_id = issue["id"]
    states = get_team_states(team_id)
    match = next(
        (s for s in states if s["name"].lower() == target_state_name.lower()),
        None,
    )
    if not match:
        team_name = issue.get("team", {}).get("name", "?")
        print(f'Could not find state "{target_state_name}" for team {team_name}.')
        print("Available states:", ", ".join(s["name"] for s in states))
        if _exit_on_fail:
            sys.exit(1)
        return False

    mutation = """
    mutation UpdateIssue($id: String!, $stateId: String!) {
      issueUpdate(id: $id, input: { stateId: $stateId }) { success }
    }
    """
    res = gql(mutation, {"id": issue_id, "stateId": match["id"]})
    success = res.get("data", {}).get("issueUpdate", {}).get("success", False)
    if success:
        print(f'✅ Linear status updated → {match["name"]}')
    else:
        print("❌ Failed to update Linear status")
        if _exit_on_fail:
            sys.exit(1)
    return success
