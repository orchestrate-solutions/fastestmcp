"""Resources module for MCP server"""

# Import component system
from fastestmcp.components import register_component


def register_resources(server_app):
    """Register all resources with the server"""
    # Register 2 resource instances using component template
    result = register_component("resources", "resource_template", server_app, count=2)
    if not result["success"]:
        print(f"Warning: Failed to register resources: {result.get('error', 'Unknown error')}")
    return result
