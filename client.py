import json
from openai import OpenAI
from logutil import Log

APIKEYFILE="secure/api.key"

class StoryTimeClient:
    def __init__(self, app):
        self._client = None
        self.log = Log()
        self.app = app

    def clear_log():
        self.log.clear

    def _update_status(self, message):
        if hasattr(self.app, 'set_status'):
            self.app.set_status(message)

    def connect(self):
        try:
            with open(APIKEYFILE, "r") as f:
                key = f.read().strip()
                self._client = OpenAI(
                    api_key=key,
                    default_headers={"OpenAI-Beta": "assistants=v2"}
                )
                self.log.write("API Key Loaded", {"status": "success"})
        except FileNotFoundError:
            self._update_status("API key file not found")
            self.log.write("API Key Load Error", {"error": "api.key not found"})
            self._client = None
        return self

    def is_ready(self):
        return self._client is not None

    def list_assistants(self):
        try:
            result = self._client.beta.assistants.list()
            self.log.write("List Assistants", result.to_dict())
            return result
        except Exception as e:
            msg = f"Failed to fetch assistants: {e}"
            self._update_status(msg)
            self.log.write("Fetch Assistants Error", {"error": str(e)})
            raise

    def create_thread(self, thread_name):
        result = self._client.beta.threads.create()
        self.log.write("Create Thread", {"thread_id": result.id, "name": thread_name})
        return result

    def create_message(self, thread_id, role, content):
        result = self._client.beta.threads.messages.create(thread_id=thread_id, role=role, content=content)
        self.log.write("Create Message", {"thread_id": thread_id, "role": role, "content": content})
        return result

    def run_thread(self, thread_id, assistant_id):
        result = self._client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
        self.log.write("Run Thread", {"thread_id": thread_id, "assistant_id": assistant_id, "run_id": result.id})
        return result

    def get_run_status(self, thread_id, run_id):
        result = self._client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        self.log.write("Run Status", {"thread_id": thread_id, "run_id": run_id, "status": result.status})
        return result

    def get_messages(self, thread_id):
        result = self._client.beta.threads.messages.list(thread_id=thread_id)
        reply_text = result.data[0].content[0].text.value.strip() if result.data else ""
        self.log.write("Cycle Complete", {"thread_id": thread_id, "reply": reply_text})
        self.log.end_cycle()
        return result
