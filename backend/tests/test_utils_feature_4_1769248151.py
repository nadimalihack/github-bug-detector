"""Tests for utils_feature_4_1769248151."""
import pytest

# Import the module - this will work at head, fail at base
from backend.src.utils_feature_4_1769248151 import calculate_value_4, get_feature_name_4


class TestFeature4:
    """Test class for feature 4."""

    def test_calculate_value_basic(self):
        """Test basic calculation."""
        result = calculate_value_4(10)
        assert result == 10 * 2 + 4

    def test_calculate_value_zero(self):
        """Test with zero input."""
        result = calculate_value_4(0)
        assert result == 4

    def test_get_feature_name(self):
        """Test feature name getter."""
        name = get_feature_name_4()
        assert name == "feature_4"

    def test_calculate_negative(self):
        """Test with negative input."""
        result = calculate_value_4(-5)
        assert result == -5 * 2 + 4
