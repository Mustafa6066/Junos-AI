#!/usr/bin/env python3
"""Quick API test for v21.1"""
import urllib.request, json

BASE = "http://localhost:5555"

def test(name, path):
    try:
        r = urllib.request.urlopen(f"{BASE}/api/{path}", timeout=10)
        data = json.loads(r.read())
        if isinstance(data, list):
            print(f"✅ {name}: {len(data)} items")
        elif isinstance(data, dict):
            keys = list(data.keys())[:5]
            print(f"✅ {name}: keys={keys}")
        else:
            print(f"✅ {name}: {str(data)[:80]}")
    except Exception as e:
        print(f"❌ {name}: {e}")

test("Health", "health")
test("Topology", "topology")
test("Devices", "devices")
test("Stats", "network-stats")
test("Templates", "templates")
test("Logs", "logs")
test("Scheduled Tasks", "scheduled-tasks")
test("Workflows", "workflows")
print("\nDone!")
