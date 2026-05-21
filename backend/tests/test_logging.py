"""
Unit tests for the logging configuration module.
Tests JSON formatting, context tracking, and logger configuration.
"""

import pytest
import sys
import os
import json
import logging
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from logging_config import (
    setup_logging,
    JSONFormatter,
    set_context,
    clear_context,
    get_logger
)


class TestJSONFormatter:
    """Tests for JSONFormatter class."""
    
    def test_format_log_entry(self):
        """Test formatting a basic log entry."""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        json_str = formatter.format(record)
        data = json.loads(json_str)
        
        assert data["message"] == "Test message"
        assert data["level"] == "INFO"
        assert data["logger"] == "test_logger"
        assert "timestamp" in data
    
    def test_format_with_context(self):
        """Test formatting with thread context."""
        formatter = JSONFormatter()
        set_context({"request_id": "123", "user_id": "user_456"})
        
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="Context message",
            args=(),
            exc_info=None
        )
        
        json_str = formatter.format(record)
        data = json.loads(json_str)
        
        assert data["request_id"] == "123"
        assert data["user_id"] == "user_456"
        
        clear_context()
    
    def test_format_with_exception(self):
        """Test formatting with exception info."""
        formatter = JSONFormatter()
        try:
            raise ValueError("Test error")
        except ValueError:
            exc_info = sys.exc_info()
            
        record = logging.LogRecord(
            name="test_logger",
            level=logging.ERROR,
            pathname=__file__,
            lineno=10,
            msg="Error occurred",
            args=(),
            exc_info=exc_info
        )
        
        json_str = formatter.format(record)
        data = json.loads(json_str)
        
        assert "exception" in data
        assert "ValueError: Test error" in data["exception"]


class TestLoggingSetup:
    """Tests for logging setup configuration."""
    
    @pytest.fixture
    def log_dir(self):
        """Create temp log directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_setup_logging_creates_files(self, log_dir):
        """Test logging setup creates log files."""
        setup_logging(log_dir=log_dir)
        
        logger = get_logger("test_setup")
        logger.info("Test log")
        logger.error("Test error")
        
        assert os.path.exists(os.path.join(log_dir, "app.log"))
        assert os.path.exists(os.path.join(log_dir, "error.log"))
    
    def test_setup_logging_json_format(self, log_dir):
        """Test logging setup uses JSON format."""
        setup_logging(log_dir=log_dir, json_format=True)
        
        logger = get_logger("test_json")
        logger.info("JSON log")
        
        # Flush handlers
        for handler in logging.getLogger().handlers:
            handler.flush()
            
        with open(os.path.join(log_dir, "app.log"), 'r') as f:
            line = f.readline()
            data = json.loads(line)
            assert data["message"] == "JSON log"


class TestContextHelpers:
    """Tests for context helper functions."""
    
    def test_set_and_clear_context(self):
        """Test setting and clearing context."""
        context = {"key": "value"}
        set_context(context)
        
        # Verify context is set (implementation detail check)
        from logging_config import _local_context
        assert _local_context.context == context
        
        clear_context()
        assert not hasattr(_local_context, "context")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
