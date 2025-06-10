import json
from typing import Any, Optional, Dict
from pydantic import BaseModel, Field
from fastapi import Depends, HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Annotated
from core.common import get_gpt_client


class UiComponentResponseSchema(BaseModel):
    """Schema for UI component response."""

    name: Optional[str] = Field(default=None, description="Name of the component.")
    component: Optional[str] = Field(default=None, description="Component code.")


class UiComponentRequestSchema(BaseModel):
    """Schema for UI component request."""

    prompt: str


class UiComponentAgent:
    """Agent for generating UI components directly from user questions and data."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]):
        self.client = client

    async def generate_ui_component(self, question: str) -> UiComponentResponseSchema:
        """Generate UI component based on the user's question and the data."""
        try:
            data_str = """{
                "companyData": {
                    "yearlyData": [
                        {
                            "year": 2005,
                            "revenue": 1250000,
                            "expenses": 850000,
                            "workers": 45,
                            "companyCars": 12,
                            "workerBenefits": 25000
                        },
                        {
                            "year": 2006,
                            "revenue": 1450000,
                            "expenses": 920000,
                            "workers": 52,
                            "companyCars": 15,
                            "workerBenefits": 28000
                        },
                        {
                            "year": 2007,
                            "revenue": 1680000,
                            "expenses": 1050000,
                            "workers": 58,
                            "companyCars": 18,
                            "workerBenefits": 30000
                        },
                        {
                            "year": 2008,
                            "revenue": 1820000,
                            "expenses": 1150000,
                            "workers": 65,
                            "companyCars": 20,
                            "workerBenefits": 32000
                        },
                        {
                            "year": 2009,
                            "revenue": 1950000,
                            "expenses": 1250000,
                            "workers": 72,
                            "companyCars": 22,
                            "workerBenefits": 35000
                        },
                        {
                            "year": 2010,
                            "revenue": 2100000,
                            "expenses": 1350000,
                            "workers": 80,
                            "companyCars": 25,
                            "workerBenefits": 38000
                        },
                        {
                            "year": 2011,
                            "revenue": 2250000,
                            "expenses": 1450000,
                            "workers": 88,
                            "companyCars": 28,
                            "workerBenefits": 40000
                        },
                        {
                            "year": 2012,
                            "revenue": 2400000,
                            "expenses": 1550000,
                            "workers": 95,
                            "companyCars": 30,
                            "workerBenefits": 42000
                        },
                        {
                            "year": 2013,
                            "revenue": 2550000,
                            "expenses": 1650000,
                            "workers": 102,
                            "companyCars": 32,
                            "workerBenefits": 45000
                        },
                        {
                            "year": 2014,
                            "revenue": 2700000,
                            "expenses": 1750000,
                            "workers": 110,
                            "companyCars": 35,
                            "workerBenefits": 48000
                        },
                        {
                            "year": 2015,
                            "revenue": 2850000,
                            "expenses": 1850000,
                            "workers": 118,
                            "companyCars": 38,
                            "workerBenefits": 50000
                        },
                        {
                            "year": 2016,
                            "revenue": 3000000,
                            "expenses": 1950000,
                            "workers": 125,
                            "companyCars": 40,
                            "workerBenefits": 52000
                        },
                        {
                            "year": 2017,
                            "revenue": 3150000,
                            "expenses": 2050000,
                            "workers": 132,
                            "companyCars": 42,
                            "workerBenefits": 55000
                        },
                        {
                            "year": 2018,
                            "revenue": 3300000,
                            "expenses": 2150000,
                            "workers": 140,
                            "companyCars": 45,
                            "workerBenefits": 58000
                        },
                        {
                            "year": 2019,
                            "revenue": 3450000,
                            "expenses": 2250000,
                            "workers": 148,
                            "companyCars": 48,
                            "workerBenefits": 60000
                        },
                        {
                            "year": 2020,
                            "revenue": 3600000,
                            "expenses": 2350000,
                            "workers": 155,
                            "companyCars": 50,
                            "workerBenefits": 62000
                        },
                        {
                            "year": 2021,
                            "revenue": 3750000,
                            "expenses": 2450000,
                            "workers": 162,
                            "companyCars": 52,
                            "workerBenefits": 65000
                        },
                        {
                            "year": 2022,
                            "revenue": 3900000,
                            "expenses": 2550000,
                            "workers": 170,
                            "companyCars": 55,
                            "workerBenefits": 68000
                        },
                        {
                            "year": 2023,
                            "revenue": 4050000,
                            "expenses": 2650000,
                            "workers": 178,
                            "companyCars": 58,
                            "workerBenefits": 70000
                        },
                        {
                            "year": 2024,
                            "revenue": 4200000,
                            "expenses": 2750000,
                            "workers": 185,
                            "companyCars": 60,
                            "workerBenefits": 72000
                        },
                        {
                            "year": 2025,
                            "revenue": 4350000,
                            "expenses": 2850000,
                            "workers": 192,
                            "companyCars": 62,
                            "workerBenefits": 75000
                        }
                    ]
                }
            }"""

            # Create a model with structured output
            structured_output_model = self.client.with_structured_output(
                UiComponentResponseSchema
            )

            # Define the system and human messages for component generation
            messages = [
                SystemMessage(
                    """You are a specialized React developer skilled at creating UI components.
                    Your task is to create a React component based on the user's question and the provided data.
                    
                    Follow these guidelines:
                    1. Analyze the data carefully to understand its structure and content
                    2. Create a React component that best presents the data according to the user's request
                    3. Use modern React practices with functional components
                    4. Use Tailwind CSS for styling
                    5. Include proper data organization and structure
                    6. Give the component a meaningful name
                    7. Include proper imports and export default statement
                    8. Make sure the component can be rendered immediately
                    
                    IMPORTANT RESTRICTION: The component MUST ONLY include ONE import statement:
                    - ONLY use: "import React from 'react';"
                    - DO NOT import any other libraries, components, hooks, or utilities
                    - DO NOT use any external dependencies
                    - All functionality must be self-contained within the component
                    - If charts or visualizations are needed, implement them using pure React and HTML/CSS
                    
                    IMPORTANT: Use these custom color and typography classes from the application's global.css:
                    
                    /* Background colors */
                    - bg-dark: Dark background
                    - bg-primary: Primary background
                    - bg-secondary: Secondary background
                    - bg-tertiary: Tertiary background
                    
                    /* Text colors */
                    - text-light: Light text (white)
                    - text-accent: Accent text (teal)
                    - text-highlight: Highlighted text (amber)
                    
                    /* Card backgrounds */
                    - bg-card-light: Light card background
                    - bg-card-medium: Medium card background
                    - bg-card-dark: Dark card background
                    
                    /* Accent colors */
                    - accent-dark: Dark accent
                    - accent-primary: Primary accent
                    
                    /* Typography utility classes */
                    - title-main: Main title (largest)
                    - title-section: Section heading
                    - title-subsection: Subsection heading
                    - title-card: Card title
                    - text-regular: Regular body text
                    - text-small: Small text
                    - text-caption: Caption text
                    - metric-large: Large metric display
                    - metric-medium: Medium metric display
                    - metric-small: Small metric display
                    - text-center: Centered text
                    
                    /* Custom padding utility classes */
                    - padding-xs: Extra small padding (0.25rem)
                    - padding-sm: Small padding (0.5rem)
                    - padding-md: Medium padding (1rem)
                    - padding-lg: Large padding (1.5rem)
                    - padding-xl: Extra large padding (2rem)
                    - padding-2xl: Double extra large padding (3rem)
                    
                    /* Directional padding utilities */
                    - padding-x-xs, padding-y-xs: Horizontal/vertical extra small padding
                    - padding-x-sm, padding-y-sm: Horizontal/vertical small padding
                    - padding-x-md, padding-y-md: Horizontal/vertical medium padding
                    - padding-x-lg, padding-y-lg: Horizontal/vertical large padding
                    - padding-x-xl, padding-y-xl: Horizontal/vertical extra large padding
                    - padding-x-2xl, padding-y-2xl: Horizontal/vertical double extra large padding
                    
                    /* Responsive width guidelines */
                    Use "w-full" combined with appropriate max-width constraints based on the amount of information:
                    - For minimal data (1-3 data points): w-full max-w-[250px]
                    - For small components (simple metrics): w-full max-w-[300px]
                    - For medium data displays (charts, small tables): w-full max-w-[400px]
                    - For data-rich components (comparison tables): w-full max-w-[500px] 
                    - For comprehensive dashboards or complex tables: w-full max-w-[600px] or w-full max-w-[800px]
                    - For full-width layouts: w-full (without max-width)
                    
                    When displaying multiple related metrics or data points:
                    - Use flex layout with flex-wrap: "flex flex-wrap gap-4"
                    - Apply appropriate width constraints to each child component
                    - Ensure the layout is responsive on smaller screens
                    
                    Provide your response as:
                    - name: The name of your component (PascalCase)
                    - component: The complete React component code with imports and exports
                    """
                ),
                HumanMessage(
                    f"""
                    Question: {question}
                    
                    Data: {data_str}
                    
                    Please create a React component that addresses my question using the provided data.
                    """
                ),
            ]

            # Generate the component
            response = await structured_output_model.ainvoke(messages)
            return response

        except Exception as e:
            # Handle errors and provide helpful error messages
            error_detail = str(e)
            if len(error_detail) > 100:
                error_detail = error_detail[:100] + "..."

            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate UI component: {error_detail}",
            )
