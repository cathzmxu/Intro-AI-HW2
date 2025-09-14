import os
from dotenv import load_dotenv

# Load .env from parent directory
load_dotenv(dotenv_path="../.env")

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("API key loaded successfully!")
else:
    print("API key not found.")