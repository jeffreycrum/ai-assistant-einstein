"""
Unit tests for the clear_chat() function.
"""

import pytest

# Import after conftest has set up mocks
from main import clear_chat


@pytest.mark.unit
def test_clear_chat_returns_empty_string_and_list():
    """Test that clear_chat returns an empty string and an empty list."""
    # Act
    result = clear_chat()

    # Assert
    assert isinstance(result, tuple), "clear_chat should return a tuple"
    assert len(result) == 2, "clear_chat should return a tuple of 2 elements"
    assert result[0] == "", "First element should be an empty string"
    assert result[1] == [], "Second element should be an empty list"


@pytest.mark.unit
def test_clear_chat_return_types():
    """Test that clear_chat returns correct data types."""
    # Act
    msg, history = clear_chat()

    # Assert
    assert isinstance(msg, str), "First return value should be a string"
    assert isinstance(history, list), "Second return value should be a list"


@pytest.mark.unit
def test_clear_chat_is_idempotent():
    """Test that calling clear_chat multiple times produces the same result."""
    # Act
    result1 = clear_chat()
    result2 = clear_chat()
    result3 = clear_chat()

    # Assert
    assert result1 == result2 == result3, "clear_chat should be idempotent"


@pytest.mark.unit
def test_clear_chat_string_is_empty():
    """Test that the returned string is specifically empty, not None or other falsy value."""
    # Act
    msg, _ = clear_chat()

    # Assert
    assert msg == "", "Message should be empty string"
    assert not msg, "Message should be falsy"
    assert len(msg) == 0, "Message should have zero length"


@pytest.mark.unit
def test_clear_chat_list_is_empty():
    """Test that the returned list is specifically empty, not None or other falsy value."""
    # Act
    _, history = clear_chat()

    # Assert
    assert history == [], "History should be empty list"
    assert not history, "History should be falsy"
    assert len(history) == 0, "History should have zero length"
