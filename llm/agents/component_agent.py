import json
from typing import Annotated, Any, Optional
from fastapi import Depends
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from core.common import get_gpt_client


class ComponentRequestSchema(BaseModel):
    prompt: str


class ComponentResponseSchema(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the component.")
    component: Optional[str] = Field(default=None, description="Component code.")


class ComponentAgent:
    """Agent for generating UI components."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]):
        self.client = client

    async def generate_ui_component(
        self, request: ComponentRequestSchema, data: Any | dict
    ) -> ComponentResponseSchema:
        try:
            model = self.client.with_structured_output(ComponentResponseSchema)
            data_summary = json.dumps(data)
            user_prompt = request.prompt
            messages = [
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

            response = await model.ainvoke(messages)

            return response
        except Exception as e:
            print(f"Error while generating component: {e}")
            return ComponentResponseSchema(
                name="Error", component="Failed to generate component."
            )
