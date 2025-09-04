"""
Area of Responsibility: Tools for OpenAPI Server
- Register custom tools that complement auto-generated OpenAPI tools
- Provide utility functions for API interaction
- Document tool schemas and usage for discoverability
"""

from typing import Optional

def register_tools(server):
    """
    Register custom tools for the OpenAPI server.
    These tools complement the auto-generated OpenAPI tools.
    """

    @server.tool(name="validate_api_key", description="Validate an API key format and strength")
    def validate_api_key(api_key: str) -> dict:
        """
        Validate an API key for format and security strength.
        """
        if not api_key:
            return {
                "valid": False,
                "error": "API key is required",
                "strength": "none"
            }

        # Check length
        length_score = min(len(api_key) / 32, 1.0)  # Max score at 32+ chars

        # Check character diversity
        has_upper = any(c.isupper() for c in api_key)
        has_lower = any(c.islower() for c in api_key)
        has_digit = any(c.isdigit() for c in api_key)
        has_special = any(not c.isalnum() for c in api_key)

        diversity_score = sum([has_upper, has_lower, has_digit, has_special]) / 4.0

        # Overall strength
        strength_score = (length_score + diversity_score) / 2.0

        if strength_score >= 0.8:
            strength = "strong"
        elif strength_score >= 0.6:
            strength = "medium"
        elif strength_score >= 0.3:
            strength = "weak"
        else:
            strength = "very_weak"

        return {
            "valid": len(api_key) >= 8,
            "length": len(api_key),
            "strength": strength,
            "strength_score": round(strength_score, 2),
            "has_uppercase": has_upper,
            "has_lowercase": has_lower,
            "has_digits": has_digit,
            "has_special_chars": has_special
        }

    @server.tool(name="format_api_request", description="Format and validate API request parameters")
    def format_api_request(endpoint: str, method: str = "GET", params: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        """
        Format and validate API request parameters.
        """
        # Validate HTTP method
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        method = method.upper()
        if method not in valid_methods:
            return {
                "valid": False,
                "error": f"Invalid HTTP method: {method}",
                "valid_methods": valid_methods
            }

        # Validate endpoint
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint

        # Process parameters
        processed_params = params or {}
        processed_headers = headers or {}

        # Add default headers
        if "Content-Type" not in processed_headers and method in ["POST", "PUT", "PATCH"]:
            processed_headers["Content-Type"] = "application/json"
        if "Accept" not in processed_headers:
            processed_headers["Accept"] = "application/json"

        return {
            "valid": True,
            "method": method,
            "endpoint": endpoint,
            "params": processed_params,
            "headers": processed_headers,
            "formatted_url": f"{{base_url}}{endpoint}",
            "query_string": "&".join([f"{k}={v}" for k, v in processed_params.items()]) if processed_params else ""
        }

    @server.tool(name="parse_api_response", description="Parse and analyze API response data")
    def parse_api_response(response_data: str, content_type: str = "application/json") -> dict:
        """
        Parse and analyze API response data.
        """
        import json

        try:
            if content_type == "application/json":
                parsed = json.loads(response_data)
            else:
                # For other content types, return as-is
                parsed = response_data

            # Analyze the response
            if isinstance(parsed, dict):
                analysis = {
                    "type": "object",
                    "keys": list(parsed.keys()),
                    "key_count": len(parsed),
                    "nested_objects": sum(1 for v in parsed.values() if isinstance(v, dict)),
                    "arrays": sum(1 for v in parsed.values() if isinstance(v, list))
                }
            elif isinstance(parsed, list):
                analysis = {
                    "type": "array",
                    "length": len(parsed),
                    "item_types": list(set(type(item).__name__ for item in parsed[:10])),  # Sample first 10
                    "all_same_type": len(set(type(item).__name__ for item in parsed)) == 1
                }
            else:
                analysis = {
                    "type": type(parsed).__name__,
                    "length": len(str(parsed)) if hasattr(parsed, '__len__') else None
                }

            return {
                "parsed": True,
                "data": parsed,
                "analysis": analysis,
                "content_type": content_type
            }

        except json.JSONDecodeError as e:
            return {
                "parsed": False,
                "error": f"JSON parsing error: {str(e)}",
                "data": response_data,
                "content_type": content_type
            }
        except Exception as e:
            return {
                "parsed": False,
                "error": f"Parsing error: {str(e)}",
                "data": response_data,
                "content_type": content_type
            }

    @server.tool(name="generate_api_report", description="Generate a comprehensive API usage report")
    def generate_api_report(requests_count: int = 0, errors_count: int = 0, avg_response_time: float = 0.0) -> dict:
        """
        Generate a comprehensive API usage report.
        """
        total_requests = requests_count + errors_count
        error_rate = (errors_count / total_requests * 100) if total_requests > 0 else 0

        # Determine health status
        if error_rate > 10:
            health_status = "critical"
        elif error_rate > 5:
            health_status = "warning"
        elif error_rate > 1:
            health_status = "fair"
        else:
            health_status = "good"

        # Performance rating
        if avg_response_time < 200:
            performance_rating = "excellent"
        elif avg_response_time < 500:
            performance_rating = "good"
        elif avg_response_time < 1000:
            performance_rating = "fair"
        else:
            performance_rating = "poor"

        return {
            "summary": {
                "total_requests": total_requests,
                "successful_requests": requests_count,
                "failed_requests": errors_count,
                "error_rate_percentage": round(error_rate, 2),
                "avg_response_time_ms": avg_response_time
            },
            "health": {
                "status": health_status,
                "score": round(100 - error_rate, 2),
                "recommendations": [
                    "Monitor error rates closely" if error_rate > 5 else "API performing well",
                    "Consider caching for better performance" if avg_response_time > 500 else "Response times acceptable",
                    "Review error patterns" if errors_count > 0 else "No errors detected"
                ]
            },
            "performance": {
                "rating": performance_rating,
                "response_time_category": "fast" if avg_response_time < 500 else "slow",
                "throughput_estimate": f"~{int(60000 / max(avg_response_time, 1))} req/min"
            },
            "generated_at": "2025-01-01T00:00:00Z"
        }