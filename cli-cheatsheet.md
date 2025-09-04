# FastestMCP CLI - Complete Reference Guide

## 🚀 Overview

FastestMCP CLI is a powerful tool for generating MCP (Model Context Protocol) servers and clients with granular component control. It supports multiple generation levels, predefined templates, and flexible project structures.

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [Server Generation](#server-generation)
- [Client Generation](#client-generation)
- [Templates](#templates)
- [Advanced Usage](#advanced-usage)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## 🔧 Installation

```bash
# Install from source
pip install -e .

# Or install the CLI directly
pip install fastestmcp

# Verify installation
fastestmcp --help
```

## ⚡ Quick Start

### Generate a basic server (Level 1)
```bash
fastestmcp server --name my-server --level 1
```

### Generate a server
```bash
fastestmcp server --template weather --name weather-app
```

### Generate a client
```bash
fastestmcp client --name my-client --apis 2
```

## 🛠️ Commands

### Main Commands

| Command | Description |
|---------|-------------|
| `fastestmcp server` | Generate MCP server |
| `fastestmcp client` | Generate MCP client |
| `fastestmcp --help` | Show help information |

### Server Generation Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--name` | string | **required** | Project/server name |
| `--level` | 1-5 | - | Generation complexity level |
| `--template` | string | - | Use predefined template |
| `--tools` | number | 2 | Number of tools to generate |
| `--resources` | number | 1 | Number of resources to generate |
| `--prompts` | number | 0 | Number of prompts to generate |
| `--notifications` | number | 0 | Number of notification types |
| `--subscriptions` | number | 0 | Number of subscription types |
| `--transport` | stdio/http/sse | stdio | Transport protocol |
| `--structure` | mono/structured | mono | Project structure |
| `--type` | fastmcp/mcp | fastmcp | MCP implementation type |
| `--output` | path | . | Output directory |

### Client Generation Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--name` | string | **required** | Client name |
| `--template` | string | - | Use predefined client template |
| `--apis` | number | 2 | Number of API endpoints |
| `--integrations` | number | 1 | Number of integrations |
| `--handlers` | number | 1 | Number of event handlers |
| `--notifications` | number | 0 | Number of notification subscriptions |
| `--subscriptions` | number | 0 | Number of subscription handlers |
| `--transport` | stdio/http/websocket | stdio | Transport protocol |
| `--structure` | mono/structured | mono | Project structure |
| `--type` | fastmcp/mcp | fastmcp | MCP implementation type |
| `--output` | path | . | Output directory |

## 🏗️ Server Generation

### Generation Levels

#### Level 1: Zero-Config (80% of use cases)
```bash
fastestmcp server --level 1 --name basic-server
```
- Minimal server with basic tool and resource
- Perfect for simple applications
- Auto-generated documentation

#### Level 2: Minimal Config (15% of use cases)
```bash
fastestmcp server --level 2 --name enhanced-server
```
- Multiple tools and resources
- Basic error handling
- Configuration options

#### Level 3: Advanced Features (4% of use cases)
```bash
fastestmcp server --level 3 --name advanced-server
```
- Complex component architecture
- Custom notifications and subscriptions
- Advanced error handling

#### Level 4: Enterprise (0.9% of use cases)
```bash
fastestmcp server --level 4 --name enterprise-server
```
- Full enterprise features
- Multi-transport support
- Advanced logging and monitoring

#### Level 5: Maximum Complexity (0.1% of use cases)
```bash
fastestmcp server --level 5 --name max-server
```
- Maximum feature set
- All available components
- Production-ready architecture

### Transport Types

#### STDIO Transport
```bash
fastestmcp server --name stdio-server --transport stdio
```
- Standard input/output communication
- Best for local development
- Simple and reliable

#### HTTP Transport
```bash
fastestmcp server --name http-server --transport http
```
- REST API endpoints
- Remote client connections
- Web service integration

#### SSE Transport
```bash
fastestmcp server --name sse-server --transport sse
```
- Server-sent events
- Real-time notifications
- Streaming data support

### Project Structures

#### Monolithic Structure
```bash
fastestmcp server --name mono-server --structure mono
```
- Single file server
- Simple deployment
- Easy to understand

#### Structured Architecture
```bash
fastestmcp server --name structured-server --structure structured
```
- Modular components
- Separate files for tools/resources
- Scalable architecture

## 🤖 Client Generation

### Basic Client
```bash
fastestmcp client --name basic-client
```
- Simple MCP client
- Basic API integration
- Event handling

### Advanced Client
```bash
fastestmcp client --name advanced-client --apis 5 --integrations 3 --notifications 2
```
- Multiple API endpoints
- Complex integrations
- Notification handling

### Client with Templates
```bash
fastestmcp client --template api-client --name api-consumer
```
- Pre-configured client templates
- Domain-specific functionality
- Best practices included

## 📋 Templates

### Server Templates

| Template | Description | Tools | Resources | Prompts |
|----------|-------------|-------|-----------|---------|
| `weather` | Weather monitoring app | get_weather, get_forecast | weather_data, location_info | weather_summary |
| `file-organizer` | File organization system | organize_files, sort_by_type, cleanup_old | file_structure, disk_usage | organization_plan |
| `code-reviewer` | Code analysis and review | review_code, check_bugs, suggest_fixes | code_analysis, bug_reports | review_summary |
| `github-monitor` | GitHub repository monitoring | monitor_repo, get_issues, check_prs | repo_data, contributor_stats | repo_health_report |
| `todo-manager` | Task management system | add_todo, list_todos, complete_todo, delete_todo | todo_list, completed_tasks | productivity_report |
| `subscription-server` | Event-driven server with subscriptions | broadcast_notification, manage_subscriptions, send_event | subscription_list, notification_history, event_log | subscription_help, notification_guide |
| `event-driven-server` | Real-time event processing | trigger_event, broadcast_update, handle_subscription | event_stream, notification_queue, subscriber_list | event_handling_guide, subscription_management |

### Client Templates

| Template | Description | APIs | Integrations | Handlers |
|----------|-------------|------|--------------|----------|
| `api-client` | Generic REST/GraphQL client | rest_api, graphql_api, webhook_handler | http_client, auth_handler, rate_limiter | request_processor, response_parser |
| `database-client` | SQL/NoSQL database client | query_executor, schema_inspector, migration_runner | connection_pool, query_builder, result_formatter | transaction_manager, error_handler |
| `filesystem-client` | File system operations client | file_manager, directory_scanner, permission_handler | path_resolver, file_watcher, sync_manager | io_processor, metadata_extractor |
| `notification-client` | Subscription-based notification client | notification_api, subscription_api, event_handler | priority_queue, event_processor, notification_filter | notification_handler, subscription_manager |
| `monitoring-client` | System monitoring and metrics | metrics_collector, alert_manager, log_aggregator | time_series_db, alert_rules, dashboard_generator | data_processor, threshold_checker |

## 🎯 Advanced Usage

### Custom Component Counts
```bash
# Server with specific component counts
fastestmcp server --name custom-server \
  --tools 5 \
  --resources 3 \
  --prompts 2 \
  --notifications 1 \
  --subscriptions 1
```

### Full Configuration
```bash
# Complete server configuration
fastestmcp server --name full-server \
  --transport http \
  --structure structured \
  --type fastmcp \
  --output ./my-servers
```

### Client with All Features
```bash
# Feature-complete client
fastestmcp client --name full-client \
  --apis 4 \
  --integrations 3 \
  --handlers 2 \
  --notifications 1 \
  --subscriptions 1 \
  --transport websocket \
  --structure structured
```

## 📚 Examples

### Weather Server
```bash
fastestmcp server --template weather --name weather-monitor --transport http
```

### File Organizer
```bash
fastestmcp server --template file-organizer --name file-manager --structure structured
```

### GitHub Monitor
```bash
fastestmcp server --template github-monitor --name repo-watcher --notifications 2
```

### Todo Manager
```bash
fastestmcp server --template todo-manager --name task-tracker --subscriptions 1
```

### API Client
```bash
fastestmcp client --template api-client --name rest-consumer --apis 3
```

### Database Client
```bash
fastestmcp client --template database-client --name db-manager --integrations 2
```

### Custom Server with All Features
```bash
fastestmcp server --name enterprise-server \
  --tools 10 \
  --resources 5 \
  --prompts 3 \
  --notifications 2 \
  --subscriptions 2 \
  --transport http \
  --structure structured \
  --type fastmcp
```

## 🔧 Generated Project Structure

### Monolithic Structure
```
my-server/
├── server.py          # Main server file
├── pyproject.toml     # Project configuration
├── README.md          # Documentation
└── tests/
    └── test_server.py # Test file
```

### Structured Architecture
```
my-server/
├── src/
│   ├── server.py      # Main server file
│   └── components/    # Modular components
│       ├── tools.py
│       ├── resources.py
│       ├── prompts.py
│       ├── notifications.py
│       └── subscriptions.py
├── pyproject.toml
├── README.md
└── tests/
    ├── test_server.py
    └── test_components.py
```

## 🐛 Troubleshooting

### Common Issues

#### Command not found
```bash
# Ensure CLI is installed
pip install -e .
fastestmcp --help
```

#### Permission errors
```bash
# Use sudo if needed
sudo pip install fastestmcp

# Or install in user directory
pip install --user fastestmcp
```

#### Template not found
```bash
# List available templates
fastestmcp server --help

# Check template names are correct
fastestmcp server --template weather --name test
```

#### Import errors in generated code
```bash
# Install dependencies
pip install fastmcp

# For HTTP transport
pip install fastmcp[http]

# For SSE transport
pip install fastmcp[sse]
```

### Debug Mode
```bash
# Enable verbose output
fastestmcp server --name debug-server --level 1
cd debug-server
python -c "import server; print('Server imports successfully')"
```

### Testing Generated Code
```bash
# Run generated tests
cd my-server
python -m pytest tests/

# Manual testing
python server.py  # For stdio servers
python -m uvicorn server:app  # For HTTP servers
```

## 📖 Component Reference

### Server Components

#### Tools
- **Definition**: Executable functions that perform actions
- **Examples**: Data processing, API calls, file operations
- **Best Practices**: Keep tools focused, add proper error handling

#### Resources
- **Definition**: Data sources that can be read by clients
- **Examples**: Configuration files, database connections, API endpoints
- **Best Practices**: Use consistent naming, provide metadata

#### Prompts
- **Definition**: Interactive guides and templates for users
- **Examples**: Setup wizards, help systems, tutorials
- **Best Practices**: Make prompts contextual and helpful

#### Notifications
- **Definition**: Server-initiated messages to clients
- **Examples**: Status updates, alerts, progress reports
- **Best Practices**: Use appropriate priority levels

#### Subscriptions
- **Definition**: Long-running connections for real-time data
- **Examples**: Event streams, live updates, monitoring
- **Best Practices**: Handle connection lifecycle properly

### Client Components

#### APIs
- **Definition**: External service integrations
- **Examples**: REST APIs, GraphQL endpoints, WebSocket connections
- **Best Practices**: Implement proper error handling and retries

#### Integrations
- **Definition**: Internal service connections
- **Examples**: Database connections, file systems, message queues
- **Best Practices**: Use connection pooling and proper cleanup

#### Handlers
- **Definition**: Event processing functions
- **Examples**: Message processors, error handlers, data transformers
- **Best Practices**: Keep handlers focused and testable

## 🎨 Customization

### Custom Templates
```python
# In templates.py
CUSTOM_TEMPLATES = {
    'my-template': {
        'description': 'My custom server template',
        'tools': ['custom_tool'],
        'resources': ['custom_resource'],
        'prompts': ['custom_prompt']
    }
}
```

### Extending Generators
```python
# Create custom generator
def generate_custom_component(name: str, config: dict) -> str:
    """Generate custom component code"""
    # Your custom generation logic
    pass
```

## 📊 Performance Tips

### Optimization Strategies
- Use structured architecture for large projects
- Minimize component count for simple applications
- Choose appropriate transport for your use case
- Use HTTP transport for web applications
- Use STDIO for local development

### Memory Management
- Components load on-demand
- Use structured architecture to reduce import overhead
- Minimize global state in components

### Scaling Considerations
- Use structured architecture for teams > 3 developers
- Separate concerns with modular components
- Use appropriate transport for expected load

## 🔗 Integration Examples

### With FastAPI
```bash
fastestmcp server --name api-server --transport http --structure structured
# Generated server integrates seamlessly with FastAPI
```

### With Streamlit
```bash
fastestmcp client --name streamlit-client --apis 3 --integrations 2
# Generated client works with Streamlit applications
```

### With Django
```bash
fastestmcp client --name django-client --apis 4 --handlers 3
# Generated client integrates with Django applications
```

## 📝 Best Practices

### Project Organization
- Use structured architecture for projects > 1000 lines
- Keep component files focused and single-purpose
- Use consistent naming conventions
- Add comprehensive documentation

### Code Quality
- Include error handling in all tools
- Add input validation for resources
- Use type hints for better IDE support
- Write comprehensive tests

### Deployment
- Use appropriate transport for production
- Configure logging for monitoring
- Set up proper error handling
- Use structured architecture for scalability

---

**FastestMCP CLI**: Because building MCP servers and clients should be as easy as running a command. 🚀</content>
<parameter name="filePath">/Users/jwink/Documents/github/fastmcp-templates/CLI_REFERENCE.md