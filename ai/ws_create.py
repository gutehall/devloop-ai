#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

try:
    from platform_utils import paste_from_clipboard
except ImportError:
    def paste_from_clipboard() -> str:
        try:
            return subprocess.check_output(["pbpaste"]).decode("utf-8", errors="replace")
        except Exception:
            return ""

PROMPTS_DIR_DEFAULT = "prompt"
WARP_ORCH_PROMPT = "warp_orchestrator.md"
CLAUDE_ORCH_PROMPT = "claude_orchestrator.md"
WATCH_INTERVAL = 1.5
WATCH_TIMEOUT = 60


def pbcopy(text: str) -> None:
    p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
    p.communicate(text.encode("utf-8"))

def pbpaste() -> str:
    return paste_from_clipboard()

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def extract_json_block(text: str) -> str | None:
    """
    Extracts content inside ```json ... ``` fences. Returns raw JSON string or None.
    """
    marker = "```json"
    if marker not in text:
        return None
    start = text.find(marker) + len(marker)
    end = text.find("```", start)
    if end == -1:
        return None
    return text[start:end].strip()


def is_valid_linear_json(raw: str) -> bool:
    """Check if string parses as Linear project/issues JSON."""
    try:
        data = json.loads(raw)
        return isinstance(data.get("issues"), list)
    except (json.JSONDecodeError, TypeError):
        return False

def run_ai_linear_create(json_text: str) -> int:
    """Calls ai-linear-create by piping JSON to it."""
    ai_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = [sys.executable, os.path.join(ai_dir, "ai_linear_create.py")]
    env = os.environ.copy()
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, env=env)
    p.communicate(json_text.encode("utf-8"))
    return p.returncode

def open_planning_app(use_claude: bool) -> None:
    """Open Warp or Claude app. On non-macOS or if app missing, user pastes manually."""
    import platform
    if platform.system() != "Darwin":
        return
    app = "Claude" if use_claude else "Warp"
    try:
        subprocess.Popen(["open", "-a", app])
    except (subprocess.SubprocessError, FileNotFoundError):
        pass


def main():
    ap = argparse.ArgumentParser(
        description="ws-create: generate structured planning prompt, then create Project/Issues in Linear from JSON output."
    )
    ap.add_argument("task", nargs="*", help="Task description.")
    ap.add_argument("--prompts-dir", default=PROMPTS_DIR_DEFAULT, help="Path to prompts directory.")
    ap.add_argument("--claude", action="store_true", help="Use Claude instead of Warp (when Warp not installed).")
    ap.add_argument("--no-open-warp", action="store_true", help="Do not auto-open Warp (ignored if --claude).")
    ap.add_argument("--no-open-claude", action="store_true", help="Do not auto-open Claude (only with --claude).")
    ap.add_argument("--commit-only", action="store_true", help="Skip planning step; expect JSON already in clipboard and create in Linear.")
    ap.add_argument("--watch", action="store_true", help="Poll clipboard until valid JSON appears (timeout 60s), then create in Linear.")
    args = ap.parse_args()

    use_claude = args.claude
    orch_file = CLAUDE_ORCH_PROMPT if use_claude else WARP_ORCH_PROMPT
    app_name = "Claude" if use_claude else "Warp"

    prompts_dir = Path(args.prompts_dir)
    orch_path = prompts_dir / orch_file

    if args.commit_only:
        clip = pbpaste()
        json_block = extract_json_block(clip) or clip.strip()
        if not json_block:
            print("❌ Clipboard is empty. Copy the ```json ... ``` block from Warp or Claude, then run:")
            print("   ws-create --commit-only")
            sys.exit(1)
        print("→ Creating in Linear from clipboard JSON…")
        rc = run_ai_linear_create(json_block)
        sys.exit(rc)

    task = " ".join(args.task).strip()
    if not task:
        task = input(f"Describe the task for {app_name}: ").strip()
    if not task:
        print("No task provided.")
        sys.exit(1)

    if not orch_path.exists():
        print(f"❌ Missing prompt file: {orch_path}")
        sys.exit(1)

    orch_prompt = read_text(orch_path)

    combined = f"""{orch_prompt}

---

# TASK
{task}

# IMPORTANT
After the plan, output a JSON block between ```json fences with:
{{
  "project": {{ "name": "...", "description": "...", "priority": 1-4 }},
  "issues": [
    {{ "title": "...", "description": "...", "priority": 1-4, "labels": ["type:feature"], "complexity": 1-5, "dependencies": [] }}
  ]
}}
"""
    pbcopy(combined)

    print(f"✅ Copied {orch_file} + task to clipboard.")
    if use_claude:
        if not args.no_open_claude:
            open_planning_app(use_claude=True)
    else:
        if not args.no_open_warp:
            open_planning_app(use_claude=False)

    print("\nNext steps (still part of this single flow):")
    print(f"1) Paste into {app_name} (⌘V) and run the prompt.")
    print(f"2) In {app_name} output: copy the ```json ... ``` block to clipboard.")
    if args.watch:
        print("\nWatching clipboard (Ctrl+C to cancel, timeout 60s)…")
        start = time.monotonic()
        json_block = None
        while (time.monotonic() - start) < WATCH_TIMEOUT:
            clip = pbpaste()
            json_block = extract_json_block(clip) or clip.strip()
            if json_block and is_valid_linear_json(json_block):
                break
            time.sleep(WATCH_INTERVAL)
        if not json_block or not is_valid_linear_json(json_block):
            print("❌ Timeout. No valid JSON in clipboard.")
            sys.exit(1)
    else:
        input("\nWhen you have copied the JSON block, press Enter to create in Linear… ")
        clip = pbpaste()
        json_block = extract_json_block(clip) or clip.strip()
    if not json_block:
        print("❌ Could not find JSON in clipboard.")
        print(f"Make sure you copied the ```json ... ``` block from {app_name} output.")
        sys.exit(1)

    print("→ Creating Project/Issues in Linear…")
    rc = run_ai_linear_create(json_block)
    sys.exit(rc)

if __name__ == "__main__":
    main()
