"""
Unit tests for the response standardization module.
Tests success, error, and paginated response structures.
"""

import pytest
import sys
import os
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from responses import APIResponse, json_response


class TestAPIResponse:
    """Tests for APIResponse class."""
    
    def test_success_structure(self):
        """Test success response structure."""
        data = {"id": 1, "name": "test"}
        resp = APIResponse.success(data=data)
        
        assert resp["status"] == "success"
        assert resp["code"] == 200
        assert resp["data"] == data
        assert "timestamp" in resp
    
    def test_error_structure(self):
        """Test error response structure."""
        resp = APIResponse.error("Invalid input", code=400)
        
        assert resp["status"] == "error"
        assert resp["code"] == 400
        assert resp["message"] == "Invalid input"
        assert "data" not in resp
    
    def test_error_with_details(self):
        """Test error response with details."""
        details = {"field": "username", "error": "required"}
        resp = APIResponse.error(
            "Validation failed", 
            error_code="VALIDATION_ERROR",
            details=details
        )
        
        assert resp["details"] == details
        assert resp["error_code"] == "VALIDATION_ERROR"
    
    def test_paginated_response(self):
        """Test paginated response structure."""
        items = [1, 2, 3]
        resp = APIResponse.paginated(items, total=10, page=1, page_size=5)
        
        assert resp["data"] == items
        assert "meta" in resp
        pagination = resp["meta"]["pagination"]
        assert pagination["total"] == 10
        assert pagination["page"] == 1
        assert pagination["total_pages"] == 2
        assert pagination["has_next"] is True
        assert pagination["has_prev"] is False


class TestJSONHelper:
    """Tests for JSON conversion helper."""
    
    def test_json_conversion(self):
        """Test dictionary to JSON conversion."""
        resp = APIResponse.success(data={"key": "value"})
        json_str = json_response(resp)
        data = json.loads(json_str)
        
        assert data["status"] == "success"
        assert data["data"]["key"] == "value"
    
    def test_datetime_serialization(self):
        """Test datetime serialization in JSON."""
        now = datetime.now()
        resp = APIResponse.success(data={"time": now})
        json_str = json_response(resp)
        data = json.loads(json_str)
        
        assert isinstance(data["data"]["time"], str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
