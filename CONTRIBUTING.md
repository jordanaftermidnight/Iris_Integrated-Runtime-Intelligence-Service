# 🤝 Contributing to Multi-AI MCP Integration

Thank you for your interest in contributing to the Multi-AI MCP Integration project! This guide will help you get started with contributing code, documentation, or reporting issues.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## 📜 Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- **Be respectful**: Treat all community members with respect and kindness
- **Be inclusive**: Welcome newcomers and help them succeed
- **Be collaborative**: Work together to improve the project
- **Be constructive**: Provide helpful feedback and suggestions
- **Be patient**: Remember that everyone is learning and growing

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:
- Python 3.8 or higher
- Git
- Basic understanding of async Python programming
- Familiarity with AI/LLM concepts
- Understanding of MCP (Model Context Protocol)

### Quick Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/multi-ai-mcp.git
   cd multi-ai-mcp
   ```

2. **Set up development environment**
   ```bash
   ./setup.sh
   source venv/bin/activate
   pip install -r requirements-dev.txt
   ```

3. **Verify setup**
   ```bash
   python3 tests/test_system.py
   ```

## 🛠️ Development Setup

### Development Dependencies

Install additional development tools:
```bash
pip install -r requirements-dev.txt
```

This includes:
- `pytest` - Testing framework
- `pytest-asyncio` - Async testing support
- `black` - Code formatting
- `flake8` - Code linting
- `mypy` - Type checking
- `pre-commit` - Git hooks

### Pre-commit Hooks

Set up pre-commit hooks to ensure code quality:
```bash
pre-commit install
```

This will automatically run code formatting and linting before each commit.

### Environment Configuration

Create a development `.env` file:
```bash
cp .env.example .env.dev
# Edit .env.dev with your development configuration
```

## 🎯 How to Contribute

### 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected vs actual behavior**
4. **Environment information**:
   ```bash
   python3 --version
   ollama --version
   uname -a
   ```
5. **Error logs** and stack traces
6. **Configuration files** (remove sensitive data)

Use our bug report template:
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Environment**
- OS: [e.g. macOS 14.0]
- Python version: [e.g. 3.11]
- Ollama version: [e.g. 0.1.25]

**Additional context**
Add any other context about the problem here.
```

### 💡 Suggesting Features

For feature requests, please:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** clearly
3. **Explain the expected behavior**
4. **Consider implementation complexity**
5. **Discuss alternatives** you've considered

### 🔧 Code Contributions

#### Types of Contributions Welcome

- **Bug fixes**: Fix existing issues
- **New features**: Add new AI providers, tools, or capabilities
- **Performance improvements**: Optimize existing code
- **Documentation**: Improve guides, examples, or API docs
- **Tests**: Add or improve test coverage
- **Examples**: Create new usage examples

#### Getting Assigned

1. **Comment on issues** you'd like to work on
2. **Wait for assignment** before starting work
3. **Ask questions** if requirements are unclear
4. **Provide time estimates** for completion

## 📝 Development Guidelines

### Code Style

We follow PEP 8 with some specific guidelines:

```python
# Good: Clear, descriptive names
async def consult_multiple_providers(request: MultiAIConsultationRequest) -> Dict[str, Any]:
    """Consult multiple AI providers with the given request."""
    pass

# Good: Type hints for all functions
def calculate_provider_score(
    success_rate: float, 
    response_time: float
) -> float:
    return success_rate * (1.0 - min(response_time / 10.0, 0.5))

# Good: Proper error handling
try:
    result = await provider.consult(request)
except ProviderError as e:
    logger.error(f"Provider consultation failed: {e}")
    raise ConsultationError(f"Failed to consult {provider.name}") from e
```

### Code Organization

- **Keep functions small** and focused on single responsibilities
- **Use descriptive variable names** that explain intent
- **Add docstrings** to all public functions and classes
- **Handle errors gracefully** with appropriate exception types
- **Log important events** at appropriate levels

### Performance Considerations

- **Use async/await** for I/O operations
- **Implement caching** where appropriate
- **Consider rate limiting** for external APIs
- **Monitor resource usage** in resource-intensive operations
- **Profile performance** for critical paths

### Security Guidelines

- **Never commit secrets** or API keys
- **Use environment variables** for configuration
- **Validate all inputs** from external sources
- **Implement proper error handling** to avoid information leakage
- **Follow principle of least privilege** for permissions

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_gemini.py

# Run with coverage
pytest --cov=src

# Run integration tests only
pytest tests/test_system.py
```

### Writing Tests

Follow these patterns for new tests:

```python
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

class TestMultiAIIntegration:
    @pytest.fixture
    async def multi_ai(self):
        """Create MultiAIIntegration instance for testing."""
        return MultiAIIntegration()
    
    @pytest.mark.asyncio
    async def test_provider_selection_auto(self, multi_ai):
        """Test automatic provider selection."""
        # Arrange
        request = MultiAIConsultationRequest(
            query="test query",
            preferred_provider=AIProvider.AUTO
        )
        
        # Act
        result = await multi_ai.consult_multi_ai(request)
        
        # Assert
        assert result["success"] is True
        assert len(result["responses"]) >= 1
    
    def test_configuration_loading(self):
        """Test configuration file loading."""
        # Test configuration loading logic
        pass
```

### Test Categories

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **System Tests**: Test complete workflows
- **Performance Tests**: Test response times and resource usage

## 📚 Documentation

### Documentation Types

1. **Code Documentation**: Docstrings and comments
2. **User Guides**: Installation, configuration, usage
3. **API Reference**: Complete API documentation
4. **Examples**: Practical usage examples
5. **Troubleshooting**: Common issues and solutions

### Writing Documentation

- **Use clear, simple language**
- **Provide practical examples**
- **Include code snippets**
- **Test all examples** to ensure they work
- **Update docs** when making code changes

### Documentation Format

Use Markdown with the following conventions:

```markdown
# Main Heading (H1)

## Section Heading (H2)

### Subsection Heading (H3)

#### Detail Heading (H4)

**Bold text** for emphasis
*Italic text* for terms
`code` for inline code
```

## 🔄 Pull Request Process

### Before Submitting

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow coding guidelines
   - Add tests for new functionality
   - Update documentation

3. **Test your changes**
   ```bash
   pytest
   flake8 src/
   black src/
   mypy src/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new provider selection strategy"
   ```

### Commit Message Format

Use conventional commits format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(gemini): add support for new Gemini model
fix(ollama): handle connection timeout gracefully
docs(readme): update installation instructions
test(integration): add provider comparison tests
```

### Pull Request Guidelines

1. **Fill out the PR template** completely
2. **Reference related issues** using keywords (fixes #123)
3. **Describe changes** clearly in the description
4. **Include screenshots** for UI changes
5. **Ensure all checks pass** before requesting review

### Review Process

1. **Automated checks** must pass
2. **At least one maintainer** must review
3. **Address feedback** promptly
4. **Update documentation** if needed
5. **Squash commits** before merging (if requested)

## 🚢 Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release notes
- [ ] Tag release in Git
- [ ] Publish to PyPI (if applicable)

## 🏷️ Issue Labels

We use these labels to categorize issues:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested
- `priority-high` - High priority issue
- `priority-low` - Low priority issue

## 🎉 Recognition

Contributors are recognized in:

- **README.md** contributors section
- **CHANGELOG.md** for significant contributions
- **GitHub releases** notes
- **Special mentions** in project updates

## 📞 Getting Help

If you need help:

1. **Check existing documentation**
2. **Search existing issues**
3. **Ask in discussions** for general questions
4. **Create an issue** for specific problems
5. **Join our community** channels (if available)

## 🙏 Thank You

Thank you for contributing to Multi-AI MCP Integration! Your contributions help make this project better for everyone in the developer community.

---

**Happy coding!** 🚀