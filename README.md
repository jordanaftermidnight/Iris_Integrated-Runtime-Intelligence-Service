# 🚀 Iris - Integrated Runtime Intelligence Service

**Professional AI Development Assistant with Multi-Provider Intelligence**

[![Version](https://img.shields.io/badge/version-2.4.0-blue.svg)](package.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![IDE Features](https://img.shields.io/badge/IDE%20Features-✅%20Integrated-blue.svg)]()

---

## 🎯 **What is Iris?**

Iris is a **professional AI development assistant** that provides **IDE-level intelligence** with multi-provider AI consultation. It combines the power of 5 AI providers with intelligent caching, local processing options, and universal compatibility across any editor or platform.

### **🚀 Key Features**
- **🧠 Multi-AI Intelligence** - 5 providers with intelligent routing
- **⚡ 85%+ Cache Hit Rate** - Instant responses for repeated queries  
- **🏠 Local Processing** - Privacy-focused with Ollama support
- **🔧 Professional IDE Tools** - Code completion, debugging, refactoring
- **🔄 Universal Compatibility** - Works with any editor/IDE
- **💰 Cost Optimized** - Mistral-first approach minimizes API costs

---

## 🛠️ **Quick Start**

### **Installation**

#### **Option 1: Install from GitHub (Recommended)**
```bash
# Clone and install
git clone https://github.com/jordanaftermidnight/multi-ai-integration-CLI.git
cd multi-ai-integration-CLI
npm install
npm install -g .

# Verify installation
iris --version
iris help
```

#### **Option 2: Direct npm install (when published)**
```bash
# Install globally (when available on npm)
npm install -g iris-ai

# Verify installation
iris --version
```

#### **Option 3: Run without global install**
```bash
# Clone and run directly
git clone https://github.com/jordanaftermidnight/multi-ai-integration-CLI.git
cd multi-ai-integration-CLI
npm install
npm start help
```

### **Basic Usage**
```bash
# Chat with AI
iris chat "Explain async/await in JavaScript"

# Get code completion
iris complete ./src/app.js 42 15

# Generate commit message
iris commit

# Analyze workspace
iris workspace
```

### **Setup AI Providers** (Optional)
```bash
# Set API keys for enhanced capabilities
export OPENAI_API_KEY="your-key"    # GPT-4o, o1-preview
export GROQ_API_KEY="your-key"      # Ultra-fast inference
export GEMINI_API_KEY="your-key"    # Multimodal analysis
export ANTHROPIC_API_KEY="your-key" # Advanced reasoning

# Start local AI (free, private)
ollama serve  # Runs Mistral/Qwen locally
```

---

## 💻 **Professional IDE Features**

### **🧠 Smart Code Intelligence**
```bash
# Intelligent code completion
iris complete ./src/utils.js 25 10

# Explain complex code
iris explain ./algorithms/sort.py 15 35

# Smart refactoring suggestions
iris refactor ./api/routes.js 100 150
```

### **🔧 Development Workflow**
```bash
# Generate intelligent commit messages
iris commit

# Comprehensive code review
iris review ./components/Header.jsx

# Generate test cases
iris test ./math-utils.js calculateAverage

# Debug with context
iris debug ./app.js "TypeError: Cannot read property" trace.log
```

### **🏗️ Project Intelligence**
```bash
# Analyze entire workspace
iris workspace

# Get file context and dependencies
iris context ./src/database/models/User.js

# Check project health
iris health
```

---

## 🎯 **Multi-Provider AI**

Iris intelligently routes queries to the best AI provider:

| Provider | Strengths | Cost | Speed |
|----------|-----------|------|-------|
| **Ollama** | Local, Private, Free | 🆓 Free | ⚡ Fast |
| **Groq** | Ultra-fast inference | 💰 Low | 🚀 Ultra-fast |
| **OpenAI** | Advanced reasoning | 💰💰 High | 🐌 Slow |
| **Gemini** | Multimodal analysis | 💰 Medium | ⚡ Fast |
| **Claude** | General purpose | 💰💰 High | 🐌 Medium |

### **Smart Routing Examples**
```bash
# Coding tasks → Ollama (fast, free) → OpenAI (complex)
iris chat "Write a REST API" --task=code

# Creative tasks → Ollama → Gemini (multimodal)
iris chat "Design a logo concept" --task=creative

# Fast queries → Groq (ultra-fast)
iris chat "What is 2+2?" --task=fast

# Force specific provider
iris chat "Analyze this image" --provider=gemini
```

---

## 📚 **Command Reference**

### **Core Commands**
```bash
iris chat <message>              # Chat with smart provider selection
iris providers                   # Show provider status
iris health                      # System health check
iris help                        # Show all commands
```

### **IDE Integration**
```bash
iris complete <file> <line> <col> # Code completion
iris explain <file> [start] [end] # Code explanation
iris refactor <file> <start> <end> # Refactoring suggestions
iris debug <file> [error] [trace] # Debug assistance
iris commit                       # Smart commit messages
iris review <file> [start] [end]  # Code review
iris test <file> [function]       # Generate tests
iris workspace                    # Project analysis
iris context <file>               # File context
```

### **File Processing**
```bash
iris file <path>                 # Analyze single file
iris dir <path>                  # Process directory
```

---

## ⚙️ **Configuration**

### **Environment Variables**
```bash
# Optional API keys (Ollama works without any keys)
export OPENAI_API_KEY="sk-..."      # OpenAI GPT-4o, o1
export GROQ_API_KEY="gsk_..."       # Groq Llama/Mixtral
export GEMINI_API_KEY="AI..."       # Google Gemini
export ANTHROPIC_API_KEY="sk-ant-..." # Claude
export OLLAMA_HOST="http://localhost:11434" # Ollama server
```

### **Configuration Files**
```bash
# Copy example configs
cp config/gemini-config.example.json config/gemini-config.json
cp config/llama2-config.example.json config/llama2-config.json

# Edit with your preferences
# See config/ directory for examples
```

---

## 🚀 **Why Choose Iris?**

### **🆚 vs Traditional IDE Extensions**
- ✅ **Multi-provider AI** vs single provider
- ✅ **85%+ cache hit rate** vs no caching
- ✅ **Works everywhere** vs editor-specific
- ✅ **Local processing** vs cloud-only
- ✅ **Cost optimized** vs expensive API usage

### **🆚 vs Other AI Tools**
- ✅ **Intelligent routing** vs manual provider selection
- ✅ **Project-wide context** vs single file awareness
- ✅ **Professional features** vs basic chat
- ✅ **Performance optimization** vs no caching
- ✅ **Privacy options** vs cloud-dependent

---

## 📄 **Documentation**

- **[Enhanced README](README_IRIS_ENHANCED.md)** - Comprehensive feature guide
- **[Optimized Features](README_OPTIMIZED.md)** - Performance optimization details
- **[Quick Start](QUICKSTART.md)** - Get started in 5 minutes
- **[Examples](examples/)** - Usage examples and integrations
- **[Configuration](config/)** - Setup and customization

---

## 🤝 **Contributing**

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📧 **Support**

- **Issues**: [GitHub Issues](https://github.com/jordanaftermidnight/multi-ai-integration-CLI/issues)
- **Email**: jordanaftermidnight@users.noreply.github.com

---

## 📜 **License**

MIT License - see [LICENSE](LICENSE) file for details.

---

**Transform your development workflow with professional AI intelligence! 🚀**