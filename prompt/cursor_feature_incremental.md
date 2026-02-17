# Cursor Feature Incremental Mode

Purpose:
Implement features in thin slices (minimum viable increments).

Rules:
- Deliver the smallest usable increment first (thin-slice).
- Each slice must have acceptance criteria and tests.
- Avoid implementing all polish in first commit.
- Prefer feature flags for experiments or gradual rollout.

Workflow:
1. Define thin-slice acceptance criteria.
2. Implement minimal path end-to-end.
3. Add tests + basic docs (if applicable).
4. Iterate: add enhancements in subsequent issues.
5. Keep PRs small and focused.
