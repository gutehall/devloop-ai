# Prompt Library

Curated prompts for the Devloop AI workflow: **Warp** or **Claude** (planning & orchestration) and **Cursor** (AI implementation agent).

---

## Claude Prompts (Planning & Execution)

Use these in Claude (desktop, API, or Cursor) when Warp is not available. Claude can plan, orchestrate, and create Linear issues using the same flow as Warp.

| Prompt | Purpose |
|--------|---------|
| `claude_session_bootstrap.md` | Paste first in a new session. Sets working rules, repo context, and task scope. |
| `claude_orchestrator.md` | Linear planning (project + issues). Outputs JSON for `ai-linear-create` / `ws-create`. Use instead of `warp_orchestrator` when Warp is not installed. |
| `claude_linear_epic_breakdown.md` | Create an Epic and breakdown into milestones and stories with acceptance criteria, sizing, labels. |
| `claude_linear_sprint_planning.md` | Sprint plan from backlog. Propose goal, select issues by capacity, dependencies, risks. |
| `claude_lightweight_prd.md` | Lightweight PRD for features. Problem, goals, non-goals, requirements, rollout. |
| `claude_add_feature.md` | Add a feature end-to-end. Implementation plan, integration points, tests, docs. |
| `claude_refactor_plan.md` | Refactor plan with safety rails. Staged plan, validation, rollback. |
| `claude_refactor_execute_stage1.md` | Execute first stage of a refactor. Plan boundaries, implement stage 1, summarize next. |
| `claude_fix_bug.md` | Fix a bug. Root cause, regression test, minimal patch. |
| `claude_debug_triage.md` | Fast debug triage. Hypotheses ranked, verification steps, fix path. |
| `claude_debug_deep_dive.md` | Deep debug with instrumentation. Repro harness, root cause, patch. |
| `claude_code_review.md` | Code review for PR or branch. Verdict, major/minor issues, follow-ups. |
| `claude_cli_command.md` | Create or improve a CLI command. Implementation, tests, help text. |
| `claude_threat_model.md` | Lightweight STRIDE-style threat model. Threats, risk ratings, mitigations. |
| `claude_security_scan.md` | Pragmatic security scan. Auth, validation, injection, secrets, dependencies. |
| `claude_security_hardening_refactor.md` | Harden an area without changing behavior. Risks, refactor steps, tests. |
| `claude_test_strategy.md` | Test strategy for a module. Unit, integration, property, negative tests, placement. |

---

## Warp Prompts (Planning)

Use these in Warp to analyze, plan, and create Linear issues before handing off to Cursor.

| Prompt | Purpose |
|--------|---------|
| `warp_velocity.md` | Fast planning mode. Decides project vs single issue, creates Linear-ready issues optimized for 1–2 day execution. |
| `warp_mode_structured.md` | Full structured planning. Scans repo, produces implementation plans, creates projects/issues with metadata (priority, labels, complexity, dependencies). |
| `warp_orchestrator.md` | High-level orchestration. Creates Linear projects or issues with title, description, priority, labels, complexity, dependencies. |
| `warp_architecture.md` | Design or evaluate significant system changes. Compares 2–3 approaches, explains trade-offs, recommends simplest viable option. |
| `warp_debug.md` | Diagnose bugs and propose minimal fixes. Focuses on root cause, evidence, smallest change, regression test. |
| `warp_release.md` | Prepare a release. Generates changelog, migration steps, semver bump, rollback plan, deployment checklist. |
| `warp_security_audit.md` | Audit code for security risks. Analyzes validation, auth, data exposure, injection, dependencies. Outputs ranked findings and fixes. |
| `warp_review.md` | Review implementation plans before execution. Surfaces hidden complexity, missing edge cases, risks, scope creep. |
| `warp_refactor.md` | Plan safe refactors. No functional changes, incremental steps, tests must pass. Outputs target area, plan, validation strategy. |
| `warp_performance.md` | Analyze performance risks. Checks loops, N+1 queries, data structures, blocking ops, memory. Outputs bottlenecks and optimizations. |
| `warp_test_strategy.md` | Improve test coverage. Analyzes existing tests, missing edge cases, critical paths. Suggests high-leverage and regression tests. |

---

## Cursor Prompts (Implementation)

Use these in Cursor to guide the AI agent during implementation.

| Prompt | Purpose |
|--------|---------|
| `cursor_velocity.md` | Default implementation mode. Minimal working solution, small focused changes (1–2 days), follow existing patterns, add tests, ensure CI passes. |
| `cursor_bugfix.md` | Fix bugs safely. Reproduce first, target root cause, add regression test, keep changes minimal. |
| `cursor_refactor_safe.md` | Refactor without changing behavior. Incremental, reversible changes, full test suite passes after each step. |
| `cursor_feature_incremental.md` | Implement features in thin slices. Smallest usable increment first, feature flags for rollout, iterate in subsequent issues. |
| `cursor_schema_change.md` | Database/schema changes. Additive changes, migration plan, rollback steps, backward compatibility. |
| `cursor_security_hardening.md` | Patch security issues. Prioritize by severity, minimal changes, document residual risks. |
| `cursor_test_generation.md` | Generate high-value tests. Focus on critical paths, edge cases, meaningful integration tests. |
| `cursor_performance_optimize.md` | Fix performance bottlenecks. Measure first, targeted changes, validate improvements, include metrics in PR. |
| `cursor_code_review.md` | Self-review before PR. Checks acceptance criteria, edge cases, test quality, naming, performance/security. |
| `cursor_pr_finalize.md` | Polish PR description and commit message. Summary, what changed, why, testing steps, linked issues, limitations. |
| `cursor_explain_change.md` | Explain changes in plain English for reviewers. What changed, why, what to check, assumptions, manual test steps. |

---

## Usage

- **Warp:** Paste prompt content into Warp chat when planning. Use `warp_velocity.md` or `warp_mode_structured.md` for the main planning loop.
- **Claude:** Paste prompt content into Claude (desktop, API, or Cursor). Use `claude_orchestrator.md` with `ws-create --claude` to plan and create Linear issues when Warp is not installed.
- **Cursor:** Drop prompt content into Cursor chat, or save under `/prompts/cursor/`. Prefer snippets or text expansion for speed.
- **Flow:** Plan in Warp or Claude → create Linear issues (via `ws-create`) → use `ai-go` or `ai-start` → implement in Cursor with the appropriate prompt.

---

## CLI Integration

| Script | Prompts used |
|--------|--------------|
| `ws-create` | Uses `warp_orchestrator` (default) or `claude_orchestrator` (with `--claude`). Opens Warp or Claude accordingly. |
| `ai-go` | Uses built-in velocity prompt + Linear issue (URL, title, description). No prompt selection. |
| `ai-start` | Loads from `cursor_<name>.md` via `--prompt` (e.g. `ai-start --prompt bugfix`). Default: velocity. |
| `ai-prompt` | Copies any prompt to clipboard for manual use in Warp, Claude, or Cursor. |

**`ws-create --claude`** — Use when Warp is not installed. Copies `claude_orchestrator` + task to clipboard and opens Claude (or prints instructions). Output JSON → `ai-linear-create`.

**`ai-go`** is the full-flow option: ensures clean worktree, runs `git pull --rebase`, picks issue, creates branch, copies prompt+issue (with Linear URL), opens Cursor. Optional `--no-status` skips Linear status update.
