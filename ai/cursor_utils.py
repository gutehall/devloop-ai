"""Shared Cursor prompt and payload helpers for ai_go and ai_start."""
import os

_PROMPT_DIR = os.path.join(os.path.dirname(__file__), "..", "prompt")
_CURSOR_VELOCITY_PATH = os.path.join(_PROMPT_DIR, "cursor_velocity.md")

_CURSOR_FAST_PROMPT_FALLBACK = """You are implementing this issue.

Primary goal:
Deliver a minimal working solution that satisfies the acceptance criteria.

Rules:
- Do not refactor unrelated code.
- Do not redesign architecture.
- Keep changes small and focused.
- Follow existing patterns.
- Prefer simple solutions over clever ones.
- Stop if scope expands.

Execution steps:
1. Read relevant files before coding.
2. Implement minimal solution.
3. Add or update tests.
4. Ensure CI passes.
5. Re-check acceptance criteria.

If ambiguity exists:
- Make the safest reasonable assumption.
- Document the assumption in code comments or PR description.

Do not:
- Introduce new abstractions unless required.
- Change APIs unless explicitly required.
- Perform speculative improvements.
"""


def _load_cursor_velocity() -> str:
    """Load cursor_velocity.md as single source of truth. Fallback to built-in if file missing."""
    try:
        if os.path.isfile(_CURSOR_VELOCITY_PATH):
            with open(_CURSOR_VELOCITY_PATH) as f:
                return f.read().strip()
    except OSError:
        pass
    return _CURSOR_FAST_PROMPT_FALLBACK


# Single source of truth: cursor_velocity.md (or fallback)
CURSOR_FAST_PROMPT = _load_cursor_velocity()


def build_cursor_payload(issue: dict, prompt_text: str | None = None) -> str:
    """Build the Cursor payload: prompt + issue context (identifier, URL, title, description)."""
    text = prompt_text if prompt_text is not None else CURSOR_FAST_PROMPT
    return f"""{text}

--- LINEAR ISSUE {issue['identifier']} ---
Title: {issue['title']}
URL: {issue['url']}

Description:
{issue.get('description') or '(no description)'}
"""
