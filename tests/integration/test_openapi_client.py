import asyncio
import pytest
import subprocess
import time
import os
import sys
from fastmcp import Client

@pytest.fixture(scope="module")
def openapi_server():
    """Start the OpenAPI MCP server for testing"""
    env = os.environ.copy()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    env['PYTHONPATH'] = project_root

    # Start the OpenAPI server
    proc = subprocess.Popen([
        sys.executable, "server/openapi/api_server.py"
    ], env=env, cwd=project_root)

    # Wait for server to start
    time.sleep(2)

    yield proc

    # Cleanup
    proc.terminate()
    proc.wait()

@pytest.mark.asyncio
async def test_openapi_server_tools(openapi_server):
    """Test that the OpenAPI server generates the expected tools"""
    async with Client("http://127.0.0.1:8000/mcp/") as client:
        # List the tools that were automatically generated
        tools = await client.list_tools()

        # Verify we have the expected tools
        tool_names = [tool.name for tool in tools]
        assert "get_users" in tool_names
        assert "get_user_by_id" in tool_names

        print(f"Generated Tools: {tool_names}")

@pytest.mark.asyncio
async def test_openapi_server_tool_execution(openapi_server):
    """Test that the OpenAPI server tools execute correctly"""
    async with Client("http://127.0.0.1:8000/mcp/") as client:
        # Call one of the generated tools
        user = await client.call_tool("get_user_by_id", {"id": 1})

        # Verify we got a response
        assert user.data is not None
        assert isinstance(user.data, dict)

        print(f"Tool result: {user.data}")