"""Tests for utility_1 - imports will FAIL at base commit."""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.src.utility_1_1769249064 import compute_1, get_name_1


def test_compute_1_basic():
    """Test basic computation."""
    assert compute_1(10) == 10 * 3 + 1


def test_compute_1_zero():
    """Test with zero."""
    assert compute_1(0) == 1


def test_compute_1_negative():
    """Test negative input."""
    assert compute_1(-5) == -5 * 3 + 1


def test_get_name_1():
    """Test name getter."""
    assert get_name_1() == "utility_1"
