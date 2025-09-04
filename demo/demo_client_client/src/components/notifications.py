"""
MCP Client notifications and subscriptions
- Client for managing notifications with priority queues
- Handles subscription management and event processing
"""

import heapq
import asyncio

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
