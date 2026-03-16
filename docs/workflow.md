# Workflow: Claude Code → Linear → GitHub

This repo uses an AI-driven workflow optimized for fast execution.

## Tools

- **Claude Code:** Planning, orchestration, and implementation (`/plan`, `/next`, `/done`)
- **Linear:** Source of truth (issues, projects, statuses)
- **GitHub:** PRs and merge
- **Local scripts:** See [ai-tools-overview](ai-tools-overview.md) for fallback reference

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

Rule: `/next` only works on issues in **Ready for build**.

---

## Planning (Claude Code → Linear)

Use `/plan` in Claude Code to read Linear state and create issues directly via MCP.

```
/plan "Add user authentication flow"
/plan                                # Open-ended planning session
```

Claude reads existing issues and projects, drafts new ones, creates them in Linear via MCP. No clipboard, no intermediate scripts.

After planning, promote issues to **Ready for build** in Linear (or use `ai-list --state Planned --move-to-ready` as fallback).

---

## Start Work

```
/next           # List unblocked issues, pick one, implement
/next FIN-42    # Jump straight to a specific issue
```

Claude Code will:
1. Set the issue In Progress in Linear
2. Create the git branch
3. Read the issue and explore relevant code
4. Implement — minimal solution, no plan mode gate

See [claude_velocity.md](../prompt/claude_velocity.md) for implementation rules.

---

## Create PR

```
/done           # Commit, push, create PR with "Closes ID", print URL
/done FIN-42    # Specify issue explicitly
```

Claude Code will:
1. Detect issue from branch name
2. Show git log + diff stat
3. Stage and commit any uncommitted changes
4. Push branch
5. Create PR via `gh pr create` with `Closes FIN-42` in body

The `Closes <ID>` triggers Linear's GitHub integration to auto-move the issue to Done on merge.

---

## Status Handling

**Automatic via GitHub–Linear integration:** PR body includes `Closes FIN-XXX` (`/done` adds this):
- PR opened → In Review
- PR merged → Done

**Manual fallback:**

```bash
ai-status LIN-123 "In Progress"
ai-done                      # Mark current issue Done (after merge)
```

---

## Fallback: Python CLI Tools

The Python scripts (`ai-go`, `ai-start`, `ws-create`, `ai-pr`) are retained as fallback but deprecated. Use Claude Code commands by default.

See [ai-tools-overview](ai-tools-overview.md) for reference.
