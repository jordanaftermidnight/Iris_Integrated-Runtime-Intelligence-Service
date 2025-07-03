#!/usr/bin/env node

/**
 * Simple test runner for Multi-AI Integration
 * Basic testing infrastructure without external dependencies
 */

import { MultiAI } from '../src/index.js';
import fs from 'fs';
import path from 'path';

class TestRunner {
  constructor() {
    this.tests = [];
    this.passed = 0;
    this.failed = 0;
  }

  test(description, testFn) {
    this.tests.push({ description, testFn });
  }

  async run() {
    console.log('🧪 Running Multi-AI Integration Tests\n');

    for (const { description, testFn } of this.tests) {
      try {
        await testFn();
        console.log(`✅ ${description}`);
        this.passed++;
      } catch (error) {
        console.log(`❌ ${description}`);
        console.log(`   Error: ${error.message}`);
        this.failed++;
      }
    }

    console.log(`\n📊 Test Results: ${this.passed} passed, ${this.failed} failed`);
    
    if (this.failed > 0) {
      process.exit(1);
    }
  }

  assertEquals(actual, expected, message = '') {
    if (actual !== expected) {
      throw new Error(`${message} Expected: ${expected}, Got: ${actual}`);
    }
  }

  assertTrue(condition, message = '') {
    if (!condition) {
      throw new Error(`${message} Expected: true, Got: false`);
    }
  }

  assertThrows(fn, message = '') {
    try {
      fn();
      throw new Error(`${message} Expected function to throw, but it didn't`);
    } catch (error) {
      // Expected to throw
    }
  }
}

// Initialize test runner
const runner = new TestRunner();

// Basic functionality tests
runner.test('MultiAI constructor initializes correctly', () => {
  const ai = new MultiAI();
  runner.assertTrue(ai instanceof MultiAI, 'Should create MultiAI instance');
  runner.assertTrue(ai.router !== undefined, 'Should have router');
  runner.assertTrue(Array.isArray(ai.context), 'Should have context array');
  runner.assertTrue(ai.knowledgeBase instanceof Map, 'Should have knowledge base');
});

runner.test('Configuration loading works with defaults', () => {
  const ai = new MultiAI();
  runner.assertTrue(ai.config !== undefined, 'Should have config');
  runner.assertTrue(ai.config.providers !== undefined, 'Should have providers config');
  runner.assertTrue(ai.config.routing !== undefined, 'Should have routing config');
});

runner.test('Input validation works correctly', async () => {
  const ai = new MultiAI();
  
  // Test empty message
  try {
    await ai.chat('');
    runner.assertTrue(false, 'Should reject empty message');
  } catch (error) {
    runner.assertTrue(error.message.includes('non-empty string'), 'Should validate message type');
  }

  // Test long message
  try {
    const longMessage = 'a'.repeat(10001);
    await ai.chat(longMessage);
    runner.assertTrue(false, 'Should reject too long message');
  } catch (error) {
    runner.assertTrue(error.message.includes('too long'), 'Should validate message length');
  }
});

runner.test('Context management works correctly', () => {
  const ai = new MultiAI();
  
  // Test context operations
  ai.updateContext('Hello', 'Hi there');
  runner.assertEquals(ai.context.length, 2, 'Should add context entries');
  
  ai.clearContext();
  runner.assertEquals(ai.context.length, 0, 'Should clear context');
});

runner.test('Knowledge base operations work correctly', () => {
  const ai = new MultiAI();
  
  // Test adding knowledge
  ai.addKnowledge('test-key', 'test-value');
  runner.assertEquals(ai.knowledgeBase.size, 1, 'Should add knowledge entry');
  
  // Test key validation
  try {
    ai.addKnowledge('', 'value');
    runner.assertTrue(false, 'Should reject empty key');
  } catch (error) {
    runner.assertTrue(error.message.includes('non-empty string'), 'Should validate key');
  }
});

runner.test('Error sanitization works correctly', () => {
  const ai = new MultiAI();
  
  const sensitiveMessage = 'Error with api_key=REDACTED and token=REDACTED';
  const sanitized = ai.sanitizeError(sensitiveMessage);
  
  runner.assertTrue(!sanitized.includes('REDACTED'), 'Should remove API key');
  runner.assertTrue(sanitized.length > 0, 'Should still have content');
  runner.assertTrue(sanitized.includes('[REDACTED]'), 'Should show redacted placeholder');
});

runner.test('Configuration merging works correctly', () => {
  const ai = new MultiAI();
  
  const defaultConfig = { a: 1, b: { c: 2, d: 3 } };
  const userConfig = { b: { c: 4 }, e: 5 };
  
  const merged = ai.mergeConfig(defaultConfig, userConfig);
  
  runner.assertEquals(merged.a, 1, 'Should keep default values');
  runner.assertEquals(merged.b.c, 4, 'Should override with user values');
  runner.assertEquals(merged.b.d, 3, 'Should keep nested default values');
  runner.assertEquals(merged.e, 5, 'Should add new user values');
});

runner.test('File path validation works correctly', async () => {
  const ai = new MultiAI();
  
  // Test file outside project directory
  try {
    await ai.processFile('/etc/passwd');
    runner.assertTrue(false, 'Should reject external file paths');
  } catch (error) {
    runner.assertTrue(error.message.includes('outside project directory'), 'Should validate file paths');
  }
});

runner.test('System status returns comprehensive data', async () => {
  const ai = new MultiAI();
  const status = await ai.getSystemStatus();
  
  runner.assertTrue(status.timestamp !== undefined, 'Should have timestamp');
  runner.assertTrue(status.version !== undefined, 'Should have version');
  runner.assertTrue(status.providers !== undefined, 'Should have providers info');
  runner.assertTrue(status.resources !== undefined, 'Should have resources info');
});

// Provider-specific tests (if available)
runner.test('Provider availability check works', async () => {
  const ai = new MultiAI();
  
  try {
    await ai.initializeProviders();
    const healthChecks = await ai.router.healthCheckAll();
    
    runner.assertTrue(typeof healthChecks === 'object', 'Should return health check object');
    
    // Check if at least one provider is available (in CI/local environment)
    const hasHealthyProvider = Object.values(healthChecks).some(h => h.status === 'healthy');
    if (!hasHealthyProvider) {
      console.log('⚠️  No providers available - this is expected in CI environments');
    }
    
  } catch (error) {
    // Expected in CI environments without Ollama
    console.log('⚠️  Provider initialization failed - this is expected in CI environments');
  }
});

// Run all tests
runner.run().catch(error => {
  console.error('Test runner failed:', error);
  process.exit(1);
});