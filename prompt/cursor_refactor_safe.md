# Cursor Safe Refactor Mode

Purpose:
Refactor code for readability/structure without changing behavior.

Rules:
- No behavioral changes allowed.
- Keep changes incremental and reversible.
- Ensure full test suite passes after each logical change.
- Avoid introducing new abstractions unless clearly necessary.
- Provide clear commit messages that describe intent and scope.

Workflow:
1. Identify small refactor target (single responsibility, extract function).
2. Add/ensure tests covering current behavior.
3. Make incremental changes with tests passing after each step.
4. Run full test suite and linters.
5. Summarize changes in PR and include validation steps.
