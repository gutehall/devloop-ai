# AI Tools Overview

CLI scripts in `ai/` for the Warp → Linear → Cursor → GitHub workflow.

## Quick Reference

| Tool | Alias | Purpose |
|------|-------|---------|
| ai_go.py | ai-go | Full start: pull, pick issue, branch, open Cursor (optional `--agent`) |
| ai_start.py | ai-start | Pick issue, create branch, open Cursor (optional `--agent`, prompt selection) |
| ai_pr.py | ai-pr | Stage, commit, push, create PR via gh (`--skip-commit` if already committed) |
| ai_list.py | ai-list | List Linear issues; `--move-to-ready` promotes Planned → Ready for build |
| ai_prompt.py | ai-prompt | Copy prompt to clipboard or list prompts |
| ai_status.py | ai-status | Update Linear issue state |
| ai_done.py | ai-done | Mark current branch's issue as Done |
| ai_linear_create.py | ai-linear-create | Create Linear project/issues from JSON |
| ws_create.py | ws-create | Warp orchestration: prompt + task → create in Linear |

## Workflow Steps

```
Plan (Warp) → ai-list / ws-create / ai-linear-create
     ↓
Promote Planned → Ready → ai-list --state Planned --move-to-ready
     ↓
Start work → ai-go or ai-start (optionally --agent for Cursor CLI)
     ↓
Implement (Cursor)
     ↓
Create PR → ai-pr
     ↓
Status → ai-status / ai-done
```

## Documentation

- [ai-go](ai-go.md) — Full start flow with safety checks
- [ai-start](ai-start.md) — Lighter start with prompt selection
- [ai-pr](ai-pr.md) — Stage, commit, push, create PR
- [ai-list](ai-list.md) — List Linear issues
- [ai-prompt](ai-prompt.md) — Copy prompts to clipboard
- [ai-status](ai-status.md) — Update Linear issue state
- [ai-done](ai-done.md) — Mark issue Done
- [ai-linear-create](ai-linear-create.md) — Create issues from Warp JSON
- [ws-create](ws-create.md) — Warp orchestration workflow
