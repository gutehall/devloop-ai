# ai-pr

Stage, commit, push, then generate PR description from current branch and copy to clipboard.

## Purpose

Runs `git add -A`, `git commit` (with issue key and title as message), and `git push`. Then reads the current git branch, extracts the Linear issue key (e.g. lin-123), fetches the issue title from Linear, generates a PR body with summary, diffstat, testing steps, and linked issue, and copies it to clipboard.

## Usage

```bash
ai-pr                    # Use issue key from branch name (e.g. lin-123-add-feature)
ai-pr --issue FIN-587    # Override: use this issue key instead
```

Either the branch name must contain an issue key, or use `--issue` to specify it.

## Arguments

| Option | Description |
|--------|-------------|
| `--issue <key>` | Override: use this issue key (e.g. FIN-587) instead of extracting from branch |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LINEAR_API_KEY` | (required) | Linear API key |
| `LINEAR_MAIN_BRANCH` | origin/main | Base branch for diff (or from git config) |

## Requirements

- Branch name must contain issue key (e.g. lin-123, PROJ-456)
- Linear API key
- Clipboard access

## Output

PR body includes:

- Summary
- What changed (diffstat)
- Why
- Testing & Validation checklist
- Linked issues (Closes LIN-XXX)
- Known limitations & risks

## Workflow Context

Run after implementing an issue. `ai-pr` stages all changes, commits with `{ISSUE}: {title}`, and pushes. Then either:

- Paste into GitHub when creating a PR manually, or
- Run `ai-create-pr` to create the PR via gh CLI

## See Also

- [ai-create-pr](ai-create-pr.md) — Create PR via GitHub CLI
- [workflow](workflow.md) — Full workflow
