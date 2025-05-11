import json
import os

LOG_DIR = "log"
ONECYCLELOG = os.path.join(LOG_DIR, "one_cycle.log")
RUNNINGLOG = os.path.join(LOG_DIR, "running.log")

class Log:
    def __init__(self, path=ONECYCLELOG, echo=False):
        self.path = path
        self.echo = echo
        self._end_cycle = True

        # Ensure the log directory exists
        os.makedirs(LOG_DIR, exist_ok=True)

    def clear(self):
        try:
            os.remove(RUNNINGLOG)
        except FileNotFoundError:
            pass

    def end_cycle(self):
        self._end_cycle = True

    def heading(self, label, payload=None):
        self._write(f"\n### {label} ###\n", payload)

    def write(self, label, payload=None):
        self._write(f"--- {label} ---\n", payload)

    def _write(self, label, payload=None):
        payload = payload or {}
        try:
            if self._end_cycle:
                self._end_cycle = False
                open(ONECYCLELOG, "w").close()

            with open(ONECYCLELOG, "a") as f:
                f.write(f"--- {label} ---\n")
                json.dump(payload, f, indent=2)
                f.write("\n")

            with open(RUNNINGLOG, "a") as f:
                f.write(f"--- {label} ---\n")
                json.dump(payload, f, indent=2)
                f.write("\n")

            if self.echo:
                print(f"--- {label} ---")
                print(json.dumps(payload, indent=2))

        except Exception as e:
            print(f"Failed to write to log file: {e}")
