# ws-create

Planning orchestration: generate prompt + task, paste in Warp or Claude, then create project/issues in Linear from JSON output.

## Purpose

End-to-end planning flow: copies the orchestrator prompt plus your task to clipboard, opens Warp or Claude, waits for you to run the prompt and copy the JSON output, then creates the project and issues in Linear via ai-linear-create. Use `--claude` when Warp is not installed.

## Usage

```bash
# Interactive: prompt for task (default: Warp)
ws-create

# Use Claude instead of Warp (when Warp not installed)
ws-create "Add user authentication flow" --claude

# With task as arguments
ws-create "Add user authentication flow"

# Skip opening the planning app
ws-create "Refactor API" --no-open-warp
ws-create "Refactor API" --claude --no-open-claude

# Commit only: JSON already in clipboard (e.g. from previous Warp/Claude run)
ws-create --commit-only

# Watch clipboard: auto-create when valid JSON appears (timeout 60s)
ws-create "Add auth flow" --watch

# Custom prompts directory (default: prompt)
ws-create --prompts-dir prompt
```

## Arguments

| Option | Default | Description |
|--------|---------|-------------|
| `task` | (prompted) | Task description |
| `--claude` | false | Use Claude instead of Warp (uses claude_orchestrator.md) |
| `--prompts-dir` | prompt | Path to prompts directory (must contain warp_orchestrator.md or claude_orchestrator.md) |
| `--no-open-warp` | false | Do not auto-open Warp after copying prompt |
| `--no-open-claude` | false | Do not auto-open Claude (only with `--claude`) |
| `--commit-only` | false | Skip planning; create in Linear from clipboard JSON |
| `--watch` | false | Poll clipboard until valid JSON appears (timeout 60s), then create in Linear |

## Flow

1. **Planning:** Copies `warp_orchestrator.md` (or `claude_orchestrator.md` with `--claude`) + your task + JSON output instructions to clipboard
2. **App:** Opens Warp or Claude (unless `--no-open-warp` / `--no-open-claude`); you paste and run the prompt
3. **Copy:** Copy the ```json ... ``` block from output
4. **Create:** Press Enter; script reads clipboard and runs ai-linear-create

With `--commit-only`, step 1–3 are skipped; clipboard must already contain the JSON.

With `--watch`, step 4 is automatic: the script polls the clipboard every 1.5s; when valid JSON appears, it creates in Linear without pressing Enter. Timeout: 60 seconds.

## Requirements

- `prompt/warp_orchestrator.md` (default) or `prompt/claude_orchestrator.md` (with `--claude`)
- Linear API key (for ai-linear-create)
- Clipboard access
- Warp or Claude (use `--claude` when Warp is not installed; use `--no-open-warp` / `--no-open-claude` if pasting manually)

## Workflow Context

Use when planning a new feature or project. Warp or Claude produces structured JSON; ws-create turns it into Linear projects and issues in one flow.

## See Also

- [ai-linear-create](ai-linear-create.md) — Creates issues from JSON
- [workflow](workflow.md) — Planning workflow
