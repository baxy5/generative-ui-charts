from typing import Annotated, List, Optional, TypedDict, Union
from fastapi import Depends
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from core.common import get_gpt_client


class LayoutOptionSchema(BaseModel):
    """Schema for individual layout option."""

    layout_id: str = Field(description="Unique identifier for this layout option")
    layout_name: str = Field(description="Human-readable name for the layout")
    description: str = Field(description="Brief description of the layout approach")
    page_title: str = Field(default=None, description="Title of the page.")
    html: str = Field(default=None, description="HTML code.")
    css: str = Field(default=None, description="CSS code.")
    js: str = Field(default=None, description="Javascript code.")


class LayoutGenerationResponseSchema(BaseModel):
    """Schema for layout generation phase response."""

    layouts: List[LayoutOptionSchema] = Field(description="List of 3 layout options")


class DashboardRequestSchema(BaseModel):
    """API endpoint request schema."""

    question: str
    phase: str = Field(
        default="generate_layouts",
        description="Either 'generate_layouts' or 'finalize_dashboard'",
    )
    selected_layout_id: Optional[str] = Field(
        default=None, description="Required for finalize phase"
    )


class DashboardResponseSchema(BaseModel):
    """API endpoint response structure."""

    url: List[str]
    layouts: Optional[List[LayoutOptionSchema]] = None


class AgentState(TypedDict):
    """State of the agent's workflow."""

    question: str
    data: str
    ui_descriptor: str
    css_descriptor: str
    phase: str
    selected_layout_id: Optional[str]
    result: LayoutGenerationResponseSchema


class DashboardAgent:
    """Agent for generating dashboard layouts."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]) -> None:
        self.client = client
        self.checkpoint_saver = InMemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)

        async def generate_layouts(state: AgentState) -> AgentState:
            """Generate three layouts from the data."""
            structured_model = self.client.with_structured_output(
                LayoutGenerationResponseSchema
            )
            messages = [
                SystemMessage(
                    """You are a UI layout expert. Generate 3 distinct layout approaches for the provided data and user request. Focus on:

                        1. **Layout Structure**: Different ways to organize the information
                        2. **Visualization Approach**: Different chart types, table vs cards, etc.
                        3. **User Experience**: Different interaction patterns

                        For each layout, provide:
                        - A unique layout_id
                        - A descriptive name and description
                        - Simplified HTML structure for preview (no complex styling)
                        - Basic CSS for thumbnail preview

                        Make each layout distinctly different in approach - not just styling variations."""
                ),
                HumanMessage(
                    f"""Generate 3 different layout options for:

                        **USER REQUEST:** {state['question']}
                        **DATA:** {state['data']}

                        Create layouts that differ in:
                        1. Information hierarchy (what's emphasized)
                        2. Visualization method (charts vs tables vs cards)
                        3. User interaction patterns (drilling down vs filtering vs overview)
                        
                        Keep the HTML simple - focus on structure, not final styling."""
                ),
            ]

            response = await structured_model.ainvoke(messages)

            state["result"] = response
            return state

        async def finalize_dashboard(
            state: AgentState,
        ) -> AgentState:
            """Finalize user decided dashboard layout."""
            structured_model = self.client.with_structured_output(
                LayoutGenerationResponseSchema
            )

            messages = [
                SystemMessage(
                    """You are an expert web developer specializing in creating data-driven UI components that will be embedded in iframes. Your task is to generate a complete, self-contained web component with HTML, CSS, and JavaScript based on the provided data structure, UI component descriptors, and CSS styling guidelines.

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
                        - Include comprehensive data validation and sanitization

                        ## OUTPUT FORMAT:
                        Return a single layout with the complete HTML, CSS, and JavaScript implementation."""
                ),
                HumanMessage(
                    f"""Create the final dashboard component using the selected layout:

                        **USER REQUEST:** {state['question']}
                        **DATA:** {state['data']}
                        **SELECTED LAYOUT ID:** {state['selected_layout_id']}
                        **UI DESCRIPTORS:** {state['ui_descriptor']}
                        **CSS DESCRIPTORS:** {state['css_descriptor']}

                        Generate a single, complete dashboard component based on the selected layout."""
                ),
            ]

            response = await structured_model.ainvoke(messages)

            state["result"] = response
            return state

        def route_phase_node(state: AgentState) -> AgentState:
            # This node just passes through the state
            return state

        def route_phase_condition(state: AgentState) -> str:
            # This function determines which path to take
            if state["phase"] == "generate_layouts":
                return "generate_layouts"
            else:
                return "finalize_dashboard"

        graph.add_node("route_phase", route_phase_node)
        graph.add_node("generate_layouts", generate_layouts)
        graph.add_node("finalize_dashboard", finalize_dashboard)

        graph.set_entry_point("route_phase")
        graph.add_conditional_edges(
            "route_phase",
            route_phase_condition,
            {
                "generate_layouts": "generate_layouts",
                "finalize_dashboard": "finalize_dashboard",
            },
        )

        graph.add_edge("generate_layouts", END)
        graph.add_edge("finalize_dashboard", END)

        return graph.compile(checkpointer=self.checkpoint_saver)
