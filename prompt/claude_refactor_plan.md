# Refactor plan (with safety rails)

## Target
Refactor: <target_area>

## Goals
- Improve: <readability|structure|performance|testability|security>
- Preserve behavior (unless listed)
- Reduce risk with incremental commits

## Constraints
- Deadlines: <deadline>
- Compatibility: <compat_constraints>
- Tooling: <tooling>

## Scope
<files>

## Task
1. Map current behavior & implicit contracts (APIs, side effects).
2. Propose a staged refactor plan (3–8 commits).
3. For each stage:
   - code changes
   - tests to add/update
   - validation steps
4. Identify rollback strategy.

## Output
- Staged plan + rationale
- Key risks and how you mitigate them
