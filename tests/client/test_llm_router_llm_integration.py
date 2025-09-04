
import pytest
import requests
import subprocess
import time
import os
from tests.utilities.llm_test_utils import llm_call

# Global variable to track the mock server process
_mock_server_process = None

@pytest.fixture(scope="session", autouse=True)
def mock_llm_server():
    """Start mock LLM server before tests and stop it after"""
    global _mock_server_process

    # Start the mock server
    server_script = os.path.join(os.path.dirname(__file__), "../../mock_llm_server.py")
    _mock_server_process = subprocess.Popen(
        ["uv", "run", "python", server_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(server_script)
    )

    # Wait for server to start
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8765/health", timeout=2)
            if response.status_code == 200:
                break
        except (requests.exceptions.RequestException, requests.exceptions.Timeout):
            pass
        time.sleep(0.5)
    else:
        # If server didn't start, terminate the process and skip tests
        if _mock_server_process:
            _mock_server_process.terminate()
            _mock_server_process.wait()
        pytest.skip("Mock LLM server failed to start")

    yield  # Run the tests

    # Cleanup: Stop the server
    if _mock_server_process:
        try:
            _mock_server_process.terminate()
            _mock_server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _mock_server_process.kill()
            _mock_server_process.wait()

@pytest.mark.integration
def test_llm_tool_call():
    """Test LLM tool calling capability"""
    messages = [
        {"role": "system", "content": "You are an agent. When you need to call a tool, respond ONLY in JSON using: {\"tool\": \"TOOL_NAME\", \"args\": { ... }}."},
        {"role": "user", "content": "Call the foo tool with x=1."}
    ]
    result = llm_call(messages)
    assert '"tool": "foo"' in result or (isinstance(result, dict) and result["tool"] == "foo")
    assert '"x": 1' in result or (isinstance(result, dict) and result["args"]["x"] == 1)

@pytest.mark.integration
def test_llm_prompt_call():
    """Test LLM prompt calling capability"""
    messages = [
        {"role": "system", "content": "You are an agent. When you need to call a prompt, respond ONLY in JSON using: {\"prompt\": \"PROMPT_NAME\", \"args\": { ... }}."},
        {"role": "user", "content": "Call the baz prompt with y=2."}
    ]
    result = llm_call(messages)
    assert '"prompt": "baz"' in result or (isinstance(result, dict) and result["prompt"] == "baz")
    assert '"y": 2' in result or (isinstance(result, dict) and result["args"]["y"] == 2)
