#!/usr/bin/env python3
"""
FastestMCP Runner - Like npx for Python
Run FastestMCP without installing it globally
"""

import sys
import subprocess
import tempfile
import os
from pathlib import Path

def main():
    print("🚀 FastestMCP Runner - Running without global installation...")
    
    # Check if we're in a uv environment
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True, check=True)
        print("Using uv to run FastestMCP...")
        # Use uvx to run fastestmcp
        subprocess.run(['uvx', 'fastestmcp'] + sys.argv[1:], check=True)
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Fallback to pip
    try:
        print("Using pip to install and run FastestMCP temporarily...")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create virtual environment
            venv_path = Path(tmpdir) / 'venv'
            subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
            
            # Install fastestmcp (latest version)
            pip_path = venv_path / 'bin' / 'pip'
            subprocess.run([str(pip_path), 'install', 'fastestmcp'], check=True)
            
            # Run fastestmcp
            fastestmcp_path = venv_path / 'bin' / 'fastestmcp'
            subprocess.run([str(fastestmcp_path)] + sys.argv[1:], check=True)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running FastestMCP: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Cancelled")
        sys.exit(0)

if __name__ == "__main__":
    main()
