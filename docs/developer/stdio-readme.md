# Stdio Server — FastMCP Modular Implementation

This folder contains a modular FastMCP-compatible server scaffold with stdio transport, designed for custom MCP server development.

## Overview

The stdio server provides a complete FastMCP server implementation with modular architecture, allowing for full customization and control over server behavior.

## Files

- `server.py` - Main entrypoint that instantiates and runs the FastMCP server
- `app/` - Modular business logic directory containing:
  - `tools.py` - Tool definitions and registration
  - `resources.py` - Resource definitions and registration
  - `prompts.py` - Prompt definitions and registration
  - `subscriptions.py` - Subscription handlers
  - `auth.py` - Authentication providers
  - `discovery.py` - Service discovery logic
  - `schema.py` - Data schema definitions

## Quick Start

1. Run the server:
```sh
python server.py
```

## Architecture

The server uses a modular registration pattern:

```python
server = FastMCP(name="My MCP Server")
register_tools(server)
register_resources(server)
register_prompts(server)
register_subscriptions(server)
register_auth(server)
register_discovery(server)
register_schema(server)
```

## Transport

- **Stdio Transport**: Designed for local MCP clients
- **Modular Registration**: Easy to extend with new components
- **Decorator Pattern**: Clean API for defining tools, resources, and prompts

## Use Cases

- **Custom MCP Development**: Build servers with specific business logic
- **Local Integration**: Perfect for desktop applications and local AI assistants
- **Full Control**: Complete customization of server behavior and capabilities

## Extending

Add new components by:

1. Creating functions in the appropriate `app/` module
2. Using FastMCP decorators (`@server.tool`, `@server.resource`, etc.)
3. Registering the functions in `server.py`

## Testing

See `tests/server/` for comprehensive unit tests covering:
- Tool registration and execution
- Resource handling
- Prompt generation
- Subscription management
- Authentication flows

## Related Documentation

- [FastMCP Server Guide](https://fastmcp.dev/docs/server)
- [MCP Specification](https://modelcontextprotocol.io/specification)