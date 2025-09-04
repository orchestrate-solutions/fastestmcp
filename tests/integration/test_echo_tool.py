import subprocess
import pytest
import time
import os
import sys
from client.client import MCPClient

MCP_CONFIG_PATH = "tests/integration/mcp_stdio_only.json"

@pytest.fixture(scope="module")
def mcp_server():
    env = os.environ.copy()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    env['PYTHONPATH'] = project_root
    env['PATH'] = f"{project_root}/.venv/bin:" + env.get('PATH', '')
    proc = subprocess.Popen([
        sys.executable, "server/stdio/server.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=project_root, env=env)
    time.sleep(2)
    yield proc
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()

@pytest.mark.asyncio
async def test_echo_tool(mcp_server):
    client = MCPClient(MCP_CONFIG_PATH)
    async with client._client:
        # List tools
        tools = await client.tools.list()
        # Call echo tool
        response = await client.tools.call('echo', text='hello world')
        import json
        echoed = json.loads(response.content[0].text)
        assert echoed['text'] == 'hello world'
