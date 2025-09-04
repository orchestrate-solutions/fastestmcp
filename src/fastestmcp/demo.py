#!/usr/bin/env python3
"""
FastestMCP Demo - Show all three levels in action
"""

print("🚀 FastestMCP Demo - Three Levels of Simplicity")
print("=" * 50)

# Level 1: Zero-Config
"""
Demo script showing FastestMCP usage at different levels
"""

from fastestmcp import Server

print("\n📍 LEVEL 1: Zero-Config (80% of use cases)")
print("-" * 40)

level1_app = Server("demo-level1")

@level1_app.tool
def greet(name: str) -> str:
    """Say hello to someone"""
    return f"Hello, {name}! Welcome to FastestMCP Level 1!"

@level1_app.tool
def calculate(a: float, b: float, operation: str) -> str:
    """Perform basic calculations"""
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        result = a / b if b != 0 else "Error: Division by zero"
    else:
        result = f"Unknown operation: {operation}"

    return f"{a} {operation} {b} = {result}"

print("✅ Level 1 server created with 2 tools")
print("   - greet: Says hello")
print("   - calculate: Performs basic math")

# Level 2: Minimal Config
print("\n📍 LEVEL 2: Minimal Config (15% of use cases)")
print("-" * 40)

level2_app = Server("demo-level2", config={
    "logging": True,
    "error_handling": True
})

# Add a component
from fastestmcp import FileSystem
fs = FileSystem("./demo-data")
level2_app.add_component(fs)

@level2_app.tool
def analyze_text(text: str) -> dict:
    """Analyze text statistics"""
    words = len(text.split())
    chars = len(text)
    sentences = len(text.split('.'))

    return {
        "word_count": words,
        "character_count": chars,
        "sentence_count": sentences,
        "average_word_length": chars / words if words > 0 else 0
    }

@level2_app.tool
def save_analysis(text: str, filename: str) -> str:
    """Analyze text and save results to file"""
    analysis = analyze_text(text)

    # In real implementation, this would save to file
    # fs.save_file(filename, json.dumps(analysis, indent=2))

    return f"Analysis saved to {filename}: {analysis}"

print("✅ Level 2 server created with component and 2 tools")
print("   - FileSystem component added")
print("   - analyze_text: Text statistics")
print("   - save_analysis: Analyze and save results")

# Level 3: Full Control
print("\n📍 LEVEL 3: Full Control (5% of use cases)")
print("-" * 40)

# This would use the full FastMCP API
from mcp.server.fastmcp.server import FastMCP

level3_server = FastMCP(name="demo-level3")

@level3_server.tool()
def advanced_calculation(expression: str) -> str:
    """Evaluate a mathematical expression"""
    try:
        # WARNING: eval() is dangerous in production!
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@level3_server.resource("data://demo/info")
def get_demo_info() -> str:
    """Get demo information"""
    import json
    return json.dumps({
        "version": "1.0.0",
        "levels": ["Level 1", "Level 2", "Level 3"],
        "timestamp": __import__('datetime').datetime.now().isoformat()
    })

print("✅ Level 3 server created with full MCP control")
print("   - advanced_calculation: Evaluates math expressions")
print("   - data://demo/info: Demo information resource")

# Component Marketplace Demo
print("\n🛍️ COMPONENT MARKETPLACE")
print("-" * 40)

marketplace_app = Server("marketplace-demo")

# Add multiple components
from fastestmcp import WebScraper, FileSystem
web_comp = WebScraper(urls=["httpbin.org"])
marketplace_app.add_component(web_comp)

fs_comp = FileSystem("./marketplace-data")
marketplace_app.add_component(fs_comp)

@marketplace_app.tool
def scrape_and_store(url: str) -> str:
    """Scrape content from URL and store it"""
    # In real implementation:
    # content = web_comp.scrape_url(url)
    # fs_comp.save_file(f"scraped_{hash(url)}.txt", content)

    return f"Would scrape {url} and store content (placeholder)"

print("✅ Marketplace server created with 2 components")
print("   - WebScraper: For web content")
print("   - FileSystem: For data storage")

# CLI Demo
print("\n💻 CLI TOOL DEMO")
print("-" * 40)

print("You can also create servers from command line:")
print("  fastestmcp server 'weather monitoring app'")
print("  fastestmcp server 'file organizer'")
print("  fastestmcp server 'github issue tracker'")

# Summary
print("\n🎉 DEMO COMPLETE!")
print("=" * 50)
print("""
FastestMCP provides three levels of simplicity:

🎯 Level 1 (80%): Zero-config - just add tools and run
🔧 Level 2 (15%): Minimal config - add components and settings
⚙️  Level 3 (5%): Full control - access to complete MCP API

🛍️ Component Marketplace: Pre-built components for common tasks

🚀 One-command creation: fastestmcp server "your idea here"

The goal: Make MCP server development as easy as writing a Python function!
""")

# Don't actually run the servers in demo
print("\n💡 To run any of these servers:")
print("   app.run()  # Replace 'app' with the server variable")