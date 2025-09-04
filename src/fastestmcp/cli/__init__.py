"""
FastestMCP CLI Package
Refactored CLI for generating MCP servers and clients
"""

__version__ = "0.1.0"

def main():
    """Main entry point for the FastestMCP CLI"""
    from .__main__ import main as _main
    _main()