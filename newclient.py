import httpx
from openai import OpenAI
from log import Log
import json
import uuid
from datetime import datetime

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

    def list_threads(self):
        """List all threads from the threads.json file."""
        try:
            with open("data/threads.json", "r") as f:
                threads = json.load(f)
            return threads
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def create_thread(self, thread_name):
        """Create a new thread using the OpenAI API and store it in the threads.json file."""
        thread = self.client.beta.threads.create(
            messages=[{
                "role": "user",
                "content": thread_name
            }]
        )

        new_thread = {
            "thread_id": thread.id,
            "thread_name": thread_name,
            "assistant": "TestFrame1",
            "created_at": datetime.now().isoformat(sep=' ', timespec='microseconds'),
            "last_used_at": datetime.now().isoformat(sep=' ', timespec='microseconds')
        }

        threads = self.list_threads()
        threads.append(new_thread)

        with open("data/threads.json", "w") as f:
            json.dump(threads, f, indent=2)

        return new_thread

