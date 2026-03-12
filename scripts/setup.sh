#!/usr/bin/env bash
# Devloop AI — Setup script for macOS and Linux
# Run from repo root: ./scripts/setup.sh
# Or from anywhere: bash /path/to/devloop-ai/scripts/setup.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
AI_DIR="$REPO_ROOT/ai"
PROMPT_DIR="$REPO_ROOT/prompt"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Devloop AI — Setup"
echo "=================="
echo "Repo: $REPO_ROOT"
echo ""

# Detect OS
if [[ "$(uname)" == "Darwin" ]]; then
  PLATFORM="macos"
  COPY_CMD="pbcopy"
elif [[ "$(uname)" == "Linux" ]]; then
  PLATFORM="linux"
  # Detect clipboard tool
  if command -v xclip &>/dev/null; then
    COPY_CMD="xclip -selection clipboard"
  elif command -v xsel &>/dev/null; then
    COPY_CMD="xsel --clipboard --input"
  elif command -v wl-copy &>/dev/null; then
    COPY_CMD="wl-copy"
  else
    echo -e "${YELLOW}No clipboard tool found. Install one:${NC}"
    echo "  Debian/Ubuntu: sudo apt install xclip"
    echo "  Or: sudo apt install xsel"
    echo "  Wayland: sudo apt install wl-clipboard"
    echo ""
    COPY_CMD=""
  fi
else
  echo -e "${RED}Unsupported OS. Use scripts/setup.ps1 on Windows.${NC}"
  exit 1
fi

# Check Python
if ! command -v python3 &>/dev/null; then
  echo -e "${RED}Python 3 is required. Install it first.${NC}"
  exit 1
fi

# Create venv (optional but recommended)
if [[ ! -d "$REPO_ROOT/.venv" ]]; then
  echo "Creating virtual environment..."
  python3 -m venv "$REPO_ROOT/.venv"
  echo -e "${GREEN}✓ Venv created${NC}"
fi

# Activate and install deps
echo "Installing dependencies..."
source "$REPO_ROOT/.venv/bin/activate"
pip install -q -r "$REPO_ROOT/requirements.txt"
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Make scripts executable
chmod +x "$AI_DIR"/ai_go.py "$AI_DIR"/ai_start.py "$AI_DIR"/ai_pr.py \
         "$AI_DIR"/ai_list.py "$AI_DIR"/ai_prompt.py "$AI_DIR"/ai_status.py \
         "$AI_DIR"/ai_done.py "$AI_DIR"/ws_create.py 2>/dev/null || true
echo -e "${GREEN}✓ Scripts marked executable${NC}"

# Python path for aliases (use venv python)
PYTHON_BIN="$REPO_ROOT/.venv/bin/python3"

# Detect shell config
if [[ -f "$HOME/.zshrc" ]]; then
  SHELL_RC="$HOME/.zshrc"
  SHELL_NAME="zsh"
elif [[ -f "$HOME/.bashrc" ]]; then
  SHELL_RC="$HOME/.bashrc"
  SHELL_NAME="bash"
else
  SHELL_RC="$HOME/.bashrc"
  SHELL_NAME="bash"
  touch "$SHELL_RC"
fi

# Prompt for Linear API key
echo ""
if [[ -z "$LINEAR_API_KEY" ]] && ! grep -q "LINEAR_API_KEY" "$SHELL_RC" 2>/dev/null; then
  echo "Enter your Linear API key (or press Enter to skip and add later):"
  read -r LINEAR_KEY
  LINEAR_KEY="${LINEAR_KEY//\"/}"  # Strip quotes
else
  LINEAR_KEY=""
  echo "LINEAR_API_KEY already in config or env. Skipping."
fi

# Block to append
MARKER="# --- Devloop AI (do not edit this line) ---"
BLOCK="

$MARKER
# Devloop AI — added by setup.sh
export PATH=\"\$PATH:$REPO_ROOT/.venv/bin\"

# Aliases (use from any directory)
alias ai-go=\"$PYTHON_BIN $AI_DIR/ai_go.py\"
alias ai-start=\"$PYTHON_BIN $AI_DIR/ai_start.py\"
alias ai-pr=\"$PYTHON_BIN $AI_DIR/ai_pr.py\"
alias ai-list=\"$PYTHON_BIN $AI_DIR/ai_list.py\"
alias ai-prompt=\"$PYTHON_BIN $AI_DIR/ai_prompt.py\"
alias ai-status=\"$PYTHON_BIN $AI_DIR/ai_status.py\"
alias ai-done=\"$PYTHON_BIN $AI_DIR/ai_done.py\"
alias ws-create=\"$PYTHON_BIN $AI_DIR/ws_create.py\"
"

if [[ -n "$LINEAR_KEY" ]]; then
  BLOCK="$BLOCK
export LINEAR_API_KEY=\"$LINEAR_KEY\"
export LINEAR_READY_STATE=\"Ready for build\"
"
fi

BLOCK="$BLOCK
# Warp quick commands (copy prompts to clipboard)
"

if [[ -n "$COPY_CMD" ]]; then
  BLOCK="$BLOCK
wv()  { cat \"$PROMPT_DIR/warp_velocity.md\" | $COPY_CMD && echo \"✓ warp_velocity copied\"; }
wo()  { cat \"$PROMPT_DIR/warp_orchestrator.md\" | $COPY_CMD && echo \"✓ warp_orchestrator copied\"; }
wr()  { cat \"$PROMPT_DIR/warp_review.md\" | $COPY_CMD && echo \"✓ warp_review copied\"; }
wd()  { cat \"$PROMPT_DIR/warp_debug.md\" | $COPY_CMD && echo \"✓ warp_debug copied\"; }
wa()  { cat \"$PROMPT_DIR/warp_architecture.md\" | $COPY_CMD && echo \"✓ warp_architecture copied\"; }

# Claude quick commands (when Warp not installed)
co()  { cat \"$PROMPT_DIR/claude_orchestrator.md\" | $COPY_CMD && echo \"✓ claude_orchestrator copied\"; }
cs()  { cat \"$PROMPT_DIR/claude_session_bootstrap.md\" | $COPY_CMD && echo \"✓ claude_session_bootstrap copied\"; }
"
else
  BLOCK="${BLOCK}# Clipboard not configured. Install xclip/xsel/wl-clipboard and re-run setup.
"
fi

BLOCK="${BLOCK}# --- End Devloop AI ---
"

# Append only if not already present
if ! grep -q "$MARKER" "$SHELL_RC" 2>/dev/null; then
  echo "$BLOCK" >> "$SHELL_RC"
  echo -e "${GREEN}✓ Config appended to $SHELL_RC${NC}"
else
  echo "Devloop AI block already in $SHELL_RC. Skipping."
fi

# Check for cursor command
if ! command -v cursor &>/dev/null && ! command -v cursor.exe &>/dev/null 2>/dev/null; then
  echo ""
  echo -e "${YELLOW}Cursor shell command not found.${NC}"
  echo "In Cursor: Ctrl+Shift+P → \"Shell Command: Install 'cursor' command in PATH\""
fi

# Check for gh
if ! command -v gh &>/dev/null; then
  echo ""
  echo -e "${YELLOW}GitHub CLI (gh) not found.${NC}"
  echo "Required for ai-pr. Install: https://cli.github.com/"
fi

echo ""
echo -e "${GREEN}Setup complete.${NC}"
echo ""
echo "Reload your shell config:"
echo "  source $SHELL_RC"
echo ""
echo "Or open a new terminal. Then try: ai-list"
