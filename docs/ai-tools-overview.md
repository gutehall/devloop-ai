# AI Tools Overview

Fallback CLI scripts in `ai/`. Primary workflow uses Claude Code (`/plan`, `/next`, `/done`).

## Quick Reference

| Tool | Alias | Status | Purpose |
|------|-------|--------|---------|
| ai_go.py | ai-go | deprecated | Full start: pull, pick issue, branch, open Cursor |
| ai_start.py | ai-start | deprecated | Pick issue, create branch, open Cursor |
| ai_pr.py | ai-pr | active | Stage, commit, push, create PR via gh |
| ai_list.py | ai-list | active | List Linear issues; `--move-to-ready` promotes Planned → Ready |
| ai_prompt.py | ai-prompt | active | Copy prompt to clipboard or list prompts |
| ai_status.py | ai-status | active | Update Linear issue state |
| ai_done.py | ai-done | active | Mark current branch's issue as Done |
| ai_linear_create.py | ai-linear-create | active | Create Linear project/issues from JSON |
| ws_create.py | ws-create | deprecated | Warp orchestration → Linear (replaced by `/plan`) |

## Primary Workflow (Claude Code)

```
/plan → Linear issues created via MCP
     ↓
/next → branch + implement
     ↓
/done → commit + push + PR (Closes ID)
     ↓
GitHub merge → Linear auto-Done
```

## Fallback Workflow (Python CLI)

```
ws-create / ai-linear-create → Linear issues
     ↓
ai-list --state Planned --move-to-ready
     ↓
ai-go or ai-start
     ↓
Implement (Cursor)
     ↓
ai-pr
     ↓
ai-status / ai-done
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
