
import os
from logutil import Log
from client import StoryTimeClient

def test_log():
    print("▶ Testing Log.write()")
    log = Log(echo=True)
    log.write("Test Entry", {"key": "value"})
    log.end_cycle()
    print("✓ Log write completed")

def test_api_key_loading():
    print("▶ Testing API key loading and client readiness")
    class DummyApp:
        def set_status(self, msg):
            print(f"[status] {msg}")
    dummy = DummyApp()
    log = Log("test_cycle.log")
    client = StoryTimeClient(log, dummy)
    if client.is_ready():
        print("✓ OpenAI client is ready")
    else:
        print("✗ OpenAI client is NOT ready")

if __name__ == "__main__":
    test_log()
    print()
    test_api_key_loading()

