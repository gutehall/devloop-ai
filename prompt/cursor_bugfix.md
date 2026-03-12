# Cursor Bugfix Mode

Purpose:
Safely fix a bug with minimal changes and a regression test.

Rules:
- Reproduce the bug first (failing test or repro steps) before changing any code.
- Focus on root cause, not symptoms.
- Regression test must fail before the fix and pass after; otherwise the test is insufficient.
- Avoid broad refactors or API changes.
- Keep commit small and focused.

Workflow:
1. Reproduce — write a failing test or reproduce steps.
2. Diagnose — find root cause with minimal code inspection.
3. Fix — smallest change that corrects behavior.
4. Test — add regression + run full test suite.
5. Document — short note in PR about root cause and fix.
