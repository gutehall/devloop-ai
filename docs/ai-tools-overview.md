# AI Tools Overview

CLI scripts in `ai/` for the Warp → Linear → Cursor → GitHub workflow.

## Quick Reference

| Tool | Alias | Purpose |
|------|-------|---------|
| ai_go.py | ai-go | Full start: pull, pick issue, branch, open Cursor |
| ai_start.py | ai-start | Pick issue, create branch, open Cursor (with prompt selection) |
| ai_pr.py | ai-pr | Generate PR description, copy to clipboard |
| ai_create_pr.py | ai-create-pr | Create GitHub PR via gh CLI |
| ai_list.py | ai-list | List Linear issues |
| ai_prompt.py | ai-prompt | Copy prompt to clipboard or list prompts |
| ai_status.py | ai-status | Update Linear issue state |
| ai_done.py | ai-done | Mark current branch's issue as Done |
| ai_linear_create.py | ai-linear-create | Create Linear project/issues from JSON |
| ws_create.py | ws-create | Warp orchestration: prompt + task → create in Linear |

## Workflow Steps

```
Plan (Warp) → ai-list / ws-create / ai-linear-create
     ↓
Start work → ai-go or ai-start
     ↓
Implement (Cursor)
     ↓
Create PR → ai-pr → ai-create-pr
     ↓
Status → ai-status / ai-done
```

## Documentation

- [ai-go](ai-go.md) — Full start flow with safety checks
- [ai-start](ai-start.md) — Lighter start with prompt selection
- [ai-pr](ai-pr.md) — Generate PR description
- [ai-create-pr](ai-create-pr.md) — Create PR via GitHub CLI
- [ai-list](ai-list.md) — List Linear issues
- [ai-prompt](ai-prompt.md) — Copy prompts to clipboard
- [ai-status](ai-status.md) — Update Linear issue state
- [ai-done](ai-done.md) — Mark issue Done
- [ai-linear-create](ai-linear-create.md) — Create issues from Warp JSON
- [ws-create](ws-create.md) — Warp orchestration workflow
