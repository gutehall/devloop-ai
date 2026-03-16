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

## Claude Code Prompts (Implementation)

Used by `/next` in Claude Code. The velocity prompt is the default implementation behavioral ruleset.

| Prompt | Purpose |
|--------|---------|
| `claude_velocity.md` | Default implementation mode for Claude Code. Minimal working solution, focused changes, follow existing patterns, add tests, check AC. Used by `/next`. |
| `claude_orchestrator.md` | Linear planning (project + issues). Fallback for `ws-create --claude`. |
| `claude_session_bootstrap.md` | Paste first in a new session. Sets working rules, repo context, task scope, and constraints. |

---

## Cursor Prompts (Implementation — Fallback)

Used by `ai-go` / `ai-start` when running the deprecated Python CLI tools. `ai-start` loads from `cursor_<name>.md` via `--prompt`.

| Prompt | Purpose |
|--------|---------|
| `cursor_velocity.md` | Default implementation mode for Cursor. Used by `ai-go` and `ai-start` default. |
| `cursor_bugfix.md` | Fix bugs safely. Reproduce first, target root cause, regression test. |
| `cursor_refactor_safe.md` | Refactor without changing behavior. Incremental, reversible steps. |
| `cursor_pr_finalize.md` | Polish PR description and commit message. |
| `cursor_code_review.md` | Self-review before PR. |
| `cursor_test_generation.md` | Generate high-value tests. |
| `cursor_schema_change.md` | Database/schema changes with migration plan. |
| `cursor_security_hardening.md` | Patch security issues. |
| `cursor_performance_optimize.md` | Fix performance bottlenecks. |

---

## Usage

- **Claude Code:** `/next` uses `claude_velocity.md` rules inline — no clipboard needed. `/plan` creates Linear issues directly via MCP.
- **Warp (fallback):** Paste `warp_orchestrator.md` into Warp chat. Use `ws-create` to create Linear issues from JSON output.
- **Cursor (fallback):** `ai-go` uses `cursor_velocity.md` + Linear issue. `ai-start --prompt bugfix` for other modes.

---

## CLI Integration (Fallback)

| Script | Prompts used |
|--------|--------------|
| `ws-create` | `warp_orchestrator` (default) or `claude_orchestrator` (with `--claude`). |
| `ai-go` | Loads `cursor_velocity.md` + Linear issue. |
| `ai-start` | Loads from `cursor_<name>.md` via `--prompt`. Default: cursor_velocity. |
| `ai-prompt` | Copies any prompt to clipboard for manual use. |

**Shell shortcuts** (from setup script): `wv` warp_velocity, `wo` warp_orchestrator, `wr` warp_review, `wd` warp_debug, `wa` warp_architecture, `co` claude_orchestrator, `cs` claude_session_bootstrap.
