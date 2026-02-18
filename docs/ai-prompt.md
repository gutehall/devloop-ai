# ai-prompt

Copy a prompt to clipboard or list available prompts.

## Purpose

Lists all prompts in `prompt/` or copies a specific prompt to clipboard. Supports fuzzy matching (e.g. `velocity` matches `cursor_velocity`).

## Usage

```bash
ai-prompt                    # List all available prompts
ai-prompt velocity           # Copy cursor_velocity.md
ai-prompt bugfix             # Copy cursor_bugfix.md
ai-prompt warp_velocity      # Copy warp_velocity.md (for Warp)
ai-prompt warp               # Fuzzy match: first warp_* prompt
```

## Arguments

| Argument | Description |
|----------|-------------|
| (none) | List all prompts |
| `<name>` | Copy prompt matching name (exact, prefix, or substring) |

## Requirements

- Clipboard access
- `prompt/` directory with .md files

## Workflow Context

- **Cursor:** Copy a Cursor prompt (e.g. bugfix, refactor) before or during implementation
- **Warp:** Copy a Warp prompt (e.g. warp_velocity, warp_orchestrator) for planning

## See Also

- [ai-start](ai-start.md) — Uses prompts via `--prompt` flag
- [prompt/README.md](../prompt/README.md) — Prompt library reference
