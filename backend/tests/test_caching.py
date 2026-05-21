"""
Unit tests for the caching module.
Tests LRU cache implementation and expiration logic.
"""

import pytest
import sys
import os
import time
import threading

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from caching import (
    LRUCache,
    get_repo_cache,
    get_analysis_cache,
    cache_key
)


class TestLRUCache:
    """Tests for LRUCache class."""
    
    def test_set_and_get(self):
        """Test basic set and get operations."""
        cache = LRUCache(max_size=10)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        assert cache.get("key2") is None
    
    def test_expiration(self):
        """Test item expiration."""
        cache = LRUCache(max_size=10, default_ttl=1)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        
        # Wait for expiration
        time.sleep(1.1)
        assert cache.get("key1") is None
    
    def test_custom_ttl(self):
        """Test custom TTL per item."""
        cache = LRUCache(max_size=10, default_ttl=10)
        cache.set("short_lived", "value", ttl=1)
        assert cache.get("short_lived") == "value"
        
        time.sleep(1.1)
        assert cache.get("short_lived") is None
    
    def test_lru_eviction(self):
        """Test least recently used eviction."""
        cache = LRUCache(max_size=3)
        cache.set("k1", "v1")
        cache.set("k2", "v2")
        cache.set("k3", "v3")
        
        # Access k1 to make it recently used
        cache.get("k1")
        
        # Add one more items to force eviction
        # k2 should be evicted as it's the LRU item (k1 was just accessed)
        cache.set("k4", "v4")
        
        assert cache.get("k2") is None
        assert cache.get("k1") == "v1"
        assert cache.get("k3") == "v3"
        assert cache.get("k4") == "v4"
    
    def test_stats_tracking(self):
        """Test statistics tracking."""
        cache = LRUCache(max_size=10)
        cache.set("k1", "v1")
        
        cache.get("k1")  # Hit
        cache.get("k2")  # Miss
        
        stats = cache.get_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["size"] == 1
    
    def test_thread_safety(self):
        """Test basic thread safety."""
        cache = LRUCache(max_size=100)
        
        def worker(idx):
            for i in range(100):
                cache.set(f"k_{idx}_{i}", f"v_{idx}_{i}")
                cache.get(f"k_{idx}_{i}")
        
        threads = []
        for i in range(5):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Should execute without exceptions
        assert cache.get_stats()["size"] <= 100


class TestCacheUtils:
    """Tests for utility functions."""
    
    def test_cache_key_generation(self):
        """Test cache key generation helper."""
        key = cache_key("user", "repo", 123)
        assert key == "user:repo:123"
    
    def test_get_repo_cache(self):
        """Test singleton access for repo cache."""
        c1 = get_repo_cache()
        c2 = get_repo_cache()
        assert c1 is c2
        assert isinstance(c1, LRUCache)
    
    def test_get_analysis_cache(self):
        """Test singleton access for analysis cache."""
        c1 = get_analysis_cache()
        c2 = get_analysis_cache()
        assert c1 is c2
        assert isinstance(c1, LRUCache)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
