#!/usr/bin/env python3
import json
import os
import re
import sys
import subprocess

try:
    from platform_utils import paste_from_clipboard
except ImportError:
    def paste_from_clipboard() -> str:
        try:
            return subprocess.check_output(["pbpaste"]).decode("utf-8", errors="replace")
        except Exception:
            return ""

from linear_utils import gql, gql_ok, print_errors

DEFAULT_TEAM_ID = os.environ.get("LINEAR_TEAM_ID")
DEFAULT_TEAM_NAME = os.environ.get("LINEAR_TEAM_NAME")


def linear_cli_available() -> bool:
    """Check if linear-cli (schpet/linear-cli) is installed."""
    try:
        subprocess.run(["linear", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def resolve_team_key(team_id: str) -> str | None:
    """Get team key (e.g. ENG) for linear-cli. team_id may be UUID or key."""
    # If short uppercase (e.g. ENG), likely already a key
    if len(team_id) <= 10 and team_id.isupper() and "-" not in team_id:
        return team_id
    q = """
    query Team($id: String!) {
      team(id: $id) { key }
    }
    """
    resp = gql(q, {"id": team_id})
    if gql_ok(resp):
        return resp.get("data", {}).get("team", {}).get("key")
    return None


def create_issue_via_linear_cli(
    issue: dict,
    team_key: str,
    project_name: str | None,
) -> dict | None:
    """Create issue via linear-cli. Returns {identifier, title, url} or None."""
    title = issue.get("title")
    if not title:
        return None

    description = issue.get("description") or ""
    priority = issue.get("priority")
    labels = issue.get("labels") or []
    deps = issue.get("dependencies") or []
    complexity = issue.get("complexity")

    if deps:
        description = f"{description}\n\n---\nDependencies:\n- " + "\n- ".join(deps)
    if complexity is not None:
        description = f"{description}\n\n---\nComplexity: {complexity}"
    description = description.strip()

    cmd = [
        "linear", "issue", "create",
        "-t", title,
        "--team", team_key,
        "--no-interactive",
    ]
    if description:
        cmd.extend(["-d", description])
    if priority is not None:
        cmd.extend(["--priority", str(int(priority))])
    for lbl in labels:
        if lbl:
            cmd.extend(["--label", str(lbl).strip()])
    if project_name:
        cmd.extend(["--project", project_name])

    env = {**os.environ}
    api_key = os.environ.get("LINEAR_API_KEY")
    if api_key:
        env["LINEAR_API_KEY"] = api_key

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
        )
        if result.returncode != 0:
            print(f"linear-cli error: {result.stderr or result.stdout}")
            return None

        # Parse URL from output: https://linear.app/.../issue/TEAM-123/...
        url_match = re.search(r"https://linear\.app/[^\s]+", result.stdout)
        url = url_match.group(0) if url_match else ""
        ident_match = re.search(r"([A-Z]+-\d+)", result.stdout)
        identifier = ident_match.group(1) if ident_match else ""

        return {"identifier": identifier, "title": title, "url": url}
    except Exception as e:
        print(f"linear-cli failed: {e}")
        return None

def load_input_json() -> dict:
    # Prefer stdin if piped, else clipboard
    if not sys.stdin.isatty():
        raw = sys.stdin.read()
    else:
        raw = paste_from_clipboard()

    raw = raw.strip()
    if not raw:
        print("No JSON input found. Pipe JSON into stdin or copy it to clipboard first.")
        sys.exit(1)

    # If user copied a markdown block, try to extract ```json ... ```
    if "```json" in raw:
        start = raw.find("```json") + len("```json")
        end = raw.find("```", start)
        raw = raw[start:end].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON. Make sure your Warp output includes a valid JSON block.")
        print(f"JSON error: {e}")
        sys.exit(1)

def choose_team_id() -> str:
    # 1) env override
    if DEFAULT_TEAM_ID:
        return DEFAULT_TEAM_ID

    q = """
    query Teams {
      teams {
        nodes { id name key }
      }
    }
    """
    resp = gql(q)
    if not gql_ok(resp):
        print_errors(resp)
        sys.exit(1)

    teams = resp["data"]["teams"]["nodes"]
    if not teams:
        print("No teams found in Linear workspace.")
        sys.exit(1)

    # 2) match by env team name
    if DEFAULT_TEAM_NAME:
        for t in teams:
            if t["name"].lower() == DEFAULT_TEAM_NAME.lower():
                return t["id"]

    # 3) if only one team
    if len(teams) == 1:
        return teams[0]["id"]

    # 4) prompt
    print("Select Linear team:")
    for i, t in enumerate(teams, 1):
        key = t.get("key") or ""
        print(f"{i}. {t['name']} {f'({key})' if key else ''}")
    choice = input("Team #: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(teams)):
        print("Invalid selection.")
        sys.exit(1)
    return teams[int(choice) - 1]["id"]

def get_team_labels(team_id: str) -> dict:
    # returns {label_name_lower: label_id}
    # Try team.labels first
    q1 = """
    query TeamLabels($id: String!) {
      team(id: $id) {
        id
        name
        labels {
          nodes { id name }
        }
      }
    }
    """
    resp = gql(q1, {"id": team_id})
    if gql_ok(resp) and resp.get("data", {}).get("team", {}).get("labels"):
        nodes = resp["data"]["team"]["labels"]["nodes"]
        return {n["name"].lower(): n["id"] for n in nodes}

    # Fallback: issueLabels query (if schema differs)
    q2 = """
    query IssueLabels {
      issueLabels(first: 250) { nodes { id name } }
    }
    """
    resp2 = gql(q2)
    if gql_ok(resp2):
        nodes = resp2["data"]["issueLabels"]["nodes"]
        return {n["name"].lower(): n["id"] for n in nodes}

    print("Could not fetch labels.")
    print_errors(resp)
    print_errors(resp2)
    return {}

def create_label(team_id: str, name: str) -> str:
    # Common mutation name in Linear API is issueLabelCreate
    m = """
    mutation LabelCreate($input: IssueLabelCreateInput!) {
      issueLabelCreate(input: $input) {
        success
        issueLabel { id name }
      }
    }
    """
    resp = gql(m, {"input": {"teamId": team_id, "name": name}})
    if gql_ok(resp) and resp["data"]["issueLabelCreate"]["success"]:
        return resp["data"]["issueLabelCreate"]["issueLabel"]["id"]

    print(f'Failed to create label "{name}".')
    print_errors(resp)
    return ""

def create_project(team_id: str, project: dict) -> dict:
    """
    Returns: {id, url, name} or {}
    Tries common variants: teamIds vs teamId.
    """
    name = project.get("name")
    if not name:
        return {}

    description = project.get("description") or ""
    # Priority is not always a project field in Linear; keep it in description if provided.
    prio = project.get("priority")
    if prio is not None:
        description = f"Priority: {prio}\n\n{description}".strip()

    # Variant A: teamIds
    m_teamIds = """
    mutation ProjectCreate($input: ProjectCreateInput!) {
      projectCreate(input: $input) {
        success
        project { id name url }
      }
    }
    """
    resp = gql(m_teamIds, {"input": {"name": name, "description": description, "teamIds": [team_id]}})
    if gql_ok(resp) and resp.get("data", {}).get("projectCreate", {}).get("success"):
        return resp["data"]["projectCreate"]["project"]

    # Variant B: teamId
    resp2 = gql(m_teamIds, {"input": {"name": name, "description": description, "teamId": team_id}})
    if gql_ok(resp2) and resp2.get("data", {}).get("projectCreate", {}).get("success"):
        return resp2["data"]["projectCreate"]["project"]

    print("Failed to create project.")
    print_errors(resp)
    print_errors(resp2)
    return {}

def create_issue(team_id: str, issue: dict, label_map: dict, project_id: str | None) -> dict:
    """
    Returns: {id, identifier, title, url}
    Tries common variants: projectId vs projectIds.
    """
    title = issue.get("title")
    if not title:
        raise ValueError("Issue missing title")

    description = issue.get("description") or ""
    priority = issue.get("priority")  # expecting 1–4
    complexity = issue.get("complexity")  # expecting 1–5
    labels = issue.get("labels") or []
    deps = issue.get("dependencies") or []

    # Resolve label IDs, create missing
    label_ids = []
    for lname in labels:
        key = str(lname).strip().lower()
        if not key:
            continue
        if key in label_map:
            label_ids.append(label_map[key])
        else:
            new_id = create_label(team_id, str(lname).strip())
            if new_id:
                label_map[key] = new_id
                label_ids.append(new_id)

    # Put dependencies + complexity in body for visibility even if schema differs
    extra = []
    if deps:
        extra.append("Dependencies:\n- " + "\n- ".join(deps))
    if complexity is not None:
        extra.append(f"Complexity: {complexity}")
    if extra:
        description = f"{description}\n\n---\n{'\n\n'.join(extra)}".strip()

    # Base input
    input_obj = {
        "teamId": team_id,
        "title": title,
        "description": description,
    }
    if priority is not None:
        input_obj["priority"] = int(priority)

    if label_ids:
        input_obj["labelIds"] = label_ids

    # If estimates are enabled in your workspace, "estimate" often exists.
    # We'll try setting it, but fall back gracefully if it errors.
    if complexity is not None:
        input_obj["estimate"] = int(complexity)

    m = """
    mutation IssueCreate($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        success
        issue { id identifier title url }
      }
    }
    """

    # Try with projectId first
    if project_id:
        input_obj_a = dict(input_obj)
        input_obj_a["projectId"] = project_id
        resp = gql(m, {"input": input_obj_a})
        if gql_ok(resp) and resp["data"]["issueCreate"]["success"]:
            return resp["data"]["issueCreate"]["issue"]

        # Try with projectIds
        input_obj_b = dict(input_obj)
        input_obj_b["projectIds"] = [project_id]
        resp2 = gql(m, {"input": input_obj_b})
        if gql_ok(resp2) and resp2["data"]["issueCreate"]["success"]:
            return resp2["data"]["issueCreate"]["issue"]

        # Try again without estimate (if that was the schema problem)
        input_obj_c = dict(input_obj_b)
        input_obj_c.pop("estimate", None)
        resp3 = gql(m, {"input": input_obj_c})
        if gql_ok(resp3) and resp3["data"]["issueCreate"]["success"]:
            return resp3["data"]["issueCreate"]["issue"]

        print("Failed to create issue (with project).")
        print_errors(resp)
        print_errors(resp2)
        print_errors(resp3)
        return {}

    # No project specified
    resp = gql(m, {"input": input_obj})
    if gql_ok(resp) and resp["data"]["issueCreate"]["success"]:
        return resp["data"]["issueCreate"]["issue"]

    # Retry without estimate if needed
    input_obj.pop("estimate", None)
    resp2 = gql(m, {"input": input_obj})
    if gql_ok(resp2) and resp2["data"]["issueCreate"]["success"]:
        return resp2["data"]["issueCreate"]["issue"]

    print("Failed to create issue.")
    print_errors(resp)
    print_errors(resp2)
    return {}

def main():
    data = load_input_json()

    project = data.get("project") or {}
    issues = data.get("issues") or []

    if not issues:
        print("JSON has no issues[]. Nothing to create.")
        sys.exit(1)

    team_id = choose_team_id()
    label_map = get_team_labels(team_id)

    created_project = {}
    if project.get("name"):
        print("→ Creating project…")
        created_project = create_project(team_id, project)
        if created_project:
            print(f"✅ Project: {created_project.get('name')}")
            print(f"   URL: {created_project.get('url')}")
        else:
            print("⚠️ Project creation failed; continuing to create issues without project.")

    project_id = created_project.get("id") if created_project else None
    project_name = created_project.get("name") if created_project else None

    use_linear_cli = linear_cli_available()
    if use_linear_cli:
        team_key = resolve_team_key(team_id)
        if not team_key:
            print("Could not resolve team key for linear-cli; falling back to GraphQL.")
            use_linear_cli = False

    print("\n→ Creating issues…" + (" (via linear-cli)" if use_linear_cli else ""))
    created_issues = []
    for i, iss in enumerate(issues, 1):
        if use_linear_cli:
            created = create_issue_via_linear_cli(iss, team_key, project_name)
        else:
            created = create_issue(team_id, iss, label_map, project_id)
        if created:
            created_issues.append(created)
            print(f"✅ {i}. {created.get('identifier')} — {created.get('title')}")
            print(f"   {created.get('url')}")
        else:
            print(f"❌ Failed to create issue #{i}: {iss.get('title')}")

    print("\n---")
    print("CREATION SUMMARY")
    if created_project:
        print(f"Project: {created_project.get('url')}")
    for c in created_issues:
        print(f"- {c.get('identifier')}: {c.get('url')}")

if __name__ == "__main__":
    main()
