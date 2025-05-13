import pytest
from newclient import OpenAIClient
from datetime import datetime

@pytest.fixture
def dummy_app():
    class DummyApp:
        def set_status(self, msg):
            print(f"[status] {msg}")
    return DummyApp()


def test_api_key():
    client = OpenAIClient()
    response = client.listModels()
    assert response is not None, "Response should not be None"
    assert hasattr(response, "data"), "Response should have 'data' attribute"
    assert len(response.data) > 0, "Response should contain at least one model"

def test_basic_completions_request():
    client = OpenAIClient()
    client.log.logMethodStart()
    response = client.completions().create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "List the planets."}
        ]
    )
    assert response is not None, "Response should not be None"
    assert hasattr(response, "choices"), "Response should have 'choices' attribute"
    assert len(response.choices) > 0, "Response should have at least one choice"

def test_other_completions_request():
    client = OpenAIClient()
    client.log.logMethodStart()
    response = client.completions().create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "List the planets."}
        ]
    )
    assert response is not None, "Response should not be None"
    assert hasattr(response, "choices"), "Response should have 'choices' attribute"
    assert len(response.choices) > 0, "Response should have at least one choice"

def test_list_assistants():
    client = OpenAIClient()
    client.log.logMethodStart()
    assistants = client.list_assistants()
    assert assistants is not None, "Failed to retrieve assistants"
    assert len(assistants.data) > 0, "No assistants found"

def test_thread_management():
    client = OpenAIClient()

    # Define a unique thread name with date-time
    thread_name = f"Test Thread {datetime.now().isoformat(sep=' ', timespec='seconds')}"

    # Get the list of threads and confirm the unqiue name doesn't exist
    threads = client.list_threads()
    # Ensure the thread has a 'thread_name' key before comparing
    assert all(thread.get("thread_name") != thread_name for thread in threads), "Thread name already exists"

    # Create a thread with the new name and store it in the file
    new_thread = client.create_thread(thread_name)
    assert new_thread["thread_name"] == thread_name, "Thread creation failed"

    # Get the updated list of threads and check the name is in it
    updated_threads = client.list_threads()
    client.log.append_log(f"New Thread name: {thread_name}")
    client.log.append_json(updated_threads)
    assert any(thread["thread_name"] == thread_name for thread in updated_threads), "Thread name not found in updated list"