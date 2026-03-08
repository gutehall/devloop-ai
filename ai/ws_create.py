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
ORCH_PROMPT_FILE = "warp_orchestrator.md"
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

def main():
    ap = argparse.ArgumentParser(
        description="ws-create: generate structured Warp prompt, then create Project/Issues in Linear from Warp JSON output."
    )
    ap.add_argument("task", nargs="*", help="Task description for Warp.")
    ap.add_argument("--prompts-dir", default=PROMPTS_DIR_DEFAULT, help="Path to prompts directory.")
    ap.add_argument("--no-open-warp", action="store_true", help="Do not auto-open Warp.")
    ap.add_argument("--commit-only", action="store_true", help="Skip planning step; expect JSON already in clipboard and create in Linear.")
    ap.add_argument("--watch", action="store_true", help="Poll clipboard until valid JSON appears (timeout 60s), then create in Linear.")
    args = ap.parse_args()

    prompts_dir = Path(args.prompts_dir)
    orch_path = prompts_dir / ORCH_PROMPT_FILE

    if args.commit_only:
        clip = pbpaste()
        json_block = extract_json_block(clip) or clip.strip()
        if not json_block:
            print("❌ Clipboard is empty. Copy the ```json ... ``` block from Warp, then run:")
            print("   ws-create --commit-only")
            sys.exit(1)
        print("→ Creating in Linear from clipboard JSON…")
        rc = run_ai_linear_create(json_block)
        sys.exit(rc)

    task = " ".join(args.task).strip()
    if not task:
        task = input("Describe the task for Warp: ").strip()
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

    print("✅ Copied orchestrator prompt + task to clipboard.")
    if not args.no_open_warp:
        subprocess.Popen(["open", "-a", "Warp"])

    print("\nNext steps (still part of this single flow):")
    print("1) Paste into Warp (⌘V) and run the prompt.")
    print("2) In Warp output: copy the ```json ... ``` block to clipboard.")
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
        print("Make sure you copied the ```json ... ``` block from Warp output.")
        sys.exit(1)

    print("→ Creating Project/Issues in Linear…")
    rc = run_ai_linear_create(json_block)
    sys.exit(rc)

if __name__ == "__main__":
    main()
