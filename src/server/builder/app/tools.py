"""
MCP Builder Tools
Provides tools for generating FastMCP components and validating configurations
"""

import json
import re
from typing import Dict, List, Any

from mcp.server.fastmcp.server import FastMCP

def validate_python_code(code: str) -> List[str]:
    """Basic Python code validation"""
    errors = []

    # Check for syntax errors
    try:
        compile(code, '<string>', 'exec')
    except SyntaxError as e:
        errors.append(f"Syntax error: {e}")

    # Check for common issues
    if 'import' in code and 'from' not in code:
        # This might be okay, but let's check for proper imports
        pass

    # Check for FastMCP usage
    if 'FastMCP' not in code:
        errors.append("Warning: No FastMCP import found")

    return errors

def generate_project_structure(template_name: str, project_name: str) -> Dict[str, str]:
    """Generate project structure from template"""
    templates = {
        "basic": {
            "server.py": '''from mcp.server.fastmcp.server import FastMCP

server = FastMCP(name="''' + project_name + '''")

@server.tool()
def hello_world(name: str) -> str:
    """Say hello to someone"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    server.run(transport="stdio")''',
            "requirements.txt": "fastmcp>=0.9.0",
            "README.md": '''# ''' + project_name + '''

A basic MCP server.

## Usage

```bash
python server.py
```'''
        },
        "full": {
            "server.py": '''from mcp.server.fastmcp.server import FastMCP
import json
from typing import List, Dict, Any

server = FastMCP(name="''' + project_name + '''")

# Sample data
DATA = {
    "items": [
        {"id": 1, "name": "Item 1", "value": 100},
        {"id": 2, "name": "Item 2", "value": 200}
    ]
}

@server.resource("data://items")
def get_items() -> str:
    """Get all items"""
    return json.dumps(DATA["items"], indent=2)

@server.tool()
def add_item(name: str, value: int) -> str:
    """Add a new item"""
    new_id = max(item["id"] for item in DATA["items"]) + 1
    new_item = {"id": new_id, "name": name, "value": value}
    DATA["items"].append(new_item)
    return f"Added item: {new_item}"

@server.tool()
def get_item_by_id(item_id: int) -> str:
    """Get item by ID"""
    for item in DATA["items"]:
        if item["id"] == item_id:
            return json.dumps(item, indent=2)
    return f"Item with ID {item_id} not found"

if __name__ == "__main__":
    server.run(transport="stdio")''',
            "requirements.txt": "fastmcp>=0.9.0\npytest>=7.0.0",
            "pyproject.toml": '''[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "''' + project_name.lower().replace(' ', '-') + '''"
version = "0.1.0"
description = "''' + project_name + ''' MCP Server"
dependencies = [
    "fastmcp>=0.9.0"
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]''',
            "README.md": '''# ''' + project_name + '''

A full-featured MCP server with resources and tools.

## Features

- Resource management
- Tool implementations
- Data persistence (in-memory)

## Usage

```bash
python server.py
```

## Resources

- `data://items`: JSON list of items

## Tools

- `add_item`: Add a new item
- `get_item_by_id`: Retrieve item by ID
''',
            "tests/test_server.py": '''import pytest
from ''' + project_name.lower().replace(' ', '_').replace('-', '_') + ''' import server

def test_server_creation():
    """Test that server can be created"""
    assert server.name == "''' + project_name + '''"

def test_add_item():
    """Test adding an item"""
    initial_count = len(server.DATA["items"])
    result = server.add_item("Test Item", 150)
    assert "Added item" in result
    assert len(server.DATA["items"]) == initial_count + 1

def test_get_item_by_id():
    """Test getting item by ID"""
    result = server.get_item_by_id(1)
    assert '"id": 1' in result
    assert '"name": "Item 1"' in result
'''
        }
    }

    return templates.get(template_name, templates["basic"])

def validate_mcp_config(config_json: str) -> Dict[str, Any]:
    """Validate MCP configuration JSON"""
    result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }

    try:
        config = json.loads(config_json)
    except json.JSONDecodeError as e:
        result["valid"] = False
        result["errors"].append(f"Invalid JSON: {e}")
        return result

    # Check for required structure
    if "mcpServers" not in config:
        result["valid"] = False
        result["errors"].append("Missing 'mcpServers' key")

    if "mcpServers" in config:
        servers = config["mcpServers"]
        if not isinstance(servers, dict):
            result["valid"] = False
            result["errors"].append("'mcpServers' must be an object")

        for server_name, server_config in servers.items():
            if not isinstance(server_config, dict):
                result["errors"].append(f"Server '{server_name}' config must be an object")
                continue

            # Check for required fields
            if "command" not in server_config:
                result["errors"].append(f"Server '{server_name}' missing 'command' field")

            # Check for optional but recommended fields
            if "args" not in server_config:
                result["warnings"].append(f"Server '{server_name}' missing 'args' field")

    return result

def register_tools(server: FastMCP) -> None:
    """Register all MCP Builder tools"""

    @server.tool()
    def generate_server_template(template_type: str, project_name: str) -> str:
        """Generate a FastMCP server template

        Args:
            template_type: Type of template ('basic' or 'full')
            project_name: Name of the project

        Returns:
            JSON string with generated files
        """
        if template_type not in ["basic", "full"]:
            return json.dumps({
                "error": "Invalid template type. Use 'basic' or 'full'",
                "available_types": ["basic", "full"]
            }, indent=2)

        files = generate_project_structure(template_type, project_name)
        return json.dumps({
            "project_name": project_name,
            "template_type": template_type,
            "files": files
        }, indent=2)

    @server.tool()
    def validate_server_code(code: str) -> str:
        """Validate FastMCP server code

        Args:
            code: Python code to validate

        Returns:
            JSON string with validation results
        """
        errors = validate_python_code(code)

        result = {
            "valid": len(errors) == 0,
            "errors": [e for e in errors if "Syntax error" in e],
            "warnings": [e for e in errors if "Warning" in e]
        }

        return json.dumps(result, indent=2)

    @server.tool()
    def validate_mcp_configuration(config_json: str) -> str:
        """Validate MCP configuration JSON

        Args:
            config_json: MCP configuration as JSON string

        Returns:
            JSON string with validation results
        """
        result = validate_mcp_config(config_json)
        return json.dumps(result, indent=2)

    @server.tool()
    def generate_tool_boilerplate(tool_name: str, description: str, parameters: List[Dict[str, str]]) -> str:
        """Generate boilerplate code for a FastMCP tool

        Args:
            tool_name: Name of the tool function
            description: Description of what the tool does
            parameters: List of parameter dictionaries with 'name', 'type', and 'description'

        Returns:
            Generated Python code for the tool
        """
        # Build parameter list
        param_list = []
        type_hints = []
        for param in parameters:
            name = param.get("name", "param")
            param_type = param.get("type", "str")
            param_desc = param.get("description", "")

            param_list.append(f"{name}: {param_type}")
            type_hints.append(f"        {name}: {param_desc}")

        params_str = ", ".join(param_list)
        type_hint_str = "\n".join(type_hints)

        # Generate the tool code
        code = '''@server.tool()
def ''' + tool_name + '''(''' + params_str + ''') -> str:
    """''' + description + '''
''' + type_hint_str + '''
    """
    # TODO: Implement the tool logic here
    return "''' + tool_name + ''' called with parameters: {parameters}"'''

        return code

    @server.tool()
    def generate_resource_boilerplate(resource_uri: str, description: str, return_type: str = "str") -> str:
        """Generate boilerplate code for a FastMCP resource

        Args:
            resource_uri: URI for the resource
            description: Description of the resource
            return_type: Return type of the resource function

        Returns:
            Generated Python code for the resource
        """
        func_name = resource_uri.replace('://', '_').replace('/', '_')
        code = '''@server.resource("''' + resource_uri + '''")
def get_''' + func_name + '''() -> ''' + return_type + ''':
    """''' + description + '''"""
    # TODO: Implement the resource logic here
    return "''' + resource_uri + ''' resource data"'''

        return code

    @server.tool()
    def analyze_server_code(code: str) -> str:
        """Analyze FastMCP server code for improvements

        Args:
            code: Python code to analyze

        Returns:
            JSON string with analysis results
        """
        analysis = {
            "tools_found": [],
            "resources_found": [],
            "imports": [],
            "suggestions": []
        }

        # Find tools
        tool_pattern = r'@server\.tool\(\)\s*\n\s*def\s+(\w+)'
        tool_matches = re.findall(tool_pattern, code)
        analysis["tools_found"] = tool_matches

        # Find resources
        resource_pattern = r'@server\.resource\(["\']([^"\']+)["\']'
        resource_matches = re.findall(resource_pattern, code)
        analysis["resources_found"] = resource_matches

        # Find imports
        import_pattern = r'^(?:from|import)\s+(.+)'
        import_matches = re.findall(import_pattern, code, re.MULTILINE)
        analysis["imports"] = import_matches

        # Generate suggestions
        if not tool_matches and not resource_matches:
            analysis["suggestions"].append("Add at least one tool or resource to make the server useful")

        if "FastMCP" not in code:
            analysis["suggestions"].append("Import FastMCP from mcp.server.fastmcp.server")

        if 'if __name__ == "__main__":' not in code:
            analysis["suggestions"].append("Add main block to run the server")

        return json.dumps(analysis, indent=2)