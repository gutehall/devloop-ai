# ws-create

Warp orchestration: generate prompt + task, paste in Warp, then create project/issues in Linear from Warp's JSON output.

## Purpose

End-to-end planning flow: copies the warp_orchestrator prompt plus your task to clipboard, opens Warp, waits for you to run the prompt and copy the JSON output, then creates the project and issues in Linear via ai-linear-create.

## Usage

```bash
# Interactive: prompt for task
ws-create

# With task as arguments
ws-create "Add user authentication flow"

# Skip opening Warp
ws-create "Refactor API" --no-open-warp

# Commit only: JSON already in clipboard (e.g. from previous Warp run)
ws-create --commit-only

# Watch clipboard: auto-create when valid JSON appears (timeout 60s)
ws-create "Add auth flow" --watch

# Custom prompts directory (default: prompt)
ws-create --prompts-dir prompt
```

## Arguments

| Option | Default | Description |
|--------|---------|-------------|
| `task` | (prompted) | Task description for Warp |
| `--prompts-dir` | prompt | Path to prompts directory (must contain warp_orchestrator.md) |
| `--no-open-warp` | false | Do not auto-open Warp after copying prompt |
| `--commit-only` | false | Skip planning; create in Linear from clipboard JSON |
| `--watch` | false | Poll clipboard until valid JSON appears (timeout 60s), then create in Linear |

## Flow

1. **Planning:** Copies `warp_orchestrator.md` + your task + JSON output instructions to clipboard
2. **Warp:** Opens Warp (unless `--no-open-warp`); you paste and run the prompt
3. **Copy:** Copy the ```json ... ``` block from Warp output
4. **Create:** Press Enter; script reads clipboard and runs ai-linear-create

With `--commit-only`, step 1–3 are skipped; clipboard must already contain the JSON.

With `--watch`, step 4 is automatic: the script polls the clipboard every 1.5s; when valid JSON appears, it creates in Linear without pressing Enter. Timeout: 60 seconds.

## Requirements

- `prompt/warp_orchestrator.md` (or path via `--prompts-dir`)
- Linear API key (for ai-linear-create)
- Clipboard access
- Warp (optional; use `--no-open-warp` if using another terminal)

## Workflow Context

Use when planning a new feature or project. Warp produces structured JSON; ws-create turns it into Linear projects and issues in one flow.

## See Also

- [ai-linear-create](ai-linear-create.md) — Creates issues from JSON
- [workflow](workflow.md) — Planning workflow
