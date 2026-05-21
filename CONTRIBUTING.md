# Contributing to GitHub Bug Detection System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- Git
- GitHub account

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/github-bug-detection.git
   cd github-bug-detection
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/nomanqadri34/github-bug-detection.git
   ```

## Development Setup

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Install Development Tools

```bash
pip install pre-commit pytest pytest-cov black flake8 pylint isort mypy
pre-commit install
```

## Making Changes

### Branch Naming Convention

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications

Example: `feature/add-code-analysis` or `bugfix/fix-oauth-redirect`

### Commit Message Guidelines

Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(analyzer): add support for TypeScript analysis

fix(api): resolve OAuth callback redirect issue

docs(readme): update installation instructions

test(predictor): add unit tests for risk calculation
```

### Code Style

#### Python

- Follow PEP 8 style guide
- Use Black for code formatting (line length: 127)
- Use isort for import sorting
- Maximum line length: 127 characters
- Use type hints where appropriate

```python
def calculate_risk_score(file_data: dict) -> float:
    """
    Calculate risk score for a file.
    
    Args:
        file_data: Dictionary containing file metrics
        
    Returns:
        Risk score between 0 and 1
    """
    # Implementation
    pass
```

#### JavaScript/React

- Use ES6+ syntax
- Use functional components with hooks
- Follow Airbnb JavaScript Style Guide
- Use meaningful variable names
- Add JSDoc comments for complex functions

```javascript
/**
 * Analyze repository and display results
 * @param {string} repoUrl - GitHub repository URL
 * @returns {Promise<Object>} Analysis results
 */
const analyzeRepository = async (repoUrl) => {
  // Implementation
};
```

## Testing

### Running Tests

#### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend/src --cov-report=html

# Run specific test file
pytest tests/unit/test_predictor.py

# Run specific test
pytest tests/unit/test_predictor.py::TestBugPredictor::test_extract_features_basic

# Run tests by marker
pytest -m unit
pytest -m integration
```

#### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

### Writing Tests

#### Unit Tests

```python
import pytest

class TestFeature:
    def test_basic_functionality(self):
        """Test basic functionality"""
        result = my_function(input_data)
        assert result == expected_output
        
    def test_edge_case(self):
        """Test edge case handling"""
        with pytest.raises(ValueError):
            my_function(invalid_input)
```

#### Integration Tests

```python
from fastapi.testclient import TestClient

def test_api_endpoint(client):
    """Test API endpoint"""
    response = client.post("/api/endpoint", json=payload)
    assert response.status_code == 200
    assert "expected_key" in response.json()
```

### Test Coverage Requirements

- Minimum 80% code coverage for new code
- All new features must include tests
- Bug fixes should include regression tests

## Code Quality

### Pre-commit Hooks

Pre-commit hooks run automatically before each commit:

- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON validation
- Black formatting
- isort import sorting
- Flake8 linting
- Mypy type checking
- Bandit security scanning

### Manual Quality Checks

```bash
# Format code
black backend/src
isort backend/src

# Lint code
flake8 backend/src
pylint backend/src

# Type checking
mypy backend/src

# Security scan
bandit -r backend/src
```

## Submitting Changes

### Pull Request Process

1. **Update your fork:**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes:**
   - Write code
   - Add tests
   - Update documentation

4. **Run tests and quality checks:**
   ```bash
   pytest
   black backend/src
   flake8 backend/src
   ```

5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request:**
   - Go to GitHub and create a PR from your fork
   - Fill out the PR template
   - Link related issues

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing
- [ ] Coverage maintained/improved

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

## Review Process

### What Reviewers Look For

1. **Code Quality:**
   - Follows style guidelines
   - Well-structured and readable
   - Appropriate comments and documentation

2. **Testing:**
   - Adequate test coverage
   - Tests are meaningful and comprehensive
   - Edge cases covered

3. **Functionality:**
   - Solves the intended problem
   - No unintended side effects
   - Performance considerations

4. **Documentation:**
   - README updated if needed
   - API documentation current
   - Comments explain "why" not "what"

### Addressing Review Comments

- Respond to all comments
- Make requested changes
- Push updates to the same branch
- Request re-review when ready

### Merge Criteria

- All CI checks passing
- At least one approval from maintainer
- No unresolved conversations
- Up to date with main branch

## Additional Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Writing Good Commit Messages](https://chris.beams.io/posts/git-commit/)

## Questions?

If you have questions, please:
- Check existing issues and discussions
- Create a new issue with the "question" label
- Reach out to maintainers

Thank you for contributing! 🎉
