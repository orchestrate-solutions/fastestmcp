# Level 2: Minimal Config Examples
# When you need a bit more control but still super simple

from fastestmcp import Server

# Example 1: Configured Server with Components
print("=== Example 1: Server with Components ===")

# Create server with minimal config
app = Server("content-aggregator", config={
    "logging": True,
    "error_handling": True
})

# Add component marketplace components
from fastestmcp import WebScraper, FileSystem

# Web scraper component
scraper = WebScraper(urls=["httpbin.org", "jsonplaceholder.typicode.com"])
app.add_component(scraper)

# File system component
filesystem = FileSystem("./data")
app.add_component(filesystem)

@app.tool
def scrape_and_save(url: str, filename: str) -> str:
    """Scrape content from URL and save to file"""
    try:
        # Use the web scraper component
        # content = "Sample scraped content"  # In real usage: scraper.scrape_url(url)

        # Use the file system component
        # filesystem.save_file(filename, content)  # Would save the file

        return f"Scraped content from {url} and saved to {filename}"
    except Exception as e:
        return f"Error: {str(e)}"

print("✅ Content aggregator server created")

# Example 2: Database-Enabled Server
print("\n=== Example 2: Database Server ===")

db_app = Server("task-manager", config={
    "logging": True
})

# In a real implementation, you'd add a Database component
# from fastestmcp import Database
# db = Database("sqlite:///tasks.db")
# db_app.add_component(db)

# For now, we'll simulate with in-memory storage
tasks = []

@db_app.tool
def add_task(title: str, description: str = "") -> str:
    """Add a new task"""
    task_id = len(tasks) + 1
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": False
    }
    tasks.append(task)
    return f"Added task: {title}"

@db_app.tool
def list_tasks() -> str:
    """List all tasks"""
    if not tasks:
        return "No tasks found"

    result = "Tasks:\n"
    for task in tasks:
        status = "✓" if task["completed"] else "○"
        result += f"{status} {task['id']}: {task['title']}\n"
    return result

@db_app.tool
def complete_task(task_id: int) -> str:
    """Mark a task as completed"""
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return f"Completed task: {task['title']}"

    return f"Task with ID {task_id} not found"

print("✅ Task manager server created")

# Example 3: API Integration Server
print("\n=== Example 3: API Integration ===")

api_app = Server("api-client", config={
    "error_handling": True,
    "logging": True
})

@api_app.tool
def call_json_api(url: str, method: str = "GET") -> str:
    """Call a JSON API endpoint"""
    try:
        import requests
        import json

        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, timeout=10)
        else:
            return f"Unsupported method: {method}"

        if response.status_code == 200:
            try:
                data = response.json()
                return json.dumps(data, indent=2)
            except (ValueError, TypeError):
                return response.text
        else:
            return f"API call failed with status {response.status_code}"

    except ImportError:
        return "Error: requests library required for API calls"
    except Exception as e:
        return f"Error calling API: {str(e)}"

@api_app.tool
def get_github_user(username: str) -> str:
    """Get GitHub user information"""
    url = f"https://api.github.com/users/{username}"
    return call_json_api(url)

print("✅ API client server created")

# Example 4: File Processing Server
print("\n=== Example 4: File Processor ===")

file_app = Server("file-processor", config={
    "logging": True
})

@file_app.tool
def analyze_file(filepath: str) -> str:
    """Analyze a text file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        lines = len(content.split('\n'))
        words = len(content.split())
        chars = len(content)

        return f"""File Analysis: {filepath}
Lines: {lines}
Words: {words}
Characters: {chars}
Size: {len(content)} bytes"""

    except FileNotFoundError:
        return f"File not found: {filepath}"
    except Exception as e:
        return f"Error analyzing file: {str(e)}"

@file_app.tool
def search_in_file(filepath: str, search_term: str) -> str:
    """Search for a term in a file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        lines = content.split('\n')
        matches = []

        for i, line in enumerate(lines, 1):
            if search_term.lower() in line.lower():
                matches.append(f"Line {i}: {line.strip()}")

        if matches:
            return f"Found {len(matches)} matches:\n" + "\n".join(matches[:10])  # Limit to 10
        else:
            return f"No matches found for '{search_term}'"

    except FileNotFoundError:
        return f"File not found: {filepath}"
    except Exception as e:
        return f"Error searching file: {str(e)}"

print("✅ File processor server created")

print("\n🎉 All Level 2 examples created successfully!")
print("These servers use minimal configuration while adding specific functionality.")