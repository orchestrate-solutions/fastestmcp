# FastestMCP CLI - LLM Quick Reference

## Core Commands

### Server Generation
```bash
# Level-based generation (1-5 complexity)
fastestmcp server --level 1 --name basic-server
fastestmcp server --level 3 --name advanced-server

# Template-based generation
fastestmcp server --template weather --name weather-app
fastestmcp server --template github-monitor --name repo-watcher

# Custom component counts
fastestmcp server --name custom-server --tools 5 --resources 3 --prompts 2
```

### Client Generation
```bash
# Basic client
fastestmcp client --name my-client --apis 2

# Template-based client
fastestmcp client --template api-client --name rest-consumer

# Advanced client
fastestmcp client --name advanced-client --apis 4 --integrations 3 --notifications 2
```

## Transport Options

| Transport | Use Case | Command |
|-----------|----------|---------|
| `stdio` | Local development, CLI tools | `--transport stdio` |
| `http` | Web services, remote clients | `--transport http` |
| `sse` | Real-time updates, streaming | `--transport sse` |
| `websocket` | Bidirectional communication | `--transport websocket` |

## Structure Options

| Structure | Description | Use Case |
|-----------|-------------|----------|
| `mono` | Single file, simple | Small projects, prototypes |
| `structured` | Modular components | Large projects, teams |

## Available Templates

### Server Templates
- `weather` - Weather monitoring with forecasts
- `file-organizer` - File system organization
- `code-reviewer` - Code analysis and bug detection
- `github-monitor` - Repository monitoring
- `todo-manager` - Task management system
- `subscription-server` - Event-driven with notifications
- `event-driven-server` - Real-time event processing

### Client Templates
- `api-client` - REST/GraphQL API consumer
- `database-client` - SQL/NoSQL database operations
- `filesystem-client` - File system operations
- `notification-client` - Subscription-based notifications
- `monitoring-client` - System monitoring and metrics

## Quick Examples

### Basic Server
```bash
fastestmcp server --name hello-world --level 1
cd hello-world && python server.py
```

### Weather API Server
```bash
fastestmcp server --template weather --name weather-api --transport http
cd weather-api && python -m uvicorn server:app --host 0.0.0.0 --port 8000
```

### File Organizer
```bash
fastestmcp server --template file-organizer --name file-sorter --structure structured
cd file-sorter && python src/server.py
```

### API Client
```bash
fastestmcp client --template api-client --name data-consumer --apis 3
cd data-consumer && python client.py
```

### Enterprise Server
```bash
fastestmcp server --name enterprise-api \
  --tools 10 \
  --resources 5 \
  --prompts 3 \
  --notifications 2 \
  --subscriptions 2 \
  --transport http \
  --structure structured
```

## Component Reference

### Server Components
- **Tools**: Executable functions (data processing, API calls)
- **Resources**: Data sources (files, databases, APIs)
- **Prompts**: Interactive guides and templates
- **Notifications**: Server-to-client messages
- **Subscriptions**: Real-time data streams

### Client Components
- **APIs**: External service integrations
- **Integrations**: Internal service connections
- **Handlers**: Event processing functions
- **Notifications**: Incoming message handling
- **Subscriptions**: Real-time data subscriptions

## Common Patterns

### Microservice Architecture
```bash
# Create multiple specialized servers
fastestmcp server --template weather --name weather-service --transport http
fastestmcp server --template todo-manager --name task-service --transport http
fastestmcp client --template api-client --name service-client --apis 4
```

### Full-Stack Application
```bash
# Backend API server
fastestmcp server --name backend-api --transport http --structure structured --tools 8 --resources 4

# Frontend client
fastestmcp client --name frontend-client --apis 6 --integrations 3 --transport websocket
```

### Development Workflow
```bash
# 1. Create prototype
fastestmcp server --level 1 --name prototype

# 2. Add features incrementally
fastestmcp server --name enhanced --tools 5 --resources 3 --structure structured

# 3. Create client to test
fastestmcp client --name test-client --apis 2
```

## Troubleshooting

### Installation Issues
```bash
# Reinstall CLI
pip uninstall fastestmcp
pip install -e .

# Check installation
fastestmcp --help
```

### Import Errors
```bash
# Install dependencies
pip install fastmcp

# For HTTP features
pip install fastmcp[http]

# For SSE features
pip install fastmcp[sse]
```

### Template Errors
```bash
# List available templates
fastestmcp server --help
fastestmcp client --help

# Check template names
fastestmcp server --template weather --name test
```

## Performance Tips

- Use `mono` structure for simple projects (< 1000 lines)
- Use `structured` architecture for complex applications
- Choose `stdio` for local development, `http` for production
- Minimize component count for better startup performance
- Use appropriate transport based on expected load

## File Structure Generated

### Monolithic (mono)
```
project/
├── server.py          # Main server file
├── pyproject.toml     # Configuration
├── README.md          # Documentation
└── tests/
    └── test_server.py
```

### Structured
```
project/
├── src/
│   ├── server.py      # Main entry point
│   └── components/    # Modular components
│       ├── tools.py
│       ├── resources.py
│       └── ...
├── pyproject.toml
├── README.md
└── tests/
    ├── test_server.py
    └── test_components.py
```

---

**FastestMCP CLI**: Generate production-ready MCP servers and clients in seconds! ⚡