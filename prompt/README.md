# Prompt Library

Curated prompts for the Devloop AI workflow: **Warp** or **Claude** (planning & orchestration) and **Cursor** (AI implementation agent).

---

## Warp Prompts (Planning)

Use these in Warp to analyze, plan, and create Linear issues before handing off to Cursor.

| Prompt | Purpose |
|--------|---------|
| `warp_velocity.md` | Fast planning mode. Decides project vs single issue, creates Linear-ready issues optimized for 1–2 day execution. Use with `ws-create` flow. |
| `warp_orchestrator.md` | Full orchestration for Linear. Project vs single-issue decision logic, metadata (priority, labels, complexity, dependencies). Used by `ws-create` (default). |
| `warp_review.md` | Review implementation plans before execution. Surfaces hidden complexity, missing edge cases, risks, scope creep. |
| `warp_debug.md` | Diagnose bugs and propose minimal fixes. Hypotheses, verification, minimal change, regression test. |
| `warp_architecture.md` | Design or evaluate significant system changes. Compares 2–3 approaches, trade-offs, simplest viable option. |

---

## Claude Prompts (Planning)

Use these in Claude when Warp is not available. Claude can plan and create Linear issues using the same flow as Warp.

| Prompt | Purpose |
|--------|---------|
| `claude_orchestrator.md` | Linear planning (project + issues). Outputs JSON for `ai-linear-create` / `ws-create`. Use with `ws-create --claude`. |
| `claude_session_bootstrap.md` | Paste first in a new session. Sets working rules, repo context, task scope, and constraints. |

---

## Cursor Prompts (Implementation)

Use these in Cursor to guide the AI agent during implementation. `ai-start` loads from `cursor_<name>.md` via `--prompt`. Default is `cursor_velocity.md`.

| Prompt | Purpose |
|--------|---------|
| `cursor_velocity.md` | Default implementation mode. Minimal working solution, small focused changes (1–2 days), follow existing patterns, add tests, ensure CI passes. Single source for `ai-go` and `ai-start` default. |
| `cursor_bugfix.md` | Fix bugs safely. Reproduce first, target root cause, regression test (fails before fix, passes after), minimal changes. |
| `cursor_refactor_safe.md` | Refactor without changing behavior. Incremental, reversible steps, one logical change per commit, rollback plan. |
| `cursor_pr_finalize.md` | Polish PR description and commit message. Summary, what changed, why, what to check, assumptions, manual test steps. |
| `cursor_code_review.md` | Self-review before PR. Acceptance criteria, edge cases, test quality, naming, performance/security. |
| `cursor_test_generation.md` | Generate high-value tests. Critical paths, edge cases, avoid trivial tests. |
| `cursor_schema_change.md` | Database/schema changes. Additive changes, migration plan, rollback steps, backward compatibility. |
| `cursor_security_hardening.md` | Patch security issues. Prioritize by severity, minimal changes, document residual risks. |
| `cursor_performance_optimize.md` | Fix performance bottlenecks. Measure first, targeted changes, validate improvements. |

---

## Usage

- **Warp:** Paste prompt content into Warp chat when planning. Use `warp_velocity.md` or `warp_orchestrator.md` for the main planning loop. `ws-create` copies the orchestrator + task and appends JSON output instructions.
- **Claude:** Paste prompt content into Claude (desktop, API, or Cursor). Use `claude_orchestrator.md` with `ws-create --claude` to plan and create Linear issues when Warp is not installed.
- **Cursor:** `ai-go` uses `cursor_velocity.md` (loaded from file) + Linear issue. `ai-start` uses the same by default, or `--prompt bugfix` / `--prompt refactor` for other modes.

---

## CLI Integration

| Script | Prompts used |
|--------|--------------|
| `ws-create` | `warp_orchestrator` (default) or `claude_orchestrator` (with `--claude`). Appends JSON schema at runtime. |
| `ai-go` | Loads `cursor_velocity.md` + Linear issue (URL, title, description). No prompt selection. |
| `ai-start` | Loads from `cursor_<name>.md` via `--prompt` (e.g. `ai-start --prompt bugfix`). Default: cursor_velocity. |
| `ai-prompt` | Copies any prompt to clipboard for manual use in Warp, Claude, or Cursor. |

**Shell shortcuts** (from setup script): `wv` warp_velocity, `wo` warp_orchestrator, `wr` warp_review, `wd` warp_debug, `wa` warp_architecture, `co` claude_orchestrator, `cs` claude_session_bootstrap.
