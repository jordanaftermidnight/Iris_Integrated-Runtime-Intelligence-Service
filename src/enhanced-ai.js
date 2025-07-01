#!/usr/bin/env node

/**
 * Enhanced Multi-AI Integration CLI
 * Backward compatibility wrapper and CLI entry point
 * 
 * This file maintains compatibility with the original enhanced-ai.js
 * while using the new modular architecture.
 */

import MultiAI from './index.js';
import { runCLI } from './cli.js';

// Export the main class for backward compatibility
export { MultiAI as EnhancedAI };
export default MultiAI;

// Run CLI if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runCLI().catch(error => {
    console.error('❌ CLI Error:', error.message);
    process.exit(1);
  });
}