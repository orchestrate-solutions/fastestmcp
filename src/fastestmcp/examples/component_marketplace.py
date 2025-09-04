# Component Marketplace Examples
# Showcasing the power of pre-built components

from fastestmcp import Server, WebScraper, FileSystem

# Example 1: Content Aggregator
print("=== Example 1: Content Aggregator ===")

content_app = Server("content-aggregator")

# Add web scraping component
scraper = WebScraper(urls=["httpbin.org", "jsonplaceholder.typicode.com"])
content_app.add_component(scraper)

# Add file system component
filesystem = FileSystem("./content")
content_app.add_component(filesystem)

@content_app.tool
def aggregate_content(topic: str) -> str:
    """Aggregate content about a topic from multiple sources"""
    # In a real implementation, this would:
    # 1. Use the scraper to get content from various sources
    # 2. Process and filter the content
    # 3. Save results using the filesystem component

    return f"""Content aggregated for topic: {topic}

Sources checked: {len(scraper.urls)}
Content saved to: ./content/{topic}.txt

This is a placeholder - in the real implementation,
this would scrape actual content and save it to files."""

print("✅ Content aggregator created")

# Example 2: Data Pipeline
print("\n=== Example 2: Data Pipeline ===")

pipeline_app = Server("data-pipeline")

# Add database component (simulated)
# db = Database("sqlite:///pipeline.db")
# pipeline_app.add_component(db)

# Add file system for data storage
data_fs = FileSystem("./data")
pipeline_app.add_component(data_fs)

@pipeline_app.tool
def process_csv_data(filepath: str) -> str:
    """Process CSV data file"""
    try:
        import csv
        import json

        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        # Basic processing
        row_count = len(data)
        columns = list(data[0].keys()) if data else []

        # Save processed data
        output_file = filepath.replace('.csv', '_processed.json')
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        return f"""Processed CSV file: {filepath}
Rows: {row_count}
Columns: {', '.join(columns)}
Output saved to: {output_file}"""

    except FileNotFoundError:
        return f"File not found: {filepath}"
    except Exception as e:
        return f"Error processing CSV: {str(e)}"

@pipeline_app.tool
def validate_data(filepath: str) -> str:
    """Validate data file format and content"""
    try:
        # Check file extension
        if filepath.endswith('.csv'):
            import csv
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)

            issues = []

            # Check for empty rows
            empty_rows = sum(1 for row in data if not any(row.values()))
            if empty_rows > 0:
                issues.append(f"{empty_rows} empty rows found")

            # Check for missing values
            for i, row in enumerate(data):
                missing = [k for k, v in row.items() if not v]
                if missing:
                    issues.append(f"Row {i+1}: missing values in {', '.join(missing)}")

            if issues:
                return "Validation issues found:\n" + "\n".join(issues)
            else:
                return f"✅ File {filepath} passed validation"

        elif filepath.endswith('.json'):
            import json
            with open(filepath, 'r') as f:
                data = json.load(f)

            if isinstance(data, (list, dict)):
                return f"✅ Valid JSON file with {len(data)} top-level items"
            else:
                return "⚠️ Valid JSON but unexpected structure"

        else:
            return f"Unsupported file type: {filepath}"

    except Exception as e:
        return f"Error validating file: {str(e)}"

print("✅ Data pipeline created")

# Example 3: Notification System
print("\n=== Example 3: Notification Hub ===")

notify_app = Server("notification-hub")

# In a real implementation, you'd add notification components
# from fastestmcp import SlackNotifier, EmailSender
# slack = SlackNotifier(webhook_url="...")
# email = EmailSender(api_key="...")
# notify_app.add_component(slack)
# notify_app.add_component(email)

@notify_app.tool
def send_notification(message: str, channel: str = "general") -> str:
    """Send a notification to specified channel"""
    # In real implementation, this would use actual notification services
    return f"""Notification sent!

Message: {message}
Channel: {channel}
Timestamp: {__import__('datetime').datetime.now().isoformat()}

(This is a placeholder - real implementation would send to Slack/Email/etc.)"""

@notify_app.tool
def schedule_reminder(message: str, delay_minutes: int = 60) -> str:
    """Schedule a reminder notification"""
    from datetime import datetime, timedelta

    reminder_time = datetime.now() + timedelta(minutes=delay_minutes)

    return f"""Reminder scheduled!

Message: {message}
Time: {reminder_time.isoformat()}
Delay: {delay_minutes} minutes

(This is a placeholder - real implementation would use a scheduler)"""

print("✅ Notification hub created")

# Example 4: Custom Component Creation
print("\n=== Example 4: Custom Component ===")

from fastestmcp import Component

class MathComponent(Component):
    """Custom math component with advanced calculations"""

    def __init__(self):
        super().__init__("math", "Advanced mathematical operations")

    def register(self, server: Server):
        @server.tool
        def calculate_factorial(n: int) -> str:
            """Calculate factorial of a number"""
            if n < 0:
                return "Error: Factorial not defined for negative numbers"
            if n > 20:
                return "Error: Number too large (max 20)"

            result = 1
            for i in range(1, n + 1):
                result *= i

            return f"Factorial of {n} is {result}"

        @server.tool
        def solve_quadratic(a: float, b: float, c: float) -> str:
            """Solve quadratic equation ax² + bx + c = 0"""
            discriminant = b**2 - 4*a*c

            if discriminant > 0:
                root1 = (-b + discriminant**0.5) / (2*a)
                root2 = (-b - discriminant**0.5) / (2*a)
                return f"Two real roots: {root1:.2f}, {root2:.2f}"
            elif discriminant == 0:
                root = -b / (2*a)
                return f"One real root: {root:.2f}"
            else:
                real_part = -b / (2*a)
                imag_part = (-discriminant)**0.5 / (2*a)
                return f"Complex roots: {real_part:.2f} ± {imag_part:.2f}i"

custom_app = Server("math-solver")
math_comp = MathComponent()
custom_app.add_component(math_comp)

print("✅ Custom math component created")

print("\n🎉 All component marketplace examples created!")
print("These demonstrate the power of reusable components in FastestMCP.")