#!/bin/bash
# Quick Iris Runner - Run without global installation
# Usage: ./run-iris.sh help
# Usage: ./run-iris.sh chat "Hello"

cd "$(dirname "$0")"

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install --prefer-offline --no-audit --progress=false
fi

# Run Iris with all arguments
node src/enhanced-ai.js "$@"