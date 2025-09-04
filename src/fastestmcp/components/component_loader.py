"""
Component Loader - Dynamic component loading and management system
Similar to React components, allows importing and using reusable MCP components
"""

import importlib
import inspect
from typing import Dict, Any, List, Callable, Optional
from pathlib import Path


class ComponentLoader:
    """
    Dynamic component loader for MCP server/client components.
    Provides React-like component importing and usage patterns.
    """

    def __init__(self, components_base_path: str = "fastestmcp.components"):
        self.components_base_path = components_base_path
        self.loaded_components: Dict[str, Any] = {}

    def load_component(self, component_type: str, component_name: str) -> Any:
        """
        Load a component dynamically by type and name.

        Args:
            component_type: Type of component (tools, resources, prompts, etc.)
            component_name: Name of the component file (without .py extension)

        Returns:
            The loaded component module

        Example:
            loader = ComponentLoader()
            tool_component = loader.load_component("tools", "tool_template")
        """
        module_path = f"{self.components_base_path}.{component_type}.{component_name}"

        try:
            if module_path not in self.loaded_components:
                self.loaded_components[module_path] = importlib.import_module(module_path)

            return self.loaded_components[module_path]

        except ImportError as e:
            raise ImportError(f"Could not load component {component_type}.{component_name}: {e}")

    def get_component_functions(self, component_type: str, component_name: str,
                               function_prefix: Optional[str] = None) -> List[Callable]:
        """
        Get all functions from a component that match a prefix pattern.

        Args:
            component_type: Type of component
            component_name: Name of the component
            function_prefix: Optional prefix to filter functions (e.g., "tool_", "get_resource_")

        Returns:
            List of function objects

        Example:
            functions = loader.get_component_functions("tools", "tool_template", "tool_")
        """
        module = self.load_component(component_type, component_name)
        functions = []

        for name, obj in inspect.getmembers(module):
            if (inspect.isfunction(obj) and
                (function_prefix is None or name.startswith(function_prefix)) and
                not name.startswith('_')):
                functions.append(obj)

        return functions

    def get_register_function(self, component_type: str, component_name: str) -> Optional[Callable]:
        """
        Get the register function for a component type.

        Args:
            component_type: Type of component
            component_name: Name of the component

        Returns:
            The register function if it exists

        Example:
            register_func = loader.get_register_function("tools", "tool_template")
            if register_func:
                register_func(server_app, count=3)
        """
        module = self.load_component(component_type, component_name)

        # Look for register_* function
        register_name = f"register_{component_type.rstrip('s')}"  # Remove 's' from plural
        if hasattr(module, register_name):
            return getattr(module, register_name)

        # Fallback: look for any function starting with "register"
        for name, obj in inspect.getmembers(module):
            if name.startswith("register") and inspect.isfunction(obj):
                return obj

        return None

    def create_component_instance(self, component_type: str, component_name: str,
                                server_app: Any, count: int = 1, **kwargs) -> Dict[str, Any]:
        """
        Create and register a component instance with a server.

        Args:
            component_type: Type of component
            component_name: Name of the component
            server_app: The MCP server application instance
            count: Number of instances to create
            **kwargs: Additional arguments for the register function

        Returns:
            Dictionary with registration results

        Example:
            result = loader.create_component_instance("tools", "tool_template", server, count=2)
        """
        register_func = self.get_register_function(component_type, component_name)

        if register_func is None:
            return {
                "success": False,
                "error": f"No register function found for {component_type}.{component_name}"
            }

        try:
            # Call the register function with server and count
            register_func(server_app, count=count, **kwargs)

            return {
                "success": True,
                "component_type": component_type,
                "component_name": component_name,
                "count": count,
                "registered_functions": len(self.get_component_functions(component_type, component_name))
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to register component: {str(e)}"
            }

    def list_available_components(self, component_type: Optional[str] = None) -> Dict[str, List[str]]:
        """
        List all available components by type.

        Args:
            component_type: Optional specific type to list, or None for all types

        Returns:
            Dictionary mapping component types to lists of component names

        Example:
            all_components = loader.list_available_components()
            tool_components = loader.list_available_components("tools")
        """
        component_types = ["tools", "resources", "prompts", "notifications", "subscriptions", "tests"]

        if component_type:
            component_types = [component_type]

        available = {}

        for comp_type in component_types:
            try:
                # Try to list files in the component directory
                components_path = Path(__file__).parent / comp_type
                if components_path.exists():
                    component_files = [
                        f.stem for f in components_path.glob("*.py")
                        if not f.name.startswith("__")
                    ]
                    available[comp_type] = component_files
                else:
                    available[comp_type] = []
            except Exception:
                available[comp_type] = []

        return available

    def get_component_info(self, component_type: str, component_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a component.

        Args:
            component_type: Type of component
            component_name: Name of the component

        Returns:
            Dictionary with component information

        Example:
            info = loader.get_component_info("tools", "tool_template")
        """
        try:
            self.load_component(component_type, component_name)

            functions = self.get_component_functions(component_type, component_name)
            register_func = self.get_register_function(component_type, component_name)

            return {
                "component_type": component_type,
                "component_name": component_name,
                "module_path": f"{self.components_base_path}.{component_type}.{component_name}",
                "functions_count": len(functions),
                "function_names": [f.__name__ for f in functions],
                "has_register_function": register_func is not None,
                "register_function_name": register_func.__name__ if register_func else None,
                "loaded": True
            }

        except Exception as e:
            return {
                "component_type": component_type,
                "component_name": component_name,
                "loaded": False,
                "error": str(e)
            }


# Global component loader instance (similar to React's component system)
component_loader = ComponentLoader()


def use_component(component_type: str, component_name: str) -> Any:
    """
    React-like hook to use a component.
    Convenience function that uses the global component loader.

    Args:
        component_type: Type of component
        component_name: Name of the component

    Returns:
        The loaded component module

    Example:
        tool_component = use_component("tools", "tool_template")
        register_func = tool_component.register_tools
    """
    return component_loader.load_component(component_type, component_name)


def register_component(component_type: str, component_name: str, server_app: Any,
                      count: int = 1, **kwargs) -> Dict[str, Any]:
    """
    React-like function to register a component with a server.
    Convenience function that uses the global component loader.

    Args:
        component_type: Type of component
        component_name: Name of the component
        server_app: The MCP server application instance
        count: Number of instances to create
        **kwargs: Additional arguments

    Returns:
        Registration result dictionary

    Example:
        result = register_component("tools", "tool_template", server, count=3)
        if result["success"]:
            print(f"Registered {result['count']} tools")
    """
    return component_loader.create_component_instance(
        component_type, component_name, server_app, count, **kwargs
    )