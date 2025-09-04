#!/usr/bin/env python3
"""
FastestMCP CLI - Main entry point
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any

# Import from our modular CLI components
from .templates import TEMPLATES, CLIENT_TEMPLATES
from .server_generator import generate_complex_server, generate_level_boilerplate, generate_server_from_template
from .client_generator import generate_complex_client


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="FastestMCP CLI - Advanced boilerplate generator with granular component control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fastestmcp server --level 1 --name myapp --transport stdio --structure mono
  fastestmcp server --template weather --name myweather --structure structured
  fastestmcp server --type openapi --name api-server --transport http
  fastestmcp server --name custom --tools 3 --resources 2 --prompts 1 --transport http --structure structured

Client Examples:
  fastestmcp client --name myclient --apis 3 --integrations 2 --transport http --structure structured
  fastestmcp client --template api-client --name myapi --structure mono
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Server generation command
    server_parser = subparsers.add_parser('server', help='Generate MCP server')
    server_parser.add_argument('--level', type=int, choices=[1, 2, 3, 4, 5], help='Generation level (1-5, higher = more complex)')
    server_parser.add_argument('--template', choices=list(TEMPLATES.keys()), help='Use a predefined template')
    server_parser.add_argument('--name', required=True, help='Name of the project/server')
    server_parser.add_argument('--tools', type=int, default=2, help='Number of tools to generate (default: 2)')
    server_parser.add_argument('--resources', type=int, default=1, help='Number of resources to generate (default: 1)')
    server_parser.add_argument('--prompts', type=int, default=0, help='Number of prompts to generate (default: 0)')
    server_parser.add_argument('--notifications', type=int, default=0, help='Number of notification types to generate (default: 0)')
    server_parser.add_argument('--subscriptions', type=int, default=0, help='Number of subscription types to generate (default: 0)')
    server_parser.add_argument('--transport', choices=['stdio', 'http', 'sse'], default='stdio', help='Transport type for server (default: stdio)')
    server_parser.add_argument('--structure', choices=['mono', 'structured'], default='mono', help='Project structure (default: mono)')
    server_parser.add_argument('--type', choices=['fastmcp', 'mcp'], default='fastmcp', help='MCP server type (default: fastmcp)')
    server_parser.add_argument('--output', default='.', help='Output directory (default: current directory)')

    # Client generation command
    client_parser = subparsers.add_parser('client', help='Generate MCP client')
    client_parser.add_argument('--template', choices=list(CLIENT_TEMPLATES.keys()), help='Use a predefined client template')
    client_parser.add_argument('--name', required=True, help='Name of the client')
    client_parser.add_argument('--apis', type=int, default=2, help='Number of API endpoints for client (default: 2)')
    client_parser.add_argument('--integrations', type=int, default=1, help='Number of integrations for client (default: 1)')
    client_parser.add_argument('--handlers', type=int, default=1, help='Number of event handlers for client (default: 1)')
    client_parser.add_argument('--notifications', type=int, default=0, help='Number of notification subscriptions for client (default: 0)')
    client_parser.add_argument('--subscriptions', type=int, default=0, help='Number of subscription handlers for client (default: 0)')
    client_parser.add_argument('--transport', choices=['stdio', 'http', 'websocket'], default='stdio', help='Transport type for client (default: stdio)')
    client_parser.add_argument('--structure', choices=['mono', 'structured'], default='mono', help='Project structure (default: mono)')
    client_parser.add_argument('--type', choices=['fastmcp', 'mcp'], default='fastmcp', help='MCP client type (default: fastmcp)')
    client_parser.add_argument('--output', default='.', help='Output directory (default: current directory)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == 'server':
            # Server generation
            if args.level:
                # Level-based generation
                result = generate_level_boilerplate(args.level, args.name, args.output)
                print(f"✅ {result}")

            elif args.template:
                # Template-based generation
                result = generate_server_from_template(args.template, args.name, args.output)
                print(f"✅ {result}")

            else:
                # Custom server generation with transport support
                print(f"DEBUG: Generating server with notifications={args.notifications}, subscriptions={args.subscriptions}")
                message, structure = generate_complex_server(
                    name=args.name,
                    tools=args.tools,
                    resources=args.resources,
                    prompts=args.prompts,
                    notifications=args.notifications,
                    subscriptions=args.subscriptions,
                    transport=args.transport,
                    structure=args.structure,
                    server_type=args.type,
                    output_dir=args.output
                )
                print(f"✅ {message}")
                print(structure)

        elif args.command == 'client':
            # Client generation
            if args.template:
                # Template-based client generation
                template = CLIENT_TEMPLATES[args.template]
                message, structure = generate_complex_client(
                    name=args.name,
                    apis=len(template.get('apis', [])),
                    integrations=len(template.get('integrations', [])),
                    handlers=len(template.get('handlers', [])),
                    notifications=len(template.get('notifications', [])),
                    subscriptions=len(template.get('subscriptions', [])),
                    transport=args.transport,
                    structure=args.structure,
                    client_type=args.type,
                    output_dir=args.output
                )
                print(f"✅ {message}")
                print(structure)

            else:
                # Custom client generation
                message, structure = generate_complex_client(
                    name=args.name,
                    apis=args.apis,
                    integrations=args.integrations,
                    handlers=args.handlers,
                    notifications=args.notifications,
                    subscriptions=args.subscriptions,
                    transport=args.transport,
                    structure=args.structure,
                    client_type=args.type,
                    output_dir=args.output
                )
                print(f"✅ {message}")
                print(structure)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()