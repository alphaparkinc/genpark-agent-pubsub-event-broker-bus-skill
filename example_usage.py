from client import PubSubEventBrokerBus

bus = PubSubEventBrokerBus()
bus.subscribe("agent.task.*", "indexer_worker")
bus.subscribe("agent.task.completed", "notification_gateway")

res = bus.publish("agent.task.completed", {"task_id": "job_991", "exit_code": 0})
print("=== Event Bus Publish Telemetry ===")
print("Delivered to Subscribers:", res["subscribers"])
print("Delivered Count:", res["delivered_count"])
