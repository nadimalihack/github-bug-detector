"""Tests for utils_feature_1_1769248122."""
import pytest

# Import the module - this will work at head, fail at base
from backend.src.utils_feature_1_1769248122 import calculate_value_1, get_feature_name_1


class TestFeature1:
    """Test class for feature 1."""

    def test_calculate_value_basic(self):
        """Test basic calculation."""
        result = calculate_value_1(10)
        assert result == 10 * 2 + 1

    def test_calculate_value_zero(self):
        """Test with zero input."""
        result = calculate_value_1(0)
        assert result == 1

    def test_get_feature_name(self):
        """Test feature name getter."""
        name = get_feature_name_1()
        assert name == "feature_1"

    def test_calculate_negative(self):
        """Test with negative input."""
        result = calculate_value_1(-5)
        assert result == -5 * 2 + 1
