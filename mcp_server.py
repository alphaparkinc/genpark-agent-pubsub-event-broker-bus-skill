import sys
import json
from client import PubSubEventBrokerBus

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "publish_event",
                        "description": "Publishes an event to matching topic subscribers.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "topic": {"type": "string"},
                                "payload": {"type": "object"}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        args = params.get("arguments", {})
        bus = PubSubEventBrokerBus()
        res = bus.publish(args.get("topic", "agent.general"), args.get("payload", {}))
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
            }
        }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    bus = PubSubEventBrokerBus()
    print(json.dumps(bus.publish("test", {"hello": "world"}), indent=2))

if __name__ == "__main__":
    main()
