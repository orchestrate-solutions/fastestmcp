# MCP Builder Server

An MCP server that provides FastMCP components, templates, best practices, and development tools to help you build better MCP servers.

## Features

### Resources
- **Templates**: Pre-built FastMCP server templates (basic, resource server, tool server)
- **Best Practices**: Comprehensive guides for error handling, resource design, and tool design
- **Configuration Examples**: Sample `pyproject.toml` and `mcp.json` files
- **Development Prompts**: Interactive guides for common development tasks

### Tools
- **Template Generation**: Generate complete project structures from templates
- **Code Validation**: Validate FastMCP server code for common issues
- **Configuration Validation**: Validate MCP configuration files
- **Boilerplate Generation**: Generate tool and resource boilerplate code
- **Code Analysis**: Analyze server code and provide improvement suggestions

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastmcp-templates
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
cd server/builder
python server.py
```

## Usage

### MCP Configuration

Add to your `mcp.json`:

```json
{
  "mcpServers": {
    "mcp-builder": {
      "command": "python",
      "args": ["-m", "server.builder.server"],
      "cwd": "/path/to/fastmcp-templates"
    }
  }
}
```

### Available Resources

- `templates://list` - List all available templates
- `templates://basic_server` - Basic server template
- `templates://resource_server` - Resource server template
- `templates://tool_server` - Tool server template
- `best-practices://list` - List best practice guides
- `best-practices://error_handling` - Error handling guide
- `best-practices://resource_design` - Resource design guide
- `best-practices://tool_design` - Tool design guide
- `config://examples/pyproject.toml` - Sample pyproject.toml
- `config://examples/mcp.json` - Sample MCP configuration
- `prompts://list` - List development prompts
- `prompts://server_setup` - Server setup guide
- `prompts://tool_creation` - Tool creation guide
- `prompts://resource_design` - Resource design guide
- `prompts://testing_guide` - Testing guide
- `prompts://deployment_guide` - Deployment guide

### Available Tools

- `generate_server_template` - Generate a complete server template
- `validate_server_code` - Validate FastMCP server code
- `validate_mcp_configuration` - Validate MCP configuration
- `generate_tool_boilerplate` - Generate tool boilerplate code
- `generate_resource_boilerplate` - Generate resource boilerplate code
- `analyze_server_code` - Analyze server code for improvements

## Example Usage

### Generate a Basic Server

```python
# Using the generate_server_template tool
result = await call_tool("generate_server_template", {
    "template_type": "basic",
    "project_name": "My Server"
})
```

### Validate Server Code

```python
# Using the validate_server_code tool
code = '''
from mcp.server.fastmcp.server import FastMCP

server = FastMCP(name="Test Server")

@server.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"
'''

result = await call_tool("validate_server_code", {"code": code})
```

### Generate Tool Boilerplate

```python
# Using the generate_tool_boilerplate tool
result = await call_tool("generate_tool_boilerplate", {
    "tool_name": "calculate_sum",
    "description": "Calculate the sum of two numbers",
    "parameters": [
        {"name": "a", "type": "int", "description": "First number"},
        {"name": "b", "type": "int", "description": "Second number"}
    ]
})
```

## Development

The server is organized into modules:

- `server.py` - Main server entry point
- `app/resources.py` - Resource definitions and templates
- `app/tools.py` - Tool implementations
- `app/prompts.py` - Development prompts and guides

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.