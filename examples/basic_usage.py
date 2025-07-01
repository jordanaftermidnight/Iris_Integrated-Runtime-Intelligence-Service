#!/usr/bin/env python3
"""
Basic usage examples for Multi-AI MCP Integration
"""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from multi_ai_integration import MultiAIIntegration, MultiAIConsultationRequest, AIProvider

async def basic_consultation_example():
    """Example: Basic AI consultation with automatic provider selection"""
    print("🤖 Basic AI Consultation Example")
    print("=" * 50)
    
    # Initialize the multi-AI system
    multi_ai = MultiAIIntegration()
    
    # Create a consultation request
    request = MultiAIConsultationRequest(
        query="What are the best practices for API authentication?",
        context="Building a RESTful API for a web application",
        preferred_provider=AIProvider.AUTO,
        compare_responses=False
    )
    
    # Perform consultation
    result = await multi_ai.consult_multi_ai(request)
    
    if result["success"]:
        print("✅ Consultation successful!")
        print(f"📝 Summary:\n{result['summary']}")
    else:
        print(f"❌ Consultation failed: {result['error']}")

async def provider_specific_example():
    """Example: Consulting specific AI providers"""
    print("\n🎯 Provider-Specific Consultation Example")
    print("=" * 50)
    
    multi_ai = MultiAIIntegration()
    
    # Consult Gemini specifically
    print("📡 Consulting Gemini...")
    gemini_request = MultiAIConsultationRequest(
        query="How should I structure a microservices architecture?",
        context="Designing a scalable e-commerce platform",
        preferred_provider=AIProvider.GEMINI
    )
    
    gemini_result = await multi_ai.consult_multi_ai(gemini_request)
    
    if gemini_result["success"]:
        print("✅ Gemini consultation successful!")
        print(f"📄 Response preview: {gemini_result['summary'][:200]}...")
    else:
        print(f"❌ Gemini consultation failed: {gemini_result['error']}")
    
    # Consult Llama2 specifically
    print("\n🦙 Consulting Llama2...")
    llama_request = MultiAIConsultationRequest(
        query="What's a privacy-focused approach to user data handling?",
        context="Implementing GDPR-compliant data processing",
        preferred_provider=AIProvider.LLAMA2
    )
    
    llama_result = await multi_ai.consult_multi_ai(llama_request)
    
    if llama_result["success"]:
        print("✅ Llama2 consultation successful!")
        print(f"📄 Response preview: {llama_result['summary'][:200]}...")
    else:
        print(f"❌ Llama2 consultation failed: {llama_result['error']}")

async def system_status_example():
    """Example: Checking system status and performance"""
    print("\n📊 System Status Example")
    print("=" * 50)
    
    multi_ai = MultiAIIntegration()
    
    # Check provider availability
    availability = await multi_ai.check_provider_availability()
    print("🔌 Provider Availability:")
    for provider, available in availability.items():
        status = "✅ Available" if available else "❌ Unavailable"
        print(f"   • {provider.title()}: {status}")
    
    # Get comprehensive system status
    status = multi_ai.get_system_status()
    print("\n📈 System Statistics:")
    for provider, info in status["providers"].items():
        if info["available"]:
            stats = info.get("stats", {})
            requests = stats.get("requests", 0)
            successes = stats.get("successes", 0)
            avg_time = stats.get("avg_time", 0.0)
            success_rate = (successes / requests * 100) if requests > 0 else 0
            
            print(f"   • {provider.title()}:")
            print(f"     - Requests: {requests}")
            print(f"     - Success Rate: {success_rate:.1f}%")
            print(f"     - Avg Response Time: {avg_time:.2f}s")

async def main():
    """Run all examples"""
    print("🚀 Multi-AI MCP Integration - Usage Examples")
    print("=" * 60)
    
    try:
        await basic_consultation_example()
        await provider_specific_example()
        await system_status_example()
        
        print("\n🎉 All examples completed successfully!")
        print("\nNext steps:")
        print("• Try these patterns in Claude Code")
        print("• Experiment with different query types")
        print("• Monitor system performance over time")
        
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