"""
Shared generator functions for FastestMCP CLI
Now uses the component-based system for generating code
"""

from ..components.component_loader import ComponentLoader

# Initialize component loader
component_loader = ComponentLoader()


def generate_tools_file(tools: int, server_type: str) -> str:
    """Generate tools.py file using component templates"""
    if tools == 0:
        return ""

    code_lines = [
        '"""Tools module for MCP server"""',
        '',
        '# Import component system',
        'from fastestmcp.components import register_component',
        '',
        '',
        'def register_tools(server_app):',
        '    """Register all tools with the server"""',
        f'    # Register {tools} tool instances using component template',
        f'    result = register_component("tools", "tool_template", server_app, count={tools})',
        '    if not result["success"]:',
        '        print(f"Warning: Failed to register tools: {result.get(\'error\', \'Unknown error\')}")',
        '    return result',
        ''
    ]

    return '\n'.join(code_lines)


def generate_resources_file(resources: int, server_type: str) -> str:
    """Generate resources.py file using component templates"""
    if resources == 0:
        return ""

    code_lines = [
        '"""Resources module for MCP server"""',
        '',
        '# Import component system',
        'from fastestmcp.components import register_component',
        '',
        '',
        'def register_resources(server_app):',
        '    """Register all resources with the server"""',
        f'    # Register {resources} resource instances using component template',
        f'    result = register_component("resources", "resource_template", server_app, count={resources})',
        '    if not result["success"]:',
        '        print(f"Warning: Failed to register resources: {result.get(\'error\', \'Unknown error\')}")',
        '    return result',
        ''
    ]

    return '\n'.join(code_lines)


def generate_prompts_file(prompts: int, server_type: str) -> str:
    """Generate prompts.py file using component templates"""
    if prompts == 0:
        return ""

    code_lines = [
        '"""Prompts module for MCP server"""',
        '',
        '# Import component system',
        'from fastestmcp.components import register_component',
        '',
        '',
        'def register_prompts(server_app):',
        '    """Register all prompts with the server"""',
        f'    # Register {prompts} prompt instances using component template',
        f'    result = register_component("prompts", "prompt_template", server_app, count={prompts})',
        '    if not result["success"]:',
        '        print(f"Warning: Failed to register prompts: {result.get(\'error\', \'Unknown error\')}")',
        '    return result',
        ''
    ]

    return '\n'.join(code_lines)


def generate_notifications_file_wrapper(notifications: int, server_type: str) -> str:
    """Generate notifications.py file using component templates"""
    if notifications == 0:
        return ""

    code_lines = [
        '"""Notifications module for MCP server"""',
        '',
        '# Import component system',
        'from fastestmcp.components import register_component',
        '',
        '',
        'def register_notifications(server_app):',
        '    """Register all notification subscriptions with the server"""',
        f'    # Register {notifications} notification instances using component template',
        f'    result = register_component("notifications", "notification_template", server_app, count={notifications})',
        '    if not result["success"]:',
        '        print(f"Warning: Failed to register notifications: {result.get(\'error\', \'Unknown error\')}")',
        '    return result',
        ''
    ]

    return '\n'.join(code_lines)


def generate_subscriptions_file_wrapper(subscriptions: int, server_type: str) -> str:
    """Generate subscriptions.py file using component templates"""
    if subscriptions == 0:
        return ""

    code_lines = [
        '"""Subscriptions module for MCP server"""',
        '',
        '# Import component system',
        'from fastestmcp.components import register_component',
        '',
        '',
        'def register_subscriptions(server_app):',
        '    """Register all subscription handlers with the server"""',
        f'    # Register {subscriptions} subscription instances using component template',
        f'    result = register_component("subscriptions", "subscription_template", server_app, count={subscriptions})',
        '    if not result["success"]:',
        '        print(f"Warning: Failed to register subscriptions: {result.get(\'error\', \'Unknown error\')}")',
        '    return result',
        ''
    ]

    return '\n'.join(code_lines)