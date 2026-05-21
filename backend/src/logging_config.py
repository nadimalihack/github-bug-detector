"""
Logging configuration for the GitHub Bug Detection API.
Provides structured logging with context tracking and file rotation.
"""

import logging
import logging.handlers
import sys
import os
import json
import threading
from typing import Dict, Any, Optional
from datetime import datetime

# Global context storage
_local_context = threading.local()


class JSONFormatter(logging.Formatter):
    """Formatter that outputs JSON strings."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "path": record.pathname,
            "line": record.lineno,
            "process": record.process,
            "thread": record.threadName
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            
        # Add context if available
        if hasattr(_local_context, "context"):
            log_data.update(_local_context.context)
            
        # Add extra fields from record
        if hasattr(record, "extra"):
            log_data.update(record.extra)
            
        return json.dumps(log_data)


def set_context(context: Dict[str, Any]):
    """Set logging context for current thread."""
    _local_context.context = context


def clear_context():
    """Clear logging context for current thread."""
    if hasattr(_local_context, "context"):
        del _local_context.context


def setup_logging(
    log_dir: str = "logs",
    level: int = logging.INFO,
    json_format: bool = True
) -> logging.Logger:
    """
    Configure logging for the application.
    
    Args:
        log_dir: Directory to store log files
        level: Logging level
        json_format: Whether to use JSON formatting
        
    Returns:
        Configured root logger
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
        
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if json_format:
        console_handler.setFormatter(JSONFormatter())
    else:
        console_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
    root_logger.addHandler(console_handler)
    
    # File handler (rotating)
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    if json_format:
        file_handler.setFormatter(JSONFormatter())
    else:
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
    root_logger.addHandler(file_handler)
    
    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, "error.log"),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    if json_format:
        error_handler.setFormatter(JSONFormatter())
    else:
        error_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
    root_logger.addHandler(error_handler)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with valid configuration.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
