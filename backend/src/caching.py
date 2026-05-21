"""
Caching utilities for the GitHub Bug Detection API.
Provides in-memory caching with expiration for expensive operations.
"""

import time
import threading
from typing import Any, Dict, Optional, Tuple, TypeVar, Generic
from collections import OrderedDict

T = TypeVar('T')


class CacheEntry(Generic[T]):
    """Wrapper for cached values with timestamp."""
    def __init__(self, value: T, ttl: int):
        self.value = value
        self.expires_at = time.time() + ttl


class LRUCache:
    """
    Least Recently Used (LRU) cache implementation with TTL support.
    Thread-safe implementation for storing results of expensive operations.
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        """
        Initialize the cache.
        
        Args:
            max_size: Maximum number of items in cache
            default_ttl: Default time-to-live in seconds
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.Lock()
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            if key not in self._cache:
                self.misses += 1
                return None
            
            entry = self._cache[key]
            
            # Check expiration
            if time.time() > entry.expires_at:
                del self._cache[key]
                self.misses += 1
                return None
            
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            self.hits += 1
            return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Store value in cache.
        
        Args:
            key: Cache key
            value: Value to store
            ttl: Time-to-live in seconds (optional)
        """
        with self._lock:
            # Evict if full and new key
            if len(self._cache) >= self.max_size and key not in self._cache:
                self._cache.popitem(last=False)
                self.evictions += 1
            
            # Create entry
            ttl = ttl if ttl is not None else self.default_ttl
            self._cache[key] = CacheEntry(value, ttl)
            self._cache.move_to_end(key)
    
    def invalidate(self, key: str):
        """
        Remove item from cache.
        
        Args:
            key: Cache key
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    def clear(self):
        """Clear all items from cache."""
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0
            self.evictions = 0
    
    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        with self._lock:
            total = self.hits + self.misses
            hit_ratio = (self.hits / total) if total > 0 else 0
            
            return {
                "hits": self.hits,
                "misses": self.misses,
                "evictions": self.evictions,
                "size": len(self._cache),
                "max_size": self.max_size,
                "hit_ratio": float(f"{hit_ratio:.2f}")
            }


# Global cache instances
_repo_cache: Optional[LRUCache] = None
_analysis_cache: Optional[LRUCache] = None


def get_repo_cache() -> LRUCache:
    """Get cache for repository metadata."""
    global _repo_cache
    if _repo_cache is None:
        _repo_cache = LRUCache(max_size=5000, default_ttl=3600)  # 1 hour
    return _repo_cache


def get_analysis_cache() -> LRUCache:
    """Get cache for analysis results."""
    global _analysis_cache
    if _analysis_cache is None:
        _analysis_cache = LRUCache(max_size=1000, default_ttl=7200)  # 2 hours
    return _analysis_cache


def cache_key(*args) -> str:
    """Generate a cache key from arguments."""
    return ":".join(str(arg) for arg in args)
