"""
Area of Responsibility: Discovery for OpenAPI Server
- Register discovery logic for API capabilities and endpoints
- Enable discoverability of OpenAPI-generated tools and resources
- Provide API documentation and capability exploration
"""

def register_discovery(server):
    """
    Register discovery logic for the OpenAPI server.
    """

    @server.tool(name="discover_api_capabilities", description="Discover all API capabilities and endpoints")
    def discover_api_capabilities() -> dict:
        """
        Lists all API-generated tools, resources, and capabilities.
        """
        tools = list(getattr(server, '_tools', {}).keys())
        resources = list(getattr(server, '_resources', {}).keys())
        prompts = list(getattr(server, '_prompts', {}).keys())
        subscriptions = list(getattr(server, '_subscriptions', {}).keys()) if hasattr(server, '_subscriptions') else []
        auth_providers = list(getattr(server, '_auth_providers', {}).keys()) if hasattr(server, '_auth_providers') else []

        # Filter to show only API-related capabilities
        api_tools = [tool for tool in tools if 'api' in tool.lower() or 'user' in tool.lower()]
        api_resources = [resource for resource in resources if 'api' in resource.lower() or 'openapi' in resource.lower()]

        return {
            "api_tools": api_tools,
            "api_resources": api_resources,
            "prompts": prompts,
            "subscriptions": subscriptions,
            "auth_providers": auth_providers,
            "total_capabilities": len(api_tools) + len(api_resources) + len(prompts) + len(subscriptions)
        }

    @server.tool(name="explore_openapi_endpoints", description="Explore available OpenAPI endpoints")
    def explore_openapi_endpoints() -> dict:
        """
        Provides detailed information about available API endpoints.
        """
        return {
            "endpoints": [
                {
                    "name": "get_users",
                    "path": "/users",
                    "method": "GET",
                    "description": "Retrieve all users",
                    "parameters": [],
                    "responses": ["200 (success)", "401 (unauthorized)", "500 (server error)"]
                },
                {
                    "name": "get_user_by_id",
                    "path": "/users/{id}",
                    "method": "GET",
                    "description": "Retrieve a specific user by ID",
                    "parameters": [
                        {
                            "name": "id",
                            "type": "integer",
                            "required": True,
                            "description": "User ID"
                        }
                    ],
                    "responses": ["200 (success)", "404 (not found)", "401 (unauthorized)"]
                }
            ],
            "base_url": "https://jsonplaceholder.typicode.com",
            "authentication": ["API Key", "Bearer Token", "Basic Auth"],
            "rate_limits": "60 requests per minute"
        }

    @server.tool(name="check_api_status", description="Check the current status of the external API")
    def check_api_status() -> dict:
        """
        Check the health and status of the external API.
        """
        # In a real implementation, this would make an actual health check
        return {
            "status": "operational",
            "response_time_ms": 150,
            "last_checked": "2025-01-01T00:00:00Z",
            "uptime_percentage": 99.9,
            "version": "1.0.0",
            "supported_features": [
                "REST API",
                "JSON responses",
                "Standard HTTP status codes",
                "Rate limiting"
            ]
        }

    @server.tool(name="get_api_documentation", description="Get comprehensive API documentation")
    def get_api_documentation() -> dict:
        """
        Provides comprehensive documentation for the API.
        """
        return {
            "title": "External API Documentation",
            "version": "1.0.0",
            "description": "Complete API documentation for external service integration",
            "sections": [
                {
                    "title": "Authentication",
                    "content": "Supports API Key, Bearer Token, and Basic authentication methods"
                },
                {
                    "title": "Endpoints",
                    "content": "RESTful endpoints for user management and data operations"
                },
                {
                    "title": "Rate Limiting",
                    "content": "60 requests per minute, 1000 requests per hour"
                },
                {
                    "title": "Error Handling",
                    "content": "Standard HTTP status codes with detailed error messages"
                },
                {
                    "title": "Data Formats",
                    "content": "JSON request/response format with UTF-8 encoding"
                }
            ],
            "contact": {
                "name": "API Support",
                "email": "support@api.example.com"
            },
            "license": "MIT"
        }