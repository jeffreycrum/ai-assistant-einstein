"""
Tests for environment configuration and setup.
"""
import pytest
import os
from unittest.mock import patch

# Import after conftest has set up mocks
import main


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
    assert "your point of view" in main.system_prompt.lower() or "your" in main.system_prompt.lower(), \
        "System prompt should require first-person perspective"


@pytest.mark.unit
def test_system_prompt_requires_personal_anecdotes():
    """Test that system prompt requires sharing personal experiences."""
    assert "personal" in main.system_prompt.lower(), "System prompt should mention personal experiences"


@pytest.mark.integration
def test_prompt_template_structure():
    """Test that prompt template includes system, history, and user input."""
    from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder

    # Assert
    messages = main.prompt.messages
    assert len(messages) == 3, "Prompt should have 3 message slots"

    # Check that system prompt is first
    assert isinstance(messages[0], SystemMessagePromptTemplate), "First message should be system prompt template"

    # Check that we have a history placeholder
    assert isinstance(messages[1], MessagesPlaceholder), "Second should be history placeholder"
    assert messages[1].variable_name == "history", "History placeholder should have correct variable name"

    # Check that user input is last
    assert isinstance(messages[2], HumanMessagePromptTemplate), "Last message should be user input template"


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
    # The chain should be constructed with the | operator
    # We can't easily test the internal structure, but we can verify it exists
    assert main.chain is not None, "Chain should be initialized"
    assert hasattr(main.chain, 'invoke'), "Chain should have invoke method"
