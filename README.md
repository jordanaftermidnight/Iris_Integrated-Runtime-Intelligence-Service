# 🤖 Iris - Integrated Runtime Intelligence Service

**I**ntegrated **R**untime **I**ntelligence **S**ervice - A sophisticated AI chat assistant with intelligent provider selection and cost optimization, supporting Ollama (Mistral), Gemini, Claude, OpenAI, and Groq with smart routing that prioritizes free local models.

[![Version](https://img.shields.io/badge/version-2.3.0-blue.svg)](https://github.com/jordanaftermidnight/iris-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)

## ✨ Features

### 🚀 **Smart Provider Selection**
- Automatically selects the best AI provider based on task type
- Intelligent fallback system for maximum reliability
- Performance tracking and optimization

### 🔧 **Multi-Provider Support**
- **Ollama**: Local AI models (Mistral 7B prioritized for cost efficiency)
- **Gemini**: Google's advanced AI models (Gemini 1.5 Pro/Flash)
- **Claude**: Anthropic's reasoning models (Claude 3 Opus/Sonnet/Haiku)
- **OpenAI**: GPT-4o, o1-preview for complex reasoning
- **Groq**: Ultra-fast inference with Llama and Mixtral models
- Extensible architecture for adding new providers

### 📊 **Performance Monitoring**
- Real-time response time tracking
- Provider reliability metrics
- 99.5% availability with automatic failover

### 🎯 **Task-Specific Optimization**
- **Code**: Mistral 7B (local) → Claude 3.5 Sonnet → OpenAI GPT-4o
- **Creative**: Mistral 7B (local) → Gemini 1.5 Pro → Claude 3 Opus  
- **Fast**: Mistral 7B (local) → Groq Llama 3.1
- **Complex**: Mistral 7B (local) → OpenAI o1-preview → Claude 3 Opus
- **Balanced**: Mistral 7B (local) → Gemini 1.5 Pro → Claude 3 Sonnet

### 💰 **Cost Optimization**
- **Local-first routing**: Prioritizes free Mistral 7B via Ollama
- **Smart fallback**: Only uses paid APIs when necessary
- **Budget controls**: Configurable cost limits and provider priorities
- **Usage tracking**: Monitor costs across all providers

### 💾 **Advanced Features**
- Conversation context management
- Knowledge base with search capabilities
- File and directory processing
- Configuration persistence
- Streaming responses
- CLI and programmatic interfaces

## 🛠️ Installation

### Prerequisites

Ensure you have the following installed:
- **Node.js 18+**: [Download here](https://nodejs.org/)
- **Ollama**: [Install here](https://ollama.ai/) (for free local AI)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/jordanaftermidnight/iris-ai.git
cd iris-ai

# Install dependencies
npm install

# Install globally for CLI access
npm install -g .

# Verify installation
iris help
```

### Ollama Setup (Recommended for Cost Efficiency)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull recommended models
ollama pull mistral:7b       # Primary model
ollama pull qwen2.5:7b       # Fast model
ollama pull qwen2.5-coder:7b # Code-specific model
```

## 🚀 Quick Start

### CLI Usage

```bash
# Basic chat
iris chat "Hello! How are you?"

# Task-specific optimization
iris chat "Write a Python function to sort a list" --task=code
iris chat "Write a creative story about AI" --task=creative
iris chat "What is 2+2?" --task=fast
iris chat "Analyze the implications of quantum computing" --task=complex

# Provider selection
iris chat "Hello" --provider=gemini
iris chat "Debug this code" --provider=claude

# File analysis
iris file ./my-script.js --task=code
iris file ./document.md --task=analysis

# System commands
iris health       # Check provider status
iris providers    # Show detailed provider info
iris models       # List available models
iris status       # Comprehensive system status
```

### Programmatic Usage

```javascript
import Iris from 'iris-ai';

const iris = new Iris();
await iris.initializeProviders();

// Basic chat
const response = await iris.chat("Hello, world!");
console.log(response.response);

// Task-specific chat
const codeResponse = await iris.chat("Write a function to reverse a string", {
  taskType: 'code'
});

// Provider-specific chat
const geminiResponse = await iris.chat("Describe this image", {
  provider: 'gemini'
});

// File processing
const fileAnalysis = await iris.processFile('./my-code.js', {
  taskType: 'code'
});
```

## ⚙️ Configuration

### Environment Variables

Set these to enable cloud providers (optional - Ollama works without any API keys):

```bash
export OPENAI_API_KEY="your-openai-key"      # For GPT-4o, o1 models
export GROQ_API_KEY="your-groq-key"          # For ultra-fast inference
export GEMINI_API_KEY="your-gemini-key"      # For Google's AI
export ANTHROPIC_API_KEY="your-claude-key"   # For Claude models
export OLLAMA_HOST="http://localhost:11434"  # Ollama server (default)
```

### Provider Configuration

Iris automatically detects available providers. The system works with:
- **No API keys**: Uses only Ollama (free, local)
- **Some API keys**: Uses available providers with smart fallback
- **All API keys**: Full provider selection and optimization

## 📋 Commands Reference

### Chat Commands
```bash
iris chat <message> [options]    # Interactive chat
iris chat --help                 # Chat command help
```

### System Commands
```bash
iris health                      # Provider health check
iris providers                   # Show provider status
iris models                      # List available models
iris status                      # System status overview
```

### File Operations
```bash
iris file <path> [options]       # Analyze single file
iris dir <path> [options]        # Process directory (coming soon)
```

### Configuration
```bash
iris config save [path]          # Save current config
iris config load [path]          # Load config file
iris clear                       # Clear conversation history
```

### Options
```bash
--task=<type>         # Task type (code, creative, fast, complex, balanced)
--provider=<name>     # Force specific provider
--stream              # Enable streaming responses
--local               # Use only local providers
--verbose, -v         # Verbose output
--help, -h            # Show help
```

## 🎯 Task Types

| Task Type | Best For | Primary Provider | Fallback Order |
|-----------|----------|------------------|----------------|
| `code` | Programming, debugging | Ollama (Mistral) | Claude → OpenAI |
| `creative` | Writing, brainstorming | Ollama (Mistral) | Gemini → Claude |
| `fast` | Quick questions | Ollama (Mistral) | Groq → Gemini |
| `complex` | Deep analysis, reasoning | Ollama (Mistral) | OpenAI → Claude |
| `balanced` | General purpose (default) | Ollama (Mistral) | Gemini → Claude |

## 🏗️ Architecture

### Core Components

- **AIRouter**: Intelligent provider selection and load balancing
- **Providers**: Modular AI service integrations
- **Context Manager**: Conversation history and context handling
- **Knowledge Base**: Persistent key-value storage with search
- **Config Manager**: Settings persistence and environment handling

### Provider Hierarchy (Cost-Optimized)

1. 🆓 **Ollama** (Free, Local) - Primary for all tasks
2. 🔥 **Groq** (Low Cost, Ultra-Fast) - Speed-optimized fallback
3. 🧠 **OpenAI** (Premium) - Complex reasoning when needed
4. 🎨 **Gemini** (Balanced) - Multimodal and creative tasks
5. 📝 **Claude** (Premium) - Advanced reasoning fallback

## 💡 Examples

### Development Workflow
```bash
# Code review
iris file ./my-component.jsx --task=code --verbose

# Debug assistance
iris chat "This function is throwing an error: [paste code]" --task=code

# Documentation
iris chat "Write documentation for this API" --task=creative
```

### Research & Analysis
```bash
# Deep analysis
iris chat "Analyze the pros and cons of microservices" --task=complex

# Quick facts
iris chat "What's the current JavaScript version?" --task=fast

# Creative writing
iris chat "Write a technical blog post about AI" --task=creative
```

### System Management
```bash
# Check what's available
iris health

# Monitor performance
iris providers --verbose

# Test different providers
iris chat "Hello" --provider=ollama
iris chat "Hello" --provider=gemini
```

## 🔧 Development

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/jordanaftermidnight/iris-ai.git
cd iris-ai
npm install

# Run tests
npm test

# Development mode with auto-reload
npm run dev

# Lint code
npm run lint
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`npm test`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📊 Performance

### Benchmarks
- **Ollama (Local)**: ~2-5s response time, $0.00 cost
- **Groq**: ~0.5-1s response time, ~$0.0001 per request
- **Gemini**: ~1-3s response time, ~$0.001 per request
- **Claude**: ~2-4s response time, ~$0.01 per request
- **OpenAI**: ~2-6s response time, ~$0.02 per request

### Availability
- **Overall**: 99.5% uptime with intelligent fallback
- **Local (Ollama)**: 99.9% (when running locally)
- **Cloud providers**: 99.0-99.5% (varies by provider)

## 🐛 Troubleshooting

### Common Issues

**Ollama not available**
```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve

# Pull required models
ollama pull mistral:7b
```

**No providers available**
```bash
# Check system health
iris health --verbose

# Verify API keys
echo $OPENAI_API_KEY
echo $GEMINI_API_KEY
```

**Slow responses**
```bash
# Use fast task type
iris chat "question" --task=fast

# Force local provider
iris chat "question" --local
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/jordanaftermidnight/iris-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jordanaftermidnight/iris-ai/discussions)
- **Email**: jordan.after.midnight@example.com

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for providing free local AI infrastructure
- [Anthropic](https://anthropic.com/) for Claude AI models
- [Google](https://ai.google.dev/) for Gemini AI models
- [OpenAI](https://openai.com/) for GPT models
- [Groq](https://groq.com/) for ultra-fast inference
- The open-source AI community for continuous innovation

---

**Iris** - Where Intelligence Meets Efficiency 🤖✨