"""
Unit tests for the rate_limiter module.
Tests rate limiting functionality including token bucket algorithm.
"""

import pytest
import sys
import os
import time
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rate_limiter import (
    TokenBucket,
    RateLimiter,
    RateLimitExceeded,
    get_rate_limiter,
    check_rate_limit
)


class TestTokenBucket:
    """Tests for TokenBucket class."""
    
    def test_initial_capacity(self):
        """Test bucket starts with full capacity."""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)
        assert bucket.tokens == 10
    
    def test_consume_tokens(self):
        """Test consuming tokens from bucket."""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)
        assert bucket.consume(5) is True
        assert bucket.tokens == 5
    
    def test_consume_fails_when_empty(self):
        """Test consume fails when not enough tokens."""
        bucket = TokenBucket(capacity=5, refill_rate=1.0)
        assert bucket.consume(5) is True
        assert bucket.consume(1) is False
    
    def test_consume_single_token(self):
        """Test consuming single token."""
        bucket = TokenBucket(capacity=3, refill_rate=1.0)
        assert bucket.consume() is True
        assert bucket.consume() is True
        assert bucket.consume() is True
        assert bucket.consume() is False
    
    def test_get_wait_time_when_available(self):
        """Test wait time is 0 when tokens available."""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)
        assert bucket.get_wait_time(5) == 0
    
    def test_get_wait_time_when_depleted(self):
        """Test wait time calculation when tokens depleted."""
        bucket = TokenBucket(capacity=5, refill_rate=1.0)
        bucket.consume(5)
        wait_time = bucket.get_wait_time(2)
        assert wait_time > 0
        assert wait_time <= 2


class TestRateLimiter:
    """Tests for RateLimiter class."""
    
    def test_allows_initial_request(self):
        """Test first request is allowed."""
        limiter = RateLimiter(requests_per_minute=60, requests_per_hour=1000)
        is_allowed, retry_after = limiter.check_limit("client1")
        assert is_allowed is True
        assert retry_after is None
    
    def test_record_request(self):
        """Test recording a request."""
        limiter = RateLimiter(requests_per_minute=60, requests_per_hour=1000)
        limiter.record_request("client1")
        remaining = limiter.get_remaining("client1")
        assert remaining["minute_remaining"] == 59
    
    def test_get_remaining_counts(self):
        """Test getting remaining request counts."""
        limiter = RateLimiter(requests_per_minute=60, requests_per_hour=1000)
        remaining = limiter.get_remaining("new_client")
        assert remaining["minute_remaining"] == 60
        assert remaining["hour_remaining"] == 1000
        assert remaining["minute_limit"] == 60
        assert remaining["hour_limit"] == 1000
    
    def test_reset_client(self):
        """Test resetting a client's limits."""
        limiter = RateLimiter(requests_per_minute=60, requests_per_hour=1000)
        limiter.record_request("client1")
        limiter.record_request("client1")
        limiter.reset("client1")
        remaining = limiter.get_remaining("client1")
        assert remaining["minute_remaining"] == 60
    
    def test_separate_clients(self):
        """Test that different clients have separate limits."""
        limiter = RateLimiter(requests_per_minute=60, requests_per_hour=1000)
        limiter.record_request("client1")
        limiter.record_request("client1")
        remaining1 = limiter.get_remaining("client1")
        remaining2 = limiter.get_remaining("client2")
        assert remaining1["minute_remaining"] == 58
        assert remaining2["minute_remaining"] == 60
    
    def test_minute_limit_exceeded(self):
        """Test minute limit being exceeded."""
        limiter = RateLimiter(requests_per_minute=3, requests_per_hour=1000, burst_capacity=10)
        
        for _ in range(3):
            limiter.record_request("client1")
        
        is_allowed, retry_after = limiter.check_limit("client1")
        assert is_allowed is False
        assert retry_after is not None
        assert retry_after > 0


class TestRateLimitExceeded:
    """Tests for RateLimitExceeded exception."""
    
    def test_exception_message(self):
        """Test exception contains message."""
        exc = RateLimitExceeded("Rate limit exceeded")
        assert exc.message == "Rate limit exceeded"
    
    def test_exception_retry_after(self):
        """Test exception contains retry_after."""
        exc = RateLimitExceeded("Rate limit exceeded", retry_after=120)
        assert exc.retry_after == 120
    
    def test_default_retry_after(self):
        """Test default retry_after value."""
        exc = RateLimitExceeded("Rate limit exceeded")
        assert exc.retry_after == 60


class TestGlobalRateLimiter:
    """Tests for global rate limiter functions."""
    
    def test_get_rate_limiter_returns_instance(self):
        """Test get_rate_limiter returns a RateLimiter."""
        limiter = get_rate_limiter()
        assert isinstance(limiter, RateLimiter)
    
    def test_check_rate_limit_function(self):
        """Test check_rate_limit convenience function."""
        is_allowed, retry_after = check_rate_limit("test_client_unique_123")
        assert is_allowed is True
        assert retry_after is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
