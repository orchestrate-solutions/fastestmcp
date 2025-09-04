"""Notifications module for MCP server"""

# Import component system
from fastestmcp.components import register_component


def register_notifications(server_app):
    """Register all notification subscriptions with the server"""
    # Register 1 notification instances using component template
    result = register_component("notifications", "notification_template", server_app, count=1)
    if not result["success"]:
        print(f"Warning: Failed to register notifications: {result.get('error', 'Unknown error')}")
    return result
