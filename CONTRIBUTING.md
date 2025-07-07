# Contributing to Voice Dictation Tool

Thank you for your interest in contributing to the Voice Dictation Tool! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Development Workflow](#development-workflow)
5. [Coding Standards](#coding-standards)
6. [Commit Guidelines](#commit-guidelines)
7. [Pull Request Process](#pull-request-process)
8. [Testing](#testing)
9. [Documentation](#documentation)

## Code of Conduct

### Our Pledge

We are committed to providing a friendly, safe, and welcoming environment for all contributors, regardless of experience level, gender identity, sexual orientation, disability, personal appearance, race, ethnicity, age, religion, or nationality.

### Expected Behavior

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or hate speech
- Personal attacks or insults
- Publishing others' private information
- Any conduct which would be inappropriate in a professional setting

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**To report a bug:**

1. Use the GitHub issue tracker
2. Use the bug report template
3. Include:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs. actual behavior
   - Screenshots (if applicable)
   - System information (OS, Python version)
   - Error messages/logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:

1. Check if the enhancement has already been suggested
2. Create a detailed issue describing:
   - The problem it solves
   - How it should work
   - Why it would be useful
   - Possible implementation approach

### Contributing Code

1. **Fix bugs** - Look for issues labeled `bug`
2. **Implement features** - Look for issues labeled `enhancement`
3. **Improve documentation** - Help make docs clearer
4. **Add tests** - Increase test coverage
5. **Optimize performance** - Make the tool faster

## Development Setup

### Prerequisites

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/voice-dictation-tool.git
   cd voice-dictation-tool
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

### Development Dependencies

Create `requirements-dev.txt`:
```txt
pytest==7.4.0
pytest-cov==4.1.0
black==23.7.0
flake8==6.1.0
mypy==1.5.0
pre-commit==3.3.3
```

### Setting Up Pre-commit Hooks

1. Install pre-commit:
   ```bash
   pip install pre-commit
   ```

2. Set up hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

### 1. Create a Branch

```bash
# For bugs
git checkout -b fix/description-of-bug

# For features
git checkout -b feature/description-of-feature

# For documentation
git checkout -b docs/description-of-change
```

### 2. Make Your Changes

- Write clean, readable code
- Follow the coding standards
- Add/update tests as needed
- Update documentation

### 3. Test Your Changes

```bash
# Run the application
python voice_dictation_advanced.py

# Run tests (when available)
pytest

# Check code style
flake8 .
black --check .
```

### 4. Commit Your Changes

Follow the commit message guidelines below.

### 5. Push and Create PR

```bash
git push origin your-branch-name
```

Then create a Pull Request on GitHub.

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specifications:

- **Line length**: 88 characters (Black default)
- **Quotes**: Double quotes for strings
- **Imports**: Grouped and sorted (stdlib, third-party, local)

### Code Structure

```python
# Good example
class VoiceRecognizer:
    """Handles speech recognition functionality."""
    
    def __init__(self, language="en-US"):
        """Initialize recognizer with specified language."""
        self.language = language
        self.recognizer = sr.Recognizer()
    
    def recognize_speech(self, audio_data):
        """
        Convert audio to text using Google Speech Recognition.
        
        Args:
            audio_data: Audio data from microphone
            
        Returns:
            str: Transcribed text
            
        Raises:
            RecognitionError: If recognition fails
        """
        try:
            return self.recognizer.recognize_google(
                audio_data, 
                language=self.language
            )
        except sr.UnknownValueError:
            raise RecognitionError("Could not understand audio")
```

### PyQt5 Guidelines

- Use layouts instead of absolute positioning
- Separate UI and logic
- Use signals/slots for communication
- Follow Qt naming conventions

### Best Practices

1. **DRY** - Don't Repeat Yourself
2. **KISS** - Keep It Simple, Stupid
3. **YAGNI** - You Aren't Gonna Need It
4. Write self-documenting code
5. Add comments for complex logic
6. Use type hints where beneficial

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding/updating tests
- **chore**: Maintenance tasks

### Examples

```bash
feat(streaming): add real-time word-by-word output

Implement background listening with immediate clipboard insertion
for each recognized word, reducing perceived latency.

Closes #123
```

```bash
fix(advanced): correct hotkey registration on startup

The global hotkey was not being registered when the application
started minimized to tray. Now properly registers regardless of
initial state.

Fixes #456
```

### Commit Best Practices

1. Make atomic commits (one change per commit)
2. Write clear, concise messages
3. Reference issues when applicable
4. Use present tense ("add" not "added")
5. Limit subject line to 50 characters

## Pull Request Process

### Before Submitting

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Run all tests** and ensure they pass
4. **Update README** if adding features
5. **Check code style** compliance

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested on Windows 10
- [ ] Tested on Windows 11
- [ ] Added new tests
- [ ] All tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

1. At least one maintainer review required
2. All CI checks must pass
3. No merge conflicts
4. Follows contribution guidelines

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_recognition.py

# Run with verbose output
pytest -v
```

### Writing Tests

```python
# tests/test_recognition.py
import pytest
from voice_dictation_advanced import FloatingWidget

class TestFloatingWidget:
    def test_initial_state(self):
        """Test widget initializes in non-recording state."""
        widget = FloatingWidget()
        assert widget.is_recording == False
        
    def test_toggle_recording(self):
        """Test recording state toggles correctly."""
        widget = FloatingWidget()
        widget.toggle_recording()
        assert widget.is_recording == True
        widget.toggle_recording()
        assert widget.is_recording == False
```

### Test Guidelines

1. Write tests for all new features
2. Aim for >80% code coverage
3. Test edge cases
4. Use descriptive test names
5. Keep tests independent

## Documentation

### Documentation Standards

1. **Docstrings**: Use Google style
2. **README**: Keep updated with new features
3. **Code comments**: Explain "why" not "what"
4. **Examples**: Provide usage examples

### Docstring Example

```python
def process_audio(audio_data, language="en-US"):
    """
    Process audio data and return transcribed text.
    
    Args:
        audio_data (AudioData): The audio to process
        language (str, optional): Language code. Defaults to "en-US".
        
    Returns:
        str: The transcribed text
        
    Raises:
        ValueError: If audio_data is None
        RecognitionError: If transcription fails
        
    Example:
        >>> audio = record_audio()
        >>> text = process_audio(audio, "es-ES")
        >>> print(text)
        "Hola mundo"
    """
```

## Getting Help

### Resources

- [Python Documentation](https://docs.python.org/3/)
- [PyQt5 Documentation](https://doc.qt.io/qtforpython/)
- [Speech Recognition Docs](https://github.com/Uberi/speech_recognition)

### Communication

- **Issues**: For bugs and features
- **Discussions**: For questions and ideas
- **Pull Requests**: For code contributions

## Recognition

Contributors will be recognized in:
- The README file
- Release notes
- Project documentation

Thank you for contributing to make Voice Dictation Tool better for everyone!