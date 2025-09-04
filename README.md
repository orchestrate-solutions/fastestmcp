
# FastestMCP

**Generate production-ready MCP servers and clients in seconds.**

[![uv](https://img.shields.io/badge/⚡_uv-Recommended-blue)](https://github.com/astral-sh/uv)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](https://opensource.org/licenses/Apache-2.0)

## 👋 Quick Start

### Install
```bash
# Recommended: uv (modern, fast)
uv add fastestmcp

# Alternative: pip
pip install fastestmcp
```

### Create Your First Server
```python
from fastestmcp import Server

app = Server("my-app")

@app.tool
def hello(name: str):
    return f"Hello {name}!"

app.run()
```

**That's it!** Your MCP server is ready.

## �️ CLI Usage

Generate servers instantly:

```bash
# Weather server
fastestmcp server --template weather --name weather-app

# File organizer
fastestmcp server --template file-organizer --name file-manager

# Custom server
fastestmcp server --name custom --tools 3 --resources 2
```

## 🔗 Connect to AI Agents

Add your server to your MCP configuration so AI agents can use it:

### For Claude Desktop

Create or update `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-app": {
      "command": "python",
      "args": ["/path/to/your/server.py"]
    }
  }
}
```

### For VS Code

Create or update `.vscode/mcp.json` in your workspace:

```json
{
  "mcpServers": {
    "my-app": {
      "command": "python",
      "args": ["/path/to/your/server.py"]
    }
  }
}
```

### For Other MCP Clients

Most MCP clients look for a `mcp.json` file in:
- `~/.mcp.json` (global)
- `./mcp.json` (project-specific)
- Or their own configuration location

Example configuration:
```json
{
  "mcpServers": {
    "fastestmcp-server": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

**Restart your MCP client after updating the configuration!**

## � Installation Options

### uv (Recommended - Modern Python)
```bash
uv add fastestmcp
```

### Global Install
```bash
pip install fastestmcp
```

### From Source
```bash
git clone https://github.com/orchestrate-solutions/fastestmcp.git
cd fastestmcp
uv run python -m fastestmcp.cli --help
```

## 🎨 Examples

### Basic Tool Server
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

### Component-Based Server
```python
from fastestmcp import Server, WebScraper, FileSystem

app = Server("content-manager")
app.add_component(WebScraper(urls=["news.com"]))
app.add_component(FileSystem("/data"))
app.run()
```

## 📚 Documentation

- [CLI Reference](docs/cli/cli-cheatsheet.md)
- [Architecture Guide](docs/architecture/)
- [Examples](docs/examples/)
- [Developer Guide](docs/developer/)

## 🤝 Contributing

Open issues or PRs. Tests required for new features.

## 📄 License

Apache-2.0
