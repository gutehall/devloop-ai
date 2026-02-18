# ai-list

List Linear issues with optional filters.

## Purpose

Quick view of Linear issues in the terminal. Default: issues in "Ready for build". Can filter by state, assignee, and limit.

## Usage

```bash
ai-list                      # Issues in Ready for build (default)
ai-list --state "Planned"    # Filter by state
ai-list --state "In Progress"
ai-list --mine               # Only issues assigned to me
ai-list --limit 10           # Show at most 10 issues
ai-list --state "Planned" --mine --limit 5
```

## Arguments

| Option | Default | Description |
|--------|---------|-------------|
| `--state` | "Ready for build" | Filter by Linear state name |
| `--mine` | false | Only issues assigned to current user |
| `--limit` | 25 | Maximum number of issues to show |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LINEAR_API_KEY` | (required) | Linear API key |
| `LINEAR_READY_STATE` | "Ready for build" | Default state when `--state` not given |

## Workflow Context

Use to see what's ready to work on, what's planned, or what you're assigned to—without opening Linear in the browser.

## See Also

- [ai-go](ai-go.md) — Start work on an issue
- [ai-start](ai-start.md) — Pick and start an issue
