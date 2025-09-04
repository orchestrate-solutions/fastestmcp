
# FastestMCP Templates

**Generate production-ready MCP servers and clients in seconds with the FastestMCP CLI.**

[![uv](https://img.shields.io/badge/⚡_uv-Recommended-blue)](https://github.com/astral-sh/uv)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](https://opensource.org/licenses/Apache-2.0)

---

# FastestMCP CLI - Server & Client Generator

A powerful CLI tool for generating robust, modular Model Context Protocol (MCP) clients and servers using FastMCP.

## ✨ Key Features

- 🚀 **One-command generation** - Create servers and clients instantly
- 📋 **Multiple templates** - Weather, file-organizer, GitHub monitor, API client, and more
- 🏗️ **Flexible architecture** - Mono-file or structured projects
- 🔧 **Component-based** - Modular, testable, and reusable components
- 🌐 **Multi-transport** - stdio, HTTP, SSE, WebSocket support
- 📚 **Comprehensive docs** - CLI reference, examples, and guides

## 🚀 Quick CLI Examples

```bash
# Generate a weather monitoring server
uv run python -m fastestmcp.cli server --template weather --name weather-app

# Create a file organizer with custom components
uv run python -m fastestmcp.cli server --name file-manager --tools 3 --resources 2 --structure structured

# Build an API client
uv run python -m fastestmcp.cli client --template api-client --name rest-consumer --apis 4

# Simple server for prototyping
uv run python -m fastestmcp.cli server --level 1 --name prototype
```

## 📁 Repository Structure

- `src/fastestmcp/` — FastMCP CLI and generation templates
- `src/client/` — MCP client implementation and examples
- `src/server/` — Server templates and example applications
- `docs/` — Architecture guides and detailed documentation
- `tests/` — Comprehensive test suite with integration tests
- `cli-cheatsheet.md` — Complete CLI reference guide

## Quickstart

### Option 1: Using uv (Recommended)

1. Clone and enter the repo:

```sh
git clone https://github.com/JoshuaWink/fastmcp-templates.git
cd fastmcp-templates
```

2. Install uv if you haven't already:

```sh
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

3. Use uv to run commands (no virtual environment needed!):

```sh
# Run tests
uv run pytest -q

# Use the FastestMCP CLI
uv run python -m fastestmcp.cli --help
uv run python -m fastestmcp.cli server --template weather --name weather-app

# Run the demo
uv run python src/fastestmcp/demo.py
```

### Option 2: Using pip (Traditional)

1. Clone and enter the repo:

```sh
git clone https://github.com/JoshuaWink/fastmcp-templates.git
cd fastmcp-templates
```

2. Create and activate a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```sh
pip install -r requirements.txt
```

4. Run the test suite:

```sh
pytest -q
```

5. Use the CLI:

```sh
python -m fastestmcp.cli --help
```

## FastestMCP CLI Usage

The FastestMCP CLI provides powerful server and client generation:

### Generate MCP Servers
```sh
# Using uv (recommended)
uv run python -m fastestmcp.cli server --template weather --name weather-app
uv run python -m fastestmcp.cli server --level 1 --name basic-server

# Using pip
python -m fastestmcp.cli server --template weather --name weather-app
```

### Generate MCP Clients
```sh
# Using uv (recommended)
uv run python -m fastestmcp.cli client --template api-client --name my-client --apis 3

# Using pip
python -m fastestmcp.cli client --template api-client --name my-client --apis 3
```

### Available Templates
- **Server Templates**: weather, file-organizer, code-reviewer, github-monitor, todo-manager
- **Client Templates**: api-client, database-client, filesystem-client, notification-client

See `cli-cheatsheet.md` for complete CLI reference.

## Templates & Usage

This repo is marked as a GitHub template. Use the green "Use this template" button on GitHub to scaffold a new repo.

### Why Use uv?

**uv** is a fast Python package manager that:
- ⚡ **Blazingly fast** - Installs packages in seconds
- 🐍 **No virtual environment needed** - Manages environments automatically
- 🔄 **Drop-in replacement** for pip/pip-tools
- 📦 **Smart dependency resolution** - Avoids conflicts
- 🏃 **One-command execution** - `uv run` handles everything

### Development Workflow

```sh
# Quick setup with uv
git clone https://github.com/JoshuaWink/fastmcp-templates.git
cd fastmcp-templates

# Run tests instantly
uv run pytest

# Generate a server
uv run python -m fastestmcp.cli server --template weather --name my-weather-app

# Run your new server
cd my-weather-app && uv run python server.py
```

## Contributing

Please open issues or pull requests. Tests are required for new features.

## License

Apache-2.0
