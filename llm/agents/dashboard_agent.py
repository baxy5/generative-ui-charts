from typing import Annotated, List, Optional, TypedDict, Union
from fastapi import Depends
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from core.common import get_gpt_client
from schemas.dashboard_schema import AgentState, Layout, LayoutNode


class DashboardAgent:
    """Agent for generating dashboard layouts."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]) -> None:
        self.client = client
        self.checkpoint_saver = InMemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)

        async def generate_layouts(state: AgentState):
            """Generate three layouts from the data."""
            structured_model = self.client.with_structured_output(LayoutNode)
            messages = [
                SystemMessage(
                    """You are a UI layout designer expert. Generate 3 distinct layout approaches for the provided data and user request. Focus on:

                        1. **Layout Structure**: Different ways to organize the information
                        2. **Visualization Approach**: Different chart types, table vs cards, etc.
                        3. **User Experience**: Different interaction patterns

                        For each layout, provide:
                        - A unique layout_id, with this format: layout-[number]
                        - A descriptive page_title about the content of the dashboard
                        - Simplified HTML structure with distinct layout approaches, build different flexbox or grid for each layout 
                        - Basic CSS for the components, use white as the background of the components and grey for the borders. The borders must have 12px border radius. The dashboard layout must be middle centered and responsive.

                        Important: Watch out for these specifically — do NOT skip them.
                        - Use every information in the provided data.
                        - Use flexbox, grid or both.
                        - Do not create navigation components within the page.
                        - Watch out for the layout_id format.
                        - Page title should be describe the content of the page. No technicalities.
                        - The data and informations must be hardcoded into the html elements.

                        Make each layout distinctly different in approach."""
                ),
                HumanMessage(
                    f"""Generate 3 different layout options for:

                        **USER REQUEST:** {state['query']}
                        **DATA:** {state['data']}

                        Create layouts that differ in:
                        1. Information hierarchy (what's emphasized)
                        2. Visualization method with flexbox, grid or both. (charts,tables,cards,buttons, kpi boxes, hero section, accordions, alerts, box groups, lists, dropdowns, timelines, paragraphs, texts, numbers, decreasing and increasing numbers)
                        3. User interaction patterns (drilling down vs filtering vs overview)
                        
                        Keep the HTML simple - focus on structure, not final styling."""
                ),
            ]

            response = await structured_model.ainvoke(messages)

            state["layouts"] = response.layouts
            return state

        async def finalize_dashboard(
            state: AgentState,
        ) -> AgentState:
            """Finalize user decided dashboard layout."""
            structured_model = self.client.with_structured_output(Layout)

            messages = [
                SystemMessage(
                    """You are an expert web developer specializing in creating data-driven UI components and dashboards. Your task is to generate a complete, self-contained web components with HTML, CSS, and JavaScript based on the provided UI component descriptors, and CSS styling guidelines.

                        ## PRIMARY OBJECTIVE:
                        Transform the provided layout into an interactive, visually appealing UI component that follows the specified design patterns and styling requirements.

                        ## INPUT PROCESSING STRATEGY:

                        ### 1. UI DESCRIPTOR INTEGRATION:
                        - Use the UI descriptor as the primary guide for component structure and behavior
                        - Follow any specified layout patterns, interaction models, or component types
                        - Implement the recommended user experience patterns
                        - Adapt the descriptor guidelines to fit the actual data structure

                        ### 2. CSS DESCRIPTOR UTILIZATION:
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
                        Return a single layout with the complete page_title, HTML, CSS, and JavaScript implementation."""
                ),
                HumanMessage(
                    f"""Create the final dashboard using the selected layout:

                        **SELECTED LAYOUT:** {state['selected_layout']}
                        **UI DESCRIPTORS:** {state['ui_descriptor']}
                        **CSS Styles:** {state['design_system']}

                        Generate a single, complete dashboard based on the selected layout.
                        
                        Important:
                        - Use the CSS for styling.
                        - Use the same flexbox/grid structure of the selected layout.
                        - Hardcode the informations in the HTML.
                        """
                ),
            ]

            response = await structured_model.ainvoke(messages)

            state["final"] = response
            return state

        def route_phase_node(state: AgentState) -> AgentState:
            # This node just passes through the state
            return state

        def route_phase_condition(state: AgentState) -> str:
            # This function determines which path to take
            if state["phase"] == "layout":
                return "layout"
            else:
                return "final"

        graph.add_node("route_phase", route_phase_node)
        graph.add_node("generate_layouts", generate_layouts)
        graph.add_node("finalize_dashboard", finalize_dashboard)

        graph.set_entry_point("route_phase")
        graph.add_conditional_edges(
            "route_phase",
            route_phase_condition,
            {
                "layout": "generate_layouts",
                "final": "finalize_dashboard",
            },
        )

        graph.add_edge("generate_layouts", END)
        graph.add_edge("finalize_dashboard", END)

        return graph.compile(checkpointer=self.checkpoint_saver)
