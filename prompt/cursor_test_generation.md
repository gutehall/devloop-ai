# Cursor Test Generation Mode

Purpose:
Generate high-value tests to improve reliability.

Rules:
- Focus on critical paths, boundary conditions, and failure modes.
- Prefer meaningful integration tests for behavior across components.
- Avoid trivial tests that assert implementation details or low-value coverage.
- Keep tests deterministic and fast where possible.

Workflow:
1. Analyze code paths affected by the change.
2. Identify high-leverage scenarios to test (happy path, boundary, failure modes).
3. Write tests (unit/integration) that are clear and maintainable.
4. Run tests locally and ensure stability in CI.
5. Document test purpose in PR.
