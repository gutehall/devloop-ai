# Devloop AI  
### Warp → Linear → Cursor Automation

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

# Setup

## Create tools folder

```bash
git clone https://github.com/gutehall/devloop-ai.git
cd devloop-ai
pip install -r requirements.txt
```

## Platform setup

**macOS:** No extra setup. Clipboard and Cursor work out of the box.

**Linux:** Install a clipboard tool for copy/paste:
```bash
sudo apt install xclip    # Debian/Ubuntu
# or: sudo apt install xsel
# Wayland: sudo apt install wl-clipboard
```
Install Cursor's shell command: In Cursor, press `Ctrl+Shift+P` → "Shell Command: Install 'cursor' command in PATH".

**Windows:** Install Cursor's shell command: In Cursor, press `Ctrl+Shift+P` → "Shell Command: Install 'cursor' command in PATH". Clipboard works via pyperclip (no extra install).

## Add environment variables

**macOS / Linux:** Add to `~/.zshrc` or `~/.bashrc`:

```bash
export LINEAR_API_KEY="YOUR_LINEAR_API_KEY"
export LINEAR_READY_STATE="Ready for build"
# Optional: LINEAR_MAIN_BRANCH=origin/main  (default: origin/main or git config)
# Optional: LINEAR_IN_PROGRESS_STATE="In Progress"  (for ai-go --set-in-progress)
# Optional: LINEAR_TEAM_ID=ENG or LINEAR_TEAM_NAME="Team Name"  (for ai-linear-create / ws-create)
```

Add aliases:

```bash
alias ai-go='python3 <path/to/your/repo>/ai/ai_go.py'
alias ai-start='python3 <path/to/your/repo>/ai/ai_start.py'
alias ai-pr='python3 <path/to/your/repo>/ai/ai_pr.py'
alias ai-create-pr='python3 <path/to/your/repo>/ai/ai_create_pr.py'
alias ai-list='python3 <path/to/your/repo>/ai/ai_list.py'
alias ai-prompt='python3 <path/to/your/repo>/ai/ai_prompt.py'
alias ai-status='python3 <path/to/your/repo>/ai/ai_status.py'
alias ai-done='python3 <path/to/your/repo>/ai/ai_done.py'
alias ws-create='python3 <path/to/your/repo>/ai/ws_create.py'
```

```bash
# Warp quick commands

wv() { cat <path/to/your/repo>/prompt/warp_velocity.md | pbcopy && echo "✓ warp_velocity copied"; }
wo() { cat <path/to/your/repo>/prompt/warp_orchestrator.md | pbcopy && echo "✓ warp_orchestrator copied"; }
wr() { cat <path/to/your/repo>/prompt/warp_review.md | pbcopy && echo "✓ warp_review copied"; }
wd() { cat <path/to/your/repo>/prompt/warp_debug.md | pbcopy && echo "✓ warp_debug copied"; }
wa() { cat <path/to/your/repo>/prompt/warp_architecture.md | pbcopy && echo "✓ warp_architecture copied"; }
# Add more prompts if needed...
```

**Windows:** Add to PowerShell profile or set in System Environment Variables.

Reload (macOS/Linux):

```bash
source ~/.zshrc   # or source ~/.bashrc
```

---

## Make scripts executable (macOS/Linux)

```bash
chmod +x ai/ai_go.py
chmod +x ai/ai_start.py
chmod +x ai/ai_pr.py
chmod +x ai/ai_create_pr.py
chmod +x ai/ai_list.py
chmod +x ai/ai_prompt.py
chmod +x ai/ai_status.py
chmod +x ai/ai_done.py
chmod +x ai/ws_create.py
```

---

# Daily Workflow

## Plan in Warp

Use `prompt/warp_velocity.md` to:
- Analyze the repo
- Decide project vs single issue
- Create Linear issues (status: Planned)

Move ready work to **Ready for build**.

**`ws-create`** — Automated Warp → Linear flow:

```bash
ws-create "Add user authentication flow"   # Task as argument
ws-create                                 # Prompts for task interactively
ws-create --no-open-warp "Refactor API"   # Skip opening Warp
ws-create --commit-only                   # JSON already in clipboard
```

Flow: copies `warp_orchestrator` + your task to clipboard, opens Warp, you paste and run the prompt. Warp outputs a JSON block; copy it, press Enter, and the script creates the project and issues in Linear via `ai-linear-create`. With `--commit-only`, skips planning and creates from clipboard JSON directly.

**Quick issue overview:**

```bash
ai-list                      # Issues in Ready for build
ai-list --state "Planned"    # Filter by state
ai-list --mine               # Assigned to me
```

---

## Start Work

**`ai-go`** — Full flow with safety checks (recommended):

```bash
ai-go                        # Pull, pick issue, branch, copy prompt, open Cursor
ai-go --no-pull              # Skip git pull --rebase
ai-go --set-in-progress      # Also set Linear status to In Progress
```

**`ai-start`** — Lighter alternative with prompt selection:

```bash
ai-start                     # Default: cursor_velocity prompt
ai-start --prompt bugfix     # Use cursor_bugfix for this issue
ai-start --prompt refactor   # Use cursor_refactor_safe
```

Both will:
- Fetch Linear issues in Ready for build
- Let you choose one
- Create a branch: lin-123-short-title
- Copy Cursor prompt + issue to clipboard
- Open Cursor

Then:
- Paste into Cursor (Ctrl+V on Windows/Linux, Cmd+V on macOS)
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

- macOS, Linux, or Windows
- Python 3
- Git
- Cursor installed (with shell command in PATH)
- Linear API key
- GitHub repository
- GitHub CLI (`gh`) — for `ai-create-pr`
- `pyperclip` — `pip install -r requirements.txt`
- **Linux only:** `xclip` or `xsel` (X11) or `wl-clipboard` (Wayland) for clipboard
- **Optional:** [linear-cli](https://github.com/schpet/linear-cli) — for `ai-linear-create` / `ws-create` (uses `LINEAR_API_KEY` from env)

---

# Result

Your practical loop:

1. Warp → planning
2. `ai-go` or `ai-start` → coding
3. Cursor → implement
4. `ai-pr` → PR
5. Merge

Linear becomes backend infrastructure — not your daily workspace.

---

Built for speed. Optimized for shipping.
