# OpenAPI Server — FastMCP Integration

This folder contains a complete implementation of the FastMCP OpenAPI integration, demonstrating how to automatically convert REST APIs with OpenAPI specifications into MCP servers.

## Overview

The implementation shows how to use `FastMCP.from_openapi()` to convert any REST API with an OpenAPI spec into a fully-featured MCP server, making every endpoint available as a secure, typed tool for AI models.

## Files

- `tutorial.md` - The original step-by-step tutorial
- `api_server.py` - Basic MCP server implementation using OpenAPI spec
- `api_server_with_resources.py` - Enhanced server with custom route mapping
- `requirements.txt` - Python dependencies

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the basic server:
```bash
python api_server.py
```

3. Test the server using the integration test:
```bash
python -m pytest tests/integration/test_openapi_client.py -v
```

## Implementation Details

### Basic Server (`api_server.py`)

- Uses `FastMCP.from_openapi()` to convert OpenAPI spec to MCP tools
- Automatically generates tools for all API endpoints
- Default behavior: all endpoints become MCP Tools

### Enhanced Server (`api_server_with_resources.py`)

- Includes custom route mapping using `RouteMap`
- GET requests with path parameters become `ResourceTemplate`
- Other GET requests become `Resource`
- Non-GET requests remain as `Tool` (default)

## Architecture

```
OpenAPI Spec → FastMCP.from_openapi() → MCP Server → Tools/Resources
                                      ↓
HTTP Transport (port 8000) ← Integration Test
```

## Route Mapping Configuration

The enhanced server demonstrates advanced route mapping:

```python
route_maps=[
    # GET /users/{id} → ResourceTemplate
    RouteMap(methods=["GET"], pattern=r".*\{.*\}.*", mcp_type=MCPType.RESOURCE_TEMPLATE),
    # GET /users → Resource
    RouteMap(methods=["GET"], mcp_type=MCPType.RESOURCE),
]
```

## Testing

The implementation includes integration tests that:
- Connect to `http://127.0.0.1:8000/mcp/`
- Lists all generated tools
- Calls `get_user_by_id` tool with `{"id": 1}`
- Displays the JSON response from the live API

Run the integration test:
```bash
python -m pytest tests/integration/test_openapi_client.py -v
```

## Use Cases

- **API Integration**: Make any REST API available to LLMs
- **Tool Generation**: Automatic tool creation from OpenAPI specs
- **Resource Mapping**: Semantic mapping of GET requests to MCP Resources
- **Testing**: Complete test harness for MCP server validation

## Dependencies

- `fastmcp` - Core MCP server framework
- `httpx` - Async HTTP client for API calls

## Related Documentation

- [FastMCP OpenAPI Integration](https://fastmcp.dev/docs/openapi)
- [MCP Specification](https://modelcontextprotocol.io/specification)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com)