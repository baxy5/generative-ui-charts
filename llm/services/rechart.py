import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from models.rechart import RechartComponentResponseSchema

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Api key is not set for Openai.")


def create_model():
    """Initialize and configure the chat model."""
    model = init_chat_model("gpt-4o-mini", model_provider="openai")
    model_with_structured_output = model.with_structured_output(
        RechartComponentResponseSchema
    )
    return model_with_structured_output


# TODO: Prompt the ai to generate the component without the initial imports
def create_messages(user_prompt):
    """Create the messages for the chat model."""
    return [
        SystemMessage(
            "You are a helpful assistant that generates a react component using Recharts library based on the user's request."
        ),
        HumanMessage(content=user_prompt),
    ]


def generate_ui(user_prompt=None):
    """Generate UI components based on user prompt."""
    model = create_model()

    # Use default prompt if none provided
    if not user_prompt:
        user_prompt = """I want a Line chart from this data: const data = [
        { year: '2023', amount: 34000 },
        { year: '2024', amount: 19000 },
        { year: '2025', amount: 20000 },
        ];"""

    messages = create_messages(user_prompt)
    response = model.invoke(messages)

    return response
