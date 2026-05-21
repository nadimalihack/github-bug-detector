"""Tests for utility_4 - imports will FAIL at base commit."""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.src.utility_4_1769249091 import compute_4, get_name_4


def test_compute_4_basic():
    """Test basic computation."""
    assert compute_4(10) == 10 * 3 + 4


def test_compute_4_zero():
    """Test with zero."""
    assert compute_4(0) == 4


def test_compute_4_negative():
    """Test negative input."""
    assert compute_4(-5) == -5 * 3 + 4


def test_get_name_4():
    """Test name getter."""
    assert get_name_4() == "utility_4"
