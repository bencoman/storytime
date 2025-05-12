import json
from pathlib import Path
import httpx

class Log:
    LOG_FILE = Path("log/openai_http.log")

    @staticmethod
    def append_log(block: str):
        with Log.LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(block + "\n\n")

    @staticmethod
    def log_request(request: httpx.Request):
        try:
            body_dict = json.loads(request.content.decode())
            pretty_body = json.dumps(body_dict, indent=2)
        except Exception:
            pretty_body = request.content.decode(errors="replace")

        log = f"""--- REQUEST ---
{request.method} {request.url}

Headers:
{Log.format_headers(request.headers)}

Body:
{pretty_body}
"""
        Log.append_log(log)

    @staticmethod
    def log_response(response: httpx.Response):
        try:
            response.read()
            pretty_body = json.dumps(response.json(), indent=2)
        except Exception:
            pretty_body = response.text

        log = f"""--- RESPONSE ---
Status: {response.status_code}

Headers:
{Log.format_headers(response.headers)}

Body:
{pretty_body}
"""
        Log.append_log(log)

    @staticmethod
    def format_headers(headers):
        return "\n".join(f"{k}: {v}" for k, v in headers.items())
