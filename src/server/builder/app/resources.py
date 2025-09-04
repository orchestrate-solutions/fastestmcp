"""
MCP Builder Resources
Provides FastMCP components, templates, and best practices as MCP resources
"""

import json

from mcp.server.fastmcp.server import FastMCP

# Template data for FastMCP components
TEMPLATES = {
    "basic_server": {
        "name": "Basic MCP Server",
        "description": "A minimal MCP server template with stdio transport",
        "files": {
            "server.py": '''from mcp.server.fastmcp.server import FastMCP

server = FastMCP(name="My MCP Server")

@server.tool()
def hello_world(name: str) -> str:
    """Say hello to someone"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    server.run(transport="stdio")''',
            "requirements.txt": "fastmcp>=0.9.0",
            "README.md": '''# My MCP Server

A basic MCP server that provides a hello world tool.

## Usage

Run the server:
```bash
python server.py
```

## Tools

- `hello_world`: Says hello to a given name
'''
        }
    },
    "resource_server": {
        "name": "Resource Server Template",
        "description": "MCP server template with resource management",
        "files": {
            "server.py": '''from mcp.server.fastmcp.server import FastMCP
from typing import Dict, Any

server = FastMCP(name="Resource MCP Server")

# Sample data resource
SAMPLE_DATA = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ],
    "products": [
        {"id": 1, "name": "Widget", "price": 19.99},
        {"id": 2, "name": "Gadget", "price": 29.99}
    ]
}

@server.resource("data://users")
def get_users() -> str:
    """Get all users data"""
    return json.dumps(SAMPLE_DATA["users"], indent=2)

@server.resource("data://products")
def get_products() -> str:
    """Get all products data"""
    return json.dumps(SAMPLE_DATA["products"], indent=2)

@server.tool()
def search_users(query: str) -> str:
    """Search users by name"""
    users = SAMPLE_DATA["users"]
    results = [u for u in users if query.lower() in u["name"].lower()]
    return json.dumps(results, indent=2)

if __name__ == "__main__":
    server.run(transport="stdio")''',
            "requirements.txt": "fastmcp>=0.9.0",
            "README.md": '''# Resource MCP Server

An MCP server that demonstrates resource management and data serving.

## Resources

- `data://users`: JSON list of users
- `data://products`: JSON list of products

## Tools

- `search_users`: Search users by name
'''
        }
    },
    "tool_server": {
        "name": "Tool Server Template",
        "description": "MCP server template focused on tool development",
        "files": {
            "server.py": '''from mcp.server.fastmcp.server import FastMCP
import math
from typing import List, Dict, Any

server = FastMCP(name="Tool MCP Server")

@server.tool()
def calculate_fibonacci(n: int) -> List[int]:
    """Calculate first n Fibonacci numbers"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

@server.tool()
def analyze_text(text: str) -> Dict[str, Any]:
    """Analyze text statistics"""
    words = text.split()
    sentences = text.split('.')
    chars = len(text)

    return {
        "character_count": chars,
        "word_count": len(words),
        "sentence_count": len(sentences),
        "average_word_length": chars / len(words) if words else 0,
        "longest_word": max(words, key=len) if words else ""
    }

@server.tool()
def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
    # Convert to Celsius first
    if from_unit.lower() == "fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit.lower() == "kelvin":
        celsius = value - 273.15
    elif from_unit.lower() == "celsius":
        celsius = value
    else:
        raise ValueError(f"Unsupported temperature unit: {from_unit}")

    # Convert from Celsius to target unit
    if to_unit.lower() == "fahrenheit":
        return celsius * 9/5 + 32
    elif to_unit.lower() == "kelvin":
        return celsius + 273.15
    elif to_unit.lower() == "celsius":
        return celsius
    else:
        raise ValueError(f"Unsupported temperature unit: {to_unit}")

if __name__ == "__main__":
    server.run(transport="stdio")''',
            "requirements.txt": "fastmcp>=0.9.0",
            "README.md": '''# Tool MCP Server

An MCP server showcasing various tool implementations.

## Tools

- `calculate_fibonacci`: Generate Fibonacci sequence
- `analyze_text`: Text statistics and analysis
- `convert_temperature`: Temperature unit conversion
'''
        }
    }
}

BEST_PRACTICES = {
    "error_handling": {
        "title": "Error Handling Best Practices",
        "content": '''# Error Handling in MCP Servers

## Key Principles

1. **Graceful Degradation**: Handle errors without crashing the server
2. **Informative Messages**: Provide clear error messages to clients
3. **Logging**: Log errors for debugging while keeping user messages clean
4. **Validation**: Validate inputs early and provide helpful feedback

## Example Implementation

```python
@server.tool()
def process_data(data: str) -> str:
    """Process data with proper error handling"""
    try:
        # Validate input
        if not data:
            raise ValueError("Data cannot be empty")

        # Process data
        result = perform_processing(data)
        return f"Processed: {result}"

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return f"Error: {str(e)}"

    except Exception as e:
        logger.error(f"Unexpected error processing data: {e}")
        return "An unexpected error occurred. Please try again."
```
'''
    },
    "resource_design": {
        "title": "Resource Design Patterns",
        "content": '''# MCP Resource Design Patterns

## Resource URI Patterns

- `data://namespace/resource`: Static data resources
- `file://path/to/file`: File-based resources
- `api://endpoint`: API endpoint resources
- `config://section/key`: Configuration resources

## Best Practices

1. **Consistent Naming**: Use clear, hierarchical URIs
2. **Caching**: Implement appropriate caching strategies
3. **Security**: Validate resource access permissions
4. **Documentation**: Document resource schemas and usage

## Example Resource

```python
@server.resource("config://app/settings")
def get_app_settings() -> str:
    """Get application settings as JSON"""
    settings = {
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "max_connections": int(os.getenv("MAX_CONNECTIONS", "100")),
        "timeout": int(os.getenv("TIMEOUT", "30"))
    }
    return json.dumps(settings, indent=2)
```
'''
    },
    "tool_design": {
        "title": "Tool Design Guidelines",
        "content": '''# MCP Tool Design Guidelines

## Tool Function Best Practices

1. **Clear Purpose**: Each tool should have a single, well-defined purpose
2. **Descriptive Names**: Use action-oriented names (get_user, create_file)
3. **Parameter Validation**: Validate all inputs with helpful error messages
4. **Return Types**: Use appropriate return types (str, dict, list)
5. **Documentation**: Provide comprehensive docstrings

## Parameter Types

- **Primitive Types**: str, int, float, bool
- **Complex Types**: Use TypedDict for structured data
- **Optional Parameters**: Use Union types with None
- **Lists**: Use List[type] for collections

## Example Tool

```python
from typing import List, Optional

@server.tool()
def search_documents(
    query: str,
    limit: Optional[int] = 10,
    categories: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """Search documents with optional filters"""
    # Implementation here
    pass
```
'''
    }
}

def register_resources(server: FastMCP) -> None:
    """Register all MCP Builder resources"""

    # Template resources
    @server.resource("templates://list")
    def list_templates() -> str:
        """List all available FastMCP server templates"""
        template_info = []
        for key, template in TEMPLATES.items():
            template_info.append({
                "id": key,
                "name": template["name"],
                "description": template["description"],
                "files": list(template["files"].keys())
            })
        return json.dumps(template_info, indent=2)

    @server.resource("templates://basic_server")
    def get_basic_server_template() -> str:
        """Get the basic server template"""
        return json.dumps(TEMPLATES["basic_server"], indent=2)

    @server.resource("templates://resource_server")
    def get_resource_server_template() -> str:
        """Get the resource server template"""
        return json.dumps(TEMPLATES["resource_server"], indent=2)

    @server.resource("templates://tool_server")
    def get_tool_server_template() -> str:
        """Get the tool server template"""
        return json.dumps(TEMPLATES["tool_server"], indent=2)

    # Best practices resources
    @server.resource("best-practices://list")
    def list_best_practices() -> str:
        """List all available best practices guides"""
        practice_info = []
        for key, practice in BEST_PRACTICES.items():
            practice_info.append({
                "id": key,
                "title": practice["title"]
            })
        return json.dumps(practice_info, indent=2)

    @server.resource("best-practices://error_handling")
    def get_error_handling_practices() -> str:
        """Get error handling best practices"""
        return json.dumps(BEST_PRACTICES["error_handling"], indent=2)

    @server.resource("best-practices://resource_design")
    def get_resource_design_practices() -> str:
        """Get resource design best practices"""
        return json.dumps(BEST_PRACTICES["resource_design"], indent=2)

    @server.resource("best-practices://tool_design")
    def get_tool_design_practices() -> str:
        """Get tool design best practices"""
        return json.dumps(BEST_PRACTICES["tool_design"], indent=2)

    # Configuration examples
    @server.resource("config://examples/pyproject.toml")
    def get_pyproject_example() -> str:
        """Get example pyproject.toml for MCP servers"""
        return '''[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-mcp-server"
version = "0.1.0"
description = "My MCP Server"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
dependencies = [
    "fastmcp>=0.9.0"
]

[project.scripts]
my-server = "my_server:main"

[tool.setuptools.packages.find]
where = ["."]'''

    @server.resource("config://examples/mcp.json")
    def get_mcp_config_example() -> str:
        """Get example MCP configuration"""
        return '''{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_server"],
      "env": {
        "DEBUG": "true"
      }
    }
  }
}'''