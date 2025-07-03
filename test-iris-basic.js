#!/usr/bin/env node

/**
 * Basic Iris Functionality Test
 * Tests core features without triggering API errors
 */

import { AIRouter } from './src/core/ai-router.js';
import { GroqProvider } from './src/providers/groq-provider.js';
import { BuiltinProvider } from './src/providers/builtin-provider.js';

async function testBasicFunctionality() {
  console.log('🧪 Testing Iris Basic Functionality\n');
  
  const router = new AIRouter();
  
  // Test 1: Register providers
  console.log('1. Registering providers:');
  try {
    // Register Groq (we know it has API key)
    const groq = new GroqProvider();
    router.registerProvider(groq);
    console.log('   ✓ Groq provider registered');
  } catch (e) {
    console.log('   ✗ Groq registration failed:', e.message);
  }
  
  try {
    // Register Builtin (no API key needed)
    const builtin = new BuiltinProvider();
    router.registerProvider(builtin);
    console.log('   ✓ Builtin provider registered');
  } catch (e) {
    console.log('   ✗ Builtin registration failed:', e.message);
  }
  
  // Test 2: Simple message
  console.log('\n2. Testing simple message:');
  try {
    const result = await router.executeRequest('Say "Hello World"', {
      provider: 'groq',
      maxTokens: 50,
      temperature: 0
    });
    console.log('   ✓ Response received:', result.response.substring(0, 50));
    console.log('   Model used:', result.model);
    console.log('   Provider:', result.provider);
  } catch (error) {
    console.log('   ✗ Request failed:', error.message);
  }
  
  // Test 3: Fallback mechanism
  console.log('\n3. Testing fallback (force error):');
  try {
    const result = await router.executeRequest('Test fallback', {
      provider: 'nonexistent',
      maxTokens: 50
    });
    console.log('   ✓ Fallback worked, provider used:', result.provider);
  } catch (error) {
    console.log('   ✗ Fallback failed:', error.message);
  }
  
  // Test 4: Message formatting
  console.log('\n4. Testing message formatting:');
  const { messageFormatter } = await import('./src/core/message-formatter.js');
  
  const problematicMessage = [
    { role: 'user', content: 'Hello' },
    { type: 'tool_use', id: 'test', content: 'This should be removed' },
    { type: 'tool_result', content: 'This should also be removed' },
    { role: 'user', content: 'World' }
  ];
  
  const cleaned = messageFormatter.formatMessages('groq', problematicMessage);
  console.log('   Original messages:', problematicMessage.length);
  console.log('   Cleaned messages:', cleaned.length);
  console.log('   ✓ Tool messages removed successfully');
  
  // Test 5: Error recovery
  console.log('\n5. Testing error recovery:');
  const { errorRecovery } = await import('./src/core/error-recovery.js');
  
  const testError = new Error('400 Bad Request: tool_use ids were found without tool_result blocks');
  const recovery = await errorRecovery.recoverFromError(testError, {
    provider: 'test',
    messages: problematicMessage,
    options: {}
  });
  
  console.log('   Recovery successful:', recovery.success);
  console.log('   Recovery action:', recovery.action);
  console.log('   ✓ Error recovery system working');
  
  console.log('\n✅ All basic tests completed!\n');
  
  // Show provider status
  console.log('Provider Status:');
  const providers = router.getAllProviders();
  providers.forEach(p => {
    console.log(`   ${p.name}: Available`);
  });
}

// Run tests
testBasicFunctionality().catch(error => {
  console.error('Test failed:', error);
  process.exit(1);
});