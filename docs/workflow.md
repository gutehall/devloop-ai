# Workflow: Warp → Linear → Cursor (macOS + GitHub)

This repo uses an AI-driven workflow optimized for fast execution.

## Tools
- Warp: planning + orchestration
- Linear: source of truth (issues/projects + statuses)
- Cursor: implementation agent
- GitHub: PRs + merge
- Local scripts:
  - ai-start: pick issue → create branch → open Cursor → copy prompt+issue
  - ai-pr: generate PR description → copy to clipboard
  - ai-status (optional): move issue between Linear states

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

1. Use Warp to scan the repo + plan work.
2. Warp creates:
   - A single issue (simple work), OR
   - A project + multiple issues (complex work)
3. Warp should create issues in status **Planned**.
4. Human sanity-check, then move to **Ready for build**.

---

## Start Work (ai-start)

Command:
```bash
ai-start
