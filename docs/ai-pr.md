# ai-pr

Stage, commit, push, create PR — one command.

## Purpose

If on the base branch (e.g. main), creates a feature branch `{ISSUE}-{slugged-title}` first. Then runs `git add -A`, `git commit` (with issue key and title as message), and `git push`. Generates a PR body with summary, diffstat, testing steps, and linked issue, copies it to clipboard, and creates the PR via GitHub CLI (`gh pr create`). On success, moves the Linear issue to **Done** (configurable via `LINEAR_DONE_STATE`).

## Usage

```bash
ai-pr                    # Use issue key from branch; stage, commit, push, create PR
ai-pr --issue FIN-587    # Override; required when on main to create feature branch
ai-pr --skip-commit      # Already committed; only generate PR body and create PR
ai-pr --no-create        # Skip PR creation (only copy description to clipboard)
ai-pr --no-status       # Do not set Linear issue to Done
```

Either the branch name must contain an issue key, or use `--issue` to specify it. When on the base branch (main), you must use `--issue` to create the feature branch. If there is nothing to commit, ai-pr still generates the PR description and creates the PR (or copies to clipboard with `--no-create`).

## Arguments

| Option | Description |
|--------|-------------|
| `--issue <key>` | Override: use this issue key (e.g. FIN-587) instead of extracting from branch |
| `--skip-commit` | Skip stage/commit/push (already committed; only generate PR and create via gh) |
| `--no-create` | Skip creating PR via gh (only copy description to clipboard) |
| `--no-status` | Do not set Linear issue to Done |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LINEAR_API_KEY` | (required) | Linear API key |
| `LINEAR_MAIN_BRANCH` | origin/main | Base branch for diff (or from git config) |
| `LINEAR_DONE_STATE` | Done | Linear state to set when PR is created (use `--no-status` to skip) |

## Requirements

- Branch name must contain issue key (e.g. lin-123, PROJ-456)
- Linear API key
- Clipboard access
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated (for PR creation; use `--no-create` to skip)

## Output

PR body includes:

- Summary
- What changed (diffstat)
- Why
- Testing & Validation checklist
- Linked issues (Closes LIN-XXX)
- Known limitations & risks

## Workflow Context

Run after implementing an issue. One command: stage, commit, push, and create the PR. Description is also copied to clipboard.

## See Also

- [workflow](workflow.md) — Full workflow
