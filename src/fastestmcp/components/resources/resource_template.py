"""
Resource Component Template - Dynamic resource generation for MCP servers
"""

from typing import Any, Dict
from mcp.types import Resource
from pydantic import AnyUrl


def register_resources(server_app, count: int = 1) -> None:
    """Register all resources with the server - dynamically generated"""
    for i in range(count):
        resource_obj = create_resource(i + 1)
        server_app.add_resource(resource_obj)


def create_resource(index: int) -> Resource:
    """Create a unique resource object dynamically"""
    return Resource(
        uri=AnyUrl(f"resource://resource_{index}"),
        name=f"Resource {index}",
        description=f"Resource {index} data",
        mimeType="application/json"
    )


def create_resource_function(index: int):
    """Create a unique resource function dynamically"""
    def resource_function() -> Dict[str, Any]:
        """Dynamically generated resource function"""
        # TODO: Implement resource {index} data retrieval
        return {"resource": index, "data": "placeholder", "type": "dynamic"}

    # Set function metadata
    resource_function.__name__ = f"get_resource_{index}"
    resource_function.__doc__ = f"Get resource {index} data"

    return resource_function