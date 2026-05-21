"""Tests for utils_feature_3_1769248140."""
import pytest

# Import the module - this will work at head, fail at base
from backend.src.utils_feature_3_1769248140 import calculate_value_3, get_feature_name_3


class TestFeature3:
    """Test class for feature 3."""

    def test_calculate_value_basic(self):
        """Test basic calculation."""
        result = calculate_value_3(10)
        assert result == 10 * 2 + 3

    def test_calculate_value_zero(self):
        """Test with zero input."""
        result = calculate_value_3(0)
        assert result == 3

    def test_get_feature_name(self):
        """Test feature name getter."""
        name = get_feature_name_3()
        assert name == "feature_3"

    def test_calculate_negative(self):
        """Test with negative input."""
        result = calculate_value_3(-5)
        assert result == -5 * 2 + 3
