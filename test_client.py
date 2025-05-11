import pytest
from logutil import Log
from client import StoryTimeClient
from datetime import datetime

@pytest.fixture(scope="session", autouse=True)
def clear_running_log():
    # Use the Log class to initialize the running log with 'PYTEST RUN'
    Log(pytest_run=True)

@pytest.fixture(scope="session")
def log_instance():
    # Create a single Log instance for the entire test session
    return Log(pytest_run=True)

@pytest.fixture
def dummy_app():
    class DummyApp:
        def set_status(self, msg):
            print(f"[status] {msg}")
    return DummyApp()

@pytest.fixture
def client(dummy_app, log_instance):
    # Use the shared Log instance for the client
    return StoryTimeClient(log_instance, dummy_app)

def test_log(log_instance):
    log_instance.write("Test Entry", {"key": "value"})
    log_instance.end_cycle()
    # Assert no exceptions and log file is updated (if applicable)

def test_api_key_loading(client):
    assert client.is_ready(), "OpenAI client is NOT ready"

def test_list_assistants(client):
    assistants = client.list_assistants()
    assert assistants is not None, "Failed to retrieve assistants"
    assert len(assistants.data) > 0, "No assistants found"

def test_create_thread(client):
    assistant_id = "TestFrame1"
    thread_name = f"Test Thread {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    thread = client.create_thread(assistant_id, thread_name)
    assert thread.id is not None, "Thread creation failed"

def test_list_threads(client):
    threads = client.list_threads()
    assert isinstance(threads, list), "Threads should be a list"
    for thread in threads:
        assert "thread_id" in thread, "Thread ID missing"
        assert "created_at" in thread, "Thread creation date missing"
