import pytest
from logutil import Log
from client import StoryTimeClient
from datetime import datetime

@pytest.fixture
def dummy_app():
    class DummyApp:
        def set_status(self, msg):
            print(f"[status] {msg}")
    return DummyApp()

@pytest.fixture
def client(dummy_app):
    return StoryTimeClient(dummy_app).connect()

def test_log(client):
    client.log.clear()
    client.log.heading("Starting test_log")
    client.log.write("Test Entry", {"key": "value"})
    client.log.end_cycle()

def test_api_key_loading(client):
    client.log.heading("Starting test_api_key_loading")
    assert client.is_ready(), "OpenAI client is NOT ready"

def test_list_assistants(client):
    client.log.heading("Starting test_list_assistants")
    assistants = client.list_assistants()
    assert assistants is not None, "Failed to retrieve assistants"
    assert len(assistants.data) > 0, "No assistants found"

def test_create_thread(client):
    client.log.heading("Starting test_create_thread")
    thread_name = f"Test Thread {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    thread = client.create_thread(thread_name)
    assert thread.id is not None, "Thread creation failed"

