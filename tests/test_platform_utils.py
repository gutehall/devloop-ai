"""Tests for platform_utils with mocks (no real clipboard/subprocess)."""
from unittest.mock import MagicMock, patch

import platform_utils


class TestCopyToClipboard:
    def test_returns_true_when_pyperclip_succeeds(self):
        """When pyperclip is available, copy succeeds and returns True."""
        mock_pyperclip = MagicMock()
        with patch.dict("sys.modules", {"pyperclip": mock_pyperclip}):
            result = platform_utils.copy_to_clipboard("hello")
            assert result is True
            mock_pyperclip.copy.assert_called_once_with("hello")

    def test_returns_false_when_pyperclip_raises(self):
        """When pyperclip raises, falls through to platform fallback."""
        mock_pyperclip = MagicMock()
        mock_pyperclip.copy.side_effect = Exception("clipboard error")
        with patch.dict("sys.modules", {"pyperclip": mock_pyperclip}):
            with patch.object(platform_utils.subprocess, "Popen", side_effect=FileNotFoundError):
                # Platform fallback will fail (no pbcopy/xclip/etc)
                result = platform_utils.copy_to_clipboard("hello")
                assert result is False


class TestPasteFromClipboard:
    def test_returns_string_when_pyperclip_succeeds(self):
        """When pyperclip is available, paste returns clipboard content."""
        mock_pyperclip = MagicMock()
        mock_pyperclip.paste.return_value = "pasted content"
        with patch.dict("sys.modules", {"pyperclip": mock_pyperclip}):
            result = platform_utils.paste_from_clipboard()
            assert result == "pasted content"
            mock_pyperclip.paste.assert_called_once()
