# ai-create-pr

Create GitHub PR with clipboard content via GitHub CLI.

## Purpose

Creates a PR using `gh pr create` with the body from clipboard. If clipboard is empty, runs `ai-pr` first to generate the description, then creates the PR.

## Usage

```bash
ai-create-pr                 # Create PR with clipboard content
ai-pr && ai-create-pr        # Generate description, then create (one-liner)
```

## Arguments

None.

## Requirements

- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- Clipboard with PR body, or run after `ai-pr` (script will invoke ai-pr if clipboard empty)
- Branch with issue key in name (for ai-pr fallback)

## Workflow Context

Run after `ai-pr` to complete the PR creation in the terminal without opening the browser. If you've already run `ai-pr`, `ai-create-pr` alone will use the clipboard content.

## See Also

- [ai-pr](ai-pr.md) — Generate PR description
- [workflow](workflow.md) — Full workflow
