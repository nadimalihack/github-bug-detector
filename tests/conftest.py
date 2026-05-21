"""
Pytest configuration and shared fixtures
"""
import pytest
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_path))

@pytest.fixture
def sample_commit_data():
    """Sample commit data for testing"""
    return {
        "commits": [
            {
                "sha": "abc123",
                "message": "fix: critical bug in authentication",
                "author": "test_user",
                "date": "2024-01-15T10:30:00Z",
                "files": [
                    {
                        "filename": "auth.py",
                        "additions": 10,
                        "deletions": 5,
                        "changes": 15
                    }
                ]
            },
            {
                "sha": "def456",
                "message": "feat: add new feature",
                "author": "test_user",
                "date": "2024-01-16T14:20:00Z",
                "files": [
                    {
                        "filename": "feature.py",
                        "additions": 50,
                        "deletions": 2,
                        "changes": 52
                    }
                ]
            }
        ]
    }

@pytest.fixture
def sample_repository_data():
    """Sample repository data for testing"""
    return {
        "name": "test/repo",
        "description": "Test repository",
        "language": "Python",
        "stars": 100,
        "forks": 20,
        "open_issues": 5
    }

@pytest.fixture
def sample_code_snippet():
    """Sample code for analysis"""
    return """
def authenticate_user(username, password):
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)
    return result

def process_data(data):
    # Hardcoded credentials
    api_key = "sk_test_1234567890"
    response = requests.get(f"https://api.example.com/data?key={api_key}")
    return response.json()
"""

@pytest.fixture
def mock_github_token():
    """Mock GitHub token for testing"""
    return "ghp_test_token_1234567890"

@pytest.fixture
def sample_bug_patterns():
    """Sample bug patterns for ML testing"""
    return [
        {"file": "auth.py", "bug_keywords": 5, "commit_frequency": 10, "complexity": 0.7, "has_bug": 1},
        {"file": "utils.py", "bug_keywords": 1, "commit_frequency": 2, "complexity": 0.3, "has_bug": 0},
        {"file": "api.py", "bug_keywords": 3, "commit_frequency": 8, "complexity": 0.6, "has_bug": 1},
        {"file": "models.py", "bug_keywords": 0, "commit_frequency": 1, "complexity": 0.2, "has_bug": 0},
    ]

@pytest.fixture
def sample_analysis_result():
    """Sample analysis result"""
    return {
        "repository_name": "test/repo",
        "overall_repository_risk": 0.65,
        "total_files_analyzed": 10,
        "high_risk_files": 3,
        "modules": [
            {
                "file": "auth.py",
                "risk_score": 0.85,
                "reason": "High frequency of bug-related commits",
                "recommendations": ["Add input validation", "Implement rate limiting"]
            },
            {
                "file": "api.py",
                "risk_score": 0.72,
                "reason": "Complex authentication logic",
                "recommendations": ["Add unit tests", "Refactor large functions"]
            }
        ]
    }

@pytest.fixture
def temp_model_file(tmp_path):
    """Create temporary model file"""
    model_file = tmp_path / "test_model.pkl"
    return str(model_file)

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("GITHUB_TOKEN", "test_token")
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini_key")
    monkeypatch.setenv("MONGODB_URI", "mongodb://localhost:27017")
    monkeypatch.setenv("JWT_SECRET", "test_secret")
    monkeypatch.setenv("FRONTEND_URL", "http://localhost:3000")

@pytest.fixture
def api_client():
    """FastAPI test client"""
    from fastapi.testclient import TestClient
    try:
        from api import app
        return TestClient(app)
    except ImportError:
        pytest.skip("API module not available")
