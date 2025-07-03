#!/usr/bin/env node

/**
 * Test API Integration
 * Verifies all providers work with the new error recovery system
 * 
 * @author Jordan After Midnight
 * @copyright 2025 Jordan After Midnight. All rights reserved.
 */

import { AIRouter } from './src/core/ai-router.js';
import { GroqProvider } from './src/providers/groq-provider.js';
import { OpenAIProvider } from './src/providers/openai-provider.js';
import { ClaudeProvider } from './src/providers/claude-provider.js';
import { GeminiProvider } from './src/providers/gemini-provider.js';

async function testProvider(router, providerName, testMessage) {
  console.log(`\n🧪 Testing ${providerName}...`);
  
  try {
    const result = await router.executeRequest(testMessage, {
      provider: providerName,
      maxTokens: 100,
      temperature: 0.3,
      taskType: 'balanced'
    });
    
    console.log(`✅ ${providerName} responded successfully`);
    console.log(`   Model: ${result.model}`);
    console.log(`   Response length: ${result.response.length} chars`);
    console.log(`   Response time: ${result.responseTime || 'N/A'}ms`);
    
    return { provider: providerName, success: true };
  } catch (error) {
    console.log(`❌ ${providerName} failed: ${error.message}`);
    return { provider: providerName, success: false, error: error.message };
  }
}

async function runTests() {
  console.log('🚀 Starting API Integration Tests');
  console.log('================================\n');
  
  const router = new AIRouter();
  
  // Register providers
  const providers = [
    { name: 'groq', instance: new GroqProvider() },
    { name: 'openai', instance: new OpenAIProvider() },
    { name: 'claude', instance: new ClaudeProvider() },
    { name: 'gemini', instance: new GeminiProvider() }
  ];
  
  for (const { name, instance } of providers) {
    try {
      router.registerProvider(instance);
      console.log(`📦 Registered ${name} provider`);
    } catch (error) {
      console.log(`⚠️  Failed to register ${name}: ${error.message}`);
    }
  }
  
  // Test messages that previously caused errors
  const testCases = [
    {
      name: 'Simple message',
      message: 'Hello, please respond with "OK" if you can see this message.'
    },
    {
      name: 'Message with special characters',
      message: 'Can you process this: <script>alert("test")</script> safely?'
    },
    {
      name: 'Long message',
      message: 'Please summarize this: ' + 'Lorem ipsum '.repeat(100)
    },
    {
      name: 'Message with tool references (should be stripped)',
      message: 'Process this without tool_use or tool_result blocks'
    }
  ];
  
  const results = [];
  
  for (const testCase of testCases) {
    console.log(`\n📝 Test Case: ${testCase.name}`);
    console.log('─'.repeat(40));
    
    for (const provider of ['groq', 'openai', 'claude', 'gemini']) {
      const result = await testProvider(router, provider, testCase.message);
      results.push({ ...result, testCase: testCase.name });
    }
  }
  
  // Summary
  console.log('\n\n📊 Test Summary');
  console.log('===============\n');
  
  const providerStats = {};
  results.forEach(result => {
    if (!providerStats[result.provider]) {
      providerStats[result.provider] = { success: 0, failed: 0 };
    }
    if (result.success) {
      providerStats[result.provider].success++;
    } else {
      providerStats[result.provider].failed++;
    }
  });
  
  for (const [provider, stats] of Object.entries(providerStats)) {
    const total = stats.success + stats.failed;
    const successRate = ((stats.success / total) * 100).toFixed(1);
    console.log(`${provider}: ${stats.success}/${total} passed (${successRate}%)`);
  }
  
  // Show error recovery report
  const { errorRecovery } = await import('./src/core/error-recovery.js');
  const recoveryReport = errorRecovery.getRecoveryReport();
  
  if (recoveryReport.totalRecoveries > 0) {
    console.log('\n\n🔧 Error Recovery Report');
    console.log('========================\n');
    console.log(`Total recoveries: ${recoveryReport.totalRecoveries}`);
    console.log('\nBy Strategy:');
    for (const [strategy, count] of Object.entries(recoveryReport.byStrategy)) {
      console.log(`  ${strategy}: ${count}`);
    }
    console.log('\nBy Provider:');
    for (const [provider, count] of Object.entries(recoveryReport.byProvider)) {
      console.log(`  ${provider}: ${count}`);
    }
  }
  
  console.log('\n✨ Testing complete!');
}

// Run tests
runTests().catch(error => {
  console.error('Test suite failed:', error);
  process.exit(1);
});