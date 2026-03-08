# ai-go

Full start flow: pull latest, pick Linear issue, create branch, copy prompt to clipboard, open Cursor.

## Purpose

One command to begin work on an issue. Ensures clean worktree, pulls latest changes, fetches issues in "Ready for build", lets you pick one, creates a branch, copies the velocity prompt + issue to clipboard, and opens Cursor.

## Usage

```bash
ai-go                        # Full flow (sets Linear status to In Progress by default)
ai-go --no-pull              # Skip git pull --rebase
ai-go --agent                # Run Cursor agent CLI instead of opening editor (skips paste)
ai-go --no-status            # Do not set Linear status to In Progress
```

## Arguments

| Option | Description |
|--------|-------------|
| `--no-pull` | Do not run `git pull --rebase` before picking an issue |
| `--agent` | Run Cursor agent CLI with the prompt instead of opening editor (requires `agent` in PATH) |
| `--no-status` | Do not update the selected issue's Linear status to In Progress |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LINEAR_API_KEY` | (required) | Linear API key |
| `LINEAR_READY_STATE` | "Ready for build" | State to filter issues |
| `LINEAR_IN_PROGRESS_STATE` | "In Progress" | State for `--set-in-progress` |

## Requirements

- Clean git worktree (commit or stash changes first)
- Linear API key
- Cursor installed with shell command in PATH
- Clipboard access (pyperclip or platform fallback)

## Workflow Context

Use at the start of your coding session. After running:

1. Paste (Ctrl+V / Cmd+V) into Cursor chat
2. Implement the issue
3. Use `ai-pr` when done

## See Also

- [ai-start](ai-start.md) — Lighter alternative with `--prompt` selection
- [workflow](workflow.md) — Full workflow overview
