"""
Unit tests for predictor module
"""
import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_path))


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
        
    def test_extract_features_bug_keywords(self):
        """Test bug keyword detection in commits"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        commit_data = {
            "commits": [
                {
                    "sha": "abc123",
                    "message": "fix: critical bug in authentication",
                    "files": [{"filename": "auth.py", "additions": 10, "deletions": 5}]
                },
                {
                    "sha": "def456",
                    "message": "hotfix: patch security vulnerability",
                    "files": [{"filename": "auth.py", "additions": 3, "deletions": 2}]
                }
            ]
        }
        
        features = predictor.extract_features(commit_data)
        auth_file = next((f for f in features["files"] if f["file"] == "auth.py"), None)
        
        assert auth_file is not None
        assert auth_file["bug_keywords"] >= 2
        
    def test_extract_features_commit_frequency(self):
        """Test commit frequency calculation"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        commit_data = {
            "commits": [
                {"sha": f"sha{i}", "message": "update", "files": [{"filename": "test.py"}]}
                for i in range(5)
            ]
        }
        
        features = predictor.extract_features(commit_data)
        test_file = next((f for f in features["files"] if f["file"] == "test.py"), None)
        
        assert test_file is not None
        assert test_file["commit_frequency"] == 5
        
    def test_extract_features_complexity(self):
        """Test complexity score calculation"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        commit_data = {
            "commits": [
                {
                    "sha": "abc123",
                    "message": "update",
                    "files": [{"filename": "complex.py", "additions": 100, "deletions": 50, "changes": 150}]
                }
            ]
        }
        
        features = predictor.extract_features(commit_data)
        complex_file = next((f for f in features["files"] if f["file"] == "complex.py"), None)
        
        assert complex_file is not None
        assert complex_file["complexity"] > 0
        assert complex_file["complexity"] <= 1.0
        
    def test_calculate_risk_score(self):
        """Test risk score calculation"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        file_features = {
            "bug_keywords": 5,
            "commit_frequency": 10,
            "complexity": 0.8
        }
        
        risk_score = predictor.calculate_risk_score(file_features)
        
        assert isinstance(risk_score, float)
        assert 0 <= risk_score <= 1.0
        
    def test_calculate_risk_score_high_risk(self):
        """Test high risk score calculation"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        file_features = {
            "bug_keywords": 10,
            "commit_frequency": 20,
            "complexity": 0.9
        }
        
        risk_score = predictor.calculate_risk_score(file_features)
        
        assert risk_score > 0.7
        
    def test_calculate_risk_score_low_risk(self):
        """Test low risk score calculation"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        file_features = {
            "bug_keywords": 0,
            "commit_frequency": 1,
            "complexity": 0.1
        }
        
        risk_score = predictor.calculate_risk_score(file_features)
        
        assert risk_score < 0.3
        
    def test_generate_reason_high_risk(self):
        """Test reason generation for high risk files"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        file_features = {
            "bug_keywords": 8,
            "commit_frequency": 15,
            "complexity": 0.85
        }
        
        reason = predictor.generate_reason(file_features)
        
        assert isinstance(reason, str)
        assert len(reason) > 0
        assert any(keyword in reason.lower() for keyword in ["bug", "commit", "complex"])
        
    def test_predict_with_empty_data(self):
        """Test prediction with empty commit data"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        result = predictor.predict({"commits": []})
        
        assert result["overall_repository_risk"] == 0
        assert len(result["modules"]) == 0
        
    def test_predict_with_valid_data(self, sample_commit_data):
        """Test prediction with valid commit data"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        result = predictor.predict(sample_commit_data)
        
        assert "repository_name" in result
        assert "overall_repository_risk" in result
        assert "modules" in result
        assert isinstance(result["modules"], list)
        
    def test_predict_sorts_by_risk(self):
        """Test that predictions are sorted by risk score"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        commit_data = {
            "commits": [
                {
                    "sha": "1",
                    "message": "fix bug",
                    "files": [{"filename": "high_risk.py", "additions": 100, "deletions": 50}]
                },
                {
                    "sha": "2",
                    "message": "update docs",
                    "files": [{"filename": "low_risk.py", "additions": 5, "deletions": 1}]
                }
            ]
        }
        
        result = predictor.predict(commit_data)
        
        if len(result["modules"]) > 1:
            for i in range(len(result["modules"]) - 1):
                assert result["modules"][i]["risk_score"] >= result["modules"][i + 1]["risk_score"]
                
    def test_normalize_score(self):
        """Test score normalization"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        
        assert predictor.normalize_score(0) == 0.0
        assert predictor.normalize_score(100) == 1.0
        assert 0 <= predictor.normalize_score(50) <= 1.0
        
    def test_extract_features_handles_missing_fields(self):
        """Test feature extraction with missing fields"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        commit_data = {
            "commits": [
                {
                    "sha": "abc123",
                    "message": "update",
                    "files": [{"filename": "test.py"}]  # Missing additions/deletions
                }
            ]
        }
        
        features = predictor.extract_features(commit_data)
        
        assert isinstance(features, dict)
        assert "files" in features
        
    def test_calculate_overall_risk(self):
        """Test overall repository risk calculation"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        modules = [
            {"risk_score": 0.8},
            {"risk_score": 0.6},
            {"risk_score": 0.4}
        ]
        
        overall_risk = predictor.calculate_overall_risk(modules)
        
        assert isinstance(overall_risk, float)
        assert 0 <= overall_risk <= 1.0
        assert overall_risk > 0.4  # Should be influenced by high risk files
        
    def test_filter_low_risk_files(self):
        """Test filtering of low risk files"""
        from predictor import BugPredictor
        
        predictor = BugPredictor()
        modules = [
            {"file": "high.py", "risk_score": 0.8},
            {"file": "low.py", "risk_score": 0.1},
            {"file": "medium.py", "risk_score": 0.5}
        ]
        
        filtered = predictor.filter_low_risk_files(modules, threshold=0.3)
        
        assert len(filtered) == 2
        assert all(m["risk_score"] >= 0.3 for m in filtered)
