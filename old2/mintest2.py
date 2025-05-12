import httpx
import json
from openai import OpenAI
from pathlib import Path

# Set up a custom HTTP client with hooks
APIKEYFILE = "secure/api.key"
with open(APIKEYFILE, "r") as f:
    key = f.read().strip()

# Path to your log file
LOG_FILE = Path("log/openai_http.log")

def append_log(block: str):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(block + "\n\n")

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
        # Ensure the response content is fully read
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


## INTEGRATE THE ABOVE CODE INTO logutil.py
## INTEGRATE TEH BELOW CODE INTO client.py, but keeping assistant api rather than completions api

# Create custom HTTP client with logging
http_client = httpx.Client(
    event_hooks={
        "request": [log_request],
        "response": [log_response],
    },
    timeout=30.0,
)

# Create OpenAI client
client = OpenAI(
    api_key=key,
    http_client=http_client,
)

# Make a test request
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "List the planets."}
    ]
)