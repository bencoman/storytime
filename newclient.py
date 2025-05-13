import httpx
from openai import OpenAI
from log import Log

APIKEYFILE = "secure/api.key"

class OpenAIClient:

    def __init__(self):
        self.log = Log.single_instance()

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
            default_headers={"OpenAI-Beta": "assistants=v2"}

        )
        self.log.lognote("OpenAIClient initialized")

    def completions(self):
        return self.client.chat.completions

    def listModels(self):
        return self.client.models.list()

    def list_assistants(self):
        # Assuming this method fetches a list of assistants from the OpenAI API
        return self.client.beta.assistants.list()

