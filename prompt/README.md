# Prompt Library

Curated prompts for the Devloop AI workflow: **Warp** (planning & orchestration) and **Cursor** (AI implementation agent).

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
- **Cursor:** Drop prompt content into Cursor chat, or save under `/prompts/cursor/`. Prefer snippets or text expansion for speed.
- **Flow:** Plan in Warp → create Linear issues → use `ai-start` → implement in Cursor with the appropriate prompt.
