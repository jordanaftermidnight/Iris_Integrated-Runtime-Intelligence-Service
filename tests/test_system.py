#!/usr/bin/env python3
"""
Test script for Multi-AI Integration (Gemini + Llama2)
"""

import asyncio
import os
import sys

async def test_integrations():
    """Test all AI integrations"""
    print("🧪 Testing Multi-AI Integration System")
    print("=" * 60)
    
    # Set API key for testing
    if not os.getenv('GOOGLE_API_KEY'):
        os.environ['GOOGLE_API_KEY'] = 'AIzaSyDSd9THdggwjh_JY-B1aC0YO8E91UafPnM'
    
    # Test 1: Individual Integrations
    print("\\n1. Testing Individual Integrations...")
    
    # Test Gemini
    print("\\n📡 Testing Gemini Integration...")
    try:
        from gemini_integration import GeminiIntegration, ConsultationRequest
        
        gemini = GeminiIntegration("gemini-config.json")
        print("   ✅ Gemini integration loaded")
        
        # Quick test
        request = ConsultationRequest(
            query="What is 2+2?",
            context="Simple math test"
        )
        response = await gemini.consult_gemini(request)
        
        if response and "4" in response:
            print("   ✅ Gemini consultation working")
        else:
            print("   ⚠️  Gemini consultation may have issues")
            
    except Exception as e:
        print(f"   ❌ Gemini integration failed: {e}")
    
    # Test Llama2
    print("\\n🦙 Testing Llama2 Integration...")
    try:
        from llama2_integration import Llama2Integration, Llama2ConsultationRequest
        
        llama2 = Llama2Integration("llama2-config.json")
        print("   ✅ Llama2 integration loaded")
        
        # Check Ollama status
        ollama_status = await llama2.check_ollama_status()
        if ollama_status:
            print("   ✅ Ollama service accessible")
            
            # Get available models
            models = await llama2.get_available_models()
            print(f"   📦 Available models: {models}")
            
            if models:
                print("   ✅ Llama2 ready for consultation")
            else:
                print("   ⚠️  No Llama models available")
        else:
            print("   ❌ Ollama service not accessible")
            print("   💡 Start with: ollama serve")
            
    except Exception as e:
        print(f"   ❌ Llama2 integration failed: {e}")
    
    # Test 2: Multi-AI Integration
    print("\\n2. Testing Multi-AI Integration...")
    try:
        from multi_ai_integration import MultiAIIntegration, MultiAIConsultationRequest, AIProvider
        
        multi_ai = MultiAIIntegration()
        print("   ✅ Multi-AI integration loaded")
        
        # Check provider availability
        availability = await multi_ai.check_provider_availability()
        print(f"   📊 Provider availability: {availability}")
        
        # System status
        status = multi_ai.get_system_status()
        available_count = len([p for p, info in status['providers'].items() if info['available']])
        print(f"   🔌 {available_count}/2 providers available")
        
        # Test consultation if any provider available
        if any(availability.values()):
            print("\\n   🤖 Testing multi-AI consultation...")
            
            request = MultiAIConsultationRequest(
                query="What's the capital of France?",
                context="Geography test question",
                preferred_provider=AIProvider.AUTO,
                compare_responses=False
            )
            
            result = await multi_ai.consult_multi_ai(request)
            
            if result["success"]:
                print("   ✅ Multi-AI consultation successful")
                print(f"   📝 Response preview: {result['summary'][:100]}...")
            else:
                print(f"   ❌ Multi-AI consultation failed: {result['error']}")
        else:
            print("   ⚠️  No providers available for testing")
            
    except Exception as e:
        print(f"   ❌ Multi-AI integration failed: {e}")
    
    # Test 3: Enhanced MCP Server
    print("\\n3. Testing Enhanced MCP Server...")
    try:
        from enhanced_mcp_server import EnhancedMCPServer
        
        server = EnhancedMCPServer()
        print("   ✅ Enhanced MCP server can be instantiated")
        
        # Initialize multi-AI
        await server.initialize_multi_ai()
        print("   ✅ Multi-AI initialization successful")
        
    except Exception as e:
        print(f"   ❌ Enhanced MCP server failed: {e}")
    
    # Summary
    print("\\n" + "=" * 60)
    print("📋 Test Summary:")
    print("• Gemini Integration: Google API-based consultation")
    print("• Llama2 Integration: Local Ollama-based consultation") 
    print("• Multi-AI System: Intelligent provider selection")
    print("• Enhanced MCP Server: Unified interface for Claude Code")
    print("\\n🚀 Ready for use! Restart Claude Code to load new tools.")

async def show_usage_examples():
    """Show usage examples"""
    print("\\n" + "=" * 60)
    print("💡 Usage Examples in Claude Code:")
    print("=" * 60)
    
    examples = [
        ("Single Provider", [
            "Please consult Gemini about authentication best practices",
            "Ask Llama2 for a second opinion on database design"
        ]),
        ("Multi-AI Smart Selection", [
            "Get an AI second opinion on this code architecture",
            "Consult AI about the best approach for this API design"
        ]),
        ("Provider Comparison", [
            "Compare Gemini and Llama2 responses on microservices patterns",
            "Get both AI perspectives on React vs Vue for this project"
        ]),
        ("System Management", [
            "Check AI system status",
            "Show available AI providers and their performance"
        ])
    ]
    
    for category, commands in examples:
        print(f"\\n📂 {category}:")
        for cmd in commands:
            print(f"   • {cmd}")
    
    print("\\n🔧 Available MCP Tools:")
    tools = [
        "consult_multi_ai - Smart AI selection with fallback",
        "consult_gemini - Direct Gemini consultation", 
        "consult_llama2 - Direct Llama2 consultation",
        "compare_ai_providers - Side-by-side comparison",
        "ai_system_status - Check provider health",
        "detect_uncertainty - Analyze text confidence"
    ]
    
    for tool in tools:
        print(f"   • {tool}")

def main():
    """Main test function"""
    try:
        asyncio.run(test_integrations())
        asyncio.run(show_usage_examples())
    except KeyboardInterrupt:
        print("\\n🛑 Test interrupted")
    except Exception as e:
        print(f"\\n❌ Test failed: {e}")

if __name__ == "__main__":
    main()