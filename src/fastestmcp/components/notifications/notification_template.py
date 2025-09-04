"""
Notification Component Template - Dynamic notification generation for MCP servers
"""

import time
from typing import Dict, Any, AsyncGenerator


def register_notifications(server_app, count: int = 1) -> None:
    """Register all notification subscriptions with the server - dynamically generated"""
    for i in range(count):
        # Generate unique notification subscription dynamically
        notification_func = create_notification_function(i + 1)
        server_app.add_subscription(notification_func)

        # Generate unique notification checking tool dynamically
        check_func = create_check_function(i + 1)
        server_app.add_tool(check_func)

    # Register overview tool
    server_app.add_tool(get_all_notifications)


def create_notification_function(index: int):
    """Create a unique notification function dynamically"""
    async def notification_function(message: str = "Default notification", priority: str = "info") -> Dict[str, Any]:
        """
        Notification subscription {index}.
        This function handles server notification broadcasting for a specific notification channel.
        
        Extensibility:
        - You can add custom logic for filtering, formatting, or routing notifications here.
        - Integrate with external systems (e.g., email, Slack) by extending this function.
        - Add validation or enrichment of notification payloads as needed.
        
        TODO: Implement custom notification delivery or logging as required by your application.
        """
        notification_data = {
            "type": "notification",
            "id": f"notification_{index}",
            "message": message,
            "priority": priority,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "server_time": time.time(),
            "category": f"category_{index}",
            "metadata": {
                "source": "server",
                "version": "1.0",
                "notification_index": index
            }
        }

        # Log the notification for debugging
        print(f"📢 Broadcasting notification {index}: {message} (priority: {priority})")

        # TODO: Add custom notification delivery logic here

        return notification_data

    # Set function metadata
    notification_function.__name__ = f"notification_{index}"
    # Docstring is already set above
    return notification_function


def create_check_function(index: int):
    """Create a unique notification check function dynamically"""
    def check_function() -> Dict[str, Any]:
        """
        Check notification {index} status and recent updates.
        This function provides a status overview for a specific notification subscription.

        Extensibility:
        - Add logic to fetch real-time status from a database or cache.
        - Integrate with monitoring or alerting systems.
        - Customize the returned status fields as needed.

        TODO: Implement real status checks or metrics collection.
        """
        return {
            "notification_id": f"notification_{index}",
            "type": "notification_status",
            "status": "active",
            "last_check": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "pending_notifications": 0,
            "category": f"category_{index}",
            "description": f"Notification subscription {index} status"
        }

    # Set function metadata
    check_function.__name__ = f"check_notification_{index}"
    # Docstring is already set above
    return check_function


def get_all_notifications() -> Dict[str, Any]:
    """
    Get comprehensive status of all notification subscriptions.
    """
    # This would need to be updated to dynamically generate based on count
    # For now, return a generic overview
    return {
        "type": "notifications_overview",
        "total_notifications": "dynamic",
        "active_notifications": "dynamic",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "notifications": []
    }