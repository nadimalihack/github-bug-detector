#!/usr/bin/env python
"""
Comprehensive test runner script for GitHub Bug Detection System
"""
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and print results"""
    print(f"\n{'='*80}")
    print(f"Running: {description}")
    print(f"{'='*80}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=False)
    
    if result.returncode != 0:
        print(f"\n❌ {description} failed with exit code {result.returncode}")
        return False
    else:
        print(f"\n✅ {description} passed")
        return True


def run_unit_tests(verbose=False):
    """Run unit tests"""
    cmd = "pytest tests/unit"
    if verbose:
        cmd += " -v"
    cmd += " --cov=backend/src --cov-report=term --cov-report=html"
    return run_command(cmd, "Unit Tests")


def run_integration_tests(verbose=False):
    """Run integration tests"""
    cmd = "pytest tests/integration"
    if verbose:
        cmd += " -v"
    cmd += " --cov=backend/src --cov-append --cov-report=term"
    return run_command(cmd, "Integration Tests")


def run_all_tests(verbose=False):
    """Run all tests"""
    cmd = "pytest tests/"
    if verbose:
        cmd += " -v"
    cmd += " --cov=backend/src --cov-report=term --cov-report=html --cov-report=xml"
    return run_command(cmd, "All Tests")


def run_linting():
    """Run code linting"""
    results = []
    
    # Flake8
    results.append(run_command(
        "flake8 backend/src --count --statistics",
        "Flake8 Linting"
    ))
    
    # Pylint
    results.append(run_command(
        "pylint backend/src --exit-zero",
        "Pylint Analysis"
    ))
    
    return all(results)


def run_formatting_check():
    """Check code formatting"""
    results = []
    
    # Black
    results.append(run_command(
        "black --check backend/src",
        "Black Formatting Check"
    ))
    
    # isort
    results.append(run_command(
        "isort --check-only backend/src",
        "Import Sorting Check"
    ))
    
    return all(results)


def run_type_checking():
    """Run type checking"""
    return run_command(
        "mypy backend/src --ignore-missing-imports",
        "Type Checking (mypy)"
    ))


def run_security_scan():
    """Run security scanning"""
    results = []
    
    # Bandit
    results.append(run_command(
        "bandit -r backend/src -f screen",
        "Security Scan (Bandit)"
    ))
    
    # Safety
    results.append(run_command(
        "safety check --json || true",
        "Dependency Security Check (Safety)"
    ))
    
    return all(results)


def run_coverage_report():
    """Generate coverage report"""
    return run_command(
        "coverage report --show-missing",
        "Coverage Report"
    )


def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Run tests for GitHub Bug Detection System")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "all", "lint", "format", "type", "security", "coverage"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick tests only (unit tests)"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run full test suite including quality checks"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("GitHub Bug Detection System - Test Runner")
    print("="*80)
    
    results = []
    
    if args.quick:
        results.append(run_unit_tests(args.verbose))
    elif args.full:
        results.append(run_all_tests(args.verbose))
        results.append(run_linting())
        results.append(run_formatting_check())
        results.append(run_type_checking())
        results.append(run_security_scan())
        results.append(run_coverage_report())
    else:
        if args.type == "unit":
            results.append(run_unit_tests(args.verbose))
        elif args.type == "integration":
            results.append(run_integration_tests(args.verbose))
        elif args.type == "all":
            results.append(run_all_tests(args.verbose))
        elif args.type == "lint":
            results.append(run_linting())
        elif args.type == "format":
            results.append(run_formatting_check())
        elif args.type == "type":
            results.append(run_type_checking())
        elif args.type == "security":
            results.append(run_security_scan())
        elif args.type == "coverage":
            results.append(run_coverage_report())
    
    # Summary
    print("\n" + "="*80)
    print("Test Summary")
    print("="*80)
    
    if all(results):
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
