import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv(dotenv_path="../.env")
api_key = os.getenv("OPENAI_API_KEY")

print("API key:", api_key is not None)

url = "https://api.openai.com/v1/audio/speech"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-4o-mini-tts",
    "input": "Hello, world!",
    "voice": "onyx"
}

try:
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        print("Audio saved as output.mp3")
    else:
        print("Error:", response.status_code, response.text)
except Exception as e:
    print("Exception occurred:", str(e))