import os
import json
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from models.rechart import RechartComponentResponseSchema
from .common import create_structured_model, get_data

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Api key is not set for Openai.")

medical_data = get_data("mock-data/response_1748851964185.json")


def create_model():
    model = create_structured_model(RechartComponentResponseSchema)
    return model


# TODO: Prompt the ai to generate the component without the initial imports
def create_messages(user_prompt):
    data_summary = json.dumps(medical_data)

    return [
        SystemMessage(
            f"""You are a helpful assistant that generates a react component using Recharts library based on the medical data and user requests.
            
            Medical data:
            {data_summary}
            
            1. Use the Recharts library components
            2. Use the ResponsiveContainer component to ensure the chart is responsive
            3. The "data" variable must be defined in the beginning of the component
            4. Create complete React components that visualize the data according to user requests
            5. The component must end with the "export default [componentName]" statement
            6. Return clean, well-structured React code
            
            This dataset contains multiple medical test results over time with various measurements.
            """
        ),
        HumanMessage(content=f"""Using the medical data, {user_prompt}"""),
    ]


def generate_ui(user_prompt=None):
    model = create_model()

    if not user_prompt:
        user_prompt = """Create a line chart showing hemoglobin levels over time from 2021 to 2025, with the reference range displayed as a shaded area."""

    messages = create_messages(user_prompt)
    response = model.invoke(messages)

    return response
