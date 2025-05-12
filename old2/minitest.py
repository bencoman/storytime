import logging
import openai
from openai import OpenAI
import os

#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("openai")
logger.setLevel(logging.DEBUG)

# Enable OpenAI HTTP logging to the console
# TODO: The 'openai.log' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(log="debug")'
# openai.log = "debug"

# Output the OpenAI library version to the console
print(f"OpenAI library version: {openai.__version__}")

# Load API key from secure folder
API_KEY_PATH = "secure/api.key"
if not os.path.exists(API_KEY_PATH):
    raise FileNotFoundError(f"API key file not found at {API_KEY_PATH}")

with open(API_KEY_PATH, "r") as f:
    api_key = f.read().strip()

# Initialize OpenAI client

# Perform an API request to generate a log
try:
    # Use the latest OpenAI API interface to create a chat completion
#    client = OpenAI(api_key=api_key,log="debug")
    client=OpenAI(
                    api_key=api_key,
                    default_headers={"OpenAI-Beta": "assistants=v2"}
                )
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "List some models available in OpenAI."}
    ])
    print("API request successful. Response:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"API request failed: {e}")
