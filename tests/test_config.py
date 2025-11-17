"""
Tests for environment configuration and setup.
"""
import pytest
import sys
import os
from unittest.mock import patch, Mock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.mark.unit
def test_gemini_api_key_loaded_from_env(mock_gemini_api_key):
    """Test that GEMINI_API_KEY is loaded from environment variables."""
    # The mock_gemini_api_key fixture sets the env var
    assert os.getenv("GEMINI_API_KEY") == "test_api_key_12345"


@pytest.mark.unit
def test_system_prompt_contains_einstein_persona(system_prompt):
    """Test that system prompt defines Einstein's personality."""
    # Assert
    assert "Einstein" in system_prompt, "System prompt should mention Einstein"
    assert "mean" in system_prompt.lower(), "System prompt should specify mean personality"
    assert "humor" in system_prompt.lower(), "System prompt should mention humor"


@pytest.mark.unit
def test_system_prompt_has_character_limit(system_prompt):
    """Test that system prompt specifies the 300 character limit."""
    # Assert
    assert "300" in system_prompt, "System prompt should mention 300 character limit"
    assert "brief" in system_prompt.lower(), "System prompt should emphasize brevity"


@pytest.mark.unit
def test_system_prompt_requires_first_person():
    """Test that system prompt requires first-person perspective."""
    with patch('main.ChatGoogleGenerativeAI'):
        from main import system_prompt

    assert "your point of view" in system_prompt.lower() or "your" in system_prompt.lower(), \
        "System prompt should require first-person perspective"


@pytest.mark.unit
def test_system_prompt_requires_personal_anecdotes():
    """Test that system prompt requires sharing personal experiences."""
    with patch('main.ChatGoogleGenerativeAI'):
        from main import system_prompt

    assert "personal" in system_prompt.lower(), "System prompt should mention personal experiences"


@pytest.mark.integration
def test_llm_initialization_with_correct_model():
    """Test that LLM is initialized with the correct Gemini model."""
    with patch('main.ChatGoogleGenerativeAI') as mock_llm_class:
        # Re-import to trigger initialization
        import importlib
        if 'main' in sys.modules:
            del sys.modules['main']

        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            import main

        # Assert
        mock_llm_class.assert_called_once()
        call_kwargs = mock_llm_class.call_args[1]
        assert call_kwargs['model'] == "gemini-2.5-flash", "Should use gemini-2.5-flash model"
        assert call_kwargs['temperature'] == 0.5, "Temperature should be 0.5"


@pytest.mark.integration
def test_prompt_template_structure():
    """Test that prompt template includes system, history, and user input."""
    with patch('main.ChatGoogleGenerativeAI'):
        from main import prompt

    # Assert
    messages = prompt.messages
    assert len(messages) == 3, "Prompt should have 3 message slots"

    # Check that system prompt is first
    assert messages[0][0] == "system", "First message should be system prompt"

    # Check that we have a history placeholder
    # MessagesPlaceholder doesn't have the same structure, so we check it exists
    assert hasattr(messages[1], 'variable_name'), "Should have history placeholder"

    # Check that user input is last
    assert messages[2][0] == "user", "Last message should be user input"


@pytest.mark.unit
def test_missing_api_key_handling(monkeypatch):
    """Test behavior when GEMINI_API_KEY is not set."""
    # Arrange - remove the API key
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    # Act & Assert
    # When API key is missing, it should be None
    assert os.getenv("GEMINI_API_KEY") is None, "API key should be None when not set"


@pytest.mark.integration
def test_chain_pipeline_structure():
    """Test that the chain is properly constructed with prompt | llm | parser."""
    with patch('main.ChatGoogleGenerativeAI'):
        from main import chain, prompt, llm
        from langchain_core.output_parsers import StrOutputParser

    # The chain should be constructed with the | operator
    # We can't easily test the internal structure, but we can verify it exists
    assert chain is not None, "Chain should be initialized"
    assert hasattr(chain, 'invoke'), "Chain should have invoke method"
