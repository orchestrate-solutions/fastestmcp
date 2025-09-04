"""
Test Template for Prompt Components - Reusable test patterns for MCP server prompts
"""

import pytest
from unittest.mock import Mock, patch


class TestPromptComponents:
    """Test cases for prompt components"""

    def test_prompt_1_basic_functionality(self):
        """Test prompt_1 basic input/output functionality"""
        from fastestmcp.components.prompts.prompt_template import prompt_1

        result = prompt_1("test context")
        assert "Prompt 1 response for: test context" in result
        assert isinstance(result, str)

    def test_prompt_1_empty_context(self):
        """Test prompt_1 with empty context"""
        from fastestmcp.components.prompts.prompt_template import prompt_1

        result = prompt_1("")
        assert "Prompt 1 response for: " in result

    def test_prompt_2_basic_functionality(self):
        """Test prompt_2 basic input/output functionality"""
        from fastestmcp.components.prompts.prompt_template import prompt_2

        result = prompt_2("test context")
        assert "Prompt 2 analysis of: test context" in result
        assert isinstance(result, str)

    def test_prompt_3_basic_functionality(self):
        """Test prompt_3 basic input/output functionality"""
        from fastestmcp.components.prompts.prompt_template import prompt_3

        result = prompt_3("test context")
        assert "Prompt 3 creative response for: test context" in result

    def test_create_prompt_basic_structure(self):
        """Test create_prompt returns proper Prompt object"""
        from fastestmcp.components.prompts.prompt_template import create_prompt

        result = create_prompt(1)

        assert hasattr(result, 'name')
        assert hasattr(result, 'description')
        assert hasattr(result, 'arguments')
        assert result.name == "prompt_1"
        assert result.description == "Prompt 1 - generates responses based on context"
        assert result.arguments is not None
        assert len(result.arguments) == 1

    def test_create_prompt_argument_structure(self):
        """Test create_prompt generates correct argument structure"""
        from fastestmcp.components.prompts.prompt_template import create_prompt

        result = create_prompt(2)

        assert result.name == "prompt_2"
        assert result.arguments is not None
        argument = result.arguments[0]
        assert argument.name == "context"
        assert argument.description == "Context for the prompt"
        assert argument.required == True

    def test_register_prompts_with_mock_server(self):
        """Test register_prompts function with mocked server"""
        from fastestmcp.components.prompts.prompt_template import register_prompts

        mock_server = Mock()
        register_prompts(mock_server, count=2)

        # Verify add_prompt was called twice
        assert mock_server.add_prompt.call_count == 2

    def test_register_prompts_zero_count(self):
        """Test register_prompts with zero count"""
        from fastestmcp.components.prompts.prompt_template import register_prompts

        mock_server = Mock()
        register_prompts(mock_server, count=0)

        # Verify add_prompt was not called
        mock_server.add_prompt.assert_not_called()

    def test_prompt_response_consistency(self):
        """Test that prompt responses are consistent for same input"""
        from fastestmcp.components.prompts.prompt_template import prompt_1

        result1 = prompt_1("same context")
        result2 = prompt_1("same context")

        assert result1 == result2

    def test_different_prompts_different_responses(self):
        """Test that different prompts give different responses"""
        from fastestmcp.components.prompts.prompt_template import prompt_1, prompt_2

        result1 = prompt_1("test context")
        result2 = prompt_2("test context")

        assert result1 != result2
        assert "Prompt 1" in result1
        assert "Prompt 2" in result2

    def test_prompt_handles_special_characters(self):
        """Test prompts handle special characters in context"""
        from fastestmcp.components.prompts.prompt_template import prompt_1

        special_context = "test@#$%^&*()_+{}|:<>?[]\\;',./"
        result = prompt_1(special_context)

        assert special_context in result
        assert "Prompt 1 response for:" in result