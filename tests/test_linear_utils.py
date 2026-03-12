"""Tests for linear_utils."""
import pytest

# Import after path is set by conftest
import linear_utils


class TestSlug:
    def test_normal_string(self):
        assert linear_utils.slug("Add user authentication") == "add-user-authentication"

    def test_empty_string(self):
        assert linear_utils.slug("") == ""

    def test_truncation_to_40_chars(self):
        s = "a" * 50
        assert len(linear_utils.slug(s)) == 40

    def test_strips_leading_trailing_hyphens(self):
        assert linear_utils.slug("  Hello World  ") == "hello-world"
        assert linear_utils.slug("---foo---") == "foo"

    def test_lowercase(self):
        assert linear_utils.slug("UPPERCASE") == "uppercase"

    def test_replaces_special_chars_with_hyphen(self):
        assert linear_utils.slug("foo@bar#baz!") == "foo-bar-baz"

    def test_unicode_collapsed_to_hyphen(self):
        # Non-alphanumeric chars become hyphens
        result = linear_utils.slug("café & naïve")
        assert "caf" in result
        assert result.count("-") >= 2


class TestAuthHeader:
    def test_bearer_prefix_added_when_missing(self, monkeypatch):
        monkeypatch.setenv("LINEAR_API_KEY", "sk_abc123")
        # Reload to pick up new env
        import importlib
        importlib.reload(linear_utils)
        try:
            assert linear_utils._auth_header() == "Bearer sk_abc123"
        finally:
            importlib.reload(linear_utils)

    def test_bearer_prefix_preserved(self, monkeypatch):
        monkeypatch.setenv("LINEAR_API_KEY", "Bearer tok")
        import importlib
        importlib.reload(linear_utils)
        try:
            assert linear_utils._auth_header() == "Bearer tok"
        finally:
            importlib.reload(linear_utils)

    def test_lin_api_preserved(self, monkeypatch):
        monkeypatch.setenv("LINEAR_API_KEY", "lin_api_xyz")
        import importlib
        importlib.reload(linear_utils)
        try:
            assert linear_utils._auth_header() == "lin_api_xyz"
        finally:
            importlib.reload(linear_utils)

    def test_empty_when_no_api_key(self, monkeypatch):
        monkeypatch.delenv("LINEAR_API_KEY", raising=False)
        import importlib
        importlib.reload(linear_utils)
        try:
            assert linear_utils._auth_header() == ""
        finally:
            importlib.reload(linear_utils)


class TestGqlOk:
    def test_no_errors_key(self):
        assert linear_utils.gql_ok({"data": {"foo": "bar"}}) is True

    def test_empty_errors_list(self):
        assert linear_utils.gql_ok({"data": {}, "errors": []}) is True

    def test_errors_present(self):
        assert linear_utils.gql_ok({"errors": [{"message": "x"}]}) is False


class TestGetIssueByKey:
    def test_valid_format_returns_none_without_api(self, monkeypatch):
        monkeypatch.delenv("LINEAR_API_KEY", raising=False)
        import importlib
        importlib.reload(linear_utils)
        try:
            with pytest.raises(SystemExit):
                linear_utils.get_issue_by_key("LIN-123")
        finally:
            importlib.reload(linear_utils)

    def test_invalid_key_formats(self):
        """Invalid formats should return None before any API call."""
        from unittest.mock import patch

        with patch.object(linear_utils, "gql") as mock_gql:
            assert linear_utils.get_issue_by_key("") is None
            assert linear_utils.get_issue_by_key("123") is None
            assert linear_utils.get_issue_by_key("LIN") is None
            assert linear_utils.get_issue_by_key("LIN-") is None
            assert linear_utils.get_issue_by_key("not-valid") is None
            mock_gql.assert_not_called()
