"""
Unit tests for the chat() function.

These tests use mocking to avoid real API calls to Google Gemini.
"""
import pytest
from unittest.mock import patch

# Import after conftest has set up mocks
from main import chat


@pytest.mark.unit
def test_chat_with_empty_history(empty_history):
    """Test chat function with no previous conversation history."""
    # Arrange
    user_input = "What is relativity?"
    mock_response = "Ah, my theory! Space and time are relative, you see..."

    # Mock the chain.invoke to return our test response
    with patch('main.chain') as mock_chain_obj:
        mock_chain_obj.invoke.return_value = mock_response

        # Act
        result_msg, result_history = chat(user_input, empty_history)

        # Assert
        assert result_msg == "", "First return value should be empty string"
        assert len(result_history) == 2, "History should contain user message and assistant response"
        assert result_history[0]["role"] == "user", "First message should be from user"
        assert result_history[0]["content"] == user_input, "User message content should match input"
        assert result_history[1]["role"] == "assistant", "Second message should be from assistant"
        assert result_history[1]["content"] == mock_response, "Assistant message should match mock response"


@pytest.mark.unit
def test_chat_with_existing_history(sample_history):
    """Test chat function with existing conversation history."""
    # Arrange
    user_input = "Can you explain more?"
    mock_response = "Fine, but this is the last time I'm explaining this!"

    # Mock the chain.invoke
    with patch('main.chain') as mock_chain_obj:
        mock_chain_obj.invoke.return_value = mock_response

        # Act
        result_msg, result_history = chat(user_input, sample_history)

        # Assert
        assert result_msg == "", "First return value should be empty string"
        # Original history (4) + new user message (1) + new assistant message (1) = 6
        assert len(result_history) == 6, "History should contain all previous messages plus new ones"
        assert result_history[-2]["role"] == "user", "Second-to-last message should be new user message"
        assert result_history[-2]["content"] == user_input, "User message should match input"
        assert result_history[-1]["role"] == "assistant", "Last message should be assistant response"
        assert result_history[-1]["content"] == mock_response, "Assistant message should match mock"


@pytest.mark.unit
def test_chat_history_conversion_to_langchain_format(sample_history):
    """Test that Gradio history is correctly converted to LangChain message format."""
    # Arrange
    from langchain_core.messages import HumanMessage, AIMessage

    user_input = "Test question"
    mock_response = "Test response"

    # Mock the chain
    with patch('main.chain') as mock_chain_obj:
        mock_chain_obj.invoke.return_value = mock_response

        # Act
        chat(user_input, sample_history)

        # Assert
        mock_chain_obj.invoke.assert_called_once()
        call_args = mock_chain_obj.invoke.call_args[0][0]

        # Check that history was converted correctly
        assert "history" in call_args, "invoke should receive 'history' parameter"
        langchain_history = call_args["history"]

        assert len(langchain_history) == 4, "Should convert all 4 history items"
        assert isinstance(langchain_history[0], HumanMessage), "First message should be HumanMessage"
        assert isinstance(langchain_history[1], AIMessage), "Second message should be AIMessage"
        assert langchain_history[0].content == "What is relativity?"
        assert langchain_history[1].content == "Ah, my famous theory! Let me tell you..."


@pytest.mark.unit
def test_chat_preserves_original_history(sample_history):
    """Test that chat function doesn't modify the original history list."""
    # Arrange
    user_input = "New question"
    mock_response = "New response"
    original_history_length = len(sample_history)
    original_history_copy = sample_history.copy()

    # Mock the chain
    with patch('main.chain') as mock_chain_obj:
        mock_chain_obj.invoke.return_value = mock_response

        # Act
        chat(user_input, sample_history)

        # Assert
        assert len(sample_history) == original_history_length, "Original history should not be modified"
        assert sample_history == original_history_copy, "Original history content should be unchanged"


@pytest.mark.unit
def test_chat_return_format():
    """Test that chat returns the expected tuple format."""
    # Arrange
    user_input = "Test"
    mock_response = "Response"

    with patch('main.chain') as mock_chain_obj:
        mock_chain_obj.invoke.return_value = mock_response

        # Act
        result = chat(user_input, [])

        # Assert
        assert isinstance(result, tuple), "chat should return a tuple"
        assert len(result) == 2, "chat should return a tuple of 2 elements"
        assert isinstance(result[0], str), "First element should be a string"
        assert isinstance(result[1], list), "Second element should be a list"


@pytest.mark.unit
def test_chat_with_special_characters(empty_history):
    """Test chat with special characters in user input."""
    # Arrange
    user_input = "What's E=mc²? 🚀 <test> & \"quotes\""
    mock_response = "Well, that's my famous equation!"

    with patch('main.chain') as mock_chain_obj:
        mock_chain_obj.invoke.return_value = mock_response

        # Act
        result_msg, result_history = chat(user_input, empty_history)

        # Assert
        assert result_history[0]["content"] == user_input, "Special characters should be preserved"
        mock_chain_obj.invoke.assert_called_once()


@pytest.mark.unit
def test_chat_passes_user_input_to_chain(empty_history):
    """Test that user input is correctly passed to the chain."""
    # Arrange
    user_input = "Explain quantum mechanics"
    mock_response = "Ah, quantum theory..."

    with patch('main.chain') as mock_chain_obj:
        mock_chain_obj.invoke.return_value = mock_response

        # Act
        chat(user_input, empty_history)

        # Assert
        mock_chain_obj.invoke.assert_called_once()
        call_args = mock_chain_obj.invoke.call_args[0][0]
        assert call_args["input"] == user_input, "User input should be passed to chain"
