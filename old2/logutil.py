import json
import os
import openai
import logging
import httpx

LOG_DIR = "log"
ONECYCLELOG = os.path.join(LOG_DIR, "one_cycle.log")
RUNNINGLOG = os.path.join(LOG_DIR, "running.log")

class Log:
    def __init__(self, path=ONECYCLELOG, echo=False):
        self.path = path
        self.echo = echo
        self._end_cycle = True
        print("LOG INIT"   )

        # Ensure the log directory exists
        os.makedirs(LOG_DIR, exist_ok=True)

        # Enable OpenAI HTTP logging
        # TODO: The 'openai.log' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(log="debug")'
        # openai.log = "debug"

        # Initialize logger
        self.logger = logging.getLogger("Log")
        handler = logging.FileHandler(RUNNINGLOG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def clear(self):
        try:
            os.remove(RUNNINGLOG)
        except FileNotFoundError:
            pass

    def end_cycle(self):
        self._end_cycle = True

    def heading(self, label, payload=None):
        self._write(f"\n{{'header: ' : '### {label} ###'}}\n", payload)

    def write(self, label, payload=None):
        self._write(f"{{--- {label} ---}}\n", payload)

    def _write(self, label, payload=None):
        return
        payload = payload or {}
        try:
            if self._end_cycle:
                self._end_cycle = False
                open(ONECYCLELOG, "w").close()

            with open(ONECYCLELOG, "a") as f:
                f.write(f"{label}")
                json.dump(payload, f, indent=2)
                f.write("\n")

            print(f"Writing to RUNNINGLOG: {label}")  # Debugging output
            with open(RUNNINGLOG, "a") as f:
                f.write(f"{label}")
                json.dump(payload, f, indent=2)
                f.write("\n")

            if self.echo:
                print(f"{label}")
                print(json.dumps(payload, indent=2))

        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def log_local(self, event, details=None):
        """Log local interactions, such as file operations or non-API events."""
        self._write(f"{{Local Event: {event} - Details: {details} }}")

# Log the actual request body as pretty-printed JSON
def log_request(request: httpx.Request):
    try:
        body_dict = json.loads(request.content.decode())
        pretty_body = json.dumps(body_dict, indent=2)
    except Exception:
        pretty_body = request.content.decode(errors="replace")

    log = f"""--- REQUEST ---
{request.method} {request.url}

Headers:
{format_headers(request.headers)}

Body:
{pretty_body}
"""
    append_log(log)

# Log the response body as pretty-printed JSON
def log_response(response: httpx.Response):
    try:
        response.read()
        pretty_body = json.dumps(response.json(), indent=2)
    except Exception:
        pretty_body = response.text

    log = f"""--- RESPONSE ---
Status: {response.status_code}

Headers:
{format_headers(response.headers)}

Body:
{pretty_body}
"""
    append_log(log)

# Helper to format headers
def format_headers(headers):
    return "\n".join(f"{k}: {v}" for k, v in headers.items())

# Append log to file
def append_log(block: str):
    with open(RUNNINGLOG, "a", encoding="utf-8") as f:
        f.write(block + "\n\n")
