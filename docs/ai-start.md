# ai-start

Pick Linear issue, create branch, copy prompt to clipboard, open Cursor.

## Purpose

Lighter alternative to ai-go. Fetches issues in "Ready for build", lets you pick one, creates a branch, copies prompt + issue to clipboard, and opens Cursor. Supports selecting different Cursor prompt modes (e.g. bugfix, refactor).

## Usage

```bash
ai-start                     # Default: cursor_velocity prompt
ai-start --prompt bugfix     # Use cursor_bugfix for this issue
ai-start --prompt refactor   # Use cursor_refactor_safe
ai-start --prompt velocity   # Explicit velocity (default)
```

## Arguments

| Option | Description |
|--------|-------------|
| `--prompt <name>` | Load prompt from `prompt/cursor_<name>.md` or `prompt/<name>.md` |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LINEAR_API_KEY` | (required) | Linear API key |
| `LINEAR_READY_STATE` | "Ready for build" | State to filter issues |

## Requirements

- Linear API key
- Cursor installed with shell command in PATH
- Clipboard access

## Workflow Context

Use when you want prompt selection (bugfix vs feature vs refactor) without the git pull and clean-worktree checks of ai-go. Good for quick iteration when you're already up to date.

## See Also

- [ai-go](ai-go.md) — Full flow with pull and optional status update
- [ai-prompt](ai-prompt.md) — List and copy prompts manually
