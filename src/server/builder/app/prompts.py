"""
MCP Builder Prompts
Provides helpful prompts for FastMCP development tasks
"""

from mcp.server.fastmcp.server import FastMCP

PROMPTS = {
    "server_setup": {
        "name": "FastMCP Server Setup",
        "description": "Guide for setting up a new FastMCP server",
        "content": '''I'll help you set up a new FastMCP server. Here's what we need to do:

1. **Choose a server type:**
   - Basic server (minimal setup)
   - Resource server (with data management)
   - Tool server (focused on functionality)

2. **Project structure:**
   - Create a Python package
   - Set up dependencies
   - Configure the server

3. **Implementation:**
   - Define your server class
   - Add tools and resources
   - Set up the main entry point

Let me know what type of server you want to create and I'll generate the complete setup for you.'''
    },
    "tool_creation": {
        "name": "Tool Creation Guide",
        "description": "Step-by-step guide for creating FastMCP tools",
        "content": '''Creating a FastMCP tool involves these steps:

1. **Define the tool function:**
   ```python
   @server.tool()
   def my_tool(param1: str, param2: int = 0) -> str:
       """Description of what the tool does"""
       # Implementation here
       return f"Result: {param1} with {param2}"
   ```

2. **Parameter types:**
   - `str`: Text input
   - `int`: Integer numbers
   - `float`: Decimal numbers
   - `bool`: True/false values
   - `List[type]`: Arrays of values
   - `Optional[type]`: Optional parameters

3. **Best practices:**
   - Use clear, descriptive names
   - Provide comprehensive docstrings
   - Handle errors gracefully
   - Return meaningful results

What tool would you like to create?'''
    },
    "resource_design": {
        "name": "Resource Design Guide",
        "description": "Guide for designing and implementing MCP resources",
        "content": '''MCP Resources provide data and content to clients. Here's how to design them:

1. **URI Patterns:**
   - `data://namespace/resource`: Static data
   - `file://path/to/file`: File content
   - `api://endpoint`: API responses
   - `config://section/key`: Configuration data

2. **Resource Function:**
   ```python
   @server.resource("data://mydata/items")
   def get_items() -> str:
       """Get all items as JSON"""
       return json.dumps(items, indent=2)
   ```

3. **Best Practices:**
   - Use consistent URI schemes
   - Return appropriate content types
   - Handle access permissions
   - Cache when appropriate

What kind of resource do you need to create?'''
    },
    "testing_guide": {
        "name": "Testing FastMCP Servers",
        "description": "Guide for testing FastMCP server implementations",
        "content": '''Testing your FastMCP server ensures reliability:

1. **Unit Tests:**
   ```python
   def test_my_tool():
       result = my_tool("test")
       assert "test" in result
   ```

2. **Integration Tests:**
   - Test server startup
   - Test tool/resource interactions
   - Test error handling

3. **Test Structure:**
   ```
   tests/
   ├── test_tools.py
   ├── test_resources.py
   ├── test_integration.py
   ```

4. **Running Tests:**
   ```bash
   pytest tests/
   ```

What aspect of testing do you need help with?'''
    },
    "deployment_guide": {
        "name": "Deployment Guide",
        "description": "Guide for deploying FastMCP servers",
        "content": '''Deploying your FastMCP server:

1. **Package your server:**
   - Create setup.py or pyproject.toml
   - Define dependencies
   - Set up entry points

2. **MCP Configuration:**
   ```json
   {
     "mcpServers": {
       "my-server": {
         "command": "python",
         "args": ["-m", "my_server"]
       }
     }
   }
   ```

3. **Distribution:**
   - PyPI for public packages
   - Private repositories for internal use
   - Docker containers for complex deployments

What deployment scenario are you working with?'''
    }
}

def register_prompts(server: FastMCP) -> None:
    """Register all MCP Builder prompts"""

    @server.resource("prompts://list")
    def list_prompts() -> str:
        """List all available development prompts"""
        import json
        prompt_info = []
        for key, prompt in PROMPTS.items():
            prompt_info.append({
                "id": key,
                "name": prompt["name"],
                "description": prompt["description"]
            })
        return json.dumps(prompt_info, indent=2)

    @server.resource("prompts://server_setup")
    def get_server_setup_prompt() -> str:
        """Get the server setup guide"""
        import json
        return json.dumps(PROMPTS["server_setup"], indent=2)

    @server.resource("prompts://tool_creation")
    def get_tool_creation_prompt() -> str:
        """Get the tool creation guide"""
        import json
        return json.dumps(PROMPTS["tool_creation"], indent=2)

    @server.resource("prompts://resource_design")
    def get_resource_design_prompt() -> str:
        """Get the resource design guide"""
        import json
        return json.dumps(PROMPTS["resource_design"], indent=2)

    @server.resource("prompts://testing_guide")
    def get_testing_guide_prompt() -> str:
        """Get the testing guide"""
        import json
        return json.dumps(PROMPTS["testing_guide"], indent=2)

    @server.resource("prompts://deployment_guide")
    def get_deployment_guide_prompt() -> str:
        """Get the deployment guide"""
        import json
        return json.dumps(PROMPTS["deployment_guide"], indent=2)