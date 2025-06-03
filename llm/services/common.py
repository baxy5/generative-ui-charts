import os
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

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


def create_structured_model(schema):
    """Create a structured model."""
    model = init_chat_model("gpt-4o-mini", model_provider="openai")
    model_with_structured_output = model.with_structured_output(schema)
    return model_with_structured_output
