"""PubSub Event Broker Bus Engine.
100% Python Standard Library.
"""

import time
from typing import Dict, List, Any

class PubSubEventBrokerBus:
    """Dispatches asynchronous event notifications across isolated agent workers via topic matching."""
    def __init__(self):
        self.subscribers: Dict[str, List[str]] = {}
        self.event_log: List[Dict[str, Any]] = []

    def subscribe(self, topic_pattern: str, handler_name: str):
        if topic_pattern not in self.subscribers:
            self.subscribers[topic_pattern] = []
        if handler_name not in self.subscribers[topic_pattern]:
            self.subscribers[topic_pattern].append(handler_name)

    def publish(self, topic: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        delivered = []
        for pattern, handlers in self.subscribers.items():
            if pattern == topic or (pattern.endswith(".*") and topic.startswith(pattern[:-2])):
                delivered.extend(handlers)
        event = {
            "topic": topic,
            "payload": payload,
            "delivered_to": delivered,
            "timestamp": time.time()
        }
        self.event_log.append(event)
        return {
            "status": "PUBLISHED",
            "topic": topic,
            "delivered_count": len(delivered),
            "subscribers": delivered
        }
