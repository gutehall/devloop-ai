# Cursor Schema Change Mode

Purpose:
Make database/schema changes safely and backward-compatible.

Rules:
- Prefer additive schema changes when possible.
- Always include a migration plan and rollback steps.
- Ensure old and new code can coexist during rollout.
- Include data validation and integrity checks.
- Keep migrations idempotent and tested.

Workflow:
1. Propose migration steps and safety checks.
2. Implement migration and code changes in staged manner.
3. Add tests for migration logic (if applicable).
4. Plan deployment: migrate-readiness, rollout, monitoring.
5. Provide rollback steps and data recovery considerations.
