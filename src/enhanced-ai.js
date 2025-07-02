#!/usr/bin/env node

/**
 * Multi-AI Integration CLI - Global Entry Point
 * Single command execution: multi-ai
 */

import MultiAI from './index.js';
import { runCLI } from './cli.js';

// Export the main class for programmatic usage
export { MultiAI as EnhancedAI };
export default MultiAI;

// Always run CLI when this file is executed
runCLI().catch(error => {
  console.error('❌ CLI Error:', error.message);
  process.exit(1);
});