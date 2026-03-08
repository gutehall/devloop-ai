# ai-list

List Linear issues with optional filters.

## Purpose

Quick view of Linear issues in the terminal. Default: issues in "Ready for build". Can filter by state, assignee, and limit.

## Usage

```bash
ai-list                      # Issues in Ready for build (default)
ai-list --state "Planned"    # Filter by state
ai-list --state "Planned" --move-to-ready   # Promote selected Planned issues to Ready for build
ai-list --mine               # Only issues assigned to me
ai-list --limit 10           # Show at most 10 issues
```

When using `--move-to-ready`, enter selection (e.g. `1,3,5` or `1-3`) to move those issues to Ready for build without opening Linear.

## Arguments

| Option | Default | Description |
|--------|---------|-------------|
| `--state` | "Ready for build" | Filter by Linear state name |
| `--move-to-ready` | false | After listing, prompt to move selected issues to Ready for build |
| `--mine` | false | Only issues assigned to current user |
| `--limit` | 25 | Maximum number of issues to show |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LINEAR_API_KEY` | (required) | Linear API key |
| `LINEAR_READY_STATE` | "Ready for build" | Target state for `--move-to-ready` |
| `LINEAR_PLANNED_STATE` | "Planned" | State used when `--move-to-ready` (defaults to Planned) |

## Workflow Context

Use to see what's ready to work on, what's planned, or what you're assigned to—without opening Linear in the browser.

## See Also

- [ai-go](ai-go.md) — Start work on an issue
- [ai-start](ai-start.md) — Pick and start an issue
