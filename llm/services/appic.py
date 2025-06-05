import json
import os
from dotenv import load_dotenv
from models.appic import AppicResponseSchema
from .common import create_structured_model, get_data
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Api key is not set for Openai.")

data = get_data("mock-data/appic.json")


def create_model():
    model = create_structured_model(AppicResponseSchema)
    return model


def create_messages(user_prompt):
    data_summary = json.dumps(data)

    system_message = f"""You are a specialized UI generator that creates visually rich and well-structured React components based on the provided data and user requests.
    
                Provided data: {data_summary}
    
                You MUST follow these requirements strictly:

                1. Generate only HTML5 (use className instead of class) and TailwindCSS code in React - no custom CSS or styled components.
                
                2. COLOR USAGE - You MUST use these predefined color classes throughout the UI (not just black and white):
                   - Background colors: bg-dark, bg-primary, bg-secondary, bg-tertiary
                   - Text colors: text-light, text-accent, text-highlight
                   - Element/card/section backgrounds: bg-card-light, bg-card-medium, bg-card-dark
                   - Accent colors: accent-dark, accent-primary
                   - Use color contrast appropriately for readability
                
                3. TYPOGRAPHY - Use a clear hierarchy with different sizes for different content types:
                   - Main titles: text-4xl font-bold (with appropriate color)
                   - Section headings: text-3xl font-bold
                   - Sub-headings: text-2xl font-semibold
                   - Card titles: text-xl font-semibold
                   - Regular text: text-base
                   - Small/caption text: text-sm
                   - Center text when appropriate (titles, card headings, etc.)
                
                4. SPACING & LAYOUT - Create visual breathing room:
                   - Sections: my-16 or py-16
                   - Between elements: my-8 or py-8
                   - Card padding: p-6 or p-8
                   - Use mx-auto for centered containers
                
                5. STRUCTURE - Use modern layout techniques:
                   - Implement grid layouts using grid-cols-1 md:grid-cols-2 lg:grid-cols-3 for cards
                   - Use flexbox (flex flex-col md:flex-row) for horizontal layouts
                   - Create multi-column layouts for larger screens
                   - Keep mobile-first approach with responsive breakpoints
                
                6. COMPONENTS - Include all these fundamental elements:
                   - Container divs with max-w-7xl mx-auto
                   - Cards with shadow-lg and rounded-lg
                   - Buttons with hover effects
                   - Proper spacing between sections
                
                7. REFINEMENTS:
                   - Use rounded-lg for all border radius needs
                   - Add borders with specified colors where appropriate
                   - Implement hover:scale-105 or similar effects on interactive elements
                   - Use gap-4 or gap-6 between grid/flex items
                
                Return only the complete React component code without explanations."""

    return [
        SystemMessage(system_message),
        HumanMessage(
            content=f"""Generate a full-page React UI based on the data provided which relevant to the user prompt: {user_prompt}
                     
                     The code should be a single React functional component using only HTML5 and TailwindCSS with the approved color palette. Make it visually appealing and fully responsive.
                     """
        ),
    ]


def generate_ui(user_prompt=None):
    model = create_model()

    if not user_prompt:
        user_prompt = """Tell me everything about Appic."""

    messages = create_messages(user_prompt)

    response = model.invoke(messages)

    return response
