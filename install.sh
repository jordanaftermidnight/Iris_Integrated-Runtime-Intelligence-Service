#!/bin/bash

# One-line installer for Multi-AI MCP Integration
# Usage: curl -fsSL https://raw.githubusercontent.com/your-username/multi-ai-mcp/main/install.sh | bash

set -e

echo "🚀 Multi-AI MCP Integration - One-Line Installer"
echo "================================================"

# Configuration
REPO_URL="https://github.com/your-username/multi-ai-mcp.git"
INSTALL_DIR="$HOME/multi-ai-mcp"

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Git
    if ! command -v git &> /dev/null; then
        print_error "Git is required but not installed. Please install Git first."
        exit 1
    fi
    
    # Check Python 3.8+
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3.8+ is required but not installed. Please install Python first."
        exit 1
    fi
    
    if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        print_error "Python 3.8+ is required. Current version: $(python3 --version)"
        exit 1
    fi
    
    print_status "Prerequisites check passed"
}

# Clone repository
clone_repo() {
    print_status "Cloning repository..."
    
    # Remove existing installation if present
    if [[ -d "$INSTALL_DIR" ]]; then
        print_warning "Existing installation found. Removing..."
        rm -rf "$INSTALL_DIR"
    fi
    
    # Clone the repository
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    
    print_status "Repository cloned to $INSTALL_DIR"
}

# Run setup
run_setup() {
    print_status "Running setup script..."
    
    # Make setup script executable
    chmod +x setup.sh
    
    # Run setup
    ./setup.sh
}

# Main installer
main() {
    echo
    print_status "Starting one-line installation..."
    
    check_prerequisites
    clone_repo
    run_setup
    
    echo
    echo "🎉 One-line installation completed!"
    echo
    echo "Installation location: $INSTALL_DIR"
    echo
    echo "To complete setup:"
    echo "1. cd $INSTALL_DIR"
    echo "2. Edit .env file to add your GOOGLE_API_KEY"
    echo "3. Restart Claude Code"
    echo
    echo "For manual setup, run: $INSTALL_DIR/setup.sh"
}

# Handle errors
trap 'print_error "Installation failed. Please check the error messages above."' ERR

# Run installer
main "$@"