"""
Area of Responsibility: Resources for OpenAPI Server
- Register resources for API documentation and metadata
- Expose OpenAPI specifications and API information
- Provide cached API responses as resources
"""

def register_resources(server):
    """
    Register resources for the OpenAPI server.
    """

    @server.resource(
        uri="resource://openapi/spec",
        name="OpenAPI Specification",
        description="The OpenAPI specification document for the external API"
    )
    def openapi_spec_resource():
        """
        Return the OpenAPI specification as a resource.
        """
        # In a real implementation, this would load the actual OpenAPI spec
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "External API",
                "version": "1.0.0",
                "description": "OpenAPI specification for the external API"
            },
            "servers": [
                {"url": "https://api.example.com"}
            ],
            "paths": {
                "/users": {
                    "get": {
                        "summary": "Get users",
                        "responses": {
                            "200": {"description": "Success"}
                        }
                    }
                }
            }
        }

    @server.resource(
        uri="resource://openapi/metadata",
        name="API Metadata",
        description="Metadata about the external API integration"
    )
    def api_metadata_resource():
        """
        Return metadata about the API integration.
        """
        return {
            "api_name": "External API",
            "base_url": "https://api.example.com",
            "version": "1.0.0",
            "authentication_methods": ["api_key", "bearer_token", "basic_auth"],
            "rate_limits": {
                "requests_per_minute": 60,
                "requests_per_hour": 1000
            },
            "supported_formats": ["json", "xml"],
            "last_updated": "2025-01-01T00:00:00Z"
        }

    @server.resource(
        uri="resource://openapi/endpoints",
        name="Available Endpoints",
        description="List of all available API endpoints"
    )
    def api_endpoints_resource():
        """
        Return a list of available API endpoints.
        """
        return {
            "endpoints": [
                {
                    "path": "/users",
                    "method": "GET",
                    "description": "Get all users",
                    "parameters": [],
                    "responses": ["200", "401", "403", "500"]
                },
                {
                    "path": "/users/{id}",
                    "method": "GET",
                    "description": "Get user by ID",
                    "parameters": [
                        {
                            "name": "id",
                            "type": "integer",
                            "required": True,
                            "description": "User ID"
                        }
                    ],
                    "responses": ["200", "404", "401", "500"]
                }
            ],
            "total_endpoints": 2,
            "last_updated": "2025-01-01T00:00:00Z"
        }

    @server.resource(
        uri="resource://openapi/health",
        name="API Health Status",
        description="Current health status of the external API"
    )
    def api_health_resource():
        """
        Return the health status of the external API.
        """
        # In a real implementation, this would check the actual API health
        return {
            "status": "healthy",
            "timestamp": "2025-01-01T00:00:00Z",
            "response_time_ms": 150,
            "uptime_percentage": 99.9,
            "last_error": None,
            "version": "1.0.0"
        }