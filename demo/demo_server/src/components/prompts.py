"""Prompts module for MCP server"""

# Import component system
from fastestmcp.components import register_component


def register_prompts(server_app):
    """Register all prompts with the server"""
    # Register 2 prompt instances using component template
    result = register_component("prompts", "prompt_template", server_app, count=2)
    if not result["success"]:
        print(f"Warning: Failed to register prompts: {result.get('error', 'Unknown error')}")
    return result
