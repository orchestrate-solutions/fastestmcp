"""
Test Template for Resource Components - Reusable test patterns for MCP server resources
"""

import pytest
from unittest.mock import Mock, patch
from pydantic import AnyUrl


class TestResourceComponents:
    """Test cases for resource components"""

    def test_get_resource_1_basic_structure(self):
        """Test get_resource_1 returns correct data structure"""
        from fastestmcp.components.resources.resource_template import get_resource_1

        result = get_resource_1()

        assert isinstance(result, dict)
        assert "resource" in result
        assert "data" in result
        assert "type" in result
        assert result["resource"] == 1
        assert result["type"] == "example"

    def test_get_resource_2_basic_structure(self):
        """Test get_resource_2 returns correct data structure"""
        from fastestmcp.components.resources.resource_template import get_resource_2

        result = get_resource_2()

        assert isinstance(result, dict)
        assert result["resource"] == 2
        assert result["type"] == "configuration"

    def test_get_resource_3_basic_structure(self):
        """Test get_resource_3 returns correct data structure"""
        from fastestmcp.components.resources.resource_template import get_resource_3

        result = get_resource_3()

        assert isinstance(result, dict)
        assert result["resource"] == 3
        assert result["type"] == "metadata"

    def test_create_resource_basic_structure(self):
        """Test create_resource returns proper Resource object"""
        from fastestmcp.components.resources.resource_template import create_resource

        result = create_resource(1)

        assert hasattr(result, 'uri')
        assert hasattr(result, 'name')
        assert hasattr(result, 'description')
        assert hasattr(result, 'mimeType')
        assert result.name == "Resource 1"
        assert result.description == "Resource 1 data"
        assert result.mimeType == "application/json"

    def test_create_resource_uri_format(self):
        """Test create_resource generates correct URI"""
        from fastestmcp.components.resources.resource_template import create_resource

        result = create_resource(5)

        assert str(result.uri) == "resource://resource_5"
        assert result.name == "Resource 5"

    def test_register_resources_with_mock_server(self):
        """Test register_resources function with mocked server"""
        from fastestmcp.components.resources.resource_template import register_resources

        mock_server = Mock()
        register_resources(mock_server, count=3)

        # Verify add_resource was called three times
        assert mock_server.add_resource.call_count == 3

    def test_register_resources_zero_count(self):
        """Test register_resources with zero count"""
        from fastestmcp.components.resources.resource_template import register_resources

        mock_server = Mock()
        register_resources(mock_server, count=0)

        # Verify add_resource was not called
        mock_server.add_resource.assert_not_called()

    def test_resource_data_consistency(self):
        """Test that resource data is consistent across calls"""
        from fastestmcp.components.resources.resource_template import get_resource_1

        result1 = get_resource_1()
        result2 = get_resource_1()

        assert result1 == result2
        assert result1["resource"] == result2["resource"]
        assert result1["type"] == result2["type"]

    def test_multiple_resources_unique_data(self):
        """Test that different resources return different data"""
        from fastestmcp.components.resources.resource_template import get_resource_1, get_resource_2

        result1 = get_resource_1()
        result2 = get_resource_2()

        assert result1["resource"] != result2["resource"]
        assert result1["resource"] == 1
        assert result2["resource"] == 2