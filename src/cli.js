#!/usr/bin/env node

import MultiAI from './index.js';

/**
 * Enhanced Multi-AI Integration CLI
 * Command-line interface with improved error handling and features
 */

/**
 * Parse command line arguments
 */
function parseArgs(args) {
  const result = {
    command: args[0],
    message: '',
    options: {}
  };

  // Extract task type
  const taskArg = args.find(arg => arg.startsWith('--task='));
  if (taskArg) {
    result.options.taskType = taskArg.split('=')[1];
  }

  // Extract other flags
  result.options.stream = args.includes('--stream');
  result.options.local = args.includes('--local');
  result.options.verbose = args.includes('--verbose') || args.includes('-v');

  // Extract message (everything that's not a flag)
  result.message = args
    .slice(1)
    .filter(arg => !arg.startsWith('--') && !arg.startsWith('-'))
    .join(' ');

  return result;
}

/**
 * Display help information
 */
function showHelp() {
  console.log(`
🤖 Multi-AI Integration CLI v2.2.0
====================================
Cost-Optimized AI with Mistral-First Logic

USAGE:
  multi-ai <command> [message] [options]

COMMANDS:
  chat <message>              Chat with AI using smart provider selection
  models                      List available models from all providers
  providers                   Show provider status and performance statistics
  file <path>                 Process and analyze a file
  dir <path>                  Process all files in a directory
  health                      Check system health and provider status
  status                      Show comprehensive system status
  config save/load [path]     Manage configuration files
  clear                       Clear conversation context
  help                        Show this help message

TASK TYPES:
  --task=code                 Programming, debugging, code review
  --task=creative             Writing, brainstorming, creative tasks  
  --task=fast                 Quick questions, simple queries
  --task=complex              Analysis, research, complex reasoning
  --task=balanced             General purpose (default)

OPTIONS:
  --stream                    Enable streaming responses
  --local                     Prefer local providers only
  --verbose, -v               Enable verbose output
  --help, -h                  Show this help message

EXAMPLES:
  multi-ai chat "Hello, how are you?"
  multi-ai chat "Write a Python function" --task=code
  multi-ai file ./my-script.js --task=code --verbose
  multi-ai providers
  multi-ai health

ENVIRONMENT VARIABLES:
  GEMINI_API_KEY             Google Gemini API key (optional)
  ANTHROPIC_API_KEY          Anthropic Claude API key (optional)
  OLLAMA_HOST                Ollama server host (default: http://localhost:11434)

COST OPTIMIZATION:
  🆓 Primary: Mistral 7B via Ollama (free, local)
  💰 Fallback: Gemini/Claude (paid, cloud) - only when needed

For more information, visit: https://github.com/jordanaftermidnight/multi-ai-integration-cli
`);
}

/**
 * Enhanced CLI runner with better error handling
 */
async function runCLI() {
  const args = process.argv.slice(2);
  
  // Show help for empty args or help command
  if (args.length === 0 || args.includes('--help') || args.includes('-h') || args[0] === 'help') {
    showHelp();
    return;
  }

  const { command, message, options } = parseArgs(args);

  // Initialize AI system
  const ai = new MultiAI();
  
  try {
    // Initialize providers with startup message
    if (options.verbose) {
      console.log('🚀 Starting Multi-AI Integration CLI...');
    }
    
    await ai.initializeProviders();

    // Execute command
    switch (command) {
      case 'chat':
        await handleChatCommand(ai, message, options);
        break;

      case 'providers':
        await handleProvidersCommand(ai, options);
        break;

      case 'models':
        await handleModelsCommand(ai, options);
        break;

      case 'file':
        await handleFileCommand(ai, message, options);
        break;

      case 'dir':
        await handleDirectoryCommand(ai, message, options);
        break;

      case 'health':
        await handleHealthCommand(ai, options);
        break;

      case 'status':
        await handleStatusCommand(ai, options);
        break;

      case 'config':
        await handleConfigCommand(ai, args.slice(1), options);
        break;

      case 'clear':
        await handleClearCommand(ai, options);
        break;

      default:
        console.error(`❌ Unknown command: ${command}`);
        console.log('Run "multi-ai help" to see available commands.');
        process.exit(1);
    }

  } catch (error) {
    console.error(`❌ Command failed: ${error.message}`);
    if (options.verbose) {
      console.error('Stack trace:', error.stack);
    }
    process.exit(1);
  }
}

/**
 * Handle chat command
 */
async function handleChatCommand(ai, message, options) {
  if (!message.trim()) {
    console.log('❌ Please provide a message to chat with AI');
    console.log('Usage: multi-ai chat "Your message here" [--task=type]');
    return;
  }

  try {
    console.log(`💭 Processing message...`);
    
    const startTime = Date.now();
    const response = await ai.chat(message, options);
    const duration = Date.now() - startTime;

    // Display response
    console.log(`\n[${response.provider}/${response.model}]`);
    console.log(response.response);
    
    // Show metadata if verbose
    if (options.verbose) {
      console.log(`\n📊 Metadata:`);
      console.log(`   Provider: ${response.provider}`);
      console.log(`   Model: ${response.model}`);
      console.log(`   Task Type: ${response.taskType}`);
      console.log(`   Response Time: ${duration}ms`);
      console.log(`   Context Length: ${response.contextLength}`);
      console.log(`   Timestamp: ${response.timestamp}`);
    } else {
      console.log(`\n⏱️  Response time: ${duration}ms`);
    }

  } catch (error) {
    console.error(`💬 Chat failed: ${error.message}`);
  }
}

/**
 * Handle providers command
 */
async function handleProvidersCommand(ai, options) {
  console.log('\n📊 Provider Status & Statistics:');
  
  // Show visual status first
  ai.displayProviderStatus();
  
  if (options.verbose) {
    console.log('\n📈 Detailed Statistics:');
    const stats = ai.router.getProviderStats();

    for (const [provider, data] of Object.entries(stats)) {
      console.log(`\n📋 ${provider.toUpperCase()} Statistics:`);
      console.log(`   Requests: ${data.requests}`);
      console.log(`   Success Rate: ${data.successRate}`);
      console.log(`   Avg Response Time: ${data.avgResponseTime?.toFixed(2) || 0}ms`);
      console.log(`   Total Cost: $${data.totalCost?.toFixed(4) || '0.0000'}`);
      
      if (data.capabilities) {
        const features = Object.entries(data.capabilities)
          .filter(([_, v]) => v === true)
          .map(([k, _]) => k)
          .join(', ');
        console.log(`   Features: ${features || 'None'}`);
      }
    }
    
    console.log('\n💡 Use --task flags to influence provider selection:');
    console.log('   --task=fast    → Prioritizes speed (Mistral preferred)');
    console.log('   --task=complex → Uses best reasoning model (Claude/Gemini fallback)');
    console.log('   --task=code    → Optimizes for programming tasks');
  }
}

/**
 * Handle models command
 */
async function handleModelsCommand(ai, options) {
  console.log('\n📋 Available Models:');
  
  for (const [providerName, provider] of ai.router.providers) {
    try {
      if (provider.isAvailable) {
        console.log(`\n${providerName.toUpperCase()}:`);
        
        if (provider.getAvailableModels) {
          const models = await provider.getAvailableModels();
          models.forEach(model => console.log(`  - ${model}`));
        } else if (provider.models) {
          Object.entries(provider.models).forEach(([type, model]) => {
            console.log(`  - ${model} (${type})`);
          });
        }
      }
    } catch (error) {
      console.warn(`⚠️  Failed to get models for ${providerName}: ${error.message}`);
    }
  }
}

/**
 * Handle file command
 */
async function handleFileCommand(ai, filePath, options) {
  if (!filePath.trim()) {
    console.log('❌ Please provide a file path');
    console.log('Usage: multi-ai file <path> [--task=type]');
    return;
  }

  try {
    console.log(`📄 Processing file: ${filePath}`);
    
    const result = await ai.processFile(filePath, options);
    
    console.log(`\n[${result.provider}] Analysis:`);
    console.log(result.response);
    
    if (options.verbose) {
      console.log(`\n📊 File processed successfully`);
      console.log(`   Provider: ${result.provider}`);
      console.log(`   Response time: ${result.responseTime}ms`);
    }

  } catch (error) {
    console.error(`📄 File processing failed: ${error.message}`);
  }
}

/**
 * Handle directory command
 */
async function handleDirectoryCommand(ai, dirPath, options) {
  if (!dirPath.trim()) {
    console.log('❌ Please provide a directory path');
    console.log('Usage: multi-ai dir <path> [--task=type]');
    return;
  }

  console.log(`📁 Processing directory: ${dirPath}`);
  console.log('This feature is not yet implemented in the consolidated version.');
  console.log('Coming soon in v2.1.0');
}

/**
 * Handle health command
 */
async function handleHealthCommand(ai, options) {
  console.log('\n🏥 System Health Check:');
  
  // Use new visual status display
  ai.displayProviderStatus();
  
  if (options.verbose) {
    const healthChecks = await ai.router.healthCheckAll();
    console.log('\n🔍 Detailed Health Information:');
    
    for (const [provider, health] of Object.entries(healthChecks)) {
      console.log(`\n📋 ${provider.toUpperCase()}:`);
      console.log(`   Status: ${health.status}`);
      
      if (health.models !== undefined) {
        console.log(`   Models: ${health.models}`);
      }
      
      if (health.error) {
        console.log(`   Error: ${health.error}`);
      }
      
      if (health.version) {
        console.log(`   Version: ${health.version}`);
      }
    }
  }
  
  const status = ai.getProviderStatus();
  if (status.summary.available === 0) {
    console.log('\n⚠️  No providers are currently available. Check your configuration.');
    console.log('💡 Make sure Ollama is running: ollama serve');
  } else if (!status.ollama.available) {
    console.log('\n⚠️  Primary provider (Mistral) unavailable - using fallback providers');
    console.log('💡 Start Ollama for cost-optimized operation: ollama serve');
  }
}

/**
 * Handle status command
 */
async function handleStatusCommand(ai, options) {
  console.log('\n📊 Comprehensive System Status:');
  
  const status = await ai.getSystemStatus();
  
  console.log(`\n🚀 System Information:`);
  console.log(`   Version: ${status.version}`);
  console.log(`   Timestamp: ${status.timestamp}`);
  
  console.log(`\n🤖 Providers:`);
  console.log(`   Total: ${status.providers.total}`);
  console.log(`   Healthy: ${status.providers.healthy}`);
  
  console.log(`\n💾 Resources:`);
  console.log(`   Knowledge Base Entries: ${status.resources.knowledgeBase.entries}`);
  console.log(`   Context Length: ${status.resources.context.length}/${status.resources.context.maxLength}`);
  console.log(`   Memory Usage: ${Math.round(status.resources.knowledgeBase.memoryUsage.heapUsed / 1024 / 1024)}MB`);

  if (options.verbose) {
    console.log(`\n📈 Recent Performance:`);
    status.performance.recentRequests.forEach(req => {
      console.log(`   ${req.provider}: ${req.responseTime}ms (${req.success ? 'success' : 'failed'})`);
    });
  }
}

/**
 * Handle config command
 */
async function handleConfigCommand(ai, args, options) {
  const subcommand = args[0];
  const configPath = args[1];

  switch (subcommand) {
    case 'save':
      ai.saveConfig(configPath);
      break;
      
    case 'load':
      console.log('Configuration is automatically loaded on startup');
      break;
      
    default:
      console.log('Usage: multi-ai config save/load [path]');
  }
}

/**
 * Handle clear command
 */
async function handleClearCommand(ai, options) {
  ai.clearContext();
  console.log('✅ Conversation context cleared');
  
  if (options.verbose) {
    console.log('All conversation history has been removed from memory.');
  }
}

// Run CLI if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runCLI().catch(error => {
    console.error('❌ CLI Error:', error.message);
    process.exit(1);
  });
}

export { runCLI };