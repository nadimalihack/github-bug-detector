"""Tests for utils_feature_5_1769248161."""
import pytest

# Import the module - this will work at head, fail at base
from backend.src.utils_feature_5_1769248161 import calculate_value_5, get_feature_name_5


class TestFeature5:
    """Test class for feature 5."""

    def test_calculate_value_basic(self):
        """Test basic calculation."""
        result = calculate_value_5(10)
        assert result == 10 * 2 + 5

    def test_calculate_value_zero(self):
        """Test with zero input."""
        result = calculate_value_5(0)
        assert result == 5

    def test_get_feature_name(self):
        """Test feature name getter."""
        name = get_feature_name_5()
        assert name == "feature_5"

    def test_calculate_negative(self):
        """Test with negative input."""
        result = calculate_value_5(-5)
        assert result == -5 * 2 + 5
