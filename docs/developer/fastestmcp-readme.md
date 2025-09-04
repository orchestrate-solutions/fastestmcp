# FastestMCP - Super Simple MCP Server Development

**The fastest way to build MCP servers. Zero-config, one-command creation, component marketplace.**

[![PyPI version](https://badge.fury.io/py/fastestmcp.svg)](https://badge.fury.io/py/fastestmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### Level 1: Zero-Config (80% of use cases)

```python
from fastestmcp import Server

app = Server("my-app")

@app.tool
def hello(name: str):
    return f"Hello {name}!"

app.run()  # Everything else is automatic
```

**That's it!** No configuration, no boilerplate, no complexity.

### One-Command Creation

```bash
# Natural language server creation
fastestmcp server "weather app that shows current temperature"
fastestmcp server "file organizer that sorts downloads"
fastestmcp server "github repo monitor"
```

## 🎯 Three Levels of Simplicity

### Level 1: Zero-Config (80% of use cases)
Perfect for simple tools and resources. Everything is automatic.

```python
from fastestmcp import Server

app = Server("calculator")

@app.tool
def add(a: int, b: int):
    return a + b

@app.tool
def multiply(a: int, b: int):
    return a * b

app.run()
```

### Level 2: Minimal Config (15% of use cases)
For when you need a bit more control.

```python
from fastestmcp import Server

app = Server("my-app", config={
    "tools": ["math", "web"],
    "resources": ["files", "data"]
})
```

### Level 3: Full Control (5% of use cases)
Access to the full FastMCP power when you need it.

```python
from mcp.server.fastmcp import FastMCP
# Full MCP implementation
```

## 🛍️ Component Marketplace

Add powerful functionality with one line:

```python
from fastestmcp import Server, WebScraper, Database, FileSystem

app = Server("content-aggregator")

# Add components
app.add_component(WebScraper(urls=["news.com", "tech.com"]))
app.add_component(Database("sqlite:///content.db"))
app.add_component(FileSystem("/downloads"))

app.run()
```

### Available Components

- **WebScraper**: Automatically scrape web content
- **Database**: Database operations and queries
- **FileSystem**: File system operations
- **GitHub**: GitHub API integration
- **Slack**: Slack notifications
- **Email**: Email sending
- **And more coming soon!**

## 📦 Installation

```bash
pip install fastestmcp

# Or with extras
pip install fastestmcp[web,database]
```

## 🛠️ CLI Tool

The FastestMCP CLI is organized as a modular system for maintainability:

```
src/fastestmcp/
├── cli.py              # Main entry point (25 lines - delegates to cli/ module)
├── cli/                # Modular CLI implementation
│   ├── __init__.py
│   ├── __main__.py     # Main CLI logic with subcommands
│   ├── templates.py    # Template definitions
│   ├── server_generator.py  # Server generation logic
│   ├── client_generator.py  # Client generation logic
│   └── ...
└── ...
```

### Create servers from natural language:

```bash
# Weather monitoring
fastestmcp server "weather app that shows current temperature"

# File organization
fastestmcp server "file organizer that sorts downloads by type"

# GitHub monitoring
fastestmcp server "github repo monitor that notifies of new issues"

# Custom servers
fastestmcp server "todo list manager with due date reminders"
```

### CLI Architecture

The CLI follows a clean separation of concerns:
- **`cli.py`**: Lightweight wrapper that imports from the `cli/` module
- **`cli/__main__.py`**: Main CLI logic with argument parsing and command dispatch
- **`cli/` modules**: Specialized modules for templates, generators, and utilities

This modular design ensures:
- ✅ Easy maintenance and testing
- ✅ Clear separation of concerns
- ✅ Extensible architecture
- ✅ No monolithic files

### Generated servers include:
- ✅ Complete working code
- ✅ Smart defaults
- ✅ Error handling
- ✅ Logging
- ✅ Dependencies list
- ✅ Usage examples

## 🎨 Examples

### Basic Tool Server

```python
from fastestmcp import Server

app = Server("math-tools")

@app.tool
def fibonacci(n: int) -> list:
    """Generate first n Fibonacci numbers"""
    if n <= 0:
        return []
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

@app.tool
def is_prime(num: int) -> bool:
    """Check if a number is prime"""
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

app.run()
```

### Resource Server

```python
from fastestmcp import Server

app = Server("data-server")

# Static data resource
app.resource("data://constants/pi", 3.14159)
app.resource("data://constants/e", 2.71828)

# Dynamic resource
@app.resource("data://time/current")
def get_current_time():
    from datetime import datetime
    return {"timestamp": datetime.now().isoformat()}

app.run()
```

### Component-Based Server

```python
from fastestmcp import Server, WebScraper, FileSystem

app = Server("content-manager")

# Add web scraping capability
scraper = WebScraper(urls=["example.com", "news.com"])
app.add_component(scraper)

# Add file system operations
filesystem = FileSystem("/data")
app.add_component(filesystem)

@app.tool
def process_content(url: str) -> str:
    """Process content from a URL and save to file"""
    # Scrape content
    content = scraper.scrape_url(url)

    # Save to file
    filename = f"content_{hash(url)}.txt"
    filesystem.save_file(filename, content)

    return f"Processed and saved content from {url}"

app.run()
```

## 🔧 Smart Defaults

FastestMCP automatically handles:

- **Transport Detection**: stdio, HTTP, or SSE based on environment
- **Logging**: Structured JSON logging with appropriate levels
- **Error Handling**: Graceful error responses with helpful messages
- **Dependencies**: Only loads what's needed
- **Configuration**: Sensible defaults for everything

## 🚀 Advanced Features

### Custom Components

```python
from fastestmcp import Server, Component

class CustomAPI(Component):
    def __init__(self, api_key: str):
        super().__init__("custom-api", "Custom API integration")
        self.api_key = api_key

    def register(self, server: Server):
        @server.tool
        def call_api(endpoint: str, data: dict) -> dict:
            # Your API logic here
            return {"result": "API called", "endpoint": endpoint}

app = Server("api-server")
app.add_component(CustomAPI("your-api-key"))
app.run()
```

### Configuration Files

```yaml
# server.yaml
name: "advanced-server"
version: "1.0.0"

components:
  - type: "WebScraper"
    urls: ["site1.com", "site2.com"]
  - type: "Database"
    connection: "sqlite:///data.db"

tools:
  - name: "process_data"
    description: "Process incoming data"
```

## 📊 Performance

- **Startup Time**: < 100ms for basic servers
- **Memory Usage**: Minimal overhead
- **Zero Dependencies**: Core functionality works without extras
- **Auto-scaling**: Components load on-demand

## 🤝 Contributing

We love contributions! Here's how to get involved:

1. **Report Issues**: Found a bug? [Open an issue](https://github.com/orchestrate-solutions/fastestmcp/issues)
2. **Suggest Components**: Have an idea for a new component? [Let us know](https://github.com/orchestrate-solutions/fastestmcp/discussions)
3. **Contribute Code**: See our [contributing guide](CONTRIBUTING.md)

### Adding Components

```python
# Create your component
class MyComponent(Component):
    def register(self, server: Server):
        @server.tool
        def my_tool():
            return "Hello from my component!"

# Submit a PR!
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built on top of the amazing [FastMCP](https://github.com/modelcontextprotocol) framework
- Inspired by the simplicity of modern web frameworks
- Community contributions and feedback

---

**FastestMCP**: Because building MCP servers should be as easy as writing a function. 🚀