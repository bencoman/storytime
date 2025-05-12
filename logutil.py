import json
import os
import openai
import logging

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
