"""Tests for utility_5 - imports will FAIL at base commit."""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.src.utility_5_1769249100 import compute_5, get_name_5


def test_compute_5_basic():
    """Test basic computation."""
    assert compute_5(10) == 10 * 3 + 5


def test_compute_5_zero():
    """Test with zero."""
    assert compute_5(0) == 5


def test_compute_5_negative():
    """Test negative input."""
    assert compute_5(-5) == -5 * 3 + 5


def test_get_name_5():
    """Test name getter."""
    assert get_name_5() == "utility_5"
