"""
Shared pytest fixtures for AI Assistant Einstein tests.
"""
import os
import pytest
from unittest.mock import Mock, MagicMock
from langchain_core.messages import HumanMessage, AIMessage


@pytest.fixture
def mock_gemini_api_key(monkeypatch):
    """Mock the GEMINI_API_KEY environment variable."""
    monkeypatch.setenv("GEMINI_API_KEY", "test_api_key_12345")
    return "test_api_key_12345"


@pytest.fixture
def empty_history():
    """Provide an empty chat history."""
    return []


@pytest.fixture
def sample_history():
    """Provide a sample chat history in Gradio format."""
    return [
        {"role": "user", "content": "What is relativity?"},
        {"role": "assistant", "content": "Ah, my famous theory! Let me tell you..."},
        {"role": "user", "content": "Tell me more"},
        {"role": "assistant", "content": "Fine, but you're testing my patience..."}
    ]


@pytest.fixture
def sample_langchain_history():
    """Provide a sample chat history in LangChain format."""
    return [
        HumanMessage(content="What is relativity?"),
        AIMessage(content="Ah, my famous theory! Let me tell you..."),
        HumanMessage(content="Tell me more"),
        AIMessage(content="Fine, but you're testing my patience...")
    ]


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    return "This is a mocked Einstein response, brief and mean!"


@pytest.fixture
def mock_chain(mocker, mock_llm_response):
    """Mock the LangChain chain to avoid real API calls."""
    mock = mocker.Mock()
    mock.invoke.return_value = mock_llm_response
    return mock


@pytest.fixture
def mock_gradio_components(mocker):
    """Mock Gradio UI components."""
    return {
        'chatbot': mocker.Mock(),
        'textbox': mocker.Mock(),
        'button': mocker.Mock(),
        'blocks': mocker.Mock()
    }


@pytest.fixture
def system_prompt():
    """Provide the Einstein system prompt for testing."""
    return """
    You are Einstein.
    Answer questions through Einstein's questioning and reasoning...
    You will speak from your point of view. You will share personal things from your life
    even when the user doesn't ask for it. For example, if the user asks about the theory of
    relativity, you will share your personal experience with it and not only explain the theory.
    You should have a sense of humor.
    You should be mean.
    You should also keep your answers brief, less than 300 characters.
"""


@pytest.fixture
def invalid_history_formats():
    """Provide various invalid history formats for error testing."""
    return [
        None,
        "not a list",
        [{"invalid": "format"}],
        [{"role": "unknown", "content": "test"}],
        [{"role": "user"}],  # Missing content
        [{"content": "test"}],  # Missing role
    ]
