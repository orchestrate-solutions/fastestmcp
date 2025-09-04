"""
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
