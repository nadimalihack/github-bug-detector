"""Tests for utils_feature_2_1769248131."""
import pytest

# Import the module - this will work at head, fail at base
from backend.src.utils_feature_2_1769248131 import calculate_value_2, get_feature_name_2


class TestFeature2:
    """Test class for feature 2."""

    def test_calculate_value_basic(self):
        """Test basic calculation."""
        result = calculate_value_2(10)
        assert result == 10 * 2 + 2

    def test_calculate_value_zero(self):
        """Test with zero input."""
        result = calculate_value_2(0)
        assert result == 2

    def test_get_feature_name(self):
        """Test feature name getter."""
        name = get_feature_name_2()
        assert name == "feature_2"

    def test_calculate_negative(self):
        """Test with negative input."""
        result = calculate_value_2(-5)
        assert result == -5 * 2 + 2
