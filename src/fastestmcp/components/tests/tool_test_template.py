"""
Test Template for Tool Components - Reusable test patterns for MCP server tools
"""

import pytest
from unittest.mock import Mock, patch


class TestToolComponents:
    """Test cases for tool components"""

    def test_tool_1_basic_functionality(self):
        """Test tool_1 basic input/output functionality"""
        from fastestmcp.components.tools.tool_template import tool_1

        # Test basic functionality
        result = tool_1("test input")
        assert "Tool 1 processed: test input" in result
        assert isinstance(result, str)

    def test_tool_1_empty_input(self):
        """Test tool_1 with empty input"""
        from fastestmcp.components.tools.tool_template import tool_1

        result = tool_1("")
        assert "Tool 1 processed: " in result

    def test_tool_1_special_characters(self):
        """Test tool_1 with special characters"""
        from fastestmcp.components.tools.tool_template import tool_1

        result = tool_1("test@#$%^&*()")
        assert "Tool 1 processed: test@#$%^&*()" in result

    def test_tool_2_basic_functionality(self):
        """Test tool_2 basic input/output functionality"""
        from fastestmcp.components.tools.tool_template import tool_2

        result = tool_2("test input")
        assert "Tool 2 transformed: test input" in result
        assert isinstance(result, str)

    def test_tool_3_basic_functionality(self):
        """Test tool_3 basic input/output functionality"""
        from fastestmcp.components.tools.tool_template import tool_3

        result = tool_3("test input")
        assert "Tool 3 validated: test input" in result
        assert isinstance(result, str)

    def test_register_tools_with_mock_server(self):
        """Test register_tools function with mocked server"""
        from fastestmcp.components.tools.tool_template import register_tools

        mock_server = Mock()
        register_tools(mock_server, count=2)

        # Verify add_tool was called twice
        assert mock_server.add_tool.call_count == 2

    def test_register_tools_zero_count(self):
        """Test register_tools with zero count"""
        from fastestmcp.components.tools.tool_template import register_tools

        mock_server = Mock()
        register_tools(mock_server, count=0)

        # Verify add_tool was not called
        mock_server.add_tool.assert_not_called()

    @patch('fastestmcp.components.tools.tool_template.tool_1')
    def test_register_tools_calls_correct_functions(self, mock_tool_1):
        """Test that register_tools calls the correct tool functions"""
        from fastestmcp.components.tools.tool_template import register_tools

        mock_server = Mock()
        register_tools(mock_server, count=1)

        # Verify the correct function was registered
        mock_server.add_tool.assert_called_once()
        args = mock_server.add_tool.call_args[0]
        assert len(args) == 1
        # The function should be callable
        assert callable(args[0])