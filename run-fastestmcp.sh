#!/bin/bash
# FastestMCP Runner - Like npx but for Python
set -e

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "Using uv to run FastestMCP..."
    uvx fastestmcp "$@"
    exit $?
fi

# Check if python3 is available
if command -v python3 &> /dev/null; then
    echo "Using python3 to run FastestMCP..."
    python3 -c "
import sys
import subprocess
import tempfile
import os

# Install fastestmcp temporarily
with tempfile.TemporaryDirectory() as tmpdir:
    # Create a temporary virtual environment
    venv_path = os.path.join(tmpdir, venv)
    subprocess.run([sys.executable, -m, venv, venv_path], check=True)
    
    # Install fastestmcp
    pip_path = os.path.join(venv_path, bin, pip)
    subprocess.run([pip_path, install, fastestmcp], check=True)
    
    # Run fastestmcp with provided arguments
    fastestmcp_path = os.path.join(venv_path, bin, fastestmcp)
    subprocess.run([fastestmcp_path] + sys.argv[1:], check=True)
"
    exit $?
fi

echo "Error: Neither uv nor python3 found. Please install Python 3.10+ or uv."
exit 1
