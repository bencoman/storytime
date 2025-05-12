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
    print ("CLIENT")
    return StoryTimeClient(dummy_app).connect()

def test_log(client):
    print("TEST LOG")
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

def test_reconnect_to_thread(client):
    client.log.heading("Starting test_reconnect_to_thread")
    return 
    # Step 1: Create a new thread
    thread_name = f"Reconnect Test Thread {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    thread = client.create_thread(thread_name)
    assert thread.id is not None, "Thread creation failed"

    # Step 2: Add a fact to the conversation thread
    fact_key = "test_fact"
    fact_value = "This is a test fact."
    #client.add_fact_to_thread(thread.id, {fact_key: fact_value})

    # Step 3: Look up the thread_id by name
    retrieved_thread_id = client.get_thread_id_by_name(thread_name)
    assert retrieved_thread_id == thread.id, "Failed to retrieve the correct thread ID by name"

    # Step 4: Connect to the retrieved thread_id and retrieve the fact
    connected_thread = client.connect_to_thread(retrieved_thread_id)
    retrieved_fact = connected_thread.get_fact(fact_key)

    # Step 5: Validate the retrieved fact
    assert retrieved_fact == fact_value, "Retrieved fact does not match the original fact"

