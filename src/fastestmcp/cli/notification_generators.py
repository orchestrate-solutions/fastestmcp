"""
Notification generators for FastestMCP CLI
Uses dyna        print(f"📢 Broadcasting notification {index}: {message} (priority: {priority})")

        return notification_data
    
    # Set function attributes for proper identification
    notification_func.__name__ = f"notification_{index}"
    notification_func.__doc__ = f"""
    Notification {index} - handles server notification broadcasting.

    Args:
        message: The notification message to broadcast
        priority: Priority level (low, medium, high, critical)

    Returns:
        Dict containing notification details
    """ern for unlimited scaling
"""

def generate_notifications_file(notifications: int, server_type: str) -> str:
    """Generate notifications.py file using dynamic template pattern"""
    if notifications == 0:
        return ""

    code = '''"""
Area of Responsibility: Notifications for MCP Server
- Register notification subscriptions for server events
- Handle notification broadcasting to clients
- Provide notification checking capabilities
"""

import time
from typing import Dict, Any

def create_notification_function(index: int):
    """
    Create a notification function dynamically.
    
    Args:
        index: The notification index (1-based)
        
    Returns:
        Function that handles notification broadcasting
    """
    async def notification_func(message: str = "Default notification", priority: str = "info") -> Dict[str, Any]:
        """
        Notification ''' + str(index) + ''' - handles server notification broadcasting.

        Args:
            message: The notification message to broadcast
            priority: Priority level (low, medium, high, critical)

        Returns:
            Dict containing notification details
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

        return notification_data
    
    # Set function attributes for proper identification
    notification_func.__name__ = f"notification_{index}"
    notification_func.__doc__ = f"""
    Notification {index} - handles server notification broadcasting.

    Args:
        message: The notification message to broadcast
        priority: Priority level (low, medium, high, critical)

    Returns:
        Dict containing notification details
    """
    
    return notification_func

def create_check_function(index: int):
    """
    Create a notification checking function dynamically.
    
    Args:
        index: The notification index (1-based)
        
    Returns:
        Function that handles notification status checking
    """
    def check_func():
        """
        Check notification {index} status and recent updates.
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
    
    # Set function attributes for proper identification
    check_func.__name__ = f"check_notification_{index}"
    check_func.__doc__ = f"""
    Check notification {index} status and recent updates.
    """
    
    return check_func

def register_notifications(server):
    """
    Register notification subscriptions with the MCP server.
    """

'''

    # Add dynamic notification registration
    for i in range(notifications):
        code += f'''
    # Register notification {i+1}
    notification_func_{i+1} = create_notification_function({i+1})
    server.subscription(name=f"notification_{i+1}", description=f"Notification subscription {i+1} for server events")(notification_func_{i+1})
    
    # Register notification checking tool {i+1}
    check_func_{i+1} = create_check_function({i+1})
    server.tool(name=f"check_notification_{i+1}", description=f"Check for notification {i+1} updates and status")(check_func_{i+1})
'''

    # Add the get_all_notifications tool
    code += '''
    @server.tool(name="get_all_notifications", description="Get status of all notification subscriptions")
    def get_all_notifications():
        """
        Get comprehensive status of all notification subscriptions.
        """
        notifications_status = []
'''

    for i in range(notifications):
        code += f'''
        notifications_status.append({{
            "id": "notification_{i+1}",
            "status": "active",
            "last_update": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "pending_count": 0
        }})'''

    code += '''

        return {
            "type": "notifications_overview",
            "total_notifications": len(notifications_status),
            "active_notifications": len(notifications_status),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "notifications": notifications_status
        }
'''

    return code


def generate_subscriptions_file(subscriptions: int, server_type: str) -> str:
    """Generate subscriptions.py file using dynamic template pattern"""
    if subscriptions == 0:
        return ""

    code = '''"""
Base subscription infrastructure for MCP Server
- Provides async subscription handlers with timestamped events
- Handles subscription lifecycle and event broadcasting
"""

import time
import asyncio
from typing import Dict, Any, AsyncGenerator

def create_subscription_function(index: int):
    """
    Create a subscription function dynamically.
    
    Args:
        index: The subscription index (1-based)
        
    Returns:
        Async generator function that handles event streaming
    """
    async def subscription_func(filter_criteria: str = "all") -> AsyncGenerator[Dict[str, Any], None]:
        """
        Base subscription {index} - provides event streaming with filtering.

        Args:
            filter_criteria: Criteria for filtering events (default: "all")

        Yields:
            Dict containing event data with timestamps
        """
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
    
    # Set function attributes for proper identification
    subscription_func.__name__ = f"subscription_{index}"
    subscription_func.__doc__ = f"""
    Base subscription {index} - provides event streaming with filtering.

    Args:
        filter_criteria: Criteria for filtering events (default: "all")

    Yields:
        Dict containing event data with timestamps
    """
    
    return subscription_func

def create_manage_function(index: int):
    """
    Create a subscription management function dynamically.
    
    Args:
        index: The subscription index (1-based)
        
    Returns:
        Function that handles subscription management
    """
    def manage_func(action: str = "status", filter_criteria: str = "all"):
        """
        Manage subscription {index} - get status, update filters, etc.

        Args:
            action: Action to perform (status, update_filter, pause, resume)
            filter_criteria: New filter criteria for update_filter action
        """
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
    
    # Set function attributes for proper identification
    manage_func.__name__ = f"manage_subscription_{index}"
    manage_func.__doc__ = f"""
    Manage subscription {index} - get status, update filters, etc.

    Args:
        action: Action to perform (status, update_filter, pause, resume)
        filter_criteria: New filter criteria for update_filter action
    """
    
    return manage_func

def register_subscriptions(server):
    """
    Register base subscription infrastructure with the MCP server.
    """

'''

    # Add dynamic subscription registration
    for i in range(subscriptions):
        code += f'''
    # Register subscription {i+1}
    subscription_func_{i+1} = create_subscription_function({i+1})
    server.subscription(name=f"subscription_{i+1}", description=f"Base subscription {i+1} for event streaming")(subscription_func_{i+1})
    
    # Register subscription management tool {i+1}
    manage_func_{i+1} = create_manage_function({i+1})
    server.tool(name=f"manage_subscription_{i+1}", description=f"Manage subscription {i+1} settings and filters")(manage_func_{i+1})
'''

    # Add the get_subscription_overview tool
    code += '''
    @server.tool(name="get_subscription_overview", description="Get overview of all subscriptions")
    def get_subscription_overview():
        """
        Get comprehensive overview of all subscriptions.
        """
        subscriptions_info = []
'''

    for i in range(subscriptions):
        code += f'''
        subscriptions_info.append({{
            "id": "subscription_{i+1}",
            "status": "active",
            "type": "event_stream",
            "description": f"Subscription {i+1} for event streaming"
        }})'''

    code += '''

        return {
            "type": "subscriptions_overview",
            "total_subscriptions": len(subscriptions_info),
            "active_subscriptions": len(subscriptions_info),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "subscriptions": subscriptions_info
        }
'''

    return code


def generate_client_notifications_file(notifications: int, subscriptions: int, client_type: str) -> str:
    """Generate client notifications.py file using actual working code from client templates"""
    if notifications == 0 and subscriptions == 0:
        return ""

    code = '''"""
MCP Client notifications and subscriptions
- Client for managing notifications with priority queues
- Handles subscription management and event processing
"""

import heapq
import asyncio
from typing import Dict, Any, List, Optional

class NotificationsClient:
    """
    Client for managing notifications with priority queues.
    Based on actual working client notification code.
    """
    PRIORITY_MAP = {"low": 3, "medium": 2, "high": 1, "critical": 0}

    def __init__(self, fastmcp_client):
        self._client = fastmcp_client
        self._queue = []  # (priority, count, message)
        self._counter = 0
        self._subscriptions = {}  # Active subscriptions

    def add_notification(self, message, priority="low"):
        """Add a notification to the priority queue"""
        prio = self.PRIORITY_MAP.get(priority, 3)
        heapq.heappush(self._queue, (prio, self._counter, message))
        self._counter += 1

    def get_notifications(self, max_count=None):
        """Get notifications from the queue, ordered by priority"""
        notifications = sorted(self._queue)
        if max_count:
            notifications = notifications[:max_count]
        return [msg for _, _, msg in notifications]

    def clear_notifications(self, priority=None):
        """Clear notifications, optionally by priority"""
        if priority is None:
            self._queue = []
        else:
            prio = self.PRIORITY_MAP.get(priority, 3)
            self._queue = [n for n in self._queue if n[0] != prio]

    async def subscribe(self, subscription_type: str, **kwargs):
        """Subscribe to a notification type"""
        try:
            # In real implementation, this would call the MCP server subscription
            subscription_id = f"{subscription_type}_{len(self._subscriptions)}"
            self._subscriptions[subscription_id] = {
                "type": subscription_type,
                "status": "active",
                "kwargs": kwargs,
                "created": asyncio.get_event_loop().time()
            }

            return {
                "status": "subscribed",
                "subscription_id": subscription_id,
                "type": subscription_type
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "type": subscription_type
            }

    async def unsubscribe(self, subscription_id: str):
        """Unsubscribe from a notification"""
        try:
            if subscription_id in self._subscriptions:
                del self._subscriptions[subscription_id]
                return {
                    "status": "unsubscribed",
                    "subscription_id": subscription_id
                }
            else:
                return {
                    "status": "not_found",
                    "subscription_id": subscription_id
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "subscription_id": subscription_id
            }

    def get_subscriptions(self):
        """Get list of active subscriptions"""
        return list(self._subscriptions.keys())

    def get_subscription_status(self, subscription_id: str):
        """Get status of a specific subscription"""
        return self._subscriptions.get(subscription_id, {"status": "not_found"})
'''

    return code


def generate_client_subscriptions_file(subscriptions: int, client_type: str) -> str:
    """Generate client subscriptions.py file for managing subscriptions"""
    if subscriptions == 0:
        return ""

    code = '''"""
MCP Client subscription management
- Handles subscription lifecycle and event processing
- Provides subscription monitoring and control
"""

import asyncio
from typing import Dict, Any, List, Callable, Optional

class SubscriptionClient:
    """
    Client for managing MCP subscriptions and event handling.
    """

    def __init__(self, mcp_client):
        self._client = mcp_client
        self._active_subscriptions = {}
        self._event_handlers = {}

    async def subscribe(self, subscription_name: str, handler: Optional[Callable] = None, **kwargs):
        """
        Subscribe to an MCP subscription.

        Args:
            subscription_name: Name of the subscription to subscribe to
            handler: Optional event handler function
            **kwargs: Additional parameters for the subscription
        """
        try:
            subscription_id = f"{subscription_name}_{len(self._active_subscriptions)}"

            # Store the subscription
            self._active_subscriptions[subscription_id] = {
                "name": subscription_name,
                "status": "active",
                "handler": handler,
                "kwargs": kwargs,
                "created_at": asyncio.get_event_loop().time(),
                "events_received": 0
            }

            # Store the handler if provided
            if handler:
                self._event_handlers[subscription_id] = handler

            return {
                "status": "subscribed",
                "subscription_id": subscription_id,
                "subscription_name": subscription_name
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "subscription_name": subscription_name
            }

    async def unsubscribe(self, subscription_id: str):
        """
        Unsubscribe from an MCP subscription.
        """
        try:
            if subscription_id in self._active_subscriptions:
                # Clean up the subscription
                del self._active_subscriptions[subscription_id]

                # Clean up the handler if it exists
                if subscription_id in self._event_handlers:
                    del self._event_handlers[subscription_id]

                return {
                    "status": "unsubscribed",
                    "subscription_id": subscription_id
                }
            else:
                return {
                    "status": "not_found",
                    "subscription_id": subscription_id
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "subscription_id": subscription_id
            }

    def get_active_subscriptions(self):
        """Get list of active subscription IDs"""
        return list(self._active_subscriptions.keys())

    def get_subscription_info(self, subscription_id: str):
        """Get information about a specific subscription"""
        return self._active_subscriptions.get(subscription_id, {"status": "not_found"})

    async def process_event(self, subscription_id: str, event_data: Dict[str, Any]):
        """
        Process an incoming event for a subscription.
        """
        try:
            if subscription_id in self._active_subscriptions:
                # Update event count
                self._active_subscriptions[subscription_id]["events_received"] += 1
                self._active_subscriptions[subscription_id]["last_event"] = asyncio.get_event_loop().time()

                # Call the handler if it exists
                if subscription_id in self._event_handlers:
                    handler = self._event_handlers[subscription_id]
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event_data)
                    else:
                        handler(event_data)

                return {
                    "status": "processed",
                    "subscription_id": subscription_id,
                    "event_data": event_data
                }
            else:
                return {
                    "status": "subscription_not_found",
                    "subscription_id": subscription_id
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "subscription_id": subscription_id
            }
'''

    return code
