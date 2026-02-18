# ai-status

Update a Linear issue's state.

## Purpose

Move an issue to a different Linear state (e.g. "In Progress", "In Review", "Done"). Useful when GitHub ↔ Linear integration is not configured or for manual overrides.

## Usage

```bash
ai-status LIN-123 "In Progress"
ai-status LIN-123 "In Review"
ai-status LIN-123 Done
ai-status PROJ-456 "Ready for build"
```

## Arguments

| Argument | Description |
|----------|-------------|
| `<identifier>` | Linear issue key (e.g. LIN-123, PROJ-456) |
| `<state>` | Target state name (one or more words in quotes) |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `LINEAR_API_KEY` | (required) Linear API key |

## Requirements

- Linear API key
- State name must match exactly (case-insensitive) a state in the issue's team

If the state is not found, the script lists available states for the team.

## Workflow Context

- **Manual override:** When GitHub integration doesn't auto-update Linear
- **Before ai-go/ai-start:** Move issue to "Ready for build" if needed
- **During work:** Move to "In Progress" or "In Review"
- **After merge:** Move to "Done" (or use `ai-done` for current branch)

## See Also

- [ai-done](ai-done.md) — Mark current branch's issue as Done
- [workflow](workflow.md) — Issue lifecycle
