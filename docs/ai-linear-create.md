# ai-linear-create

Create Linear project and issues from JSON (typically Warp output).

## Purpose

Parses JSON describing a project and issues, then creates them in Linear via the API. Input can be piped from stdin or read from clipboard. Extracts JSON from markdown code blocks (```json ... ```) if present.

## Usage

```bash
# From clipboard (copy Warp JSON output first)
ai-linear-create

# From stdin
echo '{"issues":[{"title":"Add X","description":"..."}]}' | ai-linear-create

# From file
cat plan.json | ai-linear-create
```

## Input Format

```json
{
  "project": {
    "name": "Project name",
    "description": "Optional description",
    "priority": 1
  },
  "issues": [
    {
      "title": "Issue title",
      "description": "Issue description",
      "priority": 1,
      "labels": ["type:feature", "risk:low"],
      "complexity": 3,
      "dependencies": []
    }
  ]
}
```

- `project` — Optional. If present, creates a project and attaches issues to it.
- `issues` — Required. Array of issue objects.
- `priority` — 1–4 (1 = Urgent, 4 = Low)
- `complexity` — 1–5 (optional)
- `labels` — Creates labels if they don't exist
- `dependencies` — Added to description (Linear dependency linking may vary)

## Environment Variables

| Variable | Description |
|----------|-------------|
| `LINEAR_API_KEY` | (required) Linear API key |
| `LINEAR_TEAM_ID` | Skip team selection; use this team |
| `LINEAR_TEAM_NAME` | Skip team selection; use team matching this name |

## Requirements

- Linear API key (from env, e.g. in `.zshrc`)
- JSON input with at least `issues` array

## linear-cli Integration

When [linear-cli](https://github.com/schpet/linear-cli) (schpet/linear-cli) is installed, the script uses it for issue creation. linear-cli reads `LINEAR_API_KEY` from the environment, so ensure it is set (e.g. in `.zshrc`).

**Install linear-cli (optional):**
```bash
brew install schpet/tap/linear
# or: deno install -A -f -g -n linear jsr:@schpet/linear-cli
```

- **With linear-cli:** Issues are created via `linear issue create`; projects still use GraphQL (linear-cli has no project create).
- **Without linear-cli:** Falls back to direct GraphQL for both projects and issues.

## Workflow Context

Used by [ws-create](ws-create.md) after Warp produces a plan. Can also be used standalone: copy Warp's JSON output to clipboard, then run `ai-linear-create`.

## See Also

- [ws-create](ws-create.md) — Full Warp → Linear flow
- [workflow](workflow.md) — Planning workflow
