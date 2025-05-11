import os
from logutil import Log
from client import StoryTimeClient

def test_log():
    print("▶ Testing Log.write()")
    log.write("Test Entry", {"key": "value"})
    log.end_cycle()
    print("✓ Log write completed")

def test_api_key_loading():
    print("▶ Testing API key loading and client readiness")
    class DummyApp:
        def set_status(self, msg):
            print(f"[status] {msg}")
    dummy = DummyApp()
    client = StoryTimeClient(log, dummy)
    if client.is_ready():
        print("✓ OpenAI client is ready")
    else:
        print("✗ OpenAI client is NOT ready")

def test_list_assistants():
    print("▶ Testing list of available assistants")
    class DummyApp:
        def set_status(self, msg):
            print(f"[status] {msg}")
    dummy = DummyApp()
    client = StoryTimeClient(log, dummy)
    if client.is_ready():
        try:
            assistants = client.list_assistants()
            print("✓ Assistants retrieved successfully")
            for assistant in assistants.data:
                print(f"- ID: {assistant.id}, Name: {assistant.name}")
        except Exception as e:
            print(f"✗ Failed to retrieve assistants: {e}")
    else:
        print("✗ OpenAI client is NOT ready")

def test_create_thread():
    print("▶ Testing thread creation")
    class DummyApp:
        def set_status(self, msg):
            print(f"[status] {msg}")
    dummy = DummyApp()
    client = StoryTimeClient(log, dummy)
    if client.is_ready():
        try:
            assistant_id = "TestFrame1"  # Example assistant ID
            thread_name = "Test Thread"
            thread = client.create_thread(assistant_id, thread_name)
            print("✓ Thread created successfully")
            print(f"- Thread ID: {thread.id}")
        except Exception as e:
            print(f"✗ Failed to create thread: {e}")
    else:
        print("✗ OpenAI client is NOT ready")

def test_list_threads():
    print("▶ Testing list of threads")
    class DummyApp:
        def set_status(self, msg):
            print(f"[status] {msg}")
    dummy = DummyApp()
    client = StoryTimeClient(log, dummy)
    if client.is_ready():
        try:
            threads = client.list_threads()
            print("✓ Threads retrieved successfully")
            for thread in threads:
                print(f"- Thread ID: {thread['thread_id']}, Created At: {thread['created_at']}")
        except Exception as e:
            print(f"✗ Failed to retrieve threads: {e}")
    else:
        print("✗ OpenAI client is NOT ready")

if __name__ == "__main__":
    log = Log(echo=True)
    test_log()
    print()
    test_api_key_loading()
    print()
    test_list_assistants()
    print()
    test_create_thread()
    print()
    test_list_threads()

