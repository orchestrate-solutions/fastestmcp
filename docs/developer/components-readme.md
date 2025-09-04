# FastestMCP Components

A React-inspired component system for building MCP (Model Context Protocol) servers and clients. This system provides reusable, modular components that can be easily imported and used to build MCP applications.

## Overview

The FastestMCP Components system is organized similar to React components:

- **Modular**: Each component type (tools, resources, prompts, etc.) is in its own folder
- **Reusable**: Components can be imported and used across different projects
- **Testable**: Each component comes with comprehensive test templates
- **Extensible**: Easy to add new component types and variants

## Component Structure

```
components/
├── tools/
│   ├── tool_template.py          # Basic tool implementations
│   └── ...                       # Custom tool components
├── resources/
│   ├── resource_template.py      # Basic resource implementations
│   └── ...                       # Custom resource components
├── prompts/
│   ├── prompt_template.py        # Basic prompt implementations
│   └── ...                       # Custom prompt components
├── notifications/
│   ├── notification_template.py  # Basic notification implementations
│   └── ...                       # Custom notification components
├── subscriptions/
│   ├── subscription_template.py  # Basic subscription implementations
│   └── ...                       # Custom subscription components
├── tests/
│   ├── tool_test_template.py     # Tool component tests
│   ├── resource_test_template.py # Resource component tests
│   └── ...                       # Test templates for each component type
└── component_loader.py           # Dynamic component loading system
```

## Usage

### Basic Component Loading

```python
from fastestmcp.components import use_component, register_component

# Load a component (similar to React's import)
tool_component = use_component("tools", "tool_template")

# Use the component's functions directly
from fastestmcp.components.tools.tool_template import register_tools

# Register with a server
register_tools(server_app, count=3)
```

### Dynamic Component Registration

```python
from fastestmcp.components import register_component

# Register a component dynamically (React-like pattern)
result = register_component("tools", "tool_template", server_app, count=2)
if result["success"]:
    print(f"Registered {result['count']} tools successfully!")

# Register multiple component types
register_component("resources", "resource_template", server_app, count=1)
register_component("prompts", "prompt_template", server_app, count=1)
register_component("notifications", "notification_template", server_app, count=1)
register_component("subscriptions", "subscription_template", server_app, count=1)
```

### Component Loader API

```python
from fastestmcp.components.component_loader import ComponentLoader

# Create a component loader
loader = ComponentLoader()

# Load a component
tool_module = loader.load_component("tools", "tool_template")

# Get component functions
functions = loader.get_component_functions("tools", "tool_template", "tool_")
print(f"Found {len(functions)} tool functions")

# Get registration function
register_func = loader.get_register_function("tools", "tool_template")

# List available components
available = loader.list_available_components()
print("Available components:", available)

# Get component information
info = loader.get_component_info("tools", "tool_template")
print(f"Component has {info['functions_count']} functions")
```

## Component Types

### Tools
Reusable tool implementations that can be registered with MCP servers.

```python
# Example tool component
def tool_1(input_data: str) -> str:
    """Tool 1 - handles input processing"""
    return f'Tool 1 processed: {input_data}'

def register_tools(server_app, count: int = 1) -> None:
    """Register tools with the server"""
    for i in range(count):
        tool_func = globals()[f"tool_{i+1}"]
        server_app.add_tool(tool_func)
```

### Resources
Reusable resource implementations for serving data.

```python
# Example resource component
def get_resource_1() -> Dict[str, Any]:
    """Get resource 1 data"""
    return {"resource": 1, "data": "example", "type": "data"}

def register_resources(server_app, count: int = 1) -> None:
    """Register resources with the server"""
    for i in range(count):
        resource_obj = create_resource(i+1)
        server_app.add_resource(resource_obj)
```

### Prompts
Reusable prompt implementations for generating responses.

```python
# Example prompt component
def prompt_1(context: str) -> str:
    """Prompt 1 - generates responses based on context"""
    return f'Prompt 1 response for: {context}'

def register_prompts(server_app, count: int = 1) -> None:
    """Register prompts with the server"""
    for i in range(count):
        prompt_obj = create_prompt(i+1)
        server_app.add_prompt(prompt_obj)
```

### Notifications
Reusable notification subscription implementations.

```python
# Example notification component
async def notification_1(message: str = "Default notification", priority: str = "info") -> Dict[str, Any]:
    """Notification subscription 1"""
    return {
        "type": "notification",
        "id": "notification_1",
        "message": message,
        "priority": priority,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    }

def register_notifications(server_app, count: int = 1) -> None:
    """Register notification subscriptions with the server"""
    for i in range(count):
        notification_func = globals()[f"notification_{i+1}"]
        server_app.add_subscription(notification_func)
```

### Subscriptions
Reusable event subscription implementations.

```python
# Example subscription component
async def subscription_1(filter_criteria: str = "all") -> AsyncGenerator[Dict[str, Any], None]:
    """Base subscription 1 - provides event streaming"""
    event_count = 0
    while True:
        event_count += 1
        event_data = {
            "type": "subscription_event",
            "subscription_id": "subscription_1",
            "event_id": f"event_1_{event_count}",
            "data": {"sequence_number": event_count}
        }
        yield event_data
        await asyncio.sleep(30)

def register_subscriptions(server_app, count: int = 1) -> None:
    """Register subscriptions with the server"""
    for i in range(count):
        subscription_func = globals()[f"subscription_{i+1}"]
        server_app.add_subscription(subscription_func)
```

## Testing Components

Each component type comes with comprehensive test templates:

```python
# Example: Testing tool components
import pytest
from fastestmcp.components.tools.tool_template import tool_1, register_tools

class TestToolComponents:
    def test_tool_1_basic_functionality(self):
        result = tool_1("test input")
        assert "Tool 1 processed: test input" in result
        assert isinstance(result, str)

    def test_register_tools_with_mock_server(self):
        mock_server = Mock()
        register_tools(mock_server, count=2)
        assert mock_server.add_tool.call_count == 2
```

## Creating Custom Components

### 1. Create Component File
Create a new component file in the appropriate directory:

```python
# components/tools/custom_math_tools.py
from typing import Union

def add_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Add two numbers together"""
    return a + b

def multiply_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Multiply two numbers"""
    return a * b

def register_tools(server_app, count: int = 1) -> None:
    """Register math tools with the server"""
    server_app.add_tool(add_numbers)
    server_app.add_tool(multiply_numbers)
```

### 2. Create Tests
Create corresponding test files:

```python
# components/tests/custom_math_tools_test.py
import pytest
from fastestmcp.components.tools.custom_math_tools import add_numbers, multiply_numbers

class TestCustomMathTools:
    def test_add_numbers_integers(self):
        result = add_numbers(2, 3)
        assert result == 5
        assert isinstance(result, int)

    def test_add_numbers_floats(self):
        result = add_numbers(2.5, 3.7)
        assert result == 6.2
        assert isinstance(result, float)

    def test_multiply_numbers(self):
        result = multiply_numbers(4, 5)
        assert result == 20
```

### 3. Use the Custom Component
```python
from fastestmcp.components import register_component

# Register your custom component
result = register_component("tools", "custom_math_tools", server_app)
```

## CLI Integration

The component system integrates with the FastestMCP CLI:

```bash
# Generate a server using components
fastestmcp server --name my-server --tools 2 --resources 1 --prompts 1

# The generated server will use the component system internally
```

## Benefits

1. **Modularity**: Components are self-contained and reusable
2. **Testability**: Each component has comprehensive tests
3. **Maintainability**: Easy to update individual components
4. **Scalability**: Simple to add new component types
5. **Consistency**: Standardized patterns across all components
6. **React-like**: Familiar patterns for developers

## Contributing

To contribute new components:

1. Follow the existing naming conventions
2. Include comprehensive tests
3. Add documentation strings
4. Update this README if adding new component types
5. Ensure components are importable and usable with the component loader

## Migration from Inline Code

When migrating existing inline component code:

1. Extract the code into separate component files
2. Create corresponding test files
3. Update imports to use the component loader
4. Test thoroughly to ensure functionality is preserved

This component system makes MCP development more modular, testable, and maintainable, similar to how React components revolutionized frontend development.