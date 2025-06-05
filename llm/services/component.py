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
            1. ALWAYS create a complete React functional component with proper imports and exports. Your code MUST include:
               - Import statements (React, any necessary hooks)
               - A properly named functional component declared with "const ComponentName = () => "
               - Return statement with JSX
               - Export default statement
            
            2. Use React for the component structure and Tailwind CSS for all styling. Do not use custom CSS or other styling methods.
            
            3. DISPLAY ALL RELEVANT DATA - Do not omit important fields from the dataset. Ensure comprehensive representation of the data.
            
            4. PROPER DATA HIERARCHY - Follow these guidelines for mapping data to typography classes:
               - Patient name, test names, and report titles should use 'title-card' class
               - Test dates, patient demographics should use 'title-subsection' class
               - Critical values, abnormal results should use 'text-highlight' color with 'text-regular' size
               - Normal values should use 'text-light' color with 'text-regular' size
               - Units, reference ranges should use 'text-small' class
               - Numeric values, especially abnormal ones, should use 'metric-small' class
               - Timestamps, minor details should use 'text-caption' class
            
            5. Use these custom color classes for all styling:
               - Background colors: bg-dark, bg-primary, bg-secondary, bg-tertiary
               - Text colors: text-light, text-accent, text-highlight
               - Card backgrounds: bg-card-light, bg-card-medium, bg-card-dark
               - Accent colors: accent-dark, accent-primary
            
            6. Use these custom typography classes for text styling:
               - Main titles: title-main
               - Section headings: title-section
               - Subsection headings: title-subsection
               - Card titles: title-card
               - Regular text: text-regular
               - Small text: text-small
               - Caption text: text-caption
               - Metrics (large): metric-large
               - Metrics (medium): metric-medium
               - Metrics (small): metric-small
               - For centered text: text-center
            
            7. Use this tailwind code for the card component: w-full max-w-[300px] h-auto min-h-[200px] bg-card-medium rounded-lg border border-gray-700 p-4
            
            8. If generating multiple components, arrange them using "flex flex-wrap gap-4" and ensure they are responsive.
            
            9. Each component MUST visually distinguish between normal and abnormal values, using colors and typography.
            
            10. Include proper data organization and grouping by test type, date, or category.
            
            11. Always create unique, specialized components based on the data type - don't reuse the same component structure for all data.

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
