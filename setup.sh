#!/bin/bash

# Multi-AI MCP Integration Setup Script
# Supports macOS, Linux (Ubuntu/Debian, CentOS/RHEL)

set -e

echo "🚀 Multi-AI MCP Integration Setup"
echo "=================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ -f /etc/debian_version ]]; then
        OS="debian"
    elif [[ -f /etc/redhat-release ]]; then
        OS="redhat"
    else
        OS="unknown"
    fi
    print_status "Detected OS: $OS"
}

# Check Python installation
check_python() {
    print_step "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
        print_status "Python $PYTHON_VERSION found"
        
        # Check if version is 3.8+
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_status "Python version is compatible (3.8+)"
        else
            print_error "Python 3.8+ required. Please upgrade Python."
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8+"
        exit 1
    fi
}

# Install Ollama
install_ollama() {
    print_step "Installing Ollama..."
    
    if command -v ollama &> /dev/null; then
        print_status "Ollama already installed"
    else
        case $OS in
            "macos")
                if command -v brew &> /dev/null; then
                    brew install ollama
                else
                    curl -fsSL https://ollama.com/install.sh | sh
                fi
                ;;
            "debian"|"redhat"|"unknown")
                curl -fsSL https://ollama.com/install.sh | sh
                ;;
        esac
        print_status "Ollama installed successfully"
    fi
}

# Setup Python virtual environment
setup_venv() {
    print_step "Setting up Python virtual environment..."
    
    if [[ ! -d "venv" ]]; then
        python3 -m venv venv
        print_status "Virtual environment created"
    fi
    
    source venv/bin/activate
    print_status "Virtual environment activated"
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    pip install -r requirements.txt
    print_status "Python dependencies installed"
}

# Setup configuration files
setup_config() {
    print_step "Setting up configuration files..."
    
    # Copy example configs if they don't exist
    for config in config/*.json; do
        if [[ -f "$config.example" && ! -f "$config" ]]; then
            cp "$config.example" "$config"
            print_status "Created $config from template"
        fi
    done
    
    # Setup .env file
    if [[ ! -f ".env" ]]; then
        cp .env.example .env
        print_status "Created .env file from template"
        print_warning "Please edit .env file to add your GOOGLE_API_KEY"
    fi
}

# Start Ollama service
start_ollama() {
    print_step "Starting Ollama service..."
    
    # Check if Ollama is already running
    if pgrep -f "ollama serve" > /dev/null; then
        print_status "Ollama service already running"
    else
        case $OS in
            "macos")
                # Start Ollama in background
                nohup ollama serve > /dev/null 2>&1 &
                sleep 3
                ;;
            "debian"|"redhat")
                # Try to start as systemd service first
                if systemctl is-enabled ollama &> /dev/null; then
                    sudo systemctl start ollama
                else
                    nohup ollama serve > /dev/null 2>&1 &
                    sleep 3
                fi
                ;;
            "unknown")
                nohup ollama serve > /dev/null 2>&1 &
                sleep 3
                ;;
        esac
        print_status "Ollama service started"
    fi
}

# Download recommended models
download_models() {
    print_step "Downloading recommended Llama models..."
    
    # Check available models
    AVAILABLE_MODELS=$(ollama list | tail -n +2 | awk '{print $1}' || echo "")
    
    # Download llama3.2:3b if not present (fast, efficient)
    if [[ ! "$AVAILABLE_MODELS" =~ "llama3.2:3b" ]]; then
        print_status "Downloading llama3.2:3b (this may take a few minutes)..."
        ollama pull llama3.2:3b
    else
        print_status "llama3.2:3b already available"
    fi
    
    # Optionally download llama2:7b (more capable)
    read -p "Download llama2:7b model? (~4GB) [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ ! "$AVAILABLE_MODELS" =~ "llama2:7b" ]]; then
            print_status "Downloading llama2:7b (this may take 10+ minutes)..."
            ollama pull llama2:7b
        else
            print_status "llama2:7b already available"
        fi
    fi
    
    print_status "Model download completed"
}

# Setup Claude Code MCP integration
setup_claude_integration() {
    print_step "Setting up Claude Code MCP integration..."
    
    CLAUDE_CONFIG_DIR="$HOME/.anthropic/claude-code"
    MCP_CONFIG="$CLAUDE_CONFIG_DIR/mcp_servers.json"
    
    # Create Claude config directory if it doesn't exist
    mkdir -p "$CLAUDE_CONFIG_DIR"
    
    # Create or update MCP servers configuration
    cat > "$MCP_CONFIG" << EOF
{
  "mcpServers": {
    "multi-ai-consultant": {
      "command": "python3",
      "args": ["$(pwd)/src/mcp_server.py"],
      "cwd": "$(pwd)",
      "env": {
        "GEMINI_CONFIG_PATH": "$(pwd)/config/gemini-config.json",
        "LLAMA2_CONFIG_PATH": "$(pwd)/config/llama2-config.json"
      }
    }
  }
}
EOF
    
    print_status "Claude Code MCP configuration created"
    print_warning "Please restart Claude Code to load the new MCP server"
}

# Test the installation
test_installation() {
    print_step "Testing installation..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Run test script
    if python3 tests/test_system.py; then
        print_status "Installation test passed!"
    else
        print_warning "Some tests failed. Check the output above."
    fi
}

# Main installation flow
main() {
    echo
    print_step "Starting Multi-AI MCP Integration setup..."
    
    detect_os
    check_python
    install_ollama
    setup_venv
    setup_config
    start_ollama
    download_models
    setup_claude_integration
    test_installation
    
    echo
    echo "🎉 Setup completed successfully!"
    echo
    echo "Next steps:"
    echo "1. Edit .env file to add your GOOGLE_API_KEY"
    echo "2. Restart Claude Code to load new MCP tools"
    echo "3. Test with: 'Get an AI second opinion on this code'"
    echo
    echo "Available tools in Claude Code:"
    echo "• consult_multi_ai - Smart AI selection"
    echo "• consult_gemini - Direct Gemini consultation"
    echo "• consult_llama2 - Direct Llama2 consultation"
    echo "• compare_ai_providers - Provider comparison"
    echo "• ai_system_status - System health check"
    echo "• detect_uncertainty - Uncertainty analysis"
    echo
}

# Run main function
main "$@"