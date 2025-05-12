import pytest
from newclient import OpenAIClient

def test_make_test_request():
    client = OpenAIClient()
    response = client.completions().create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "List the planets."}
        ]
    )
    assert response is not None, "Response should not be None"
    assert "choices" in response, "Response should contain 'choices'"
    assert len(response["choices"]) > 0, "Response should have at least one choice"
