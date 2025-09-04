# Level 1: Zero-Config Examples
# These are the simplest possible MCP servers

from fastestmcp import Server

# Example 1: Hello World
print("=== Example 1: Hello World ===")

app1 = Server("hello-world")

@app1.tool
def greet(name: str) -> str:
    """Say hello to someone"""
    return f"Hello, {name}! Welcome to FastestMCP!"

# This would run the server, but we'll skip it for the example
# app1.run()

print("✅ Hello World server created")

# Example 2: Calculator
print("\n=== Example 2: Calculator ===")

calc = Server("calculator")

@calc.tool
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

@calc.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

@calc.tool
def power(base: float, exponent: float) -> float:
    """Calculate base raised to exponent"""
    return base ** exponent

print("✅ Calculator server created")

# Example 3: Text Processor
print("\n=== Example 3: Text Processor ===")

text_app = Server("text-processor")

@text_app.tool
def word_count(text: str) -> dict:
    """Count words, characters, and lines in text"""
    words = len(text.split())
    chars = len(text)
    lines = len(text.split('\n'))

    return {
        "words": words,
        "characters": chars,
        "lines": lines
    }

@text_app.tool
def reverse_text(text: str) -> str:
    """Reverse the input text"""
    return text[::-1]

@text_app.tool
def uppercase(text: str) -> str:
    """Convert text to uppercase"""
    return text.upper()

print("✅ Text processor server created")

# Example 4: Data Server with Resources
print("\n=== Example 4: Data Server ===")

data_app = Server("data-server")

# Static resources
data_app.resource("data://constants/pi", 3.14159265359)
data_app.resource("data://constants/e", 2.71828182846)
data_app.resource("data://constants/golden_ratio", 1.61803398875)

# Dynamic resource
@data_app.tool
def get_current_time() -> str:
    """Get current timestamp"""
    from datetime import datetime
    import json
    return json.dumps({"timestamp": datetime.now().isoformat()})

@data_app.tool
def get_constant(name: str) -> str:
    """Get a mathematical constant by name"""
    constants = {
        "pi": 3.14159265359,
        "e": 2.71828182846,
        "golden_ratio": 1.61803398875
    }

    if name in constants:
        return str(constants[name])
    else:
        return f"Constant '{name}' not found. Available: {', '.join(constants.keys())}"

print("✅ Data server created")

print("\n🎉 All Level 1 examples created successfully!")
print("Each server is ready to run with: app.run()")