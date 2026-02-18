# ai-done

Mark the current branch's Linear issue as Done.

## Purpose

Convenience wrapper around ai-status. Extracts the issue key from the current branch name and sets the issue state to "Done". Use after merging a PR when GitHub ↔ Linear integration doesn't auto-update.

## Usage

```bash
ai-done
```

Must be run from a branch whose name contains an issue key (e.g. `lin-123-add-feature`).

## Arguments

None.

## Requirements

- Branch name must contain issue key (e.g. lin-123)
- Linear API key
- Team must have a "Done" state

## Workflow Context

Run after merging your PR to mark the issue complete in Linear. Equivalent to:

```bash
ai-status LIN-123 Done
```

but without typing the issue key.

## See Also

- [ai-status](ai-status.md) — Update any issue to any state
- [workflow](workflow.md) — Issue lifecycle
