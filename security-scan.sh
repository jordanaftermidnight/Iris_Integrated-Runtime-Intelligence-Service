#!/bin/bash

# IRIS Security Scanner
# Scans for potential security issues before deployment

echo "🔒 IRIS Security Scanner"
echo "========================"

# Check for exposed API keys (excluding documentation and examples)
echo "🔍 Scanning for API keys..."
if grep -r "gsk_[A-Za-z0-9]\{20,\}\|AIza[A-Za-z0-9]\{20,\}\|sk-[A-Za-z0-9]\{20,\}\|sk-ant-[A-Za-z0-9]\{20,\}" . --exclude-dir=node_modules --exclude="*.md" --exclude="*.example.*" --exclude=".git" --exclude="security-scan.sh" 2>/dev/null; then
    echo "❌ CRITICAL: Real API keys found in code!"
    exit 1
else
    echo "✅ No real API keys found in code"
fi

# Check for hardcoded secrets (excluding common false positives)
echo "🔍 Scanning for hardcoded secrets..."
# Exclude: costPerToken, maxTokens, getToken, token counting, API documentation, config keys
if grep -ri "password\s*=\|secret\s*=\|apikey\s*=\|api_key\s*=" . --include="*.js" --exclude-dir=node_modules | \
   grep -v "example\|template\|comment\|costPerToken\|maxTokens\|getToken\|sanitizeApiKeys\|process\.env" | head -5; then
    echo "⚠️  WARNING: Potential hardcoded secrets found"
else
    echo "✅ No obvious hardcoded secrets"
fi

# Check .gitignore exists
echo "🔍 Checking .gitignore..."
if [ -f ".gitignore" ]; then
    echo "✅ .gitignore exists"
    if grep -q "\.env" .gitignore; then
        echo "✅ .env files ignored"
    else
        echo "⚠️  WARNING: .env not in .gitignore"
    fi
else
    echo "❌ CRITICAL: .gitignore missing!"
    exit 1
fi

# Check for dangerous functions (excluding ESLint config and safe usage)
echo "🔍 Scanning for dangerous functions..."
# Exclude ESLint rules and comments about eval
if grep -r "eval\|Function(" . --include="*.js" --exclude-dir=node_modules --exclude=".eslintrc.js" 2>/dev/null | \
   grep -v "no-eval\|eslint\|comment\|//.*eval" | head -5; then
    echo "⚠️  WARNING: Dangerous functions found"
else
    echo "✅ No dangerous functions detected"
fi

# Check file permissions
echo "🔍 Checking file permissions..."
if find . -type f -name "*.js" -perm +111 2>/dev/null | head -5; then
    echo "⚠️  WARNING: Executable JavaScript files found"
else
    echo "✅ File permissions look good"
fi

echo ""
echo "🔒 Security scan complete!"
echo "💡 Run this script before committing: ./security-scan.sh"