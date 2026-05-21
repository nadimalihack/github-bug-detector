"""
Unit tests for the validators module.
Tests input validation functions for GitHub URLs, usernames, and code analysis.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from validators import (
    validate_github_url,
    validate_username,
    validate_repository_name,
    validate_code_snippet,
    validate_analysis_request,
    sanitize_input,
    ValidationError
)


class TestValidateGithubUrl:
    """Tests for validate_github_url function."""
    
    def test_valid_https_url(self):
        """Test valid HTTPS GitHub URL."""
        is_valid, error = validate_github_url("https://github.com/user/repo")
        assert is_valid is True
        assert error is None
    
    def test_valid_http_url(self):
        """Test valid HTTP GitHub URL."""
        is_valid, error = validate_github_url("http://github.com/user/repo")
        assert is_valid is True
        assert error is None
    
    def test_valid_url_with_trailing_slash(self):
        """Test valid URL with trailing slash."""
        is_valid, error = validate_github_url("https://github.com/user/repo/")
        assert is_valid is True
        assert error is None
    
    def test_empty_url(self):
        """Test empty URL returns error."""
        is_valid, error = validate_github_url("")
        assert is_valid is False
        assert error == "URL cannot be empty"
    
    def test_invalid_url_format(self):
        """Test invalid URL format."""
        is_valid, error = validate_github_url("not-a-url")
        assert is_valid is False
        assert "Invalid GitHub repository URL format" in error
    
    def test_non_github_url(self):
        """Test non-GitHub URL."""
        is_valid, error = validate_github_url("https://gitlab.com/user/repo")
        assert is_valid is False
        assert "Invalid GitHub repository URL format" in error


class TestValidateUsername:
    """Tests for validate_username function."""
    
    def test_valid_username(self):
        """Test valid username."""
        is_valid, error = validate_username("validuser123")
        assert is_valid is True
        assert error is None
    
    def test_valid_username_with_hyphen(self):
        """Test valid username with hyphen."""
        is_valid, error = validate_username("valid-user")
        assert is_valid is True
        assert error is None
    
    def test_empty_username(self):
        """Test empty username."""
        is_valid, error = validate_username("")
        assert is_valid is False
        assert error == "Username cannot be empty"
    
    def test_username_too_long(self):
        """Test username exceeding 39 characters."""
        is_valid, error = validate_username("a" * 40)
        assert is_valid is False
        assert "cannot exceed 39 characters" in error
    
    def test_username_with_consecutive_hyphens(self):
        """Test username with consecutive hyphens."""
        is_valid, error = validate_username("user--name")
        assert is_valid is False
        assert "consecutive hyphens" in error


class TestValidateRepositoryName:
    """Tests for validate_repository_name function."""
    
    def test_valid_repo_name(self):
        """Test valid repository name."""
        is_valid, error = validate_repository_name("my-repo")
        assert is_valid is True
        assert error is None
    
    def test_valid_repo_name_with_dots(self):
        """Test valid repository name with dots."""
        is_valid, error = validate_repository_name("my.repo.name")
        assert is_valid is True
        assert error is None
    
    def test_empty_repo_name(self):
        """Test empty repository name."""
        is_valid, error = validate_repository_name("")
        assert is_valid is False
        assert error == "Repository name cannot be empty"
    
    def test_repo_name_too_long(self):
        """Test repository name exceeding 100 characters."""
        is_valid, error = validate_repository_name("a" * 101)
        assert is_valid is False
        assert "cannot exceed 100 characters" in error


class TestValidateCodeSnippet:
    """Tests for validate_code_snippet function."""
    
    def test_valid_code_snippet(self):
        """Test valid code snippet."""
        code = "def hello():\n    print('Hello, World!')"
        is_valid, error = validate_code_snippet(code)
        assert is_valid is True
        assert error is None
    
    def test_empty_code_snippet(self):
        """Test empty code snippet."""
        is_valid, error = validate_code_snippet("")
        assert is_valid is False
        assert error == "Code snippet cannot be empty"
    
    def test_code_snippet_too_long(self):
        """Test code snippet exceeding max length."""
        is_valid, error = validate_code_snippet("a" * 100, max_length=50)
        assert is_valid is False
        assert "exceeds maximum length" in error


class TestValidateAnalysisRequest:
    """Tests for validate_analysis_request function."""
    
    def test_valid_request(self):
        """Test valid analysis request."""
        data = {"repo_url": "https://github.com/user/repo"}
        is_valid, error = validate_analysis_request(data)
        assert is_valid is True
        assert error is None
    
    def test_missing_repo_url(self):
        """Test request missing repo_url."""
        data = {}
        is_valid, error = validate_analysis_request(data)
        assert is_valid is False
        assert "Missing required field: repo_url" in error


class TestSanitizeInput:
    """Tests for sanitize_input function."""
    
    def test_normal_text(self):
        """Test normal text passes through."""
        text = "Hello, World!"
        assert sanitize_input(text) == "Hello, World!"
    
    def test_removes_null_bytes(self):
        """Test null bytes are removed."""
        text = "Hello\x00World"
        assert sanitize_input(text) == "HelloWorld"
    
    def test_empty_input(self):
        """Test empty input returns empty string."""
        assert sanitize_input("") == ""
        assert sanitize_input(None) == ""
    
    def test_preserves_newlines_and_tabs(self):
        """Test newlines and tabs are preserved."""
        text = "Hello\n\tWorld"
        assert sanitize_input(text) == "Hello\n\tWorld"
    
    def test_strips_whitespace(self):
        """Test leading/trailing whitespace is stripped."""
        text = "  Hello  "
        assert sanitize_input(text) == "Hello"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
