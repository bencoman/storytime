import json

ONECYCLELOG="one_cycle.log"
RUNNINGLOG="running.log"

class Log:
    def __init__(self):
        self._end_cycle = True

    def end_cycle(self):
        self._end_cycle = True

    def write(self, label, payload):
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

        except Exception as e:
            print(f"Failed to write to log file: {e}")
