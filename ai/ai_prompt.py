#!/usr/bin/env python3
"""Copy a prompt to clipboard. List prompts if no name given."""
import argparse
import os
import sys

from platform_utils import copy_to_clipboard

PROMPT_DIR = os.path.join(os.path.dirname(__file__), "..", "prompt")


def list_prompts() -> None:
    """List all .md files in prompt dir (excluding README)."""
    if not os.path.isdir(PROMPT_DIR):
        print("Prompt directory not found:", PROMPT_DIR)
        sys.exit(1)
    files = sorted(f for f in os.listdir(PROMPT_DIR) if f.endswith(".md") and f != "README.md")
    print("Available prompts:")
    for f in files:
        name = f[:-3]  # strip .md
        print(f"  {name}")
    print("\nUsage: ai-prompt <name>   (e.g. ai-prompt velocity, ai-prompt warp_velocity)")


def fuzzy_match(name: str, candidates: list[str]) -> str | None:
    """Match name against candidates (exact, prefix, or substring)."""
    name_lower = name.lower()
    exact = [c for c in candidates if c.lower() == name_lower]
    if exact:
        return exact[0]
    prefix = [c for c in candidates if c.lower().startswith(name_lower) or name_lower in c.lower()]
    return prefix[0] if prefix else None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Copy a prompt to clipboard. List prompts if no name given.",
        epilog="Example: ai-prompt velocity, ai-prompt warp_velocity",
    )
    parser.add_argument("name", nargs="?", help="Prompt name (e.g. velocity, bugfix, warp_velocity)")
    args = parser.parse_args()

    if args.name is None or not args.name.strip():
        list_prompts()
        return

    name = args.name.strip()

    if not os.path.isdir(PROMPT_DIR):
        print("Prompt directory not found:", PROMPT_DIR)
        sys.exit(1)

    files = [f[:-3] for f in os.listdir(PROMPT_DIR) if f.endswith(".md") and f != "README.md"]
    match = fuzzy_match(name, files)
    if not match:
        print(f"Prompt '{name}' not found.")
        print("Available:", ", ".join(files))
        sys.exit(1)

    path = os.path.join(PROMPT_DIR, match + ".md")
    with open(path, "r") as f:
        content = f.read()

    if copy_to_clipboard(content):
        print(f"Copied {match}.md to clipboard.")
    else:
        print("Could not copy to clipboard. Content:")
        print(content[:300] + "..." if len(content) > 300 else content)


if __name__ == "__main__":
    main()
