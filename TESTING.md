# Testing Infrastructure Documentation

This document provides a comprehensive overview of the testing infrastructure for the AI Assistant Einstein project.

## Overview

The testing infrastructure has been set up using **pytest** with coverage reporting, mocking capabilities, and organized test structure to ensure code quality and reliability.

## Quick Start

### Installation

Install all development dependencies:

```bash
pip install -r requirements-dev.txt
```

Or use the Makefile:

```bash
make install-dev
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run verbose
make test-verbose

# Run specific test types
make test-unit
make test-integration
```

## Test Infrastructure Components

### 1. Configuration Files

#### `pytest.ini`
Main pytest configuration including:
- Test discovery patterns
- Output formatting options
- Coverage reporting settings
- Test markers for categorization
- Default environment variables

#### `.coveragerc`
Coverage.py configuration including:
- Source code paths
- Files to exclude from coverage
- Coverage thresholds (80% minimum)
- HTML and XML report generation

#### `requirements-dev.txt`
Development dependencies including:
- pytest and plugins
- Code quality tools (black, flake8, mypy)
- Mocking and testing utilities

#### `Makefile`
Convenient commands for common development tasks

### 2. Test Structure

```
tests/
├── __init__.py              # Test package marker
├── conftest.py              # Shared fixtures and configuration
├── test_chat.py             # Tests for chat() function
├── test_clear_chat.py       # Tests for clear_chat() function
├── test_config.py           # Configuration and setup tests
└── README.md                # Testing documentation
```

### 3. Shared Fixtures (conftest.py)

Available fixtures for all tests:

- `mock_gemini_api_key` - Mocks the GEMINI_API_KEY environment variable
- `empty_history` - Provides an empty chat history list
- `sample_history` - Provides a sample conversation history (Gradio format)
- `sample_langchain_history` - Sample history in LangChain format
- `mock_llm_response` - Mock response from the LLM
- `mock_chain` - Mock LangChain chain to avoid real API calls
- `mock_gradio_components` - Mock Gradio UI components
- `system_prompt` - The Einstein system prompt for testing
- `invalid_history_formats` - Various invalid history formats for error testing

## Test Categories

Tests are organized using pytest markers:

### Unit Tests (`@pytest.mark.unit`)
- Test individual functions in isolation
- Use mocks to avoid external dependencies
- Fast execution
- Example: `test_clear_chat_returns_empty_string_and_list()`

### Integration Tests (`@pytest.mark.integration`)
- Test component interactions
- May involve multiple modules
- Test LangChain pipeline, prompt templates
- Example: `test_chain_pipeline_structure()`

### Slow Tests (`@pytest.mark.slow`)
- Tests that take longer to execute
- Can be skipped for quick feedback: `pytest -m "not slow"`

### API Tests (`@pytest.mark.api`)
- Tests involving external API calls
- Should be minimal and use mocking when possible
- May require valid API credentials

## Current Test Coverage

### Implemented Tests

#### `test_clear_chat.py` (5 tests)
✅ Basic functionality test
✅ Return type validation
✅ Idempotency test
✅ String emptiness validation
✅ List emptiness validation

#### `test_chat.py` (9 tests)
✅ Chat with empty history
✅ Chat with existing history
✅ History conversion to LangChain format
✅ Original history preservation
✅ Return format validation
✅ Special characters handling
✅ User input passed to chain
✅ And more...

#### `test_config.py` (9 tests)
✅ API key loading from environment
✅ System prompt personality traits
✅ Character limit specification
✅ First-person perspective requirement
✅ Personal anecdotes requirement
✅ LLM initialization
✅ Prompt template structure
✅ Missing API key handling
✅ Chain pipeline structure

## Test Coverage Goals

### Current Target: 80%
The `.coveragerc` file is configured to require a minimum of 80% code coverage.

### Coverage by Component

**Priority**: High coverage (90%+)
- `chat()` function - Core business logic
- `clear_chat()` function - Simple but critical
- History conversion logic

**Priority**: Medium coverage (80%+)
- LangChain integration
- Prompt template setup
- Configuration loading

**Priority**: Lower coverage (60%+)
- Gradio UI components
- Application launch code

## Writing New Tests

### Test Structure (AAA Pattern)

```python
@pytest.mark.unit
def test_example_function(fixture_name):
    # Arrange - Set up test data and mocks
    input_data = "test input"
    expected_output = "expected result"

    # Act - Execute the function under test
    result = function_under_test(input_data)

    # Assert - Verify the results
    assert result == expected_output
```

### Using Fixtures

```python
def test_with_fixtures(mock_chain, sample_history):
    # Fixtures are automatically injected
    result = chat("test", sample_history)
    assert result is not None
```

### Mocking External Dependencies

```python
from unittest.mock import patch

@pytest.mark.unit
def test_with_mock():
    with patch('main.chain') as mock_chain:
        mock_chain.invoke.return_value = "mocked response"
        result = chat("test", [])
        mock_chain.invoke.assert_called_once()
```

## Best Practices

### 1. Always Mock External APIs
- Never make real API calls in unit tests
- Use `mock_chain` fixture to mock LangChain
- Saves API costs and ensures test reliability

### 2. Use Appropriate Markers
```python
@pytest.mark.unit  # Fast, isolated tests
@pytest.mark.integration  # Component interaction tests
@pytest.mark.slow  # Long-running tests
```

### 3. Test Edge Cases
- Empty inputs
- None values
- Very long strings
- Special characters
- Invalid data formats

### 4. Keep Tests Independent
- Each test should work in isolation
- Don't rely on test execution order
- Clean up state if needed

### 5. Clear Test Names
- Use descriptive names: `test_chat_with_empty_history_returns_valid_format`
- Should explain what is being tested
- Should indicate expected behavior

## Running Specific Tests

```bash
# Run a specific test file
pytest tests/test_chat.py

# Run a specific test function
pytest tests/test_chat.py::test_chat_with_empty_history

# Run tests matching a pattern
pytest -k "history"

# Run tests by marker
pytest -m unit
pytest -m "not slow"
pytest -m "unit and not slow"
```

## Coverage Reports

### Generate HTML Coverage Report
```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Terminal Coverage Report
```bash
pytest --cov=. --cov-report=term-missing
```

### Coverage Report Locations
- HTML: `htmlcov/index.html`
- XML: `coverage.xml`
- Terminal: stdout during test run

## Continuous Integration

### Future CI/CD Integration

The testing infrastructure is ready for CI/CD integration. Recommended workflow:

```yaml
# .github/workflows/test.yml example
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Troubleshooting

### Import Errors
If you see import errors, ensure the parent directory is in the Python path:
```python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

### API Key Issues
Tests use a mocked API key by default. If you see API-related errors, check that `mock_gemini_api_key` fixture is being used.

### Coverage Too Low
To see which lines are not covered:
```bash
pytest --cov=. --cov-report=term-missing
```

Check the `htmlcov/index.html` report for detailed line-by-line coverage.

## Areas for Future Improvement

1. **Error Handling Tests**
   - API timeout scenarios
   - Network failures
   - Invalid API responses
   - Rate limiting

2. **Gradio UI Tests**
   - Component rendering
   - Event handling
   - Button clicks
   - Message submission

3. **End-to-End Tests**
   - Full conversation flows
   - Multi-turn conversations
   - Chat history persistence

4. **Performance Tests**
   - Response time benchmarks
   - Memory usage
   - Concurrent request handling

5. **Security Tests**
   - Input sanitization
   - API key protection
   - XSS prevention

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-cov Plugin](https://pytest-cov.readthedocs.io/)
- [Unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [LangChain Testing Guide](https://python.langchain.com/docs/guides/testing)

## Support

For questions or issues with the testing infrastructure, please refer to:
- `tests/README.md` - Quick testing guide
- This document - Comprehensive testing documentation
- `conftest.py` - Available fixtures and their usage
