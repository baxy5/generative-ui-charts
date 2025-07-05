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
    """Agent for generating dashboard layouts using data-driven information architecture."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]) -> None:
        self.client = client
        self.checkpoint_saver = InMemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)

        async def generate_layouts(state: AgentState):
            """Generate three layouts using data-driven information architecture approach."""
            structured_model = self.client.with_structured_output(LayoutNode)
            messages = [
                SystemMessage(
                    """You are a senior data analyst and UI architect specializing in comprehensive dashboard design. Your approach is DATA-DRIVEN INFORMATION ARCHITECTURE.

                    ## CORE METHODOLOGY: COMPREHENSIVE DATA ANALYSIS

                    ### STEP 1: COMPLETE DATA INVENTORY
                    - Analyze EVERY piece of data provided - numbers, percentages, categories, time series, hierarchies
                    - Identify data types: KPIs, trends, comparisons, distributions, relationships, historical patterns
                    - Map data relationships and dependencies
                    - Calculate derivative insights (growth rates, ratios, percentages, trends)
                    - Categorize data by business importance and user decision-making impact

                    ### STEP 2: INFORMATION HIERARCHY DESIGN
                    - **PRIMARY LEVEL**: Most critical business metrics that drive decisions (revenue, growth, performance)
                    - **SECONDARY LEVEL**: Supporting metrics that provide context (costs, margins, efficiency)
                    - **TERTIARY LEVEL**: Detailed breakdowns and granular data (departments, subcategories, trends)
                    - **CONTEXTUAL LEVEL**: Comparative and historical data for benchmarking

                    ### STEP 3: SYSTEMATIC COMPONENT SELECTION
                    **For each data element, choose the optimal component based on data characteristics:**
                    
                    **KPI BOXES**: Single critical metrics (revenue, profit, growth %, key ratios)
                    **HERO CARDS**: Important metrics with context (revenue with growth trend, customer count with retention)
                    **COMPARISON CARDS**: Side-by-side metrics (this year vs last year, plan vs actual)
                    **DATA TABLES**: Detailed breakdowns with multiple attributes (product performance, regional data, time series)
                    **CHART CONTAINERS**: Trend data, distributions, comparisons requiring visualization
                    **GROUPED SECTIONS**: Related metrics organized by business function or category

                    ### STEP 4: LAYOUT STRATEGY
                    - **TOP SECTION**: Hero KPIs and primary metrics in a prominent stats grid
                    - **MIDDLE SECTION**: Secondary metrics organized by business function/category
                    - **BOTTOM SECTION**: Detailed data tables and granular breakdowns
                    - **RESPONSIVE GRID**: Use CSS Grid for consistent alignment and responsive behavior
                    - **LOGICAL GROUPING**: Group related information using flexbox containers

                    ### REQUIREMENTS:
                    - **MANDATORY**: Use ALL data provided - create visualizations for every metric
                    - **MANDATORY**: Apply consistent information hierarchy principles
                    - **MANDATORY**: Use proper CSS Grid and Flexbox for layout organization
                    - **MANDATORY**: Create exactly 3 distinct layout approaches with format: layout-[1|2|3]
                    - **MANDATORY**: Provide descriptive page titles that reflect the data content
                    - **MANDATORY**: Hardcode all data values directly into HTML elements
                    - **MANDATORY**: Use white backgrounds with grey borders (12px border radius)
                    - **MANDATORY**: Create responsive, center-aligned layouts

                    ### LAYOUT DIFFERENTIATION:
                    **Layout 1**: Executive Summary (Primary metrics prominent, supporting data organized)
                    **Layout 2**: Operational Dashboard (Functional grouping, balanced metric distribution)
                    **Layout 3**: Analytical Deep-dive (Comprehensive data with detailed breakdowns)

                    Generate 3 distinct layouts, each showcasing different information architecture approaches while using ALL available data."""
                ),
                HumanMessage(
                    f"""Apply DATA-DRIVEN INFORMATION ARCHITECTURE to create 3 comprehensive dashboard layouts:

                    **USER REQUEST:** {state['query']}
                    **COMPREHENSIVE DATASET:** {state['data']}

                    **ANALYSIS REQUIREMENTS:**
                    1. Extract and utilize EVERY piece of data provided
                    2. Create information hierarchies based on business impact
                    3. Apply systematic component selection based on data characteristics
                    4. Design layouts that facilitate data-driven decision making

                    **OUTPUT REQUIREMENTS:**
                    - 3 distinct layout approaches (layout-1, layout-2, layout-3)
                    - Comprehensive use of all provided data
                    - Clear information hierarchy in each layout
                    - Proper CSS Grid/Flexbox organization
                    - Responsive design with centered alignment
                    - Professional styling with consistent spacing and borders

                    Focus on creating layouts that help users understand and analyze the complete dataset, not just highlights."""
                ),
            ]

            response = await structured_model.ainvoke(messages)

            state["layouts"] = response.layouts
            return state

        async def finalize_dashboard(
            state: AgentState,
        ) -> AgentState:
            """Finalize dashboard using data-driven architecture principles."""
            structured_model = self.client.with_structured_output(Layout)

            messages = [
                SystemMessage(
                    """You are a senior dashboard architect specializing in DATA-DRIVEN INFORMATION ARCHITECTURE. Your task is to create a comprehensive, professional dashboard that maximizes data utilization and user insights.

                    ## FINALIZATION METHODOLOGY:

                    ### 1. COMPREHENSIVE DATA INTEGRATION
                    - Implement EVERY data point from the selected layout
                    - Ensure no information is omitted or simplified
                    - Create derived metrics where valuable (percentages, ratios, growth rates)
                    - Maintain data accuracy and consistency across all components

                    ### 2. ADVANCED STYLING INTEGRATION
                    - **CSS SYSTEM**: Leverage provided CSS classes and design tokens systematically
                    - **COMPONENT LIBRARY**: Use appropriate components from the library (cards, stats, forms, status badges)
                    - **LAYOUT SYSTEM**: Implement proper CSS Grid and Flexbox layouts
                    - **RESPONSIVE DESIGN**: Ensure components adapt to different screen sizes
                    - **VISUAL HIERARCHY**: Use typography, spacing, and color to guide user attention

                    ### 3. INTERACTIVE DASHBOARD FEATURES
                    - **Dynamic Data Binding**: Create JavaScript that makes data interactive
                    - **Filtering & Sorting**: Add controls for data exploration
                    - **Drill-down Capabilities**: Enable users to explore details
                    - **Real-time Updates**: Implement functions for data refreshing
                    - **Export Functionality**: Add options to export or share data

                    ### 4. PROFESSIONAL IMPLEMENTATION
                    - **Semantic HTML**: Use proper HTML5 structure with accessibility
                    - **CSS Architecture**: Build upon provided styles with additional enhancements
                    - **JavaScript Logic**: Create interactive features and data manipulation
                    - **Error Handling**: Implement graceful error states and loading indicators
                    - **Performance**: Optimize for fast rendering and smooth interactions

                    ### 5. PERPLEXITY LABS STYLE
                    - **Modern Design**: Clean, minimal interface with strategic use of white space
                    - **Data-First Approach**: Prioritize data visibility and accessibility
                    - **Professional Typography**: Clear hierarchy and readable fonts
                    - **Subtle Animations**: Smooth transitions and hover effects
                    - **Intelligent Grouping**: Logical organization of related information

                    ### QUALITY STANDARDS:
                    - **Complete Data Coverage**: Every metric from the dataset should be represented
                    - **Professional Styling**: Consistent use of design system and CSS classes
                    - **Interactive Elements**: Functional JavaScript for data exploration
                    - **Responsive Layout**: Works perfectly across all device sizes
                    - **Self-contained**: Ready to deploy in iframe without external dependencies

                    ### OUTPUT REQUIREMENTS:
                    - Single comprehensive dashboard with complete page title, HTML, CSS, and JavaScript
                    - Full utilization of provided UI descriptors and CSS styling
                    - Implementation of selected layout structure with enhancements
                    - Professional, production-ready code suitable for business use"""
                ),
                HumanMessage(
                    f"""Create the final comprehensive dashboard using DATA-DRIVEN INFORMATION ARCHITECTURE:

                    **SELECTED LAYOUT:** {state['selected_layout']}
                    **UI COMPONENT LIBRARY:** {state['ui_descriptor']}
                    **CSS DESIGN SYSTEM:** {state['design_system']}

                    **IMPLEMENTATION REQUIREMENTS:**
                    1. Use the selected layout structure as the foundation
                    2. Integrate ALL data points from the original dataset
                    3. Apply CSS design system classes and components systematically
                    4. Create interactive JavaScript features for data exploration
                    5. Maintain professional styling with consistent spacing and hierarchy
                    6. Ensure responsive design with proper CSS Grid/Flexbox implementation

                    **FINAL OUTPUT:**
                    - Complete dashboard with title, HTML, CSS, and JavaScript
                    - Comprehensive data representation and analysis capabilities
                    - Professional styling using provided design system
                    - Interactive features for enhanced user experience
                    - Ready for production deployment in iframe environment

                    Focus on creating a dashboard that would be suitable for executive presentations and business decision-making."""
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
