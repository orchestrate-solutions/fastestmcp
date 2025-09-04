"""Subscriptions module for MCP server"""

# Import component system
from fastestmcp.components import register_component


def register_subscriptions(server_app):
    """Register all subscription handlers with the server"""
    # Register 1 subscription instances using component template
    result = register_component("subscriptions", "subscription_template", server_app, count=1)
    if not result["success"]:
        print(f"Warning: Failed to register subscriptions: {result.get('error', 'Unknown error')}")
    return result
