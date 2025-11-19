# Test Suite for AI Assistant Einstein

This directory contains the test suite for the AI Assistant Einstein chatbot application.

## Setup

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run tests with coverage
```bash
pytest --cov=. --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_chat.py
```

### Run tests by marker
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

### Run tests in verbose mode
```bash
pytest -v
```

## Test Structure

- `conftest.py` - Shared fixtures and test configuration
- `test_chat.py` - Tests for the chat() function
- `test_clear_chat.py` - Tests for the clear_chat() function
- `test_chain.py` - Integration tests for LangChain components
- `test_config.py` - Tests for environment and configuration

## Coverage Reports

After running tests with coverage, view the HTML report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Test Markers

- `@pytest.mark.unit` - Unit tests for individual functions
- `@pytest.mark.integration` - Integration tests for component interactions
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.api` - Tests that interact with external APIs

## Writing New Tests

1. Create a new test file with the pattern `test_*.py`
2. Import necessary fixtures from `conftest.py`
3. Use appropriate markers to categorize tests
4. Mock external dependencies (especially API calls)
5. Follow the AAA pattern: Arrange, Act, Assert

Example:

```python
import pytest

@pytest.mark.unit
def test_example_function(mock_chain):
    # Arrange
    input_data = "test input"

    # Act
    result = some_function(input_data)

    # Assert
    assert result == expected_output
```
