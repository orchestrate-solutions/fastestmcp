"""
Template and level handling functions for FastestMCP CLI
"""

from .templates import TEMPLATES
from .main_generator import generate_complex_server


def generate_level_boilerplate(level: int, name: str, output_dir: str) -> str:
    """Generate server based on complexity level"""
    # Define component counts based on level
    level_configs = {
        1: {'tools': 1, 'resources': 0, 'prompts': 0, 'transport': 'stdio', 'structure': 'mono'},
        2: {'tools': 2, 'resources': 1, 'prompts': 0, 'transport': 'stdio', 'structure': 'mono'},
        3: {'tools': 3, 'resources': 2, 'prompts': 1, 'transport': 'stdio', 'structure': 'structured'},
        4: {'tools': 4, 'resources': 3, 'prompts': 2, 'transport': 'http', 'structure': 'structured'},
        5: {'tools': 5, 'resources': 4, 'prompts': 3, 'transport': 'http', 'structure': 'structured'}
    }

    if level not in level_configs:
        raise ValueError(f"Invalid level: {level}")

    config = level_configs[level]

    message, structure = generate_complex_server(
        name=name,
        tools=config['tools'],
        resources=config['resources'],
        prompts=config['prompts'],
        notifications=0,
        subscriptions=0,
        transport=config['transport'],
        structure=config['structure'],
        server_type='fastmcp',
        output_dir=output_dir
    )

    return f"Level {level} boilerplate generated: {message}"


def generate_server_from_template(template_name: str, name: str, output_dir: str) -> str:
    """Generate server from predefined template"""
    if template_name not in TEMPLATES:
        raise ValueError(f"Template '{template_name}' not found")

    template = TEMPLATES[template_name]
    tools = len(template.get('tools', []))
    resources = len(template.get('resources', []))
    prompts = len(template.get('prompts', []))
    notifications = len(template.get('notifications', []))
    subscriptions = len(template.get('subscriptions', []))

    # Use default transport and structure for templates
    message, structure = generate_complex_server(
        name=name,
        tools=tools,
        resources=resources,
        prompts=prompts,
        notifications=notifications,
        subscriptions=subscriptions,
        transport='stdio',
        structure='mono',
        server_type='fastmcp',
        output_dir=output_dir
    )

    return f"Template '{template_name}' server generated: {message}"