import json
from openai import OpenAI
from logutil import Log
from datetime import datetime


APIKEYFILE="secure/api.key"
THREADSFILE="data/threads.json"
TESTASSISTANT="Test Frame 1"

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
                    log="debug",
                    api_key=key,
                    default_headers={"OpenAI-Beta": "assistants=v2"}
                )
                self.log.log_local("API Key Loaded", {"status": "success"})
        except FileNotFoundError:
            self._update_status("API key file not found")
            self.log.log_local("API Key Load Error", {"error": "api.key not found"})
            self._client = None
        return self

    def is_ready(self):
        return self._client is not None

    def list_assistants(self):
        try:
            result = self._client.beta.assistants.list()
            self.log.log_local("List Assistants", {"assistants": result.to_dict()})
            return result
        except Exception as e:
            msg = f"Failed to fetch assistants: {e}"
            self._update_status(msg)
            self.log.log_local("Fetch Assistants Error", {"error": str(e)})
            raise

    def create_thread(self, thread_name):
        result = self._client.beta.threads.create()

        # Prepare thread data
        thread_data = {
            "thread_id": result.id,
            "name": thread_name,
            "assistant_id": TESTASSISTANT,
            "created_at": datetime.fromtimestamp(result.created_at).isoformat(sep=' ', timespec='microseconds'),
            "last_used_at": datetime.fromtimestamp(result.created_at).isoformat(sep=' ', timespec='microseconds')
        }
        self.log.log_local("Store Thread", thread_data)

        # Read existing threads from the file
        try:
            with open(THREADSFILE, "r") as f:
                threads = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            threads = []

        # Insert the new thread data into the array
        threads.append(thread_data)

        # Write the updated array back to the file
        with open(THREADSFILE, "w") as f:
            json.dump(threads, f, indent=2)

        return result

    def create_message(self, thread_id, role, content):
        result = self._client.beta.threads.messages.create(thread_id=thread_id, role=role, content=content)
        self.log.write("Create Message", {"thread_id": thread_id, "role": role, "content": content})
        return result

    def run_thread(self, thread_id, assistant_id):
        result = self._client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
        self.log.log_local("Run Thread", {"thread_id": thread_id, "assistant_id": assistant_id, "run_id": result.id})
        return result

    def get_run_status(self, thread_id, run_id):
        result = self._client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        self.log.log_local("Run Status", {"thread_id": thread_id, "run_id": run_id, "status": result.status})
        return result

    def get_messages(self, thread_id):
        result = self._client.beta.threads.messages.list(thread_id=thread_id)
        reply_text = result.data[0].content[0].text.value.strip() if result.data else ""
        self.log.log_local("Cycle Complete", {"thread_id": thread_id, "reply": reply_text})
        return result

    def meta_add(self, assistant_id, metadata):
        result = self._client.beta.assistants.modify(
            assistant_id=assistant_id,
            metadata=metadata
        )
        self.log.log_local("Meta Add", {"assistant_id": assistant_id, "metadata": metadata})
        return result

    def meta_get(self, assistant_id):
        result = self._client.beta.assistants.retrieve(
            assistant_id=assistant_id
        )
        metadata = result.metadata if hasattr(result, 'metadata') else {}
        self.log.log_local("Meta Get", {"assistant_id": assistant_id, "metadata": metadata})
        return metadata
