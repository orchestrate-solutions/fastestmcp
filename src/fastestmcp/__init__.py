# FastestMCP - Super Simple MCP Server Development
# Level 1: Zero-Config-First Approach

"""
FastestMCP makes MCP server development ridiculously simple.

Level 1 (80% of use cases):
```python
from fastestmcp import Server

app = Server("my-app")

@app.tool
def hello(name: str):
    return f"Hello {name}!"

app.run()  # Everything else is automatic
```

That's it! No configuration, no boilerplate, no complexity.
"""

import os
import sys
import json
import asyncio
from typing import Dict, List, Any, Optional, Callable, Union
from pathlib import Path

# Auto-detect and import the right MCP components
try:
    from mcp.server.fastmcp.server import FastMCP
    from mcp.server.fastmcp.server import FastMCP as BaseFastMCP
except ImportError:
    print("Error: FastMCP not found. Install with: pip install fastmcp")
    sys.exit(1)

class Tool:
    """Simple tool wrapper"""
    def __init__(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        self.func = func
        self.name = name or func.__name__
        self.description = description or func.__doc__ or f"Tool: {self.name}"

class Resource:
    """Simple resource wrapper"""
    def __init__(self, uri: str, data: Any, mime_type: str = "application/json"):
        self.uri = uri
        self.data = data
        self.mime_type = mime_type

class Component:
    """Base component class for marketplace components"""
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    def register(self, server: 'Server'):
        """Register this component with a server"""
        raise NotImplementedError

class Server:
    """
    FastestMCP Server - Zero-config MCP server development

    Level 1: Just create, add tools/resources, run.
    Everything else is automatic.
    """

    def __init__(self, name: str, **config):
        self.name = name
        self.config = config
        self.tools: List[Tool] = []
        self.resources: List[Resource] = []
        self.components: List[Component] = []

        # Smart defaults
        self.config.setdefault('transport', self._auto_detect_transport())
        self.config.setdefault('logging', True)
        self.config.setdefault('error_handling', True)

        # Create the underlying FastMCP server
        self._server = FastMCP(name=name)

        # Auto-setup based on config
        if self.config.get('logging'):
            self._setup_logging()

        if self.config.get('error_handling'):
            self._setup_error_handling()

    def _auto_detect_transport(self) -> str:
        """Auto-detect the best transport"""
        # Check environment for MCP transport hints
        if os.getenv('MCP_TRANSPORT') == 'http':
            return 'http'
        elif os.getenv('MCP_TRANSPORT') == 'sse':
            return 'sse'
        else:
            return 'stdio'  # Default for MCP servers

    def _setup_logging(self):
        """Setup automatic logging"""
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.name)

    def _setup_error_handling(self):
        """Setup automatic error handling"""
        # This will be enhanced with better error handling
        pass

    def tool(self, func: Optional[Callable] = None, name: Optional[str] = None, description: Optional[str] = None):
        """Decorator to add a tool to the server"""
        def decorator(func):
            tool = Tool(func, name, description)
            self.tools.append(tool)

            # Register with underlying server
            @self._server.tool()
            def wrapped_tool(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    if self.config.get('logging'):
                        self.logger.info(f"Tool {tool.name} called with args: {args}, kwargs: {kwargs}")
                    return result
                except Exception as e:
                    if self.config.get('logging'):
                        self.logger.error(f"Tool {tool.name} error: {e}")
                    return f"Error in {tool.name}: {str(e)}"

            return func

        if func is None:
            return decorator
        else:
            return decorator(func)

    def resource(self, uri: str, data: Any = None, mime_type: str = "application/json"):
        """Add a resource to the server"""
        if data is None:
            # If no data provided, this is a decorator
            def decorator(func):
                resource = Resource(uri, func, mime_type)
                self.resources.append(resource)

                @self._server.resource(uri)
                def wrapped_resource():
                    try:
                        result = func()
                        if isinstance(result, (dict, list)):
                            return json.dumps(result, indent=2)
                        return str(result)
                    except Exception as e:
                        return f"Error accessing resource {uri}: {str(e)}"

                return func
            return decorator
        else:
            # Data provided directly
            resource = Resource(uri, data, mime_type)
            self.resources.append(resource)

            @self._server.resource(uri)
            def static_resource():
                if isinstance(data, (dict, list)):
                    return json.dumps(data, indent=2)
                return str(data)

    def add_component(self, component: Component):
        """Add a component from the marketplace"""
        self.components.append(component)
        component.register(self)

    def run(self, **kwargs):
        """Run the server with auto-detected settings"""
        # Register all tools and resources
        for tool in self.tools:
            # Tools are already registered via decorator
            pass

        for resource in self.resources:
            # Resources are already registered via decorator
            pass

        # Merge kwargs with auto-detected config
        run_config = {**self.config, **kwargs}

        # Run the server
        if run_config.get('transport') == 'http':
            # HTTP transport
            from mcp.server.fastmcp.server import FastMCP as HTTPFastMCP
            # This would need more implementation for HTTP
            pass
        elif run_config.get('transport') == 'sse':
            # SSE transport
            pass
        else:
            # Default stdio transport
            import asyncio
            asyncio.run(self._server.run_stdio_async())

# Component Marketplace
class WebScraper(Component):
    """Web scraping component"""

    def __init__(self, urls: List[str], name: str = "web-scraper"):
        super().__init__(name, "Automatically scrape web content")
        self.urls = urls

    def register(self, server: Server):
        @server.tool
        def scrape_url(url: str) -> str:
            """Scrape content from a URL"""
            try:
                import requests

                response = requests.get(url, timeout=10)
                # Simple text extraction without BeautifulSoup
                text = response.text
                # Remove HTML tags (basic approach)
                import re
                clean_text = re.sub(r'<[^>]+>', '', text)
                return clean_text[:2000] + "..." if len(clean_text) > 2000 else clean_text
            except ImportError:
                return "Error: requests required for web scraping"
            except Exception as e:
                return f"Error scraping {url}: {str(e)}"

class Database(Component):
    """Database component"""

    def __init__(self, connection_string: str, name: str = "database"):
        super().__init__(name, "Database operations")
        self.connection_string = connection_string

    def register(self, server: Server):
        # This would implement database operations
        # For now, just a placeholder
        @server.tool
        def query_database(query: str) -> str:
            """Execute a database query"""
            return f"Database query executed: {query} (placeholder)"

class FileSystem(Component):
    """File system operations component"""

    def __init__(self, base_path: str = ".", name: str = "filesystem"):
        super().__init__(name, "File system operations")
        self.base_path = Path(base_path)

    def register(self, server: Server):
        @server.tool
        def list_files(path: str = ".") -> str:
            """List files in a directory"""
            try:
                full_path = self.base_path / path
                files = list(full_path.iterdir())
                return json.dumps([str(f) for f in files], indent=2)
            except Exception as e:
                return f"Error listing files: {str(e)}"

        @server.tool
        def read_file(filepath: str) -> str:
            """Read content from a file"""
            try:
                full_path = self.base_path / filepath
                with open(full_path, 'r') as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file: {str(e)}"


def main():
    """Main entry point for the FastestMCP CLI"""
    from .cli import main as cli_main
    cli_main()

