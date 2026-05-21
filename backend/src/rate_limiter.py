"""
Rate limiting utilities for the GitHub Bug Detection API.
Provides request throttling and abuse prevention mechanisms.
"""

import time
from collections import defaultdict
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta
import threading


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, message: str, retry_after: int = 60):
        self.message = message
        self.retry_after = retry_after
        super().__init__(self.message)


class TokenBucket:
    """
    Token bucket algorithm implementation for rate limiting.
    
    Allows burst traffic while maintaining an average rate limit.
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket.
        
        Args:
            capacity: Maximum number of tokens in the bucket
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self._lock = threading.Lock()
    
    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from the bucket.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens were consumed, False if not enough tokens
        """
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def get_wait_time(self, tokens: int = 1) -> float:
        """
        Calculate wait time until tokens are available.
        
        Args:
            tokens: Number of tokens needed
            
        Returns:
            Seconds to wait, 0 if tokens available now
        """
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                return 0
            tokens_needed = tokens - self.tokens
            return tokens_needed / self.refill_rate


class RateLimiter:
    """
    Rate limiter for tracking and limiting requests per client.
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        burst_capacity: int = 10
    ):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Maximum requests per minute per client
            requests_per_hour: Maximum requests per hour per client
            burst_capacity: Allow burst traffic up to this amount
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.burst_capacity = burst_capacity
        
        # Track requests per client
        self._minute_counts: Dict[str, list] = defaultdict(list)
        self._hour_counts: Dict[str, list] = defaultdict(list)
        self._buckets: Dict[str, TokenBucket] = {}
        self._lock = threading.Lock()
    
    def _cleanup_old_requests(self, client_id: str):
        """Remove expired request timestamps."""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        
        # Clean minute counts
        self._minute_counts[client_id] = [
            ts for ts in self._minute_counts[client_id]
            if ts > minute_ago
        ]
        
        # Clean hour counts
        self._hour_counts[client_id] = [
            ts for ts in self._hour_counts[client_id]
            if ts > hour_ago
        ]
    
    def _get_bucket(self, client_id: str) -> TokenBucket:
        """Get or create token bucket for client."""
        if client_id not in self._buckets:
            self._buckets[client_id] = TokenBucket(
                capacity=self.burst_capacity,
                refill_rate=self.requests_per_minute / 60
            )
        return self._buckets[client_id]
    
    def check_limit(self, client_id: str) -> Tuple[bool, Optional[int]]:
        """
        Check if request is allowed for client.
        
        Args:
            client_id: Unique identifier for the client (e.g., IP address)
            
        Returns:
            Tuple of (is_allowed, retry_after_seconds)
        """
        with self._lock:
            self._cleanup_old_requests(client_id)
            
            # Check minute limit
            if len(self._minute_counts[client_id]) >= self.requests_per_minute:
                oldest = min(self._minute_counts[client_id])
                retry_after = 60 - (datetime.now() - oldest).seconds
                return False, max(1, retry_after)
            
            # Check hour limit
            if len(self._hour_counts[client_id]) >= self.requests_per_hour:
                oldest = min(self._hour_counts[client_id])
                retry_after = 3600 - (datetime.now() - oldest).seconds
                return False, max(1, retry_after)
            
            # Check token bucket for burst control
            bucket = self._get_bucket(client_id)
            if not bucket.consume():
                wait_time = bucket.get_wait_time()
                return False, max(1, int(wait_time))
            
            return True, None
    
    def record_request(self, client_id: str):
        """
        Record a request from a client.
        
        Args:
            client_id: Unique identifier for the client
        """
        with self._lock:
            now = datetime.now()
            self._minute_counts[client_id].append(now)
            self._hour_counts[client_id].append(now)
    
    def get_remaining(self, client_id: str) -> Dict[str, int]:
        """
        Get remaining request counts for a client.
        
        Args:
            client_id: Unique identifier for the client
            
        Returns:
            Dictionary with remaining counts
        """
        with self._lock:
            self._cleanup_old_requests(client_id)
            
            minute_remaining = max(0, self.requests_per_minute - len(self._minute_counts[client_id]))
            hour_remaining = max(0, self.requests_per_hour - len(self._hour_counts[client_id]))
            
            return {
                "minute_remaining": minute_remaining,
                "hour_remaining": hour_remaining,
                "minute_limit": self.requests_per_minute,
                "hour_limit": self.requests_per_hour
            }
    
    def reset(self, client_id: str):
        """
        Reset rate limit counts for a client.
        
        Args:
            client_id: Unique identifier for the client
        """
        with self._lock:
            self._minute_counts[client_id] = []
            self._hour_counts[client_id] = []
            if client_id in self._buckets:
                del self._buckets[client_id]


# Global rate limiter instance
_global_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    global _global_limiter
    if _global_limiter is None:
        _global_limiter = RateLimiter()
    return _global_limiter


def check_rate_limit(client_id: str) -> Tuple[bool, Optional[int]]:
    """
    Convenience function to check rate limit.
    
    Args:
        client_id: Unique identifier for the client
        
    Returns:
        Tuple of (is_allowed, retry_after_seconds)
    """
    limiter = get_rate_limiter()
    return limiter.check_limit(client_id)
