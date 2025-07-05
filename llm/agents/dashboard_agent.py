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
    """Agent for generating dashboard layouts using component-first design system approach."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]) -> None:
        self.client = client
        self.checkpoint_saver = InMemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)

        async def generate_layouts(state: AgentState):
            """Generate three layouts using component-first design system approach."""
            structured_model = self.client.with_structured_output(LayoutNode)
            messages = [
                SystemMessage(
                    """You are a senior UI/UX designer and front-end architect specializing in COMPONENT-FIRST DESIGN SYSTEMS. Your expertise lies in creating cohesive, scalable dashboard interfaces through strategic component selection and systematic design implementation.

                    ## CORE METHODOLOGY: COMPONENT-FIRST DESIGN SYSTEM

                    ### STEP 1: COMPONENT LIBRARY ANALYSIS
                    **Available Components & Their Optimal Use Cases:**
                    
                    **STAT CARDS (.stat-card)**: 
                    - Perfect for: Single KPI metrics, financial numbers, percentage values
                    - Structure: .stat-value (large number) + .stat-label (description)
                    - Best for: Revenue, profit, growth rates, customer counts
                    
                    **COMPANY CARDS (.company-card)**:
                    - Perfect for: Entity information with multiple attributes
                    - Structure: .company-header + .company-info + .company-description + .company-footer
                    - Best for: Product details, team information, regional data
                    
                    **ANALYTICS SECTIONS (.analytics-section)**:
                    - Perfect for: Grouped data visualization areas
                    - Structure: .chart-container + .chart-title for visual data
                    - Best for: Time series data, comparisons, trend analysis
                    
                    **FORM CONTROLS (.form-control)**:
                    - Perfect for: Interactive filtering and data selection
                    - Structure: .form-group + .form-label + input/select elements
                    - Best for: Date ranges, category filters, search functionality
                    
                    **STATUS BADGES (.status)**:
                    - Perfect for: Categorical indicators and states
                    - Variants: .status--success, .status--warning, .status--error, .status--info
                    - Best for: Performance indicators, alert levels, progress states

                    ### STEP 2: LAYOUT SYSTEM MASTERY
                    **CSS Grid & Flexbox Strategic Implementation:**
                    
                    **STATS GRID (.stats-grid)**:
                    - Use for: Top-level KPI displays (4-6 key metrics)
                    - Structure: CSS Grid with responsive columns
                    - Best Practice: 2-4 columns on desktop, 1-2 on mobile
                    
                    **CONTENT GRID (.content-grid)**:
                    - Use for: Main dashboard sections with sidebar
                    - Structure: Grid with main content area + sidebar
                    - Best Practice: 3fr 1fr ratio for main content vs sidebar
                    
                    **FLEXBOX CONTAINERS (.flex, .flex-col)**:
                    - Use for: Component internal layout and alignment
                    - Utilities: .justify-between, .items-center, .gap-16
                    - Best Practice: Combine with gap utilities for consistent spacing

                    ### STEP 3: DESIGN SYSTEM INTEGRATION
                    **CSS Custom Properties & Utility Classes:**
                    
                    **Color System**: 
                    - Primary: --color-primary (CTA buttons, key actions)
                    - Surface: --color-surface (card backgrounds)
                    - Text: --color-text (primary content), --color-text-secondary (labels)
                    - Status: --color-success, --color-error, --color-warning, --color-info
                    
                    **Spacing System**:
                    - Use consistent spacing: --space-8, --space-16, --space-24, --space-32
                    - Gap utilities: .gap-4, .gap-8, .gap-16 for component spacing
                    - Padding utilities: .py-8, .px-16 for internal component spacing
                    
                    **Typography System**:
                    - Headers: h1-h6 with proper hierarchy
                    - Body: Standard paragraph text with --color-text-secondary for labels
                    - Weights: --font-weight-medium for emphasis, --font-weight-semibold for headers

                    ### STEP 4: RESPONSIVE DESIGN STRATEGY
                    **Mobile-First Component Behavior:**
                    - Stats grid: 4 columns → 2 columns → 1 column
                    - Content grid: Sidebar → Stacked layout
                    - Cards: Full width → Constrained width
                    - Form controls: Adapt to container width

                    ### LAYOUT GENERATION REQUIREMENTS:
                    **MANDATORY SPECIFICATIONS:**
                    - **Component Selection**: Choose the most appropriate component for each data type
                    - **Layout Structure**: Use proper CSS Grid and Flexbox systematically
                    - **Design System**: Implement consistent spacing, colors, and typography
                    - **Responsive Design**: Ensure components work across all screen sizes
                    - **Data Integration**: Include ALL provided data using appropriate components
                    - **Format**: Create exactly 3 layouts with IDs: layout-1, layout-2, layout-3
                    - **Styling**: Use white backgrounds, grey borders with 12px radius, centered alignment

                    ### LAYOUT DIFFERENTIATION STRATEGY:
                    **Layout 1: Executive Overview**
                    - Primary: Large stats grid with key KPIs
                    - Secondary: Company cards for major business units
                    - Tertiary: Analytics sections for trends

                    **Layout 2: Operational Dashboard**
                    - Primary: Balanced mix of stats and form controls
                    - Secondary: Analytics sections with interactive elements
                    - Tertiary: Detailed company cards with performance data

                    **Layout 3: Analytical Workbench**
                    - Primary: Comprehensive analytics sections
                    - Secondary: Interactive form controls for data exploration
                    - Tertiary: Detailed stats with status indicators

                    Generate 3 distinct layouts that showcase different component composition strategies while maintaining design system consistency."""
                ),
                HumanMessage(
                    f"""Apply COMPONENT-FIRST DESIGN SYSTEM methodology to create 3 professional dashboard layouts:

                    **USER REQUEST:** {state['query']}
                    **DATA TO COMPONENTIZE:** {state['data']}

                    **COMPONENT MAPPING REQUIREMENTS:**
                    1. Analyze each data element and select the optimal component type
                    2. Apply consistent design system principles across all components
                    3. Create logical component hierarchies and groupings
                    4. Use proper CSS Grid/Flexbox for responsive layout organization
                    5. Implement systematic spacing, colors, and typography

                    **DESIGN SYSTEM STANDARDS:**
                    - **Stats Cards**: For numerical KPIs and metrics
                    - **Company Cards**: For entity information and profiles
                    - **Analytics Sections**: For data visualization and trends
                    - **Form Controls**: For interactive elements and filters
                    - **Status Badges**: For categorical indicators and states

                    **LAYOUT REQUIREMENTS:**
                    - 3 distinct approaches (layout-1, layout-2, layout-3)
                    - Professional component composition and arrangement
                    - Consistent use of design system tokens and utilities
                    - Responsive grid and flexbox implementation
                    - Complete data integration through appropriate components
                    - Clean, modern styling with proper spacing and alignment

                    Focus on creating layouts that demonstrate mastery of the component library and design system, resulting in professional, scalable dashboard interfaces."""
                ),
            ]

            response = await structured_model.ainvoke(messages)

            state["layouts"] = response.layouts
            return state

        async def finalize_dashboard(
            state: AgentState,
        ) -> AgentState:
            """Finalize dashboard using component-first design system approach."""
            structured_model = self.client.with_structured_output(Layout)

            messages = [
                SystemMessage(
                    """You are a senior front-end architect specializing in COMPONENT-FIRST DESIGN SYSTEMS. Your role is to create production-ready, scalable dashboard interfaces that demonstrate mastery of modern CSS frameworks and component libraries.

                    ## FINALIZATION METHODOLOGY: COMPONENT-FIRST IMPLEMENTATION

                    ### 1. COMPONENT LIBRARY MASTERY
                    **Systematic Component Implementation:**
                    
                    **Button Components (.btn)**:
                    - Primary: .btn.btn--primary (main actions, data export)
                    - Secondary: .btn.btn--secondary (secondary actions)
                    - Outline: .btn.btn--outline (tertiary actions)
                    - Sizes: .btn--sm, .btn--lg as needed
                    
                    **Card Components (.card)**:
                    - Structure: .card > .card__header + .card__body + .card__footer
                    - Use for: Grouped content, detailed information sections
                    - Styling: Automatic shadows, hover effects, border-radius
                    
                    **Form Components (.form-control)**:
                    - Structure: .form-group > .form-label + input.form-control
                    - Types: text inputs, select dropdowns, textareas
                    - Integration: Filtering, search, data input functionality
                    
                    **Stats Components (.stat-card)**:
                    - Structure: .stat-card > .stat-value + .stat-label
                    - Implementation: Large numbers, KPIs, percentage values
                    - Styling: Hover animations, consistent spacing
                    
                    **Status Components (.status)**:
                    - Variants: .status--success, .status--error, .status--warning, .status--info
                    - Use: Performance indicators, alert states, progress tracking
                    - Integration: Dynamic color coding based on data values

                    ### 2. ADVANCED CSS SYSTEM IMPLEMENTATION
                    **Design Token Integration:**
                    
                    **Color System**:
                    ```css
                    /* Primary Actions */
                    background-color: var(--color-primary);
                    color: var(--color-btn-primary-text);
                    
                    /* Surface Elements */
                    background-color: var(--color-surface);
                    border: 1px solid var(--color-card-border);
                    
                    /* Text Hierarchy */
                    color: var(--color-text);              /* Primary text */
                    color: var(--color-text-secondary);    /* Labels, secondary text */
                    
                    /* Status Colors */
                    color: var(--color-success);
                    color: var(--color-error);
                    color: var(--color-warning);
                    color: var(--color-info);
                    ```
                    
                    **Spacing System**:
                    ```css
                    /* Component Spacing */
                    padding: var(--space-16);
                    margin-bottom: var(--space-24);
                    gap: var(--space-8);
                    
                    /* Layout Spacing */
                    .gap-4 { gap: var(--space-4); }
                    .gap-8 { gap: var(--space-8); }
                    .gap-16 { gap: var(--space-16); }
                    ```
                    
                    **Typography System**:
                    ```css
                    /* Headers */
                    font-weight: var(--font-weight-semibold);
                    font-size: var(--font-size-2xl);
                    line-height: var(--line-height-tight);
                    
                    /* Body Text */
                    font-size: var(--font-size-base);
                    line-height: var(--line-height-normal);
                    ```

                    ### 3. RESPONSIVE LAYOUT IMPLEMENTATION
                    **Grid System Architecture:**
                    
                    **Dashboard Header** (.dashboard-header):
                    - Fixed header with logo and actions
                    - Responsive: Full width with centered container
                    
                    **Stats Grid** (.stats-grid):
                    - CSS Grid: repeat(auto-fit, minmax(250px, 1fr))
                    - Responsive: 4 columns → 2 columns → 1 column
                    
                    **Content Grid** (.content-grid):
                    - CSS Grid: 1fr 300px (main content + sidebar)
                    - Responsive: Stacked layout on mobile
                    
                    **Company Grid** (.companies-grid):
                    - CSS Grid: repeat(auto-fill, minmax(300px, 1fr))
                    - Responsive: Auto-fitting cards

                    ### 4. INTERACTIVE JAVASCRIPT FEATURES
                    **Component Enhancement:**
                    
                    **Data Filtering**:
                    - Form controls trigger data filtering
                    - Real-time search and category filtering
                    - Dynamic content updates
                    
                    **Modal Integration**:
                    - Click handlers for detailed views
                    - Proper modal activation/deactivation
                    - Keyboard navigation support
                    
                    **Animation System**:
                    - CSS transitions for hover effects
                    - Smooth data updates
                    - Loading states for data fetching

                    ### 5. PRODUCTION-READY IMPLEMENTATION
                    **Code Quality Standards:**
                    
                    **HTML Structure**:
                    - Semantic HTML5 elements
                    - Proper ARIA labels and roles
                    - Consistent class naming conventions
                    
                    **CSS Architecture**:
                    - Component-based styles
                    - Proper cascade management
                    - Responsive design patterns
                    
                    **JavaScript Organization**:
                    - Modular function structure
                    - Event delegation patterns
                    - Error handling and edge cases

                    ### OUTPUT REQUIREMENTS:
                    - **Complete Dashboard**: Title, HTML, CSS, JavaScript
                    - **Component Integration**: Full use of available component library
                    - **Design System**: Consistent implementation of CSS tokens
                    - **Responsive Design**: Mobile-first, progressive enhancement
                    - **Interactive Features**: Functional JavaScript for user interaction
                    - **Production Quality**: Clean, maintainable, scalable code

                    Create a dashboard that exemplifies best practices in component-first design system implementation."""
                ),
                HumanMessage(
                    f"""Create the final dashboard using COMPONENT-FIRST DESIGN SYSTEM approach:

                    **SELECTED LAYOUT:** {state['selected_layout']}
                    **COMPONENT LIBRARY:** {state['ui_descriptor']}
                    **CSS DESIGN SYSTEM:** {state['design_system']}

                    **IMPLEMENTATION REQUIREMENTS:**
                    1. **Component Integration**: Use appropriate components for each data type
                    2. **Design System**: Implement CSS tokens, utilities, and patterns systematically
                    3. **Layout System**: Apply proper CSS Grid and Flexbox with responsive behavior
                    4. **Interactive Features**: Create functional JavaScript for component interactions
                    5. **Professional Styling**: Maintain consistent spacing, colors, and typography
                    6. **Responsive Design**: Ensure optimal experience across all devices

                    **COMPONENT MAPPING STRATEGY:**
                    - **Statistical Data** → Stats Cards (.stat-card)
                    - **Entity Information** → Company Cards (.company-card)
                    - **Interactive Elements** → Form Controls (.form-control)
                    - **Categorical Data** → Status Badges (.status)
                    - **Data Visualization** → Analytics Sections (.analytics-section)

                    **TECHNICAL SPECIFICATIONS:**
                    - Use CSS custom properties for theming
                    - Implement proper component hierarchy
                    - Apply responsive grid systems
                    - Include interactive JavaScript features
                    - Maintain accessibility standards

                    **FINAL OUTPUT:**
                    - Complete dashboard with professional component composition
                    - Systematic design system implementation
                    - Interactive features for enhanced user experience
                    - Production-ready code suitable for enterprise deployment
                    - Responsive design that works perfectly across all screen sizes

                    Focus on creating a dashboard that demonstrates expertise in modern front-end architecture and component-based design systems."""
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
