"""
Subscription Component Template - Dynamic subscription generation for MCP servers
"""

import asyncio
import time
from typing import Dict, Any, AsyncGenerator


def register_subscriptions(server_app, count: int = 1) -> None:
    """Register all subscription handlers with the server - dynamically generated"""
    for i in range(count):
        # Generate unique subscription dynamically
        subscription_func = create_subscription_function(i + 1)
        server_app.add_subscription(subscription_func)

        # Generate unique management tool dynamically
        manage_func = create_manage_function(i + 1)
        server_app.add_tool(manage_func)

    # Register overview tool
    server_app.add_tool(get_subscription_overview)


def create_subscription_function(index: int):
    """Create a unique subscription function dynamically"""
    async def subscription_function(filter_criteria: str = "all") -> AsyncGenerator[Dict[str, Any], None]:
        """Dynamically generated subscription function"""
        event_count = 0

        while True:  # In real implementation, this would be event-driven
            event_count += 1

            event_data = {
                "type": "subscription_event",
                "subscription_id": f"subscription_{index}",
                "event_id": f"event_{index}_{event_count}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                "server_time": time.time(),
                "filter_criteria": filter_criteria,
                "data": {
                    "event_type": f"type_{index}",
                    "sequence_number": event_count,
                    "metadata": {
                        "source": f"subscription_{index}",
                        "priority": "normal"
                    }
                }
            }

            # Log the event for debugging
            print(f"📡 Subscription {index} event {event_count}: {filter_criteria}")

            yield event_data

            # In real implementation, this would wait for actual events
            # For demo purposes, we'll simulate periodic events
            await asyncio.sleep(30)  # Wait 30 seconds between events

    # Set function metadata
    subscription_function.__name__ = f"subscription_{index}"
    subscription_function.__doc__ = f"Base subscription {index} - provides event streaming with filtering"

    return subscription_function


def create_manage_function(index: int):
    """Create a unique subscription management function dynamically"""
    def manage_function(action: str = "status", filter_criteria: str = "all") -> Dict[str, Any]:
        """Dynamically generated subscription management function"""
        if action == "status":
            return {
                "subscription_id": f"subscription_{index}",
                "status": "active",
                "current_filter": filter_criteria,
                "events_sent": 0,
                "last_activity": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                "description": f"Subscription {index} management status"
            }
        elif action == "update_filter":
            return {
                "subscription_id": f"subscription_{index}",
                "action": "filter_updated",
                "new_filter": filter_criteria,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                "status": "updated"
            }
        else:
            return {
                "subscription_id": f"subscription_{index}",
                "action": action,
                "status": "action_not_supported",
                "supported_actions": ["status", "update_filter"],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
            }

    # Set function metadata
    manage_function.__name__ = f"manage_subscription_{index}"
    manage_function.__doc__ = f"Manage subscription {index} - get status, update filters, etc"

    return manage_function


def get_subscription_overview() -> Dict[str, Any]:
    """
    Get comprehensive overview of all subscriptions.
    """
    # This would need to be updated to dynamically generate based on count
    # For now, return a generic overview
    return {
        "type": "subscriptions_overview",
        "total_subscriptions": "dynamic",
        "active_subscriptions": "dynamic",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "subscriptions": []
    }