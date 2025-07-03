#!/usr/bin/env node

/**
 * API Error Diagnostic Tool
 * Identifies the root cause of persistent API errors
 */

console.log('🔍 API Error Diagnostic Tool\n');

// Check environment
console.log('1. Environment Check:');
console.log('   Node version:', process.version);
console.log('   Platform:', process.platform);
console.log('   Working directory:', process.cwd());

// Check for API keys
console.log('\n2. API Key Check:');
const apiKeys = {
  'GROQ_API_KEY': process.env.GROQ_API_KEY ? '✓ Set' : '✗ Missing',
  'OPENAI_API_KEY': process.env.OPENAI_API_KEY ? '✓ Set' : '✗ Missing',
  'ANTHROPIC_API_KEY': process.env.ANTHROPIC_API_KEY ? '✓ Set' : '✗ Missing',
  'GOOGLE_API_KEY': process.env.GOOGLE_API_KEY ? '✓ Set' : '✗ Missing'
};

for (const [key, status] of Object.entries(apiKeys)) {
  console.log(`   ${key}: ${status}`);
}

// Test basic HTTP request
console.log('\n3. Testing basic HTTP connectivity:');
try {
  const https = await import('https');
  await new Promise((resolve, reject) => {
    https.get('https://api.github.com', (res) => {
      console.log('   ✓ HTTPS requests working (status:', res.statusCode + ')');
      resolve();
    }).on('error', reject);
  });
} catch (error) {
  console.log('   ✗ HTTPS request failed:', error.message);
}

// Check for problematic imports
console.log('\n4. Checking imports:');
try {
  const { GroqProvider } = await import('./src/providers/groq-provider.js');
  console.log('   ✓ GroqProvider imports successfully');
  
  // Check if Groq SDK is available
  try {
    const groqModule = await import('groq-sdk');
    console.log('   ✓ groq-sdk module found');
  } catch (e) {
    console.log('   ✗ groq-sdk module missing - install with: npm install groq-sdk');
  }
} catch (error) {
  console.log('   ✗ GroqProvider import failed:', error.message);
}

// Test minimal API call
console.log('\n5. Testing minimal Groq API call:');
if (process.env.GROQ_API_KEY) {
  try {
    const Groq = (await import('groq-sdk')).default;
    const client = new Groq({
      apiKey: process.env.GROQ_API_KEY,
    });
    
    console.log('   Making test request...');
    const completion = await client.chat.completions.create({
      messages: [{ role: 'user', content: 'Say OK' }],
      model: 'llama-3.1-8b-instant',
      max_tokens: 10,
      temperature: 0
    });
    
    console.log('   ✓ API call successful:', completion.choices[0].message.content);
  } catch (error) {
    console.log('   ✗ API call failed:', error.message);
    if (error.response) {
      console.log('   Response status:', error.response.status);
      console.log('   Response data:', JSON.stringify(error.response.data, null, 2));
    }
  }
} else {
  console.log('   ⏭️  Skipping - GROQ_API_KEY not set');
}

// Check for message format issues
console.log('\n6. Checking message formatting:');
const testMessages = [
  { role: 'user', content: 'Hello' },
  { role: 'system', content: 'You are helpful' },
  { role: 'assistant', content: 'Hi there' }
];

console.log('   Test messages:', JSON.stringify(testMessages, null, 2));

// Look for tool_use or tool_result in codebase
console.log('\n7. Searching for tool_use/tool_result references:');
try {
  const fs = await import('fs').then(m => m.promises);
  const path = await import('path');
  
  async function searchInFile(filePath) {
    try {
      const content = await fs.readFile(filePath, 'utf8');
      if (content.includes('tool_use') || content.includes('tool_result')) {
        const lines = content.split('\n');
        lines.forEach((line, index) => {
          if (line.includes('tool_use') || line.includes('tool_result')) {
            console.log(`   Found in ${filePath}:${index + 1}`);
            console.log(`     ${line.trim()}`);
          }
        });
      }
    } catch (e) {
      // Ignore read errors
    }
  }
  
  const srcDir = './src';
  async function searchDir(dir) {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory() && !entry.name.startsWith('.')) {
        await searchDir(fullPath);
      } else if (entry.name.endsWith('.js')) {
        await searchInFile(fullPath);
      }
    }
  }
  
  await searchDir(srcDir);
} catch (error) {
  console.log('   ✗ Search failed:', error.message);
}

console.log('\n✨ Diagnostic complete\n');