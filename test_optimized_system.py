#!/usr/bin/env python3
"""
Comprehensive Test Suite for Optimized Multi-AI Integration
Tests all performance optimizations, caching, and commercial features

Copyright (c) 2025 Jordan After Midnight. All rights reserved.
"""

import asyncio
import time
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch
import sqlite3
from datetime import datetime

# Optional dependencies for advanced testing
try:
    import pytest
except ImportError:
    print("Warning: pytest not available, using basic testing")
    pytest = None

# Import our optimized system
from optimized_multi_ai_integration import (
    OptimizedMultiAIIntegration,
    OptimizedConsultationRequest,
    QueryPattern,
    AIProvider,
    AdvancedCache,
    QueryPatternAnalyzer,
    PerformanceMonitor,
    CachedResponse
)

class TestAdvancedCache:
    """Test suite for the advanced caching system"""
    
    @pytest.fixture
    def cache(self):
        """Create a temporary cache for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_cache = AdvancedCache(max_size=100, ttl_hours=1)
            test_cache.db_path = Path(temp_dir) / "test_cache.db"
            test_cache._init_database()
            yield test_cache
    
    @pytest.mark.asyncio
    async def test_cache_basic_operations(self, cache):
        """Test basic cache get/set operations"""
        # Test cache miss
        result = await cache.get("test query", "test context")
        assert result is None
        
        # Test cache set and hit
        from datetime import datetime
        cached_response = CachedResponse(
            response="Test response",
            provider="gemini",
            model_used="gemini-pro",
            timestamp=datetime.now()
        )
        
        await cache.set("test query", "test context", cached_response)
        
        result = await cache.get("test query", "test context")
        assert result is not None
        assert result.response == "Test response"
        assert result.provider == "gemini"
        assert result.hit_count == 1
    
    @pytest.mark.asyncio
    async def test_cache_persistence(self, cache):
        """Test cache persistence to database"""
        from datetime import datetime
        cached_response = CachedResponse(
            response="Persistent response",
            provider="llama2",
            model_used="llama2:7b",
            timestamp=datetime.now()
        )
        
        await cache.set("persistent query", "context", cached_response)
        
        # Clear memory cache
        cache.cache.clear()
        cache.access_times.clear()
        
        # Should still retrieve from database
        result = await cache.get("persistent query", "context")
        assert result is not None
        assert result.response == "Persistent response"
    
    def test_cache_hash_generation(self, cache):
        """Test query hash generation consistency"""
        hash1 = cache._generate_hash("test query", "context")
        hash2 = cache._generate_hash("test query", "context")
        hash3 = cache._generate_hash("TEST QUERY", "CONTEXT")  # Case insensitive
        hash4 = cache._generate_hash("different query", "context")
        
        assert hash1 == hash2
        assert hash1 == hash3  # Case insensitive
        assert hash1 != hash4   # Different content

class TestQueryPatternAnalyzer:
    """Test suite for query pattern analysis"""
    
    @pytest.fixture
    def analyzer(self):
        return QueryPatternAnalyzer()
    
    def test_faq_pattern_detection(self, analyzer):
        """Test FAQ pattern detection"""
        faq_queries = [
            "What is machine learning?",
            "How to install Python?",
            "Can you explain neural networks?",
            "Tell me about artificial intelligence"
        ]
        
        for query in faq_queries:
            pattern, confidence = analyzer.classify_query(query)
            assert pattern == QueryPattern.FAQ
            assert confidence > 0.3
    
    def test_technical_pattern_detection(self, analyzer):
        """Test technical pattern detection"""
        technical_queries = [
            "Implement a REST API in Python",
            "Debug this code error",
            "Create a database schema",
            "Optimize algorithm performance"
        ]
        
        for query in technical_queries:
            pattern, confidence = analyzer.classify_query(query)
            assert pattern == QueryPattern.TECHNICAL
            assert confidence > 0.3
    
    def test_creative_pattern_detection(self, analyzer):
        """Test creative pattern detection"""
        creative_queries = [
            "Write a story about robots",
            "Create a poem about nature",
            "Design a new mobile app",
            "Generate creative ideas for marketing"
        ]
        
        for query in creative_queries:
            pattern, confidence = analyzer.classify_query(query)
            assert pattern == QueryPattern.CREATIVE
            assert confidence > 0.3
    
    def test_optimization_configs(self, analyzer):
        """Test pattern-specific optimization configurations"""
        faq_config = analyzer.get_optimization_config(QueryPattern.FAQ)
        assert faq_config["cache_priority"] == "high"
        assert faq_config["preferred_provider"] == "gemini"
        
        creative_config = analyzer.get_optimization_config(QueryPattern.CREATIVE)
        assert creative_config["preferred_provider"] == "llama2"
        assert creative_config["parallel_enabled"] == False

class TestPerformanceMonitor:
    """Test suite for performance monitoring"""
    
    @pytest.fixture
    def monitor(self):
        return PerformanceMonitor()
    
    def test_request_tracking(self, monitor):
        """Test request tracking functionality"""
        # Start request
        request_id = monitor.start_request()
        assert request_id.startswith("req_")
        assert monitor.metrics["concurrent_requests"] == 1
        
        # End request
        monitor.end_request(request_id, 1.5, True, cache_hit=False)
        assert monitor.metrics["concurrent_requests"] == 0
        assert monitor.metrics["request_count"] == 1
        assert monitor.metrics["cache_misses"] == 1
        assert monitor.metrics["avg_response_time"] == 1.5
    
    def test_cache_metrics(self, monitor):
        """Test cache hit/miss tracking"""
        # Cache hit
        req1 = monitor.start_request()
        monitor.end_request(req1, 0.5, True, cache_hit=True)
        
        # Cache miss
        req2 = monitor.start_request()
        monitor.end_request(req2, 2.0, True, cache_hit=False)
        
        metrics = monitor.get_system_metrics()
        assert metrics["cache_hits"] == 1
        assert metrics["cache_misses"] == 1
        assert metrics["cache_hit_rate"] == 50.0
    
    def test_error_tracking(self, monitor):
        """Test error rate tracking"""
        # Successful request
        req1 = monitor.start_request()
        monitor.end_request(req1, 1.0, True)
        
        # Failed request
        req2 = monitor.start_request()
        monitor.end_request(req2, 0.5, False)
        
        metrics = monitor.get_system_metrics()
        assert metrics["error_count"] == 1
        assert metrics["error_rate"] == 50.0

class TestOptimizedMultiAIIntegration:
    """Test suite for the main optimized integration system"""
    
    @pytest.fixture
    def integration(self):
        """Create a test integration instance with mocked providers"""
        with patch('optimized_multi_ai_integration.GeminiIntegration') as mock_gemini, \
             patch('optimized_multi_ai_integration.Llama2Integration') as mock_llama2:
            
            # Mock successful initialization
            mock_gemini.return_value.primary_model = "gemini-pro-test"
            mock_llama2.return_value.default_model = "llama2:7b-test"
            mock_llama2.return_value.check_ollama_status = AsyncMock(return_value=True)
            
            integration = OptimizedMultiAIIntegration()
            integration.gemini_available = True
            integration.llama2_available = True
            
            return integration
    
    def test_initialization(self, integration):
        """Test proper initialization of optimized system"""
        assert integration is not None
        assert hasattr(integration, 'cache')
        assert hasattr(integration, 'pattern_analyzer')
        assert hasattr(integration, 'performance_monitor')
        assert integration.gemini_available
        assert integration.llama2_available
    
    def test_adaptive_timeout_calculation(self, integration):
        """Test adaptive timeout calculation"""
        # Short FAQ query
        faq_request = OptimizedConsultationRequest(
            query="What is AI?",
            context="",
            pattern_type=QueryPattern.FAQ
        )
        timeout = integration._calculate_adaptive_timeout(faq_request)
        assert timeout < 30  # FAQ should have shorter timeout
        
        # Long creative query
        creative_request = OptimizedConsultationRequest(
            query="Write a detailed story about a futuristic city with flying cars and AI assistants",
            context="Creative writing project",
            pattern_type=QueryPattern.CREATIVE
        )
        timeout = integration._calculate_adaptive_timeout(creative_request)
        assert timeout > 30  # Creative should have longer timeout
    
    @pytest.mark.asyncio
    async def test_provider_availability_caching(self, integration):
        """Test provider availability caching"""
        # Mock the availability check
        with patch.object(integration, 'llama2') as mock_llama2:
            mock_llama2.check_ollama_status = AsyncMock(return_value=True)
            
            # First call
            availability1 = await integration._check_provider_availability_cached()
            
            # Second call should use cache (mock should only be called once)
            availability2 = await integration._check_provider_availability_cached()
            
            assert availability1 == availability2
            assert availability1["gemini"] == True
            assert availability1["llama2"] == True
    
    def test_provider_stats_update(self, integration):
        """Test provider statistics updates"""
        # Update stats for successful request
        integration._update_provider_stats_optimized("gemini", True, 2.5)
        
        stats = integration.provider_stats["gemini"]
        assert stats["requests"] == 1
        assert stats["successes"] == 1
        assert stats["avg_time"] == 2.5
        assert stats["min_time"] == 2.5
        assert stats["max_time"] == 2.5
        
        # Update with another request
        integration._update_provider_stats_optimized("gemini", False, 1.0)
        
        stats = integration.provider_stats["gemini"]
        assert stats["requests"] == 2
        assert stats["successes"] == 1
        assert stats["failures"] == 1
        assert stats["avg_time"] == 1.75  # Average of 2.5 and 1.0
    
    def test_pattern_stats_update(self, integration):
        """Test pattern statistics tracking"""
        # Update pattern stats
        integration._update_pattern_stats(QueryPattern.FAQ, 1.5, False)
        integration._update_pattern_stats(QueryPattern.FAQ, 2.0, True)
        
        stats = integration.pattern_stats[QueryPattern.FAQ]
        assert stats["count"] == 2
        assert stats["cache_hits"] == 1
        assert stats["avg_time"] == 1.75
    
    @pytest.mark.asyncio
    async def test_optimized_consultation_with_cache(self, integration):
        """Test optimized consultation with caching"""
        request = OptimizedConsultationRequest(
            query="What is machine learning?",
            context="Educational query",
            cache_enabled=True
        )
        
        # Mock successful consultation
        with patch.object(integration, '_execute_optimized_consultations') as mock_execute:
            mock_execute.return_value = [{
                "provider": "gemini",
                "success": True,
                "response": "Machine learning is a subset of AI...",
                "response_time": 2.0,
                "model_used": "gemini-pro",
                "cache_hit": False
            }]
            
            with patch.object(integration, '_check_provider_availability_cached') as mock_availability:
                mock_availability.return_value = {"gemini": True, "llama2": True}
                
                # First request - should not be cached
                result1 = await integration.optimized_consult(request)
                assert result1["success"] == True
                assert result1["cache_hit"] == False
                
                # Second request - should hit cache
                result2 = await integration.optimized_consult(request)
                assert result2["success"] == True
                assert result2["cache_hit"] == True
                assert result2["responses"][0]["hit_count"] == 1
    
    def test_comprehensive_status(self, integration):
        """Test comprehensive status reporting"""
        status = integration.get_comprehensive_status()
        
        # Check all required sections
        assert "providers" in status
        assert "performance" in status
        assert "cache" in status
        assert "patterns" in status
        assert "configuration" in status
        assert "licensing" in status
        
        # Check licensing information
        licensing = status["licensing"]
        assert licensing["owner"] == "Jordan After Midnight"
        assert "commercial use" in licensing["restrictions"].lower()

class TestCommercialLicensing:
    """Test commercial licensing and protection features"""
    
    def test_license_file_exists(self):
        """Test that license file exists and contains proper terms"""
        license_path = Path(__file__).parent / "LICENSE"
        assert license_path.exists(), "LICENSE file must exist"
        
        license_content = license_path.read_text()
        assert "Jordan After Midnight" in license_content
        assert "Commercial License" in license_content
        assert "commercial use" in license_content.lower()
        assert "jordanaftermidnight@users.noreply.github.com" in license_content
    
    def test_license_verification(self):
        """Test license verification in integration"""
        # This should not raise an exception even without license file
        with patch('pathlib.Path.exists', return_value=False):
            integration = OptimizedMultiAIIntegration()
            # Should initialize but log warning
            assert integration is not None

@pytest.mark.integration
class TestIntegrationPerformance:
    """Integration tests for performance optimization"""
    
    @pytest.mark.asyncio
    async def test_concurrent_requests_performance(self):
        """Test performance under concurrent load"""
        integration = OptimizedMultiAIIntegration()
        
        async def make_request(query_id):
            request = OptimizedConsultationRequest(
                query=f"Test query {query_id}",
                context="Performance test",
                cache_enabled=True
            )
            
            # Mock the actual AI consultation
            with patch.object(integration, '_execute_optimized_consultations') as mock_execute:
                mock_execute.return_value = [{
                    "provider": "gemini",
                    "success": True,
                    "response": f"Response for query {query_id}",
                    "response_time": 0.1,
                    "model_used": "gemini-pro"
                }]
                
                with patch.object(integration, '_check_provider_availability_cached') as mock_availability:
                    mock_availability.return_value = {"gemini": True, "llama2": False}
                    
                    return await integration.optimized_consult(request)
        
        # Execute 10 concurrent requests
        start_time = time.time()
        tasks = [make_request(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        # Check results
        assert len(results) == 10
        assert all(result["success"] for result in results)
        assert total_time < 5.0  # Should complete within 5 seconds
        
        # Check performance metrics
        status = integration.get_comprehensive_status()
        assert status["performance"]["request_count"] >= 10
    
    def test_cache_performance_under_load(self):
        """Test cache performance with many entries"""
        cache = AdvancedCache(max_size=1000, ttl_hours=1)
        
        # Add many entries
        start_time = time.time()
        for i in range(1000):
            asyncio.run(cache.set(
                f"query {i}", 
                f"context {i}",
                CachedResponse(
                    response=f"response {i}",
                    provider="test",
                    model_used="test-model",
                    timestamp=datetime.now()
                )
            ))
        
        set_time = time.time() - start_time
        
        # Retrieve entries
        start_time = time.time()
        hits = 0
        for i in range(100):  # Test 100 random retrievals
            result = asyncio.run(cache.get(f"query {i}", f"context {i}"))
            if result:
                hits += 1
        
        get_time = time.time() - start_time
        
        print(f"Cache performance: {set_time:.2f}s for 1000 sets, {get_time:.2f}s for 100 gets")
        print(f"Hit rate: {hits}/100")
        
        assert hits > 90  # Should have high hit rate
        assert get_time < 1.0  # Should be fast retrieval

def run_performance_benchmarks():
    """Run comprehensive performance benchmarks"""
    print("\n🏃‍♂️ Running Performance Benchmarks...")
    print("="*50)
    
    # Test cache performance
    print("\n1. Cache Performance Test")
    cache = AdvancedCache(max_size=10000, ttl_hours=24)
    
    from datetime import datetime
    
    # Benchmark cache operations
    start = time.time()
    for i in range(1000):
        asyncio.run(cache.set(
            f"bench_query_{i}",
            f"bench_context_{i}",
            CachedResponse(
                response=f"benchmark response {i}",
                provider="gemini",
                model_used="gemini-pro",
                timestamp=datetime.now()
            )
        ))
    
    set_duration = time.time() - start
    print(f"   ✅ 1000 cache sets: {set_duration:.2f}s ({1000/set_duration:.0f} ops/sec)")
    
    start = time.time()
    hits = 0
    for i in range(1000):
        result = asyncio.run(cache.get(f"bench_query_{i}", f"bench_context_{i}"))
        if result:
            hits += 1
    
    get_duration = time.time() - start
    print(f"   ✅ 1000 cache gets: {get_duration:.2f}s ({1000/get_duration:.0f} ops/sec)")
    print(f"   ✅ Cache hit rate: {hits/1000*100:.1f}%")
    
    # Test pattern analysis performance
    print("\n2. Pattern Analysis Performance")
    analyzer = QueryPatternAnalyzer()
    
    test_queries = [
        "What is artificial intelligence?",
        "How to implement a neural network?",
        "Create a story about robots",
        "Debug this Python code",
        "Analyze market trends"
    ] * 200  # 1000 total queries
    
    start = time.time()
    for query in test_queries:
        pattern, confidence = analyzer.classify_query(query)
    
    analysis_duration = time.time() - start
    print(f"   ✅ 1000 pattern analyses: {analysis_duration:.2f}s ({1000/analysis_duration:.0f} ops/sec)")
    
    print("\n" + "="*50)
    print("🎯 Performance Benchmark Complete!")

if __name__ == "__main__":
    # Run the comprehensive test suite
    print("🧪 Running Comprehensive Test Suite...")
    pytest.main([__file__, "-v", "--tb=short"])
    
    # Run performance benchmarks
    run_performance_benchmarks()
    
    print("\n✅ All tests completed!")
    print("\n📄 Commercial License Notice:")
    print("   This software is protected by commercial licensing.")
    print("   Single-user personal use is permitted at no charge.")
    print("   Commercial use requires a paid license.")
    print("   Contact: jordanaftermidnight@users.noreply.github.com")