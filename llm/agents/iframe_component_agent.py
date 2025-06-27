from typing import Annotated, TypedDict
from fastapi import Depends, HTTPException
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables.config import RunnableConfig
from core.common import get_gpt_client


class IframeComponentResponseSchema(BaseModel):
    """API endpoint response structure."""

    id: str
    url: str


class IframeComponentRequestSchema(BaseModel):
    """API endpoint request schema."""

    question: str
    data: str


class AgentResponseSchema(BaseModel):
    """Schema for structured LLM response."""

    page_title: str = Field(default=None, description="Title of the page.")
    html: str = Field(default=None, description="HTML code.")
    css: str = Field(default=None, description="CSS code.")
    js: str = Field(default=None, description="Javascript code.")


class AgentState(TypedDict):
    """State schema for the agent's workflow."""

    question: str
    data: str
    result: AgentResponseSchema
    ui_descriptor: str
    css_descriptors: str


class IframeComponentAgent:
    """Agent for generating Iframe components."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]):
        self.client = client
        self.checkpoint_saver = InMemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)

        async def generate_components(state: AgentState) -> AgentResponseSchema:
            structured_model = self.client.with_structured_output(AgentResponseSchema)

            system_message = """You are an expert web developer specializing in creating data-driven UI components that will be embedded in iframes. Your task is to generate complete, self-contained web components with HTML, CSS, and JavaScript based on the provided data structure, UI component descriptors, and CSS styling guidelines.

            ## PRIMARY OBJECTIVE:
            Transform the provided data into an interactive, visually appealing UI component that follows the specified design patterns and styling requirements.

            ## INPUT PROCESSING STRATEGY:

            ### 1. DATA ANALYSIS:
            - Parse and understand the structure of the provided data
            - Identify data types (metrics, time series, categories, hierarchical, etc.)
            - Determine the most appropriate visualization method for each data element
            - Extract key insights and patterns that should be highlighted

            ### 2. UI DESCRIPTOR INTEGRATION:
            - Use the UI descriptor as the primary guide for component structure and behavior
            - Follow any specified layout patterns, interaction models, or component types
            - Implement the recommended user experience patterns
            - Adapt the descriptor guidelines to fit the actual data structure

            ### 3. CSS DESCRIPTOR UTILIZATION:
            - Apply the provided CSS styles as the foundation for the component's appearance
            - Ensure generated HTML structure is compatible with the provided CSS classes and selectors
            - Extend the provided styles with additional CSS as needed for data visualization
            - Maintain consistency with the established design system

            ## TECHNICAL REQUIREMENTS:

            ### HTML GENERATION:
            - Generate semantic HTML5 structure that maps to the data hierarchy
            - Create elements that correspond to CSS selectors in the provided styles
            - Include proper data attributes for JavaScript targeting (data-id, data-value, etc.)
            - Implement accessible markup with ARIA labels and roles
            - Structure content to support the intended interactions and visualizations

            ### CSS GENERATION:
            - Build upon the provided CSS descriptor styles
            - Add data-specific styling (charts, tables, cards, etc.)
            - Implement responsive behavior that complements the base styles
            - Create smooth transitions and hover effects
            - Ensure visual hierarchy matches data importance

            ### JAVASCRIPT GENERATION:
            - Write vanilla JavaScript that brings the data to life
            - Implement data binding and dynamic updates
            - Create interactive features (filtering, sorting, drilling down)
            - Add animations and transitions for better UX
            - Include error handling and loading states
            - Optimize for performance with large datasets

            ## DATA-TO-UI MAPPING PATTERNS:

            **NUMERICAL DATA**: Convert to charts, gauges, progress bars, or KPI cards
            **CATEGORICAL DATA**: Present as bar charts, pie charts, or grouped layouts
            **TIME SERIES DATA**: Display as line charts, area charts, or timeline components
            **TABULAR DATA**: Create interactive tables with sorting and filtering
            **HIERARCHICAL DATA**: Build tree views, nested layouts, or drill-down interfaces
            **GEOSPATIAL DATA**: Generate map-based visualizations or location cards
            **COMPARATIVE DATA**: Design side-by-side comparisons or overlay visualizations

            ## QUALITY STANDARDS:
            - Ensure the component is fully self-contained and iframe-ready
            - Implement proper error handling for missing or malformed data
            - Create responsive layouts that work across all device sizes
            - Follow accessibility best practices (WCAG 2.1 AA compliance)
            - Optimize for fast rendering and smooth interactions
            - Include comprehensive data validation and sanitization"""

            human_message = f"""Create a data-driven UI component using the three input sources provided below. Your task is to synthesize these inputs into a cohesive, functional, and visually appealing web component.

                                ## INPUT SOURCES:

                                ### 1. USER REQUEST:
                                {state['question']}

                                ### 2. DATA TO VISUALIZE:
                                {state['data']}

                                ### 3. UI COMPONENT DESCRIPTOR:
                                {state["ui_descriptor"]}

                                ### 4. CSS STYLING GUIDE:
                                {state["css_descriptors"]}

                                ## GENERATION INSTRUCTIONS:

                                ### Step 1: Data Analysis
                                - Analyze the provided data structure and identify key data patterns
                                - Determine the most effective visualization approach for this specific dataset
                                - Identify primary metrics, trends, and relationships that should be emphasized

                                ### Step 2: Design Integration
                                - Use the UI descriptor to understand the intended component behavior and layout
                                - Apply the CSS descriptor styles as your design foundation
                                - Ensure the HTML structure you create is compatible with the provided CSS classes and selectors
                                - Extend the provided styles only as necessary for data visualization needs

                                ### Step 3: Component Generation
                                - Generate HTML that creates a semantic structure matching the data hierarchy
                                - Build CSS that extends the provided styles with data-specific visualizations
                                - Write JavaScript that transforms the raw data into interactive UI elements
                                - Ensure all three parts work together seamlessly

                                ## SPECIFIC IMPLEMENTATION REQUIREMENTS:

                                ### Data Binding:
                                - Make the provided data accessible through `window.componentData = {state['data']}`
                                - Implement dynamic rendering based on the actual data structure
                                - Handle edge cases like missing data, empty arrays, or null values
                                - Create loading and error states for robust user experience

                                ### Styling Consistency:
                                - Prioritize using CSS classes and patterns from the provided CSS descriptor
                                - Only add new styles when necessary for data visualization features
                                - Maintain visual consistency with the established design system
                                - Ensure responsive behavior across different screen sizes

                                ### Interactivity:
                                - Implement user interactions that make sense for this specific data type
                                - Add hover effects, click handlers, and other appropriate interactions
                                - Include smooth transitions and animations where they enhance usability
                                - Make the component keyboard accessible and screen-reader friendly

                                ### Performance:
                                - Optimize rendering for the size and complexity of the provided dataset
                                - Use efficient DOM manipulation techniques
                                - Implement lazy loading or virtualization if dealing with large datasets
                                - Minimize unnecessary re-renders and computations

                                Generate a complete, production-ready component that transforms the provided data into an engaging, interactive user interface following the specified design guidelines."""

            messages = [
                SystemMessage(system_message),
                HumanMessage(human_message),
            ]

            response = await structured_model.ainvoke(messages)

            try:
                state["result"] = response
                return state
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Failed to generate agent response: {e}"
                )

        graph.add_node("generate_components", generate_components)

        graph.set_entry_point("generate_components")
        graph.add_edge("generate_components", END)

        return graph.compile(checkpointer=self.checkpoint_saver)

    async def generate_iframe_components(
        self,
        question: str,
        data: str,
        ui_descriptor: str,
        css: str,
    ) -> AgentResponseSchema:
        """Generate page_title, HTML, CSS and JS code."""

        initial_state: AgentState = {
            "question": question,
            "data": data,
            "ui_descriptor": ui_descriptor,
            "css_descriptors": css,
        }

        config = RunnableConfig(configurable={"thread_id": "1"})

        result = await self.graph.ainvoke(initial_state, config=config)

        if "result" in result and result["result"] is not None:
            return result["result"]
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to generate components for Iframe."
            )
