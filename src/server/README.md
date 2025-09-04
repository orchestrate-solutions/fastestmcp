# Server — fastmcp-templates

This folder contains FastMCP server implementations with multiple approaches for different use cases.

## Server Types

### Stdio Server (`stdio/`)
A modular FastMCP-compatible server scaffold with stdio transport.

**Highlights:**
- `stdio/server.py`: Entrypoint — instantiates the FastMCP server, registers tools/resources/prompts/subscriptions, and runs the server.
- `stdio/app/*`: Business logic lives here (auth, discovery, tools, prompts, subscriptions, error handling).

**Quick run (development):**
```sh
python stdio/server.py
```

**Testing:**
- See `tests/server` for unit tests that exercise registration, decorator behavior, and subscription generators.

**Extending:**
- Add new tools via `@server.tool` in `stdio/app/tools.py` and register in `stdio/server.py`.
- Add resources with `@server.resource`, prompts with `@server.prompt`, and subscriptions with `@server.subscription`.

### OpenAPI Server (`openapi/`)
Automatic REST API to MCP server conversion using OpenAPI specifications.

**Highlights:**
- `openapi/api_server.py`: Basic OpenAPI to MCP conversion
- `openapi/api_server_with_resources.py`: Enhanced server with custom route mapping
- `openapi/api_client.py`: Test client for verification
- `openapi/tutorial.md`: Complete step-by-step tutorial

**Quick run:**
```sh
cd openapi
pip install -r requirements.txt
python api_server.py
```

**Features:**
- Automatic tool generation from OpenAPI specs
- HTTP transport support
- Custom route mapping for semantic MCP types
- Complete tutorial and examples

## Choosing a Server Type

- **Use `stdio/`** for:
  - Custom MCP server development
  - Stdio transport (local MCP clients)
  - Full control over server architecture
  - Complex business logic integration

- **Use `openapi/`** for:
  - Converting existing REST APIs to MCP
  - HTTP transport (remote MCP clients)
  - Quick API integration
  - Automatic tool generation from OpenAPI specs
