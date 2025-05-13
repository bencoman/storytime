import pytest
from newclient import OpenAIClient

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