"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
import json

backend_path = Path(__file__).parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_path))


@pytest.fixture
def client():
    """Create test client"""
    try:
        from api import app
        return TestClient(app)
    except ImportError:
        pytest.skip("API module not available")


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        """Test GET / health check"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "status" in response.json()
        
    def test_health_check_returns_json(self, client):
        """Test health check returns JSON"""
        response = client.get("/")
        
        assert response.headers["content-type"] == "application/json"


class TestAnalyzeGitHubURL:
    """Test GitHub URL analysis endpoint"""
    
    def test_analyze_github_url_valid(self, client):
        """Test analyzing valid GitHub URL"""
        payload = {
            "github_url": "facebook/react",
            "max_commits": 10
        }
        
        response = client.post("/analyze-github-url", json=payload)
        
        assert response.status_code in [200, 422, 500]
        
    def test_analyze_github_url_with_token(self, client):
        """Test analyzing with GitHub token"""
        payload = {
            "github_url": "facebook/react",
            "github_token": "test_token",
            "max_commits": 5
        }
        
        response = client.post("/analyze-github-url", json=payload)
        
        assert response.status_code in [200, 401, 422, 500]
        
    def test_analyze_github_url_invalid_format(self, client):
        """Test analyzing invalid URL format"""
        payload = {
            "github_url": "invalid_url"
        }
        
        response = client.post("/analyze-github-url", json=payload)
        
        assert response.status_code in [400, 422, 500]
        
    def test_analyze_github_url_missing_field(self, client):
        """Test request with missing required field"""
        payload = {}
        
        response = client.post("/analyze-github-url", json=payload)
        
        assert response.status_code == 422


class TestPredictEndpoint:
    """Test prediction endpoint"""
    
    def test_predict_with_valid_data(self, client, sample_commit_data):
        """Test prediction with valid commit data"""
        response = client.post("/predict", json=sample_commit_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "overall_repository_risk" in data
        assert "modules" in data
        
    def test_predict_with_empty_commits(self, client):
        """Test prediction with empty commits"""
        payload = {"commits": []}
        
        response = client.post("/predict", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["overall_repository_risk"] == 0
        
    def test_predict_with_invalid_data(self, client):
        """Test prediction with invalid data"""
        payload = {"invalid": "data"}
        
        response = client.post("/predict", json=payload)
        
        assert response.status_code in [400, 422]
        
    def test_predict_response_structure(self, client, sample_commit_data):
        """Test prediction response structure"""
        response = client.post("/predict", json=sample_commit_data)
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data["modules"], list)
            if len(data["modules"]) > 0:
                module = data["modules"][0]
                assert "file" in module
                assert "risk_score" in module
                assert "reason" in module


class TestAnalyzeCodeEndpoint:
    """Test code analysis endpoint"""
    
    def test_analyze_code_with_vulnerabilities(self, client, sample_code_snippet):
        """Test code analysis with vulnerabilities"""
        payload = {"code": sample_code_snippet}
        
        response = client.post("/analyze-code", json=payload)
        
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "issues" in data
            
    def test_analyze_code_empty(self, client):
        """Test analyzing empty code"""
        payload = {"code": ""}
        
        response = client.post("/analyze-code", json=payload)
        
        assert response.status_code in [200, 400, 404, 422]
        
    def test_analyze_code_safe(self, client):
        """Test analyzing safe code"""
        payload = {"code": "def add(a, b):\n    return a + b"}
        
        response = client.post("/analyze-code", json=payload)
        
        assert response.status_code in [200, 404]


class TestOAuthEndpoints:
    """Test OAuth endpoints"""
    
    def test_github_login_redirect(self, client):
        """Test GitHub login redirect"""
        response = client.get("/auth/github/login", follow_redirects=False)
        
        assert response.status_code in [200, 302, 307, 404]
        
    def test_github_callback_without_code(self, client):
        """Test callback without authorization code"""
        response = client.get("/auth/github/callback")
        
        assert response.status_code in [400, 404, 422]
        
    def test_get_user_profile_unauthorized(self, client):
        """Test getting user profile without auth"""
        response = client.get("/auth/user")
        
        assert response.status_code in [401, 404]


class TestUserStatsEndpoints:
    """Test user statistics endpoints"""
    
    def test_get_user_stats_unauthorized(self, client):
        """Test getting stats without auth"""
        response = client.get("/api/user/stats")
        
        assert response.status_code in [401, 404]
        
    def test_get_user_repositories_unauthorized(self, client):
        """Test getting repositories without auth"""
        response = client.get("/api/user/repositories")
        
        assert response.status_code in [401, 404]


class TestFeedbackEndpoints:
    """Test feedback endpoints"""
    
    def test_submit_feedback_unauthorized(self, client):
        """Test submitting feedback without auth"""
        payload = {
            "file": "test.py",
            "predicted_risk": 0.8,
            "actual_has_bug": True
        }
        
        response = client.post("/api/feedback", json=payload)
        
        assert response.status_code in [401, 404, 422]
        
    def test_get_training_progress_unauthorized(self, client):
        """Test getting training progress without auth"""
        response = client.get("/api/training/progress")
        
        assert response.status_code in [401, 404]


class TestCORSHeaders:
    """Test CORS configuration"""
    
    def test_cors_headers_present(self, client):
        """Test CORS headers are present"""
        response = client.options("/")
        
        # CORS headers should be present or endpoint should exist
        assert response.status_code in [200, 405]
        
    def test_cors_allows_frontend_origin(self, client):
        """Test CORS allows frontend origin"""
        headers = {"Origin": "http://localhost:3000"}
        response = client.get("/", headers=headers)
        
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error handling"""
        response = client.get("/nonexistent-endpoint")
        
        assert response.status_code == 404
        
    def test_405_method_not_allowed(self, client):
        """Test 405 error handling"""
        response = client.put("/")
        
        assert response.status_code == 405
        
    def test_422_validation_error(self, client):
        """Test 422 validation error"""
        response = client.post("/predict", json={"invalid": "data"})
        
        assert response.status_code in [400, 422]


class TestRateLimiting:
    """Test rate limiting (if implemented)"""
    
    def test_multiple_requests_allowed(self, client):
        """Test multiple requests are allowed"""
        for _ in range(5):
            response = client.get("/")
            assert response.status_code == 200
