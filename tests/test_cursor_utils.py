"""Tests for cursor_utils."""
import cursor_utils


class TestBuildCursorPayload:
    def test_contains_identifier_title_url_description(self):
        issue = {
            "identifier": "LIN-42",
            "title": "Add feature X",
            "url": "https://linear.app/team/issue/LIN-42",
            "description": "Do the thing.",
        }
        payload = cursor_utils.build_cursor_payload(issue)
        assert "LIN-42" in payload
        assert "Add feature X" in payload
        assert "https://linear.app/team/issue/LIN-42" in payload
        assert "Do the thing." in payload
        assert "--- LINEAR ISSUE LIN-42 ---" in payload

    def test_no_description_uses_placeholder(self):
        issue = {
            "identifier": "LIN-1",
            "title": "Quick fix",
            "url": "https://linear.app/x/issue/LIN-1",
        }
        payload = cursor_utils.build_cursor_payload(issue)
        assert "(no description)" in payload

    def test_custom_prompt_text(self):
        issue = {
            "identifier": "LIN-99",
            "title": "Bug",
            "url": "https://linear.app/b/LIN-99",
        }
        custom = "Custom instructions here."
        payload = cursor_utils.build_cursor_payload(issue, custom)
        assert payload.startswith("Custom instructions here.")
        assert "LIN-99" in payload
        assert cursor_utils.CURSOR_FAST_PROMPT not in payload or "Custom instructions" in payload

    def test_default_uses_cursor_fast_prompt(self):
        issue = {
            "identifier": "LIN-1",
            "title": "T",
            "url": "https://x",
        }
        payload = cursor_utils.build_cursor_payload(issue)
        assert "You are implementing this issue" in payload
        assert "Primary goal" in payload
        assert "Deliver a minimal working solution" in payload
