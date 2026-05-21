"""Tests for utility_3 - imports will FAIL at base commit."""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.src.utility_3_1769249082 import compute_3, get_name_3


def test_compute_3_basic():
    """Test basic computation."""
    assert compute_3(10) == 10 * 3 + 3


def test_compute_3_zero():
    """Test with zero."""
    assert compute_3(0) == 3


def test_compute_3_negative():
    """Test negative input."""
    assert compute_3(-5) == -5 * 3 + 3


def test_get_name_3():
    """Test name getter."""
    assert get_name_3() == "utility_3"
