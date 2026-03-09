# Security hardening refactor

## Goal
Harden <area> without changing externally visible behavior (unless noted).

## Requirements
1. Identify risky patterns (inputs, auth, secrets, crypto, dependencies).
2. Propose minimal refactors to reduce attack surface.
3. Add tests for security-relevant behavior.
4. Document config changes and rollout steps.

## Scope
<files>

## Output
- Risks found + evidence
- Proposed refactor steps
- Patch outline + tests
- Rollout/rollback considerations
