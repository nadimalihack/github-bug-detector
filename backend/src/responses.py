"""
Response standardization utilities for the GitHub Bug Detection API.
Provides consistent response structures for success and error cases.
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import json


class APIResponse:
    """Standardized API response generator."""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Operation successful",
        code: int = 200,
        meta: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate success response.
        
        Args:
            data: Response payload
            message: Success message
            code: HTTP status code
            meta: Metadata (pagination, etc.)
            
        Returns:
            Standardized response dictionary
        """
        response = {
            "status": "success",
            "code": code,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": data
        }
        
        if meta:
            response["meta"] = meta
            
        return response
    
    @staticmethod
    def error(
        message: str,
        code: int = 400,
        error_code: Optional[str] = None,
        details: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Generate error response.
        
        Args:
            message: Error message
            code: HTTP status code
            error_code: Application specific error code
            details: detailed error validation messages
            
        Returns:
            Standardized error response dictionary
        """
        response = {
            "status": "error",
            "code": code,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        if error_code:
            response["error_code"] = error_code
            
        if details:
            response["details"] = details
            
        return response
    
    @staticmethod
    def paginated(
        items: List[Any],
        total: int,
        page: int,
        page_size: int,
        message: str = "Data retrieved successfully"
    ) -> Dict[str, Any]:
        """
        Generate paginated success response.
        
        Args:
            items: List of items for current page
            total: Total number of items
            page: Current page number
            page_size: Number of items per page
            message: Success message
            
        Returns:
            Standardized paginated response
        """
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        
        meta = {
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }
        
        return APIResponse.success(
            data=items,
            message=message,
            meta=meta
        )


def json_response(response_dict: Dict[str, Any]) -> str:
    """
    Convert dictionary response to JSON string.
    
    Args:
        response_dict: Response dictionary from APIResponse methods
        
    Returns:
        JSON string
    """
    return json.dumps(response_dict, default=str)
