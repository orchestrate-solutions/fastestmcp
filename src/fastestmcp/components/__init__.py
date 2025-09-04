"""
FastestMCP Components - Reusable component templates for MCP servers and clients
"""

__version__ = "0.1.0"

# Import and re-export the main component functions
from .component_loader import ComponentLoader, use_component, register_component

__all__ = [
    "ComponentLoader",
    "use_component", 
    "register_component",
    "__version__"
]