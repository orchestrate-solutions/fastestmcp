"""
Area of Responsibility: Error Handling for OpenAPI Server
- Register error analysis tools for API calls and OpenAPI operations
- Standardize error responses for external API failures
- Handle authentication, rate limiting, and network errors
"""


def register_error_handlers(server):
    """
    Register error analysis tools for the OpenAPI server.
    Note: OpenAPI servers don't support error_handler decorators,
    so we register these as regular tools for error analysis.
    """

    @server.tool(name="analyze_api_error", description="Analyze and categorize external API errors")
    def analyze_api_error(error_message: str, error_type: str = "unknown"):
        """
        Analyze errors from external API calls and provide standardized responses.
        """
        error_msg = error_message.lower()
        error_type_lower = error_type.lower()

        # Handle specific HTTP errors
        if "httpx" in error_type_lower or "aiohttp" in error_type_lower or "timeout" in error_msg:
            if "timeout" in error_msg:
                return {
                    "error": "External API timeout",
                    "type": "APITimeoutError",
                    "message": "The external API took too long to respond",
                    "suggestion": "Try again later or check API status"
                }
            elif "connection" in error_msg:
                return {
                    "error": "External API connection failed",
                    "type": "APIConnectionError",
                    "message": "Could not connect to the external API",
                    "suggestion": "Check network connectivity and API endpoint"
                }
            else:
                return {
                    "error": "External API error",
                    "type": "APIError",
                    "message": error_message,
                    "suggestion": "Check API documentation and request format"
                }

        # Handle authentication errors
        if "auth" in error_msg or "unauthorized" in error_msg or "401" in error_msg:
            return {
                "error": "Authentication failed",
                "type": "AuthenticationError",
                "message": "Invalid or missing credentials for external API",
                "suggestion": "Verify API key, token, or authentication method"
            }

        # Handle rate limiting
        if "rate" in error_msg or "429" in error_msg or "too many requests" in error_msg:
            return {
                "error": "Rate limit exceeded",
                "type": "RateLimitError",
                "message": "Too many requests to external API",
                "suggestion": "Wait before retrying or implement request throttling"
            }

        # Generic error handler
        return {
            "error": "OpenAPI server error",
            "type": error_type,
            "message": error_message,
            "suggestion": "Check logs and API documentation for more details"
        }

    @server.tool(name="validate_openapi_spec", description="Validate OpenAPI specification format")
    def validate_openapi_spec(spec_content: str):
        """
        Validate OpenAPI specification and identify potential issues.
        """
        try:
            import json
            spec = json.loads(spec_content)

            issues = []

            # Check required fields
            if "openapi" not in spec:
                issues.append("Missing 'openapi' version field")
            if "info" not in spec:
                issues.append("Missing 'info' section")
            if "paths" not in spec:
                issues.append("Missing 'paths' section")

            # Check info section
            if "info" in spec:
                info = spec["info"]
                if "title" not in info:
                    issues.append("Missing title in info section")
                if "version" not in info:
                    issues.append("Missing version in info section")

            if issues:
                return {
                    "valid": False,
                    "issues": issues,
                    "suggestion": "Fix the identified issues in your OpenAPI specification"
                }
            else:
                return {
                    "valid": True,
                    "message": "OpenAPI specification appears valid",
                    "paths_count": len(spec.get("paths", {}))
                }

        except json.JSONDecodeError as e:
            return {
                "valid": False,
                "error": "Invalid JSON format",
                "details": str(e),
                "suggestion": "Ensure the OpenAPI spec is valid JSON"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": "Validation failed",
                "details": str(e),
                "suggestion": "Check the OpenAPI specification structure"
            }