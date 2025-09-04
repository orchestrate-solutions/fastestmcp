# MCP Builder Server
# Provides FastMCP components, templates, and best practices

from mcp.server.fastmcp.server import FastMCP as BaseFastMCP

from app.resources import register_resources
from app.tools import register_tools
from app.prompts import register_prompts

class FastMCP(BaseFastMCP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

server = FastMCP(name="MCP Builder Server")
register_resources(server)
register_tools(server)
register_prompts(server)

if __name__ == "__main__":
    server.run(transport="stdio")