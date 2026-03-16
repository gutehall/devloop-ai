# Devloop AI
### Claude Code → Linear → GitHub Automation

An AI-driven development loop designed for high velocity and minimal manual overhead.

- **Claude Code** – Planning, orchestration, and implementation (`/plan`, `/next`, `/done`)
- **Linear** – Source of truth (issues & projects)
- **GitHub** – PR & merge flow

---

# Architecture

```
/plan (Claude Code → MCP → Linear issues created)
      ↓
Linear: "Ready for build"
      ↓
/next → linear branch → git checkout → implement
      ↓
/done → git commit + push → gh pr create (Closes ID) → PR URL
      ↓
GitHub merge → Linear auto-Done
```

---

# Daily Loop

```
/plan "Add X feature"    # Create Linear issues via MCP
/next                    # Pick issue, branch, implement
/done                    # Commit, push, PR with Closes ID
```

Repeat.

---

# Setup

## Quick setup (macOS, Linux, Windows)

**macOS / Linux:**
```bash
git clone https://github.com/gutehall/devloop-ai.git
cd devloop-ai
./scripts/setup.sh
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/gutehall/devloop-ai.git
cd devloop-ai
.\scripts\setup.ps1
```

The setup script will:
- Create a virtual environment and install dependencies
- Make CLI scripts executable (macOS/Linux)
- Add aliases and shell quick commands to your shell config
- Prompt for your Linear API key
- Remind you to install GitHub CLI (`gh`) if missing

After setup, reload your shell (`source ~/.zshrc` or `source ~/.bashrc`) or open a new terminal.

---

## Manual setup

```bash
git clone https://github.com/gutehall/devloop-ai.git
cd devloop-ai
pip install -r requirements.txt
```

## Add environment variables

**macOS / Linux:** Add to `~/.zshrc` or `~/.bashrc`:

```bash
export LINEAR_API_KEY="YOUR_LINEAR_API_KEY"
export LINEAR_READY_STATE="Ready for build"
# Optional: LINEAR_MAIN_BRANCH=origin/main  (default: origin/main or git config)
# Optional: LINEAR_IN_PROGRESS_STATE="In Progress"
# Optional: LINEAR_TEAM_ID=ENG or LINEAR_TEAM_NAME="Team Name"
```

**Windows:** Add to PowerShell profile or set in System Environment Variables.

---

## Claude Code setup

Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and configure the Linear MCP server. The `/next`, `/done`, and `/plan` commands are defined in `~/.claude/commands/`.

---

# Claude Code Commands

| Command | Purpose |
|---------|---------|
| `/plan` | Read Linear state, create issues via MCP |
| `/next [ID]` | Pick issue, set In Progress, branch, implement |
| `/done [ID]` | Commit, push, create PR with `Closes ID` |
| `/standup` | Daily summary |

---

# Fallback: Python CLI Tools

The Python scripts are retained for environments without Claude Code. All are deprecated for primary use.

| Tool | Alias | Purpose |
|------|-------|---------|
| ai_go.py | ai-go | Full start: pull, pick issue, branch, open Cursor |
| ai_start.py | ai-start | Pick issue, create branch, open Cursor |
| ai_pr.py | ai-pr | Stage, commit, push, create PR via gh |
| ai_list.py | ai-list | List Linear issues |
| ai_prompt.py | ai-prompt | Copy prompt to clipboard |
| ai_status.py | ai-status | Update Linear issue state |
| ai_done.py | ai-done | Mark current branch's issue as Done |
| ws_create.py | ws-create | Warp/Claude orchestration → Linear (replaced by /plan) |

See [docs/ai-tools-overview.md](docs/ai-tools-overview.md) for full reference.

---

# Design Principles

- Small issues (1–2 days max)
- No overengineering
- AI-first structure
- Minimal manual administration
- Velocity over process weight

---

# Testing

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

# Requirements

- macOS, Linux, or Windows
- Python 3
- Git
- Linear API key
- GitHub repository
- GitHub CLI (`gh`)
- `pyperclip` — `pip install -r requirements.txt`
- **Linux only:** `xclip` or `xsel` (X11) or `wl-clipboard` (Wayland) for clipboard
- **Claude Code:** [linear-cli](https://github.com/schpet/linear-cli) for `/next` branch creation

---

Built for speed. Optimized for shipping.
