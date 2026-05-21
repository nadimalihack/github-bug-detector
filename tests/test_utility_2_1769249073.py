"""Tests for utility_2 - imports will FAIL at base commit."""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.src.utility_2_1769249073 import compute_2, get_name_2


def test_compute_2_basic():
    """Test basic computation."""
    assert compute_2(10) == 10 * 3 + 2


def test_compute_2_zero():
    """Test with zero."""
    assert compute_2(0) == 2


def test_compute_2_negative():
    """Test negative input."""
    assert compute_2(-5) == -5 * 3 + 2


def test_get_name_2():
    """Test name getter."""
    assert get_name_2() == "utility_2"
