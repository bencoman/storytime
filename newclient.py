import httpx
from openai import OpenAI
from log import Log

APIKEYFILE = "secure/api.key"

class OpenAIClient:

    def __init__(self):
        with open(APIKEYFILE, "r") as f:
            self.key = f.read().strip()

        self.http_client = httpx.Client(
            event_hooks={
                "request": [Log.log_request],
                "response": [Log.log_response],
            },
            timeout=30.0,
        )

        self.client = OpenAI(
            api_key=self.key,
            http_client=self.http_client,
        )

    def completions(self):
        return self.client.chat.completions

    def make_test_request(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "List the planets."}
            ]
        )
        return response
