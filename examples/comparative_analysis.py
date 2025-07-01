#!/usr/bin/env python3
"""
Comparative analysis examples for Multi-AI MCP Integration
Shows how to get multiple AI perspectives on the same question
"""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from multi_ai_integration import MultiAIIntegration, MultiAIConsultationRequest, AIProvider

async def side_by_side_comparison():
    """Example: Compare responses from multiple AI providers"""
    print("⚖️ Side-by-Side AI Comparison Example")
    print("=" * 50)
    
    multi_ai = MultiAIIntegration()
    
    # Create a request for comparison
    request = MultiAIConsultationRequest(
        query="Should I use React or Vue.js for a new project?",
        context="Building a dashboard application with real-time data updates",
        preferred_provider=AIProvider.BOTH,  # Request both providers
        compare_responses=True  # Enable comparison mode
    )
    
    print("🤖 Consulting both AI providers...")
    result = await multi_ai.consult_multi_ai(request)
    
    if result["success"]:
        print("✅ Comparative analysis successful!")
        print(f"📊 Responses from {len(result['responses'])} providers")
        
        # Show individual responses
        print("\n📝 Individual Responses:")
        print("-" * 40)
        for i, response in enumerate(result["responses"], 1):
            if response["success"]:
                provider = response["provider"].title()
                time_taken = response["response_time"]
                model = response["model_used"]
                
                print(f"\n{i}. {provider} ({model}) - {time_taken:.2f}s:")
                print(f"   {response['response'][:300]}...")
                
        # Show comparison if available
        if "comparison" in result:
            print("\n📊 Comparison Analysis:")
            print("-" * 40)
            print(result["comparison"])
            
    else:
        print(f"❌ Comparison failed: {result['error']}")

async def architecture_decision_comparison():
    """Example: Compare AI perspectives on architecture decisions"""
    print("\n🏗️ Architecture Decision Comparison")
    print("=" * 50)
    
    multi_ai = MultiAIIntegration()
    
    questions = [
        {
            "query": "Microservices vs Monolith for a startup?",
            "context": "Building an MVP for a social media platform with 5 developers"
        },
        {
            "query": "SQL vs NoSQL database choice?",
            "context": "E-commerce platform with complex product relationships and high read traffic"
        },
        {
            "query": "REST vs GraphQL API design?",
            "context": "Mobile app backend with multiple client types and data requirements"
        }
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. {question['query']}")
        print("   " + "=" * (len(question['query']) + 2))
        
        request = MultiAIConsultationRequest(
            query=question["query"],
            context=question["context"],
            preferred_provider=AIProvider.BOTH,
            compare_responses=True
        )
        
        result = await multi_ai.consult_multi_ai(request)
        
        if result["success"]:
            successful_responses = [r for r in result["responses"] if r["success"]]
            print(f"   ✅ {len(successful_responses)} providers responded")
            
            # Show brief summary from each provider
            for response in successful_responses:
                provider = response["provider"].title()
                # Extract first sentence or 100 chars
                summary = response["response"].split('.')[0][:100] + "..."
                print(f"   • {provider}: {summary}")
        else:
            print(f"   ❌ Failed: {result['error']}")

async def performance_comparison():
    """Example: Compare performance characteristics of providers"""
    print("\n⚡ Performance Comparison Example")
    print("=" * 50)
    
    multi_ai = MultiAIIntegration()
    
    # Test questions of different complexities
    test_cases = [
        {
            "name": "Simple Question",
            "query": "What is dependency injection?",
            "context": "Basic concept explanation"
        },
        {
            "name": "Medium Complexity",
            "query": "How to implement authentication in a distributed system?",
            "context": "Designing secure microservices architecture"
        },
        {
            "name": "Complex Analysis",
            "query": "Compare different caching strategies for high-traffic applications",
            "context": "Optimizing performance for millions of concurrent users"
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        
        request = MultiAIConsultationRequest(
            query=test_case["query"],
            context=test_case["context"],
            preferred_provider=AIProvider.BOTH,
            compare_responses=True
        )
        
        result = await multi_ai.consult_multi_ai(request)
        
        if result["success"]:
            test_result = {
                "name": test_case["name"],
                "responses": []
            }
            
            for response in result["responses"]:
                if response["success"]:
                    test_result["responses"].append({
                        "provider": response["provider"],
                        "time": response["response_time"],
                        "length": len(response["response"]),
                        "model": response["model_used"]
                    })
                    
                    print(f"   • {response['provider'].title()}: "
                          f"{response['response_time']:.2f}s, "
                          f"{len(response['response'])} chars")
            
            results.append(test_result)
        else:
            print(f"   ❌ Failed: {result['error']}")
    
    # Performance summary
    if results:
        print("\n📊 Performance Summary:")
        print("-" * 30)
        
        provider_stats = {}
        for result in results:
            for response in result["responses"]:
                provider = response["provider"]
                if provider not in provider_stats:
                    provider_stats[provider] = {"times": [], "lengths": []}
                
                provider_stats[provider]["times"].append(response["time"])
                provider_stats[provider]["lengths"].append(response["length"])
        
        for provider, stats in provider_stats.items():
            avg_time = sum(stats["times"]) / len(stats["times"])
            avg_length = sum(stats["lengths"]) / len(stats["lengths"])
            print(f"• {provider.title()}:")
            print(f"  - Avg Response Time: {avg_time:.2f}s")
            print(f"  - Avg Response Length: {avg_length:.0f} chars")

async def main():
    """Run all comparative analysis examples"""
    print("🔍 Multi-AI Comparative Analysis Examples")
    print("=" * 60)
    
    try:
        await side_by_side_comparison()
        await architecture_decision_comparison()
        await performance_comparison()
        
        print("\n🎉 All comparative analysis examples completed!")
        print("\nKey insights:")
        print("• Different AI providers offer unique perspectives")
        print("• Performance varies by question complexity")
        print("• Comparison mode helps make informed decisions")
        print("• Use AUTO mode for best single response")
        print("• Use BOTH mode for comprehensive analysis")
        
    except KeyboardInterrupt:
        print("\n🛑 Examples interrupted")
    except Exception as e:
        print(f"\n❌ Example failed: {e}")

if __name__ == "__main__":
    # Set up environment
    if not os.getenv('GOOGLE_API_KEY'):
        print("⚠️  GOOGLE_API_KEY not set. Gemini examples may fail.")
        print("   Set it with: export GOOGLE_API_KEY='your-key-here'")
    
    asyncio.run(main())