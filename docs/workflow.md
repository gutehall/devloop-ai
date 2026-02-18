# Workflow: Warp → Linear → Cursor (macOS, Linux, Windows + GitHub)

This repo uses an AI-driven workflow optimized for fast execution.

## Tools

- **Warp:** Planning and orchestration
- **Linear:** Source of truth (issues, projects, statuses)
- **Cursor:** Implementation agent
- **GitHub:** PRs and merge
- **Local scripts:** See [ai-tools-overview](ai-tools-overview.md) for full reference

---

## Issue Lifecycle (Linear)

Backlog:
- Idea
- Triage
- Planned

Unstarted:
- Ready for build (gating state)

Started:
- In Progress
- In Review

Completed:
- Done

Rule: Cursor only works on issues in **Ready for build**.

---

## Planning (Warp → Linear)

1. Use Warp to scan the repo and plan work.
2. Warp creates:
   - A single issue (simple work), OR
   - A project + multiple issues (complex work)
3. Warp should create issues in status **Planned**.
4. Human sanity-check, then move to **Ready for build**.

**Tools:** [ws-create](ws-create.md) for full Warp → Linear flow, or [ai-linear-create](ai-linear-create.md) to create from JSON.

---

## Start Work

**ai-go** (recommended) — Full flow with safety checks:

```bash
ai-go                        # Pull, pick issue, branch, copy prompt, open Cursor
ai-go --set-in-progress      # Also update Linear status
```

**ai-start** — Lighter alternative with prompt selection:

```bash
ai-start                     # Default velocity prompt
ai-start --prompt bugfix     # Use bugfix prompt
```

Both fetch issues in **Ready for build**, let you pick one, create a branch, copy prompt + issue to clipboard, and open Cursor.

See [ai-go](ai-go.md) and [ai-start](ai-start.md) for details.

---

## Implement (Cursor)

1. Paste (Ctrl+V / Cmd+V) into Cursor chat.
2. Implement the issue.
3. Run tests and ensure CI passes.

---

## Create PR

```bash
ai-pr                        # Generate PR description, copy to clipboard
ai-create-pr                 # Create PR via GitHub CLI
ai-pr && ai-create-pr        # One-liner
```

See [ai-pr](ai-pr.md) and [ai-create-pr](ai-create-pr.md).

---

## Status Handling

**Preferred:** GitHub ↔ Linear integration automatically moves:
- PR opened → In Review
- PR merged → Done

**Manual:** [ai-status](ai-status.md) or [ai-done](ai-done.md):

```bash
ai-status LIN-123 "In Progress"
ai-done                      # Mark current issue Done (after merge)
```
