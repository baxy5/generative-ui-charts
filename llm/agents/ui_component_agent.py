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
import uuid

checkpoint_saver = InMemorySaver()


class UiComponentResponseSchema(BaseModel):
    """Schema for UI component response."""

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique component identifier.",
    )
    name: Optional[str] = Field(default=None, description="Name of the component.")
    component: Optional[str] = Field(default=None, description="Component code.")
    rechartComponents: Optional[list[str]] = Field(
        default=None, description="List of rechart components used in the component."
    )


class UiComponentRequestSchema(BaseModel):
    """Schema for UI component request."""

    prompt: str
    dataset: str
    dataset_name: str


class AgentState(TypedDict):
    """State used by the agent through the workflow"""

    uuid: str
    question: str
    provided_data: str
    extracted_data: str
    component_descriptors: str
    component_schema: str
    component_type: str  # 'chart' or 'ui'
    prompt_suggestions: str
    final_response: Optional[UiComponentResponseSchema]
    # Conversation memory fields
    conversation_history: list[dict]
    previous_components: list[dict]


class UiComponentAgent:
    """Agent for generating UI components directly from user questions and data."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]):
        self.client = client
        self.checkpoint_saver = checkpoint_saver
        self.graph = self._build_graph()

    def _build_context_prompt(self, state: AgentState) -> str:
        """Helper method to build context prompt from conversation history."""
        context_prompt = ""

        if state.get("conversation_history") and len(state["conversation_history"]) > 1:
            context_prompt = "\n\nConversation History:\n"
            for i, entry in enumerate(state["conversation_history"][:-1]):
                context_prompt += f"{i+1}. Previous question: {entry['question']}\n"

            if state.get("previous_components"):
                context_prompt += "\nPreviously generated components:\n"
                for i, comp in enumerate(state["previous_components"]):
                    context_prompt += f"""{i+1}. {comp["component_name"]} {comp['component_code']} {comp['rechartComponents']} (for: {comp['question']})\n"""

        return context_prompt

    def _build_graph(self):
        """Build the graph workflow for generating components."""

        # Graph initialization
        graph = StateGraph(AgentState)

        async def extract_data(state: AgentState):
            """Extract data for the user's question."""

            context_prompt = self._build_context_prompt(state)

            messages = [
                SystemMessage(
                    f"""
            You are a specialized AI assistant. Your task is to answer to the user's question
            carefully from the provided dataset. Extract all the information that answers the question.
            Provide clear rationale for you choice, and return only the relevant information for the question.
            
            Conversation history:
            {context_prompt}
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

            context_prompt = self._build_context_prompt(state)

            messages = [
                SystemMessage(
                    f"""You are a specialized UI/UX analyst. Your task is to determine whether the user's question 
                    requires a chart/graph visualization or a regular UI component.
                    
                    Respond with ONLY one word:
                    - "chart" if the user wants any kind of chart, graph, visualization, plot, or data visualization
                    - "ui" if the user wants regular UI components like cards, tables, lists, forms, etc.
                    
                    Chart keywords: chart, graph, plot, visualization, trend, analytics, statistics, metrics over time, 
                    line chart, bar chart, pie chart, scatter plot, histogram, etc.
                    
                    Conversation history:
                    {context_prompt}
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

            context_prompt = self._build_context_prompt(state)

            messages = [
                SystemMessage(
                    f"""You are a specialized dashboard designer.
                        Your task is to choose a UI component descriptor from the provided
                        components which can be used with the extracted data.
                        
                        Conversation history:
                        {context_prompt}
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

        async def prompt_suggestion(state: AgentState):

            context_prompt = self._build_context_prompt(state)

            messages = [
                SystemMessage(
                    f"""You are an expert UX and Data Analytics specialist focused on reducing user friction and improving data exploration efficiency.
                    Your task is to generate contextual prompt suggestions that help users interact with their data more effectively. 
                    These suggestions should serve as cognitive shortcuts that reduce mental effort and interaction costs while encouraging deeper data exploration.
                    
                    Consider these key aspects when generating suggestions:
                    - The user's current context and question
                    - Available data structure and relationships
                    - Existing components and their capabilities
                    - Common user workflows and exploration patterns
                    
                    Generate up to 4 prompt suggestions that:
                    - Reduce cognitive load by offering clear starting points
                    - Minimize interaction cost by providing ready-to-use prompts
                    - Encourage engagement by suggesting valuable but non-obvious analyses
                    - Improve task efficiency by guiding users toward optimal data exploration paths
                    
                    Each suggestion should be:
                    - Clear and specific enough to be immediately actionable
                    - Contextually relevant to the current data and user needs
                    - Focused on delivering actionable insights
                    - Aligned with data visualization best practices
                    
                    Conversation history:
                    {context_prompt}
                    """
                ),
                HumanMessage(
                    f"""Give me at least 4 prompt suggestions based on these informations.
                    
                        Overall data: {state['provided_data']}
                        
                        User's question: {state['question']}
                    
                        Extracted data for the user's question: {state["extracted_data"]}
                    
                        Component type: {state["component_type"]}
                    """
                ),
            ]

            response = await self.client.ainvoke(messages)

            try:
                state["prompt_suggestions"] = response.content
                return state
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to generate prompt suggestions: {e}",
                )

        async def final_component_generation(
            state: AgentState,
        ) -> UiComponentResponseSchema:
            """Final UI component generation from the extracted data and component descriptor"""
            structured_output_model = self.client.with_structured_output(
                UiComponentResponseSchema
            )

            context_prompt = self._build_context_prompt(state)

            if state["component_type"] == "chart":
                # Generate Rechart component
                messages = [
                    SystemMessage(
                        f"""You are a specialized React developer skilled at creating chart components using Recharts library.
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
                         - Include prompt suggestions component below the chart

                        CRITICAL UUID REQUIREMENT:
                         - The parent/root element of your component MUST have id="{state['uuid']}"
                         - This is the outermost container element that wraps your entire component
                         - The parent element MUST use full width: className="w-full"
                         - Example: <div id="{state['uuid']}" className="w-full">...</div>

                        LAYOUT GUIDELINES:
                         - Wrap your chart in "component-container" for consistent styling
                         - Use appropriate background colors: bg-primary, bg-secondary, bg-tertiary
                         - Use text colors: text-light, text-accent, text-highlight
                         - Apply proper spacing and padding
                         - Ensure the parent container takes full available width
                         - Add prompt suggestions in a row using "flex-container-row" class
                         - Each prompt suggestion should use "prompt-suggestion-item" class
                         - Include "prompt-suggestions-container" for the suggestions section
                         - Add "prompt-suggestions-title" for the section header

                        PROMPT SUGGESTIONS GUIDELINES:
                         - Display prompt suggestions below the main chart component.
                         - Wrap all suggestions in a container with the "prompt-suggestions-container" class.
                         - The container should have a title with the "prompt-suggestions-title" class.
                         - The suggestions themselves should be in a grid using "prompt-suggestions-grid".
                         - Each suggestion must be a div with the "prompt-suggestion-item" class.
                         - Inside each item, use an <h4> tag with class "item-title" for the main prompt question.
                         - Below the title, use a <p> tag with class "item-subtitle" for the description.
                         - The AI-generated state['prompt_suggestions'] will be a string containing several suggestions. You need to parse this string and create a separate component for each suggestion.

                        Provide your response as:
                         - name: The name of your component (PascalCase)
                         - component: The complete React component code with imports and exports
                         - rechartComponents: List of Recharts components used (e.g., ["LineChart", "XAxis", "YAxis", "CartesianGrid", "Tooltip", "Legend", "Line", "ResponsiveContainer"])
                        
                        Conversation history:
                        {context_prompt}
                        """
                    ),
                    HumanMessage(
                        f"""Create a Recharts component using the provided data.
                        
                        REMEMBER: The parent element must have id="{state['uuid']}"
                        
                        User question: {state['question']}
                        Extracted data: {state['extracted_data']}
                        Prompt suggestions: {state['prompt_suggestions']}
                        """
                    ),
                ]
            else:
                # Generate regular UI component
                messages = [
                    SystemMessage(
                        f"""You are a specialized React developer skilled at creating interactive UI components.
                        Your task is to create a React component based on the provided data and UI component descriptor.
                        
                        IMPORTANT RESTRICTIONS:
                         - The component MUST ONLY include ONE import statement: "import React from 'react';"
                         - DO NOT import any other libraries, components, hooks, or utilities
                         - DO NOT use any external dependencies
                         - All functionality must be self-contained within the component
                         - Use React hooks (useState, useEffect, useMemo) for interactivity
                         - Include prompt suggestions component below the main component

                        CRITICAL UUID REQUIREMENT:
                         - The parent/root element of your component MUST have id="{state['uuid']}"
                         - This is the outermost container element that wraps your entire component
                         - The parent element MUST use full width: className="w-full"
                         - Example: <div id="{state['uuid']}" className="w-full">...</div>

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
                         - Add prompt suggestions in a row using "flex-container-row" class
                         - Each prompt suggestion should use "prompt-suggestion-item" class
                         - Include "prompt-suggestions-container" for the suggestions section
                         - Add "prompt-suggestions-title" for the section header

                        PROMPT SUGGESTIONS GUIDELINES:
                         - Display prompt suggestions below the main component.
                         - Wrap all suggestions in a container with the "prompt-suggestions-container" class.
                         - The container should have a title with the "prompt-suggestions-title" class.
                         - The suggestions themselves should be in a grid using "prompt-suggestions-grid".
                         - Each suggestion must be a div with the "prompt-suggestion-item" class.
                         - Inside each item, use an <h4> tag with class "item-title" for the main prompt question.
                         - Below the title, use a <p> tag with class "item-subtitle" for the description.
                         - The AI-generated state['prompt_suggestions'] will be a string containing several suggestions. You need to parse this string and create a separate component for each suggestion.

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
                          
                          
                        Conversation history:
                        {context_prompt}
                        """
                    ),
                    HumanMessage(
                        f"""Create a React component using the provided data and the UI component descriptor schema(s).
                        
                        REMEMBER: The parent element must have id="{state['uuid']}"
                        
                        UI component descriptor schema: {state['component_schema']}
                        
                        Provided data: {state['extracted_data']}
                        
                        Prompt suggestions: {state['prompt_suggestions']}
                        """
                    ),
                ]

            response = await structured_output_model.ainvoke(messages)

            try:
                response.id = state["uuid"]
                state["final_response"] = response

                state["previous_components"].append(
                    {
                        "question": state["question"],
                        "component_name": response.name,
                        "component_code": response.component,
                        "rechartComponents": response.rechartComponents,
                    }
                )

                return state
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Failed to generate final component: {e}"
                )

        # Add nodes to the graph
        graph.add_node("extract_data", extract_data)
        graph.add_node("determine_component_type", determine_component_type)
        graph.add_node("component_descriptor", component_descriptor)
        graph.add_node("prompt_suggestion", prompt_suggestion)
        graph.add_node("final_component_generation", final_component_generation)

        # Define edges between nodes
        graph.set_entry_point("extract_data")
        graph.add_edge("extract_data", "determine_component_type")

        # Conditional routing based on component type
        def should_use_descriptor(state: AgentState) -> str:
            if state["component_type"] == "chart":
                return "prompt_suggestion"
            else:
                return "component_descriptor"

        graph.add_conditional_edges(
            "determine_component_type",
            should_use_descriptor,
            {
                "component_descriptor": "component_descriptor",
                "prompt_suggestion": "prompt_suggestion",
            },
        )

        graph.add_edge("component_descriptor", "prompt_suggestion")
        graph.add_edge("prompt_suggestion", "final_component_generation")
        graph.add_edge("final_component_generation", END)

        return graph.compile(checkpointer=self.checkpoint_saver)

    async def generate_ui_component(
        self, question: str, data: str, component_descriptors: json = None
    ) -> UiComponentResponseSchema:
        """Generate UI component based on the user's question and the data."""

        config = RunnableConfig(configurable={"thread_id": "1"})

        # Try to retrieve previous state from checkpointer
        previous_state: AgentState = None
        try:
            checkpoints = []
            for checkpoint in self.checkpoint_saver.list(config):
                checkpoints.append(checkpoint)

            if checkpoints:
                latest_checkpoint = max(
                    checkpoints, key=lambda x: x.metadata.get("step", 0)
                )
                previous_state = latest_checkpoint.checkpoint["channel_values"]

        except Exception as e:
            previous_state = None
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve previous state from checkpointer: {e}",
            )

        # Initial conversation history
        conversation_history = []
        previous_components = []

        if previous_state:
            conversation_history = previous_state.get("conversation_history", [])
            previous_components = previous_state.get("previous_components", [])
            conversation_history.append(
                {"question": question, "timestamp": str(uuid.uuid4())}
            )
        else:
            conversation_history = [
                {"question": question, "timestamp": str(uuid.uuid4())}
            ]

        initial_state: AgentState = {
            "uuid": f"comp_{str(uuid.uuid4()).replace('-', '')[:12]}",
            "question": question,
            "provided_data": data,
            "component_descriptors": component_descriptors or "{}",
            "conversation_history": conversation_history,
            "previous_components": previous_components,
        }

        result = await self.graph.ainvoke(initial_state, config=config)

        if "final_response" in result and result["final_response"] is not None:
            return result["final_response"]

        return UiComponentResponseSchema(
            name="Failed", component="Failed to generate component."
        )
