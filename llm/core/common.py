import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Api key is not set for Openai.")


def get_data(path: str):
    """Get the data from the json file."""
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DATA_PATH = os.path.join(PROJECT_ROOT, path)

    data = {}

    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as file:
            data = json.load(file)
    else:
        print(f"Warning: Data file not found at {DATA_PATH}")

    return data


def get_gpt_client():
    """Get the GPT client."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")
    else:
        gpt_client = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=OPENAI_API_KEY,
        )
        return gpt_client
