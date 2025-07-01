#!/usr/bin/env python3
"""
Performance monitoring examples for Multi-AI MCP Integration
Demonstrates system monitoring, metrics collection, and performance analysis
"""

import asyncio
import time
import json
import os
import sys
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from multi_ai_integration import MultiAIIntegration, MultiAIConsultationRequest, AIProvider

async def basic_performance_monitoring():
    """Example: Basic system performance monitoring"""
    print("📊 Basic Performance Monitoring Example")
    print("=" * 50)
    
    multi_ai = MultiAIIntegration()
    
    # Get initial system status
    print("🔍 Initial System Status:")
    status = multi_ai.get_system_status()
    
    for provider, info in status["providers"].items():
        if info["available"]:
            stats = info.get("stats", {})
            print(f"   • {provider.title()}:")
            print(f"     - Requests: {stats.get('requests', 0)}")
            print(f"     - Success Rate: {(stats.get('successes', 0) / max(stats.get('requests', 1), 1) * 100):.1f}%")
            print(f"     - Avg Response Time: {stats.get('avg_time', 0):.2f}s")
        else:
            print(f"   • {provider.title()}: ❌ Unavailable")
    
    # Perform some test requests to generate metrics
    print("\n🧪 Performing test requests to generate metrics...")
    
    test_queries = [
        "What is Python?",
        "Explain REST API design",
        "How does caching work?",
        "What are design patterns?",
        "Describe microservices architecture"
    ]
    
    results = []
    for i, query in enumerate(test_queries, 1):
        print(f"   {i}/5: Testing with query: '{query[:30]}...'")
        
        start_time = time.time()
        request = MultiAIConsultationRequest(
            query=query,
            context="Performance testing",
            preferred_provider=AIProvider.AUTO
        )
        
        result = await multi_ai.consult_multi_ai(request)
        end_time = time.time()
        
        results.append({
            "query": query,
            "success": result["success"],
            "total_time": end_time - start_time,
            "providers_used": len(result.get("responses", [])),
            "error": result.get("error")
        })
    
    # Analyze results
    print("\n📈 Performance Analysis:")
    successful_requests = [r for r in results if r["success"]]
    failed_requests = [r for r in results if not r["success"]]
    
    if successful_requests:
        avg_time = sum(r["total_time"] for r in successful_requests) / len(successful_requests)
        min_time = min(r["total_time"] for r in successful_requests)
        max_time = max(r["total_time"] for r in successful_requests)
        
        print(f"   ✅ Successful requests: {len(successful_requests)}/{len(results)}")
        print(f"   ⏱️  Average response time: {avg_time:.2f}s")
        print(f"   🚀 Fastest response: {min_time:.2f}s")
        print(f"   🐌 Slowest response: {max_time:.2f}s")
    
    if failed_requests:
        print(f"   ❌ Failed requests: {len(failed_requests)}")
        for failure in failed_requests:
            print(f"      - '{failure['query'][:30]}...': {failure['error']}")

async def provider_comparison_benchmark():
    """Example: Compare performance between different providers"""
    print("\n⚡ Provider Performance Comparison")
    print("=" * 50)
    
    multi_ai = MultiAIIntegration()
    
    # Check which providers are available
    availability = await multi_ai.check_provider_availability()
    available_providers = [p for p, avail in availability.items() if avail]
    
    if len(available_providers) < 2:
        print("⚠️  Need at least 2 providers for comparison. Available:", available_providers)
        return
    
    print(f"🔌 Testing providers: {', '.join(available_providers)}")
    
    # Test questions of varying complexity
    test_cases = [
        {
            "name": "Simple",
            "query": "What is HTTP?",
            "context": "Basic web protocol question"
        },
        {
            "name": "Medium",
            "query": "How to implement user authentication in a web app?",
            "context": "Security implementation question"
        },
        {
            "name": "Complex",
            "query": "Compare different database scaling strategies for high-traffic applications",
            "context": "Advanced architecture question"
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']} complexity")
        results[test_case['name']] = {}
        
        for provider in available_providers:
            print(f"   Testing {provider}...")
            
            # Create provider-specific request
            provider_enum = AIProvider.GEMINI if provider == "gemini" else AIProvider.LLAMA2
            
            request = MultiAIConsultationRequest(
                query=test_case["query"],
                context=test_case["context"],
                preferred_provider=provider_enum
            )
            
            # Time the request
            start_time = time.time()
            result = await multi_ai.consult_multi_ai(request)
            end_time = time.time()
            
            if result["success"] and result["responses"]:
                response = result["responses"][0]
                results[test_case['name']][provider] = {
                    "success": True,
                    "response_time": response["response_time"],
                    "total_time": end_time - start_time,
                    "response_length": len(response["response"]),
                    "model_used": response["model_used"]
                }
                print(f"      ✅ {response['response_time']:.2f}s ({len(response['response'])} chars)")
            else:
                results[test_case['name']][provider] = {
                    "success": False,
                    "error": result.get("error", "Unknown error")
                }
                print(f"      ❌ Failed: {result.get('error', 'Unknown')}")
    
    # Summary comparison
    print("\n📊 Performance Summary:")
    for test_name, test_results in results.items():
        print(f"\n   {test_name} Complexity:")
        successful_results = {p: r for p, r in test_results.items() if r.get("success")}
        
        if successful_results:
            # Find fastest provider
            fastest_provider = min(successful_results.keys(), 
                                 key=lambda p: successful_results[p]["response_time"])
            
            for provider, result in successful_results.items():
                speed_indicator = "🥇" if provider == fastest_provider else "⚡"
                print(f"      {speed_indicator} {provider.title()}: {result['response_time']:.2f}s "
                      f"({result['response_length']} chars)")

async def real_time_monitoring():
    """Example: Real-time system monitoring"""
    print("\n🔄 Real-Time Performance Monitoring")
    print("=" * 50)
    
    multi_ai = MultiAIIntegration()
    
    print("🕐 Monitoring system for 60 seconds (press Ctrl+C to stop early)...")
    
    start_time = time.time()
    monitoring_duration = 60  # seconds
    check_interval = 10  # seconds
    
    try:
        while time.time() - start_time < monitoring_duration:
            current_time = datetime.now().strftime("%H:%M:%S")
            
            # Get current system status
            status = multi_ai.get_system_status()
            
            print(f"\n[{current_time}] System Status:")
            
            total_requests = 0
            total_successes = 0
            
            for provider, info in status["providers"].items():
                if info["available"]:
                    stats = info.get("stats", {})
                    requests = stats.get("requests", 0)
                    successes = stats.get("successes", 0)
                    avg_time = stats.get("avg_time", 0)
                    
                    total_requests += requests
                    total_successes += successes
                    
                    success_rate = (successes / max(requests, 1)) * 100
                    
                    status_emoji = "🟢" if success_rate >= 95 else "🟡" if success_rate >= 80 else "🔴"
                    
                    print(f"   {status_emoji} {provider.title()}: "
                          f"{requests} reqs, {success_rate:.1f}% success, {avg_time:.2f}s avg")
                else:
                    print(f"   🔴 {provider.title()}: Unavailable")
            
            # Overall system health
            overall_success_rate = (total_successes / max(total_requests, 1)) * 100
            health_emoji = "🟢" if overall_success_rate >= 95 else "🟡" if overall_success_rate >= 80 else "🔴"
            
            print(f"   {health_emoji} Overall: {total_requests} requests, {overall_success_rate:.1f}% success")
            
            # Wait for next check
            await asyncio.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
    
    print(f"\n✅ Monitoring completed after {time.time() - start_time:.1f} seconds")

async def load_testing():
    """Example: Basic load testing"""
    print("\n💪 Load Testing Example")
    print("=" * 50)
    
    multi_ai = MultiAIIntegration()
    
    # Configuration
    concurrent_requests = 3
    total_requests = 10
    test_query = "What are the benefits of microservices?"
    
    print(f"🏋️  Running load test: {total_requests} requests, {concurrent_requests} concurrent")
    
    async def single_request(request_id):
        """Single test request"""
        start_time = time.time()
        
        request = MultiAIConsultationRequest(
            query=f"{test_query} (Request #{request_id})",
            context="Load testing",
            preferred_provider=AIProvider.AUTO
        )
        
        try:
            result = await multi_ai.consult_multi_ai(request)
            end_time = time.time()
            
            return {
                "request_id": request_id,
                "success": result["success"],
                "total_time": end_time - start_time,
                "error": result.get("error")
            }
        except Exception as e:
            return {
                "request_id": request_id,
                "success": False,
                "total_time": time.time() - start_time,
                "error": str(e)
            }
    
    # Run requests in batches
    results = []
    
    for batch_start in range(0, total_requests, concurrent_requests):
        batch_end = min(batch_start + concurrent_requests, total_requests)
        batch_size = batch_end - batch_start
        
        print(f"   📦 Batch {batch_start//concurrent_requests + 1}: "
              f"Requests {batch_start + 1}-{batch_end}")
        
        # Create tasks for this batch
        tasks = [
            single_request(i) 
            for i in range(batch_start + 1, batch_end + 1)
        ]
        
        # Execute batch
        batch_start_time = time.time()
        batch_results = await asyncio.gather(*tasks)
        batch_end_time = time.time()
        
        results.extend(batch_results)
        
        # Batch summary
        batch_successes = sum(1 for r in batch_results if r["success"])
        batch_time = batch_end_time - batch_start_time
        
        print(f"      ✅ {batch_successes}/{batch_size} successful in {batch_time:.2f}s")
        
        # Small delay between batches
        if batch_end < total_requests:
            await asyncio.sleep(1)
    
    # Final analysis
    print(f"\n📊 Load Test Results:")
    
    successful_results = [r for r in results if r["success"]]
    failed_results = [r for r in results if not r["success"]]
    
    print(f"   📈 Success Rate: {len(successful_results)}/{len(results)} ({len(successful_results)/len(results)*100:.1f}%)")
    
    if successful_results:
        times = [r["total_time"] for r in successful_results]
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"   ⏱️  Response Times:")
        print(f"      - Average: {avg_time:.2f}s")
        print(f"      - Fastest: {min_time:.2f}s")
        print(f"      - Slowest: {max_time:.2f}s")
    
    if failed_results:
        print(f"   ❌ Failures:")
        error_counts = {}
        for failure in failed_results:
            error = failure.get("error", "Unknown")
            error_counts[error] = error_counts.get(error, 0) + 1
        
        for error, count in error_counts.items():
            print(f"      - {error}: {count} times")

async def export_metrics():
    """Example: Export performance metrics"""
    print("\n📤 Metrics Export Example")
    print("=" * 50)
    
    multi_ai = MultiAIIntegration()
    
    # Get current metrics
    status = multi_ai.get_system_status()
    
    # Create metrics export
    metrics_export = {
        "timestamp": datetime.now().isoformat(),
        "system_info": {
            "uptime_hours": 24,  # Example uptime
            "version": "1.0.0"
        },
        "providers": status["providers"],
        "configuration": status["configuration"]
    }
    
    # Save to file
    export_filename = f"metrics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(export_filename, 'w') as f:
            json.dump(metrics_export, f, indent=2)
        
        print(f"   ✅ Metrics exported to: {export_filename}")
        print(f"   📁 File size: {os.path.getsize(export_filename)} bytes")
        
        # Show sample of exported data
        print(f"\n   📊 Sample metrics:")
        for provider, info in metrics_export["providers"].items():
            if info["available"]:
                stats = info.get("stats", {})
                print(f"      • {provider.title()}: {stats.get('requests', 0)} requests, "
                      f"{stats.get('avg_time', 0):.2f}s avg response time")
        
    except Exception as e:
        print(f"   ❌ Failed to export metrics: {e}")

async def main():
    """Run all performance monitoring examples"""
    print("🚀 Multi-AI Performance Monitoring Examples")
    print("=" * 60)
    
    try:
        await basic_performance_monitoring()
        await provider_comparison_benchmark()
        await real_time_monitoring()
        await load_testing()
        await export_metrics()
        
        print("\n🎉 All performance monitoring examples completed!")
        print("\nKey insights:")
        print("• Monitor system health regularly")
        print("• Compare provider performance for optimization")
        print("• Use load testing to validate system capacity")
        print("• Export metrics for historical analysis")
        print("• Set up alerts for performance degradation")
        
    except KeyboardInterrupt:
        print("\n🛑 Examples interrupted")
    except Exception as e:
        print(f"\n❌ Example failed: {e}")

if __name__ == "__main__":
    # Set up environment
    if not os.getenv('GOOGLE_API_KEY'):
        print("⚠️  GOOGLE_API_KEY not set. Some examples may fail.")
        print("   Set it with: export GOOGLE_API_KEY='your-key-here'")
    
    asyncio.run(main())