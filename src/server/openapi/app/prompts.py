"""
Area of Responsibility: Prompts for OpenAPI Server
- Register prompt templates for API interaction workflows
- Provide reusable templates for common API operations
- Document prompt schemas for discoverability
"""

def register_prompts(server):
    """
    Register prompt templates for the OpenAPI server.
    """

    @server.prompt(name="api_exploration_prompt", description="Guide for exploring available API endpoints")
    def api_exploration_prompt(api_name: str = "external API"):
        """
        Prompt template for exploring API capabilities.
        """
        return f"""
You are exploring the {api_name} API. Here are some things you can do:

1. **List available tools**: Use the available tools to see what API endpoints are accessible
2. **Test endpoints**: Try calling different API endpoints to understand their functionality
3. **Check responses**: Examine the structure and content of API responses
4. **Handle errors**: Be prepared for authentication, rate limiting, or network errors

Available tools will be automatically generated from the OpenAPI specification.
Start by listing the available tools to see what you can do with this API.
"""

    @server.prompt(name="api_debugging_prompt", description="Help with debugging API issues")
    def api_debugging_prompt(error_type: str = "general"):
        """
        Prompt template for debugging API issues.
        """
        return f"""
You're encountering an API issue (type: {error_type}). Here's how to debug:

**Common Issues:**
- **Authentication**: Check API keys, tokens, or credentials
- **Rate Limiting**: Wait and retry, or check rate limit headers
- **Network Issues**: Verify connectivity and DNS resolution
- **Parameter Errors**: Check required vs optional parameters
- **Response Parsing**: Verify response format matches expectations

**Debugging Steps:**
1. Check the error message and type
2. Verify your authentication credentials
3. Test with minimal parameters first
4. Check the API documentation
5. Try the same request manually (curl, Postman, etc.)

Use the available tools to test different scenarios and isolate the issue.
"""

    @server.prompt(name="api_integration_prompt", description="Guide for integrating with external APIs")
    def api_integration_prompt(integration_type: str = "general"):
        """
        Prompt template for API integration guidance.
        """
        return f"""
You're integrating with an external API (type: {integration_type}). Best practices:

**Integration Patterns:**
- **Authentication**: Securely store and rotate API credentials
- **Error Handling**: Implement retry logic and graceful degradation
- **Rate Limiting**: Respect API limits and implement backoff strategies
- **Caching**: Cache responses when appropriate to reduce API calls
- **Monitoring**: Track API usage, success rates, and performance

**Security Considerations:**
- Never log sensitive credentials or API keys
- Use HTTPS for all API communications
- Validate and sanitize all API inputs/outputs
- Implement proper timeout handling

**Performance Tips:**
- Use connection pooling for multiple requests
- Implement request batching when supported
- Cache static or infrequently changing data
- Monitor response times and set appropriate timeouts

The OpenAPI tools will handle the actual API communication, but you'll need to manage the integration logic.
"""

    @server.prompt(name="openapi_spec_analysis_prompt", description="Analyze OpenAPI specifications")
    def openapi_spec_analysis_prompt(spec_complexity: str = "medium"):
        """
        Prompt template for analyzing OpenAPI specifications.
        """
        return f"""
You're analyzing an OpenAPI specification (complexity: {spec_complexity}).

**Analysis Focus Areas:**
- **Endpoints**: What operations are available?
- **Parameters**: Required vs optional parameters
- **Authentication**: What auth methods are supported?
- **Response Schemas**: What data structures are returned?
- **Error Handling**: What error responses are possible?

**Key Questions to Answer:**
1. What is the primary purpose of this API?
2. What are the most important endpoints to test first?
3. Are there any complex parameter requirements?
4. How should authentication be handled?
5. What response formats should you expect?

Use the available tools to explore the API systematically, starting with the most basic endpoints and working up to complex operations.
"""