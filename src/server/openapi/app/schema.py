"""
Area of Responsibility: Schema Validation for OpenAPI Server
- Register schema validation and exposure for API operations
- Provide JSON schemas for request/response validation
- Enable schema discovery for API integration
"""

def register_schema(server):
    """
    Register schema validation and exposure for the OpenAPI server.
    """

    @server.resource(
        uri="schema://api_user",
        name="User API Schema",
        description="JSON schema for user-related API operations"
    )
    def user_api_schema() -> dict:
        """
        Schema for user API operations.
        """
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Unique user identifier",
                    "minimum": 1
                },
                "name": {
                    "type": "string",
                    "description": "User's full name",
                    "minLength": 1,
                    "maxLength": 100
                },
                "username": {
                    "type": "string",
                    "description": "User's username",
                    "minLength": 3,
                    "maxLength": 50
                },
                "email": {
                    "type": "string",
                    "description": "User's email address",
                    "format": "email"
                },
                "phone": {
                    "type": "string",
                    "description": "User's phone number"
                },
                "website": {
                    "type": "string",
                    "description": "User's website URL",
                    "format": "uri"
                }
            },
            "required": ["id", "name", "username", "email"]
        }

    @server.resource(
        uri="schema://api_request",
        name="API Request Schema",
        description="JSON schema for API request validation"
    )
    def api_request_schema() -> dict:
        """
        Schema for validating API requests.
        """
        return {
            "type": "object",
            "properties": {
                "endpoint": {
                    "type": "string",
                    "description": "API endpoint path",
                    "pattern": "^/"
                },
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
                    "description": "HTTP method"
                },
                "headers": {
                    "type": "object",
                    "description": "HTTP headers",
                    "additionalProperties": {"type": "string"}
                },
                "params": {
                    "type": "object",
                    "description": "Query parameters",
                    "additionalProperties": True
                },
                "data": {
                    "description": "Request body data",
                    "oneOf": [
                        {"type": "object"},
                        {"type": "array"},
                        {"type": "string"}
                    ]
                }
            },
            "required": ["endpoint", "method"]
        }

    @server.resource(
        uri="schema://api_response",
        name="API Response Schema",
        description="JSON schema for API response validation"
    )
    def api_response_schema() -> dict:
        """
        Schema for validating API responses.
        """
        return {
            "type": "object",
            "properties": {
                "status_code": {
                    "type": "integer",
                    "description": "HTTP status code",
                    "minimum": 100,
                    "maximum": 599
                },
                "headers": {
                    "type": "object",
                    "description": "Response headers",
                    "additionalProperties": {"type": "string"}
                },
                "data": {
                    "description": "Response body data",
                    "oneOf": [
                        {"type": "object"},
                        {"type": "array"},
                        {"type": "string"},
                        {"type": "null"}
                    ]
                },
                "error": {
                    "type": "object",
                    "description": "Error information if status indicates failure",
                    "properties": {
                        "message": {"type": "string"},
                        "type": {"type": "string"},
                        "code": {"type": "string"}
                    }
                }
            },
            "required": ["status_code"]
        }

    @server.resource(
        uri="schema://api_error",
        name="API Error Schema",
        description="JSON schema for API error responses"
    )
    def api_error_schema() -> dict:
        """
        Schema for API error responses.
        """
        return {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string",
                    "description": "Error message"
                },
                "type": {
                    "type": "string",
                    "description": "Error type/category"
                },
                "code": {
                    "type": "string",
                    "description": "Error code"
                },
                "details": {
                    "description": "Additional error details",
                    "oneOf": [
                        {"type": "object"},
                        {"type": "array"},
                        {"type": "string"}
                    ]
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time",
                    "description": "When the error occurred"
                },
                "request_id": {
                    "type": "string",
                    "description": "Unique request identifier"
                }
            },
            "required": ["error", "type"]
        }

    @server.resource(
        uri="schema://openapi_spec",
        name="OpenAPI Specification Schema",
        description="JSON schema for OpenAPI specification validation"
    )
    def openapi_spec_schema() -> dict:
        """
        Schema for validating OpenAPI specifications.
        """
        return {
            "type": "object",
            "properties": {
                "openapi": {
                    "type": "string",
                    "pattern": "^3\\.\\d+\\.\\d+$",
                    "description": "OpenAPI version"
                },
                "info": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "version": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["title", "version"]
                },
                "servers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "format": "uri"},
                            "description": {"type": "string"}
                        },
                        "required": ["url"]
                    }
                },
                "paths": {
                    "type": "object",
                    "description": "API endpoint definitions",
                    "additionalProperties": {"type": "object"}
                },
                "components": {
                    "type": "object",
                    "description": "Reusable components"
                }
            },
            "required": ["openapi", "info", "paths"]
        }