# Contributing to LlamaPhone

Thank you for your interest in contributing to LlamaPhone!

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Ollama (for AI features)
- Android SDK Platform Tools (for ADB/Fastboot)

### Fork and Clone

```bash
# Fork the repository on GitHub

# Clone your fork
git clone https://github.com/YOUR_USERNAME/llamaphone.git
cd llamaphone

# Add upstream remote
git remote add upstream https://github.com/llamaphone/llamaphone.git
```

### Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows

# Install dependencies
pip install -e .
pip install -e ".[dev]"
```

### Run in Development Mode

```bash
python llamaphone.py
```

## Code Style

We use Ruff for linting and formatting:

```bash
# Check code style
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

### Naming Conventions

- **Modules**: `snake_case` (e.g., `adb_tools.py`)
- **Classes**: `PascalCase` (e.g., `ADBClient`)
- **Functions**: `snake_case` (e.g., `get_devices()`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_PORT`)

### Type Hints

All functions should include type hints:

```python
def connect_device(ip: str, port: int = 5555) -> bool:
    """Connect to a device."""
    ...
```

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=llamaphone
```

### Write Tests

Place tests in the `tests/` directory:

```python
# tests/test_adb.py
import pytest
from llamaphone.ai.tools.adb_tools import ADBTools

def test_adb_devices():
    tools = ADBTools()
    result = tools.devices()
    assert isinstance(result.success, bool)
```

## Pull Request Process

### 1. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/my-feature

# Or a bugfix branch
git checkout -b fix/my-bugfix
```

### 2. Make Changes

- Write code following our style guidelines
- Add/update tests as needed
- Update documentation if applicable

### 3. Commit

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add: Feature description

- Detailed change 1
- Detailed change 2
"
```

### 4. Push and Create PR

```bash
# Push to your fork
git push origin feature/my-feature

# Create PR on GitHub
```

### PR Description Template

```markdown
## Summary
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

## Code of Conduct

- Be respectful and inclusive
- Use welcoming language
- Be collaborative
- Focus on what is best for the community
- Show courtesy and respect

## Questions?

Feel free to open an issue for questions or discussions.
