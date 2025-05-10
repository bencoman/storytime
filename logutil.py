import json

ONECYCLELOG="one_cycle.log"
RUNNINGLOG="running.log"

class Log:
    def __init__(self, path="etc/one_cycle.log", echo=False):
        self.path = path
        self.echo = echo
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

            if self.echo:
                print(f"--- {label} ---")
                print(json.dumps(payload, indent=2))


        except Exception as e:
            print(f"Failed to write to log file: {e}")
