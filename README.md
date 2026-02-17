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

---

# Repository Structure

tools/ai/
  ai_start.py     # Pick issue → create branch → open Cursor
  ai_pr.py        # Generate PR description
  ai_status.py    # Update Linear issue status (optional)

prompts/
  warp_velocity.md
  cursor_velocity.md

docs/
  workflow.md

---

# Setup

## Create tools folder

mkdir -p tools/ai

## Add environment variables

Add to your ~/.zshrc:

export LINEAR_API_KEY="YOUR_LINEAR_API_KEY"
export LINEAR_READY_STATE="Ready for build"

Reload:

source ~/.zshrc

---

## Make scripts executable

chmod +x tools/ai/ai_start.py
chmod +x tools/ai/ai_pr.py
chmod +x tools/ai/ai_status.py

Add aliases:

alias ai-start='python3 tools/ai/ai_start.py'
alias ai-pr='python3 tools/ai/ai_pr.py'
alias ai-status='python3 tools/ai/ai_status.py'

Reload:

source ~/.zshrc

---

# Daily Workflow

## Plan in Warp

Use prompts/warp_velocity.md to:
- Analyze the repo
- Decide project vs single issue
- Create Linear issues (status: Planned)

Move ready work to:
Ready for build

---

## Start Work

ai-start

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

ai-pr

This will:
- Read current branch
- Extract issue key
- Fetch issue title
- Generate PR description
- Copy to clipboard

Then:
- Create PR in GitHub
- Paste description

---

## Status Handling

Preferred:
GitHub ↔ Linear integration automatically moves:
- PR opened → In Review
- PR merged → Done

Optional manual update:

ai-status LIN-123 "In Progress"
ai-status LIN-123 "In Review"
ai-status LIN-123 Done

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

---

# Result

Your practical loop:

1. Warp → planning
2. ai-start → coding
3. Cursor → implement
4. ai-pr → PR
5. Merge

Linear becomes backend infrastructure — not your daily workspace.

---

Built for speed. Optimized for shipping.
