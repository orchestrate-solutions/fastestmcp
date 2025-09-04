#!/usr/bin/env python3
"""
FastestMCP CLI - Main entry point

This is a lightweight wrapper that delegates to the modular CLI implementation
located in the cli/ subdirectory for better maintainability and organization.
"""

import sys
import os

# Add the cli module to the path so we can import from it
cli_dir = os.path.join(os.path.dirname(__file__), 'cli')
if cli_dir not in sys.path:
    sys.path.insert(0, cli_dir)

# Import and run the main CLI function from the modular implementation
try:
    from cli.__main__ import main
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error: Could not import modular CLI: {e}")
    print("Make sure the cli/ directory and its contents are properly installed.")
    sys.exit(1)
