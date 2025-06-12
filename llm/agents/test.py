import json
from typing import Any, Optional, Dict, TypedDict
from pydantic import BaseModel, Field
from fastapi import Depends, HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables.config import RunnableConfig
from core.common import get_gpt_client


class UiComponentResponseSchema(BaseModel):
    """Schema for UI component response."""

    name: Optional[str] = Field(default=None, description="Name of the component.")
    component: Optional[str] = Field(default=None, description="Component code.")
    rechartComponents: Optional[list[str]] = Field(
        default=None, description="List of rechart components used in the component."
    )


class UiComponentRequestSchema(BaseModel):
    """Schema for UI component request."""

    prompt: str


class AgentState(TypedDict):
    """State used by the agent through the workflow"""

    question: str
    provided_data: str
    extracted_data: str
    component_descriptors: str
    component_schema: str
    component_type: str  # 'chart' or 'ui'
    final_component: Optional[UiComponentResponseSchema]


class UiComponentAgent:
    """Agent for generating UI components directly from user questions and data."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]):
        self.client = client
        self.checkpoint_saver = InMemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the graph workflow for generating components."""

        # Graph initialization
        graph = StateGraph(AgentState)

        async def extract_data(state: AgentState):
            """Extract data for the user's question."""
            messages = [
                SystemMessage(
                    f"""
            You are a specialized AI assistant. Your task is to answer to the user's question
            carefully from the provided dataset. Extract all the information that answers the question.
            Provide clear rationale for you choice, and return only the relevant information for the question.
            """
                ),
                HumanMessage(
                    f"""Provide an answer for the user's question. User's question: {state['question']}
                        
                        Provided data: {state['provided_data']}"""
                ),
            ]

            response = await self.client.ainvoke(messages)

            try:
                state["extracted_data"] = response.content
                return state
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to extract data for the user's question: {e}",
                )

        async def determine_component_type(state: AgentState):
            """Determine if the user wants a chart/graph or a regular UI component."""
            messages = [
                SystemMessage(
                    """You are a specialized UI/UX analyst. Your task is to determine whether the user's question 
                    requires a chart/graph visualization or a regular UI component.
                    
                    Respond with ONLY one word:
                    - "chart" if the user wants any kind of chart, graph, visualization, plot, or data visualization
                    - "ui" if the user wants regular UI components like cards, tables, lists, forms, etc.
                    
                    Chart keywords: chart, graph, plot, visualization, trend, analytics, statistics, metrics over time, 
                    line chart, bar chart, pie chart, scatter plot, histogram, etc.
                    """
                ),
                HumanMessage(
                    f"""Determine the component type for this request:
                    
                    User question: {state['question']}
                    Extracted data: {state['extracted_data']}
                    
                    Respond with either "chart" or "ui" only."""
                ),
            ]

            response = await self.client.ainvoke(messages)

            try:
                component_type = response.content.strip().lower()
                if component_type not in ["chart", "ui"]:
                    component_type = "ui"  # Default to UI if unclear
                state["component_type"] = component_type
                return state
            except Exception as e:
                # Default to UI component if determination fails
                state["component_type"] = "ui"
                return state

        async def component_descriptor(state: AgentState):
            """Choose a UI component descriptor for the extracted data."""
            messages = [
                SystemMessage(
                    f"""You are a specialized dashboard designer.
                        Your task is to choose a UI component descriptor from the provided
                        components which can be used with the extracted data.
                        """
                ),
                HumanMessage(
                    f"""Choose a UI component descriptor for the extracted data.
                        You have to choose carefully which UI component descriptor
                        can be used with the data.
                        
                        Extracted data: {state["extracted_data"]}
                        
                        Provided UI components: {state['component_descriptors']}"""
                ),
            ]

            response = await self.client.ainvoke(messages)

            try:
                state["component_schema"] = response.content
                return state
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to choose UI component descriptor: {e}",
                )

        async def final_component_generation(
            state: AgentState,
        ) -> UiComponentResponseSchema:
            """Final UI component generation from the extracted data and component descriptor"""
            structured_output_model = self.client.with_structured_output(
                UiComponentResponseSchema
            )

            if state["component_type"] == "chart":
                # Generate Rechart component
                messages = [
                    SystemMessage(
                        """You are a specialized React developer skilled at creating chart components using Recharts library.
                        Your task is to create a React component with charts based on the provided data.
                        
                        IMPORTANT REQUIREMENTS:
                         - Import React and necessary Recharts components
                         - Use Recharts library components (LineChart, BarChart, PieChart, etc.)
                         - Use ResponsiveContainer to ensure the chart is responsive
                         - Define the "data" variable at the beginning of the component with the provided data
                         - Create complete React components that visualize the data according to user requests
                         - The component must end with "export default [ComponentName]" statement
                         - Return clean, well-structured React code
                         - Include rechartComponents list with all Recharts components used

                        LAYOUT GUIDELINES:
                         - Wrap your chart in "component-container" for consistent styling
                         - Use appropriate background colors: bg-primary, bg-secondary, bg-tertiary
                         - Use text colors: text-light, text-accent, text-highlight
                         - Apply proper spacing and padding

                        Provide your response as:
                         - name: The name of your component (PascalCase)
                         - component: The complete React component code with imports and exports
                         - rechartComponents: List of Recharts components used (e.g., ["LineChart", "XAxis", "YAxis", "CartesianGrid", "Tooltip", "Legend", "Line", "ResponsiveContainer"])
                        """
                    ),
                    HumanMessage(
                        f"""Create a Recharts component using the provided data.
                        
                        User question: {state['question']}
                        Extracted data: {state['extracted_data']}
                        """
                    ),
                ]
            else:
                # Generate regular UI component
                messages = [
                    SystemMessage(
                        """You are a specialized React developer skilled at creating interactive UI components.
                        Your task is to create a React component based on the provided data and UI component descriptor.
                        
                        IMPORTANT RESTRICTIONS:
                         - The component MUST ONLY include ONE import statement: "import React from 'react';"
                         - DO NOT import any other libraries, components, hooks, or utilities
                         - DO NOT use any external dependencies
                         - All functionality must be self-contained within the component
                         - Use React hooks (useState, useEffect, useMemo) for interactivity

                        INTERACTIVITY GUIDELINES:
                         - CREATE INTERACTIVE COMPONENTS with minimal user interaction required
                         - For tables: Add sorting functionality (click column headers to sort ascending/descending)
                         - For tables: Add filtering functionality (search/filter inputs)
                         - For lists: Add search/filter capabilities
                         - For data displays: Add toggle views, expandable sections, or tabs
                         - Use React state management (useState) to handle user interactions
                         - Implement sorting logic for alphabetical (A-Z, Z-A) and numerical (ascending/descending) ordering
                         - Add search functionality that filters data in real-time as user types
                         - Include clear visual indicators for interactive elements (hover effects, active states)
                         - Make interactive elements intuitive (clickable headers, search icons, clear buttons)

                        TABLE-SPECIFIC INTERACTIVITY:
                         - Add sortable column headers with visual indicators (arrows for sort direction)
                         - Implement search/filter input above the table
                         - Support multiple sort types: alphabetical, numerical, date-based
                         - Add "Clear Filter" or "Reset" functionality
                         - Use cursor: pointer for clickable elements
                         - Show sort direction with ↑ ↓ arrows or similar indicators
                         - Filter should work across all columns or specific columns as appropriate

                        LAYOUT GUIDELINES:
                         - When creating components with multiple elements, ALWAYS use appropriate container classes
                         - For multiple elements in a row: use "flex-container-row" class
                         - For multiple elements in a column: use "flex-container-column" class
                         - For grid layouts with 2 items: use "grid-container-2" class
                         - For grid layouts with 3 items: use "grid-container-3" class  
                         - For grid layouts with 4 items: use "grid-container-4" class
                         - For auto-fitting grid layouts: use "grid-container-auto" class
                         - For dashboard-style layouts: use "dashboard-container" class
                         - Wrap your main content in "component-container" for consistent styling
                         - Use "container-spacing-normal" for standard spacing, "container-spacing-tight" for compact layouts
                         - Available container classes include: flex-container-*, grid-container-*, component-container, dashboard-container

                        STYLING GUIDELINES:
                         - Use the existing CSS custom classes and variables from globals.css
                         - Apply appropriate background colors: bg-primary, bg-secondary, bg-tertiary
                         - Use text colors: text-light, text-accent, text-highlight
                         - Apply component-specific classes like stat-box, info-panel, hero-section when appropriate
                         - Use data-table, data-table-container classes for tables
                         - For search inputs: use "filter-input" or "input-search" classes
                         - For clear/reset buttons: use "clear-filter-btn" or "btn-clear" classes
                         - For sortable headers: add "sortable" and "interactive-header" classes
                         - For sort indicators: use "sort-indicator" class with ↑ ↓ arrows
                         - Add hover effects and interactive styling for better UX
                         - Style interactive elements clearly (buttons, clickable headers, inputs)

                         Provide your response as:
                          - name: The name of your component (PascalCase)
                          - component: The complete React component code with imports and exports
                        """
                    ),
                    HumanMessage(
                        f"""Create a React component using the provided data and the UI component descriptor schema(s).
                        
                            UI component descriptor schema: {state['component_schema']}
                            
                            Provided data: {state['extracted_data']}
                        """
                    ),
                ]

            response = await structured_output_model.ainvoke(messages)

            try:
                state["final_component"] = response
                return state
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Failed to generate final component: {e}"
                )

        # Add nodes to the graph
        graph.add_node("extract_data", extract_data)
        graph.add_node("determine_component_type", determine_component_type)
        graph.add_node("component_descriptor", component_descriptor)
        graph.add_node("final_component_generation", final_component_generation)

        # Define edges between nodes
        graph.set_entry_point("extract_data")
        graph.add_edge("extract_data", "determine_component_type")

        # Conditional routing based on component type
        def should_use_descriptor(state: AgentState) -> str:
            if state["component_type"] == "chart":
                return "final_component_generation"
            else:
                return "component_descriptor"

        graph.add_conditional_edges(
            "determine_component_type",
            should_use_descriptor,
            {
                "component_descriptor": "component_descriptor",
                "final_component_generation": "final_component_generation",
            },
        )

        graph.add_edge("component_descriptor", "final_component_generation")
        graph.add_edge("final_component_generation", END)

        return graph.compile(checkpointer=self.checkpoint_saver)

    async def generate_ui_component(
        self, question: str, data: str, component_descriptors: json = None
    ) -> UiComponentResponseSchema:
        """Generate UI component based on the user's question and the data."""

        initial_state: AgentState = {
            "question": question,
            "provided_data": data,
            "component_descriptors": component_descriptors or "{}",
        }
        config = RunnableConfig(configurable={"thread_id": "1"})

        result = await self.graph.ainvoke(initial_state, config=config)

        if "final_component" in result and result["final_component"] is not None:
            return result["final_component"]

        return UiComponentResponseSchema(
            name="Failed", component="Failed to generate component."
        )
