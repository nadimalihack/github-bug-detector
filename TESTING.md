# Testing Guide

Comprehensive testing guide for the GitHub Bug Detection System.

## Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Test Coverage](#test-coverage)
- [Continuous Integration](#continuous-integration)

## Overview

The project uses pytest as the primary testing framework with the following test types:

- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test interactions between components
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Test system performance and scalability

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_predictor.py
│   ├── test_code_analyzer.py
│   ├── test_github_analyzer.py
│   ├── test_trainer.py
│   ├── test_utils.py
│   ├── test_gemini_analyzer.py
│   ├── test_oauth_handler.py
│   └── test_mongodb_manager.py
└── integration/             # Integration tests
    ├── __init__.py
    └── test_api_endpoints.py
```

## Running Tests

### Quick Start

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend/src --cov-report=html

# Run specific test file
pytest tests/unit/test_predictor.py

# Run specific test
pytest tests/unit/test_predictor.py::TestBugPredictor::test_extract_features_basic
```

### Using Test Runner Script

```bash
# Run all tests
python run_tests.py

# Run unit tests only
python run_tests.py --type unit

# Run integration tests
python run_tests.py --type integration

# Run with verbose output
python run_tests.py --verbose

# Quick test (unit tests only)
python run_tests.py --quick

# Full test suite with quality checks
python run_tests.py --full
```

### Test Categories

```bash
# Run tests by marker
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only
pytest -m slow           # Slow tests only
pytest -m "not slow"     # Skip slow tests
```

### Parallel Testing

```bash
# Run tests in parallel (faster)
pytest -n auto

# Run with specific number of workers
pytest -n 4
```

## Writing Tests

### Unit Test Example

```python
import pytest
from unittest.mock import Mock, patch

class TestBugPredictor:
    """Test cases for BugPredictor class"""
    
    def test_extract_features_basic(self, sample_commit_data):
        """Test basic feature extraction from commit data"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        features = predictor.extract_features(sample_commit_data)
        
        assert isinstance(features, dict)
        assert "files" in features
        assert len(features["files"]) > 0
        
    @patch('github.Github')
    def test_with_mock(self, mock_github):
        """Test with mocked dependencies"""
        mock_github.return_value.get_repo.return_value = Mock()
        
        # Test implementation
        pass
```

### Integration Test Example

```python
from fastapi.testclient import TestClient

def test_analyze_github_url(client, sample_commit_data):
    """Test GitHub URL analysis endpoint"""
    payload = {
        "github_url": "facebook/react",
        "max_commits": 10
    }
    
    response = client.post("/analyze-github-url", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "overall_repository_risk" in data
    assert "modules" in data
```

### Using Fixtures

```python
@pytest.fixture
def sample_data():
    """Provide sample data for tests"""
    return {
        "key": "value",
        "items": [1, 2, 3]
    }

def test_with_fixture(sample_data):
    """Test using fixture"""
    assert sample_data["key"] == "value"
    assert len(sample_data["items"]) == 3
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("facebook/react", ("facebook", "react")),
    ("microsoft/vscode", ("microsoft", "vscode")),
    ("https://github.com/user/repo", ("user", "repo")),
])
def test_parse_github_url(input, expected):
    """Test URL parsing with multiple inputs"""
    result = parse_github_url(input)
    assert result == expected
```

### Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function"""
    result = await async_operation()
    assert result is not None
```

### Exception Testing

```python
def test_raises_exception():
    """Test that function raises expected exception"""
    with pytest.raises(ValueError):
        invalid_operation()
        
def test_exception_message():
    """Test exception message"""
    with pytest.raises(ValueError, match="Invalid input"):
        invalid_operation()
```

## Test Coverage

### Generating Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=backend/src --cov-report=html

# Generate terminal report
pytest --cov=backend/src --cov-report=term

# Generate XML report (for CI)
pytest --cov=backend/src --cov-report=xml

# Show missing lines
pytest --cov=backend/src --cov-report=term-missing
```

### Coverage Requirements

- Minimum 80% overall coverage
- New code should have 90%+ coverage
- Critical paths require 100% coverage

### Viewing Coverage Reports

```bash
# Open HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage Configuration

Coverage settings are in `.coveragerc`:

```ini
[run]
source = backend/src
omit = */tests/*, */test_*.py
branch = True

[report]
precision = 2
show_missing = True
skip_covered = False
```

## Code Quality Checks

### Linting

```bash
# Flake8
flake8 backend/src

# Pylint
pylint backend/src

# Both
python run_tests.py --type lint
```

### Formatting

```bash
# Check formatting
black --check backend/src
isort --check-only backend/src

# Auto-format
black backend/src
isort backend/src

# Check via test runner
python run_tests.py --type format
```

### Type Checking

```bash
# Run mypy
mypy backend/src --ignore-missing-imports

# Via test runner
python run_tests.py --type type
```

### Security Scanning

```bash
# Bandit security scan
bandit -r backend/src

# Safety dependency check
safety check

# Via test runner
python run_tests.py --type security
```

## Continuous Integration

### GitHub Actions Workflow

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Manual workflow dispatch

### CI Pipeline Stages

1. **Test** - Run unit and integration tests
2. **Lint** - Code quality checks
3. **Security** - Security scanning
4. **Coverage** - Generate coverage reports
5. **Build** - Build and validate application

### Local CI Simulation

```bash
# Run full CI pipeline locally
python run_tests.py --full

# Or manually
pytest --cov=backend/src --cov-report=xml
flake8 backend/src
black --check backend/src
mypy backend/src
bandit -r backend/src
```

## Best Practices

### Test Organization

- One test file per source file
- Group related tests in classes
- Use descriptive test names
- Keep tests focused and simple

### Test Naming

```python
# Good
def test_calculate_risk_score_with_high_values():
    pass

# Bad
def test1():
    pass
```

### Assertions

```python
# Use specific assertions
assert result == expected
assert len(items) == 5
assert "key" in dictionary

# Avoid generic assertions
assert result  # Too vague
```

### Mocking

```python
# Mock external dependencies
@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"data": "value"}
    result = fetch_data()
    assert result["data"] == "value"
```

### Test Data

```python
# Use fixtures for reusable test data
@pytest.fixture
def sample_user():
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }

# Use factories for complex objects
def create_commit(message="test", files=None):
    return {
        "message": message,
        "files": files or []
    }
```

## Debugging Tests

### Running Single Test

```bash
pytest tests/unit/test_predictor.py::TestBugPredictor::test_extract_features_basic -v
```

### Using pdb

```python
def test_debug():
    import pdb; pdb.set_trace()
    result = function_to_debug()
    assert result == expected
```

### Verbose Output

```bash
pytest -vv  # Very verbose
pytest -s   # Show print statements
pytest --tb=short  # Short traceback
```

### Failed Test Rerun

```bash
# Rerun only failed tests
pytest --lf

# Rerun failed tests first
pytest --ff
```

## Performance Testing

### Timing Tests

```python
import pytest

@pytest.mark.timeout(5)
def test_performance():
    """Test must complete within 5 seconds"""
    result = expensive_operation()
    assert result is not None
```

### Benchmarking

```bash
# Install pytest-benchmark
pip install pytest-benchmark

# Run benchmarks
pytest --benchmark-only
```

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure backend is in path
export PYTHONPATH="${PYTHONPATH}:${PWD}/backend/src"
```

**Database Tests:**
```bash
# Use test database
export MONGODB_URI="mongodb://localhost:27017/test_db"
```

**API Tests:**
```bash
# Ensure test client is properly configured
# Check conftest.py for client fixture
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Mocking Guide](https://docs.python.org/3/library/unittest.mock.html)
