"""
Unit tests for utility functions
"""
import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_path))


class TestUtilityFunctions:
    """Test cases for utility functions"""
    
    def test_validate_github_url_valid(self):
        """Test validation of valid GitHub URLs"""
        from utils import validate_github_url
        
        valid_urls = [
            "https://github.com/facebook/react",
            "https://github.com/microsoft/vscode",
            "facebook/react",
            "microsoft/vscode"
        ]
        
        for url in valid_urls:
            assert validate_github_url(url) is True
            
    def test_validate_github_url_invalid(self):
        """Test validation of invalid GitHub URLs"""
        from utils import validate_github_url
        
        invalid_urls = [
            "https://gitlab.com/user/repo",
            "not_a_url",
            "github.com/user",
            ""
        ]
        
        for url in invalid_urls:
            assert validate_github_url(url) is False
            
    def test_sanitize_input_basic(self):
        """Test basic input sanitization"""
        from utils import sanitize_input
        
        assert sanitize_input("normal text") == "normal text"
        assert sanitize_input("  spaces  ") == "spaces"
        
    def test_sanitize_input_special_chars(self):
        """Test sanitization of special characters"""
        from utils import sanitize_input
        
        dangerous = "<script>alert('xss')</script>"
        sanitized = sanitize_input(dangerous)
        
        assert "<script>" not in sanitized
        assert "alert" not in sanitized
        
    def test_format_risk_score(self):
        """Test risk score formatting"""
        from utils import format_risk_score
        
        assert format_risk_score(0.856) == "85.6%"
        assert format_risk_score(0.1) == "10.0%"
        assert format_risk_score(1.0) == "100.0%"
        
    def test_calculate_percentage(self):
        """Test percentage calculation"""
        from utils import calculate_percentage
        
        assert calculate_percentage(50, 100) == 50.0
        assert calculate_percentage(1, 3) == pytest.approx(33.33, 0.01)
        assert calculate_percentage(0, 100) == 0.0
        
    def test_calculate_percentage_zero_total(self):
        """Test percentage calculation with zero total"""
        from utils import calculate_percentage
        
        assert calculate_percentage(0, 0) == 0.0
        
    def test_parse_commit_message(self):
        """Test commit message parsing"""
        from utils import parse_commit_message
        
        message = "fix: critical bug in authentication module"
        parsed = parse_commit_message(message)
        
        assert parsed["type"] == "fix"
        assert "bug" in parsed["keywords"]
        
    def test_extract_bug_keywords(self):
        """Test bug keyword extraction"""
        from utils import extract_bug_keywords
        
        text = "This is a critical bug that needs a hotfix patch"
        keywords = extract_bug_keywords(text)
        
        assert "bug" in keywords
        assert "hotfix" in keywords
        assert "patch" in keywords
        
    def test_calculate_file_complexity(self):
        """Test file complexity calculation"""
        from utils import calculate_file_complexity
        
        file_data = {
            "additions": 100,
            "deletions": 50,
            "changes": 150
        }
        
        complexity = calculate_file_complexity(file_data)
        
        assert isinstance(complexity, float)
        assert complexity > 0
        
    def test_normalize_value(self):
        """Test value normalization"""
        from utils import normalize_value
        
        assert normalize_value(50, 0, 100) == 0.5
        assert normalize_value(0, 0, 100) == 0.0
        assert normalize_value(100, 0, 100) == 1.0
        
    def test_get_file_extension(self):
        """Test file extension extraction"""
        from utils import get_file_extension
        
        assert get_file_extension("test.py") == ".py"
        assert get_file_extension("script.js") == ".js"
        assert get_file_extension("README.md") == ".md"
        assert get_file_extension("noextension") == ""
        
    def test_is_source_file(self):
        """Test source file detection"""
        from utils import is_source_file
        
        assert is_source_file("main.py") is True
        assert is_source_file("app.js") is True
        assert is_source_file("README.md") is False
        assert is_source_file("image.png") is False
        
    def test_calculate_time_difference(self):
        """Test time difference calculation"""
        from utils import calculate_time_difference
        from datetime import datetime, timedelta
        
        now = datetime.now()
        past = now - timedelta(days=7)
        
        diff = calculate_time_difference(past, now)
        
        assert diff == 7
        
    def test_format_timestamp(self):
        """Test timestamp formatting"""
        from utils import format_timestamp
        from datetime import datetime
        
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        formatted = format_timestamp(timestamp)
        
        assert isinstance(formatted, str)
        assert "2024" in formatted
        
    def test_generate_unique_id(self):
        """Test unique ID generation"""
        from utils import generate_unique_id
        
        id1 = generate_unique_id()
        id2 = generate_unique_id()
        
        assert id1 != id2
        assert len(id1) > 0
        
    def test_hash_string(self):
        """Test string hashing"""
        from utils import hash_string
        
        text = "test string"
        hashed = hash_string(text)
        
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed == hash_string(text)  # Consistent hashing
        
    def test_truncate_string(self):
        """Test string truncation"""
        from utils import truncate_string
        
        long_text = "This is a very long string that needs to be truncated"
        truncated = truncate_string(long_text, max_length=20)
        
        assert len(truncated) <= 23  # 20 + "..."
        assert truncated.endswith("...")
        
    def test_merge_dictionaries(self):
        """Test dictionary merging"""
        from utils import merge_dictionaries
        
        dict1 = {"a": 1, "b": 2}
        dict2 = {"b": 3, "c": 4}
        
        merged = merge_dictionaries(dict1, dict2)
        
        assert merged["a"] == 1
        assert merged["b"] == 3  # dict2 overwrites
        assert merged["c"] == 4
        
    def test_filter_none_values(self):
        """Test filtering None values from dictionary"""
        from utils import filter_none_values
        
        data = {"a": 1, "b": None, "c": 3, "d": None}
        filtered = filter_none_values(data)
        
        assert "a" in filtered
        assert "b" not in filtered
        assert "c" in filtered
        assert "d" not in filtered
        
    def test_chunk_list(self):
        """Test list chunking"""
        from utils import chunk_list
        
        items = list(range(10))
        chunks = chunk_list(items, chunk_size=3)
        
        assert len(chunks) == 4
        assert len(chunks[0]) == 3
        assert len(chunks[-1]) == 1
        
    def test_flatten_list(self):
        """Test list flattening"""
        from utils import flatten_list
        
        nested = [[1, 2], [3, 4], [5]]
        flattened = flatten_list(nested)
        
        assert flattened == [1, 2, 3, 4, 5]
        
    def test_remove_duplicates(self):
        """Test duplicate removal"""
        from utils import remove_duplicates
        
        items = [1, 2, 2, 3, 3, 3, 4]
        unique = remove_duplicates(items)
        
        assert len(unique) == 4
        assert set(unique) == {1, 2, 3, 4}
        
    def test_sort_by_key(self):
        """Test sorting by key"""
        from utils import sort_by_key
        
        items = [
            {"name": "c", "value": 3},
            {"name": "a", "value": 1},
            {"name": "b", "value": 2}
        ]
        
        sorted_items = sort_by_key(items, key="value")
        
        assert sorted_items[0]["value"] == 1
        assert sorted_items[-1]["value"] == 3
        
    def test_group_by_key(self):
        """Test grouping by key"""
        from utils import group_by_key
        
        items = [
            {"type": "bug", "count": 1},
            {"type": "feature", "count": 2},
            {"type": "bug", "count": 3}
        ]
        
        grouped = group_by_key(items, key="type")
        
        assert "bug" in grouped
        assert "feature" in grouped
        assert len(grouped["bug"]) == 2
