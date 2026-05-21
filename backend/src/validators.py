"""
Input validation utilities for the GitHub Bug Detection API.
Provides comprehensive validation for user inputs, repository URLs, and code analysis requests.
"""

import re
from typing import Optional, Tuple, Dict, Any


class ValidationError(Exception):
    """Custom exception for validation errors."""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


def validate_github_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a GitHub repository URL.
    
    Args:
        url: The URL to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url:
        return False, "URL cannot be empty"
    
    # Pattern for GitHub URLs
    github_pattern = r'^https?://github\.com/[\w.-]+/[\w.-]+/?$'
    
    if not re.match(github_pattern, url):
        return False, "Invalid GitHub repository URL format"
    
    return True, None


def validate_username(username: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a GitHub username.
    
    Args:
        username: The username to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username:
        return False, "Username cannot be empty"
    
    if len(username) > 39:
        return False, "Username cannot exceed 39 characters"
    
    # GitHub username pattern: alphanumeric and hyphens, cannot start/end with hyphen
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$'
    
    if not re.match(pattern, username):
        return False, "Invalid username format"
    
    if '--' in username:
        return False, "Username cannot contain consecutive hyphens"
    
    return True, None


def validate_repository_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a repository name.
    
    Args:
        name: The repository name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Repository name cannot be empty"
    
    if len(name) > 100:
        return False, "Repository name cannot exceed 100 characters"
    
    # Repository name pattern
    pattern = r'^[\w.-]+$'
    
    if not re.match(pattern, name):
        return False, "Repository name contains invalid characters"
    
    return True, None


def validate_code_snippet(code: str, max_length: int = 50000) -> Tuple[bool, Optional[str]]:
    """
    Validate a code snippet for analysis.
    
    Args:
        code: The code snippet to validate
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not code:
        return False, "Code snippet cannot be empty"
    
    if len(code) > max_length:
        return False, f"Code snippet exceeds maximum length of {max_length} characters"
    
    return True, None


def validate_analysis_request(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate a complete analysis request.
    
    Args:
        data: The request data dictionary
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['repo_url']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate repo_url
    is_valid, error = validate_github_url(data.get('repo_url', ''))
    if not is_valid:
        return False, error
    
    return True, None


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing potentially dangerous characters.
    
    Args:
        text: The input text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove control characters except newlines and tabs
    sanitized = ''.join(char for char in text if char.isprintable() or char in '\n\t')
    
    return sanitized.strip()
