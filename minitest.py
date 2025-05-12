import openai
import os

# Enable OpenAI HTTP logging to the console
openai.log = "debug"

# Output the OpenAI library version to the console
print(f"OpenAI library version: {openai.__version__}")

# Load API key from secure folder
API_KEY_PATH = "secure/api.key"
if not os.path.exists(API_KEY_PATH):
    raise FileNotFoundError(f"API key file not found at {API_KEY_PATH}")

with open(API_KEY_PATH, "r") as f:
    api_key = f.read().strip()

# Initialize OpenAI client
openai.api_key = api_key

# Perform an API request to generate a log
try:
    # Use the latest OpenAI API interface to create a chat completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "List some models available in OpenAI."}
        ]
    )
    print("API request successful. Response:")
    print(response["choices"][0]["message"]["content"])
except Exception as e:
    print(f"API request failed: {e}")
