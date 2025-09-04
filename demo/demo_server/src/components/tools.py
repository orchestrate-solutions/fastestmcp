"""Tools module for MCP server"""

# Import component system
from fastestmcp.components import register_component


def register_tools(server_app):
    """Register all tools with the server"""
    # Register 3 tool instances using component template
    result = register_component("tools", "tool_template", server_app, count=3)
    if not result["success"]:
        print(f"Warning: Failed to register tools: {result.get('error', 'Unknown error')}")
    return result
