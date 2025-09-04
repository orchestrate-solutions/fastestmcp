import httpx
from fastmcp import FastMCP

# Import all the modular components
from app.auth import register_auth
from app.error_handling import register_error_handlers
from app.prompts import register_prompts
from app.resources import register_resources
from app.subscriptions import register_subscriptions
from app.discovery import register_discovery
from app.schema import register_schema
from app.notifications import register_notifications
from app.tools import register_tools

# Create an HTTP client for the target API
client = httpx.AsyncClient(base_url="https://jsonplaceholder.typicode.com")

# Define a simplified OpenAPI spec for JSONPlaceholder
openapi_spec = {
    "openapi": "3.0.0",
    "info": {"title": "JSONPlaceholder API", "version": "1.0"},
    "paths": {
        "/users": {
            "get": {
                "summary": "Get all users",
                "operationId": "get_users",
                "responses": {"200": {"description": "A list of users."}}
            }
        },
        "/users/{id}": {
            "get": {
                "summary": "Get a user by ID",
                "operationId": "get_user_by_id",
                "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                "responses": {"200": {"description": "A single user."}}
            }
        }
    }
}

# Create the MCP server from the OpenAPI spec
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="JSONPlaceholder MCP Server"
)

# Register all the modular components
register_auth(mcp)
register_error_handlers(mcp)
register_prompts(mcp)
register_resources(mcp)
register_subscriptions(mcp)
register_discovery(mcp)
register_schema(mcp)
register_notifications(mcp)
register_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)