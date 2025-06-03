import json
import os
from dotenv import load_dotenv
from models.component import ComponentResponseSchema
from langchain_core.messages import SystemMessage, HumanMessage
from .common import create_structured_model, get_data

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Api key is not set for Openai.")

medical_data = get_data("mock-data/response_1748851964185.json")


def create_model():
    model = create_structured_model(ComponentResponseSchema)
    return model


def create_messages(user_prompt):
    data_summary = json.dumps(medical_data)

    return [
        SystemMessage(
            f"""You are a helpful assistant that generates simple text-based card components using React and Tailwind CSS, based on the provided data and user requests.
            
            Medical data:
            {data_summary}
            
            Your task is to generate React component code based on user requests and the data above.
            Follow these rules strictly:
            1. Generate simple text-based card components.
            2. Use React for the component structure and Tailwind CSS for all styling. Do not use custom CSS or other styling methods.
            3. You can generate a single component or multiple components as appropriate for the request.
            4. If generating multiple components, arrange them using Tailwind CSS flexbox or grid utilities to ensure they are responsive and well-laid out.
            5. All generated components must be responsive across different screen sizes.
            6. Each generated React component file must end with the "export default [ComponentName];" statement, where [ComponentName] is the name of your main component.
            7. Produce clean, well-structured, and production-ready React code.
            8. Create multiple components for the data, don't use the same component for all data.
            9. Don't use comments in the code.
            10. Each card component must have a border.
            11. Maximum width of the card component is 15rem. (use w-full and max-w-[15rem] for the card component)
            12. Container element of the card components must have a "flex flex-wrap gap-4" class.
            
            Design guidelines:
            - Use Tailwind CSS for styling.
            - Use flexbox or grid utilities for layout.
            - If there are at least 3 card components, make it in one row. If its more than 3, make it flex wrap.
            - Use the following colors:
                - border: gray-700
                - background: gray-800
                - text: white
                - hover: blue-600
                - active: blue-700
                - disabled: gray-600
            - Always create a border for the card component.
            - Use rounded-lg for the card component.
            

            The provided data often contains multiple records or complex information that you will need to represent in the card(s).
            """
        ),
        HumanMessage(content=f"""Using the provided data, {user_prompt}"""),
    ]


def generate_ui(user_prompt=None):
    model = create_model()

    if not user_prompt:
        user_prompt = """Generate a concise summary highlighting abnormal lab values and significant changes from previous tests."""

    messages = create_messages(user_prompt)
    response = model.invoke(messages)

    return response
