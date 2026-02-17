# Devloop AI  
### Warp → Linear → Cursor Automation (macOS + GitHub)

An AI-driven development loop designed for high velocity and minimal manual overhead.

This repository provides lightweight CLI scripts and prompt templates to orchestrate:

- **Warp** – Planning & orchestration  
- **Linear** – Source of truth (issues & projects)  
- **Cursor** – AI implementation agent  
- **GitHub** – PR & merge flow  

---

# Architecture

```
Warp (Planning)
      ↓
Linear (Structure)
      ↓
ai-start (CLI)
      ↓
Cursor (Implementation)
      ↓
ai-pr (CLI)
      ↓
GitHub PR
      ↓
Linear auto-updates
```

---

# Repository Structure

```
ai/
  ai_start.py     # Pick issue → create branch → open Cursor
  ai_pr.py        # Generate PR description
  ai_create_pr.py # Create PR via GitHub CLI
  ai_list.py      # List Linear issues
  ai_prompt.py    # Copy prompt to clipboard
  ai_status.py    # Update Linear issue status (optional)
  ai_done.py      # Mark current issue Done

prompt/
  warp_velocity.md
  cursor_velocity.md
  warp_mode_structured.md
  ... (see prompt/README.md)

docs/
  workflow.md
```

---

# Setup

## Create tools folder

```bash
git clone https://github.com/gutehall/devloop-ai.git
cd devloop-ai
```

## Add environment variables

Add to your `~/.zshrc`:

```bash
export LINEAR_API_KEY="YOUR_LINEAR_API_KEY"
export LINEAR_READY_STATE="Ready for build"
# Optional: LINEAR_MAIN_BRANCH=origin/main  (default: origin/main or git config)
```

Add aliases:

```bash
alias ai-start='python3 <path/to/your/repo>/ai/ai_start.py'
alias ai-pr='python3 <path/to/your/repo>/ai/ai_pr.py'
alias ai-create-pr='python3 <path/to/your/repo>/ai/ai_create_pr.py'
alias ai-list='python3 <path/to/your/repo>/ai/ai_list.py'
alias ai-prompt='python3 <path/to/your/repo>/ai/ai_prompt.py'
alias ai-status='python3 <path/to/your/repo>/ai/ai_status.py'
alias ai-done='python3 <path/to/your/repo>/ai/ai_done.py'
```

Reload:

```bash
source ~/.zshrc
```

---

## Make scripts executable

```bash
chmod +x ai/ai_start.py
chmod +x ai/ai_pr.py
chmod +x ai/ai_create_pr.py
chmod +x ai/ai_list.py
chmod +x ai/ai_prompt.py
chmod +x ai/ai_status.py
chmod +x ai/ai_done.py
```

---

# Daily Workflow

## Plan in Warp

Use `prompt/warp_velocity.md` to:
- Analyze the repo
- Decide project vs single issue
- Create Linear issues (status: Planned)

Move ready work to **Ready for build**.

**Quick issue overview:**

```bash
ai-list                      # Issues in Ready for build
ai-list --state "Planned"    # Filter by state
ai-list --mine               # Assigned to me
```

---

## Start Work

```bash
ai-start                     # Default: cursor_velocity prompt
ai-start --prompt bugfix     # Use cursor_bugfix for this issue
ai-start --prompt refactor   # Use cursor_refactor_safe
```

This will:
- Fetch Linear issues in Ready for build
- Let you choose one
- Create a branch: lin-123-short-title
- Copy Cursor prompt + issue to clipboard
- Open Cursor

Then:
- Paste into Cursor (⌘V)
- Implement

---

## Create PR

```bash
ai-pr                        # Generate description, copy to clipboard
ai-create-pr                 # Create PR via GitHub CLI (uses clipboard)
ai-pr && ai-create-pr        # Generate and create in one go
```

`ai-pr` will:
- Read current branch
- Extract issue key
- Fetch issue title
- Generate PR description (richer template)
- Copy to clipboard

`ai-create-pr` creates the PR via `gh` (requires [GitHub CLI](https://cli.github.com/)). If clipboard is empty, it runs `ai-pr` first.

---

## Status Handling

**Preferred:** GitHub ↔ Linear integration automatically moves:
- PR opened → In Review
- PR merged → Done

**Optional manual update:**

```bash
ai-status LIN-123 "In Progress"
ai-status LIN-123 "In Review"
ai-status LIN-123 Done
ai-done                      # Mark current branch's issue Done (after merge)
```

**Copy prompts to clipboard:**

```bash
ai-prompt                    # List available prompts
ai-prompt velocity           # Copy cursor_velocity
ai-prompt bugfix             # Copy cursor_bugfix
ai-prompt warp_velocity      # Copy warp_velocity (for Warp)
```

---

# Design Principles

- Small issues (1–2 days max)
- No overengineering
- AI-first structure
- Minimal manual administration
- Velocity over process weight

---

# Requirements

- macOS
- Python 3
- Git
- Cursor installed
- Linear API key
- GitHub repository
- GitHub CLI (`gh`) — for `ai-create-pr`

---

# Result

Your practical loop:

1. Warp → planning
2. `ai-start` → coding
3. Cursor → implement
4. `ai-pr` → PR
5. Merge

Linear becomes backend infrastructure — not your daily workspace.

---

Built for speed. Optimized for shipping.
