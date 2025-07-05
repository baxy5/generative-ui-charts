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
    """Agent for generating dashboard layouts using Perplexity-style analytics approach."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]) -> None:
        self.client = client
        self.checkpoint_saver = InMemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)

        async def generate_layouts(state: AgentState):
            """Generate three layouts using Perplexity-style analytics dashboard approach."""
            structured_model = self.client.with_structured_output(LayoutNode)
            messages = [
                SystemMessage(
                    """You are a senior product designer and data visualization expert specializing in MODERN ANALYTICS INTERFACES, inspired by Perplexity Labs and leading data platforms. Your expertise is in creating intelligent, insight-driven dashboard experiences.

                    ## CORE METHODOLOGY: PERPLEXITY-STYLE ANALYTICS DASHBOARD

                    ### DESIGN PHILOSOPHY: INTELLIGENCE-FIRST INTERFACES
                    **Core Principles:**
                    - **Information Density**: Maximize insight per pixel without overwhelming users
                    - **Contextual Hierarchy**: Surface the most relevant information based on user intent
                    - **Progressive Disclosure**: Layer information depth through intuitive interactions
                    - **Narrative Structure**: Guide users through data stories and insights
                    - **Adaptive Layout**: Respond to data patterns and user behavior

                    ### STEP 1: INTELLIGENT DATA CATEGORIZATION
                    **Data Analysis Framework:**
                    
                    **HERO METRICS** (Top 20% importance):
                    - Primary KPIs that drive business decisions
                    - Growth indicators and performance trends
                    - Critical alerts and threshold breaches
                    - Real-time status indicators
                    
                    **CONTEXTUAL INSIGHTS** (Middle 60% importance):
                    - Supporting metrics that explain the "why"
                    - Comparative analysis and benchmarking
                    - Trend analysis and pattern recognition
                    - Segmentation and breakdown data
                    
                    **EXPLORATORY DATA** (Bottom 20% importance):
                    - Detailed breakdowns and granular views
                    - Historical data and archives
                    - Auxiliary metrics and secondary KPIs
                    - Raw data tables and exports

                    ### STEP 2: MODERN ANALYTICS LAYOUT PATTERNS
                    **Layout Archetypes:**
                    
                    **EXECUTIVE COMMAND CENTER**:
                    - Prominent hero section with key metrics
                    - Real-time status grid with color-coded indicators
                    - Trend visualization panels
                    - Alert/notification sidebar
                    
                    **ANALYTICAL WORKBENCH**:
                    - Multi-panel layout with coordinated views
                    - Interactive filter bar at top
                    - Primary chart area with supporting metrics
                    - Data table with advanced sorting/filtering
                    
                    **PERFORMANCE MONITORING**:
                    - Time-series dashboard with multiple metrics
                    - Comparative views (current vs previous periods)
                    - Breakdown panels by category/segment
                    - Anomaly detection and alerts

                    ### STEP 3: ADVANCED COMPONENT STRATEGY
                    **Smart Component Selection:**
                    
                    **METRIC CARDS with CONTEXT**:
                    - Large primary value with trend indicator
                    - Sparkline or mini-chart for context
                    - Comparison data (vs previous, vs target)
                    - Color-coded status indicators
                    
                    **INTERACTIVE CHART PANELS**:
                    - Primary visualization with multiple data series
                    - Integrated controls for time range, filters
                    - Drill-down capabilities
                    - Export and sharing options
                    
                    **INSIGHT CARDS**:
                    - AI-generated insights and recommendations
                    - Anomaly detection alerts
                    - Trend analysis summaries
                    - Predictive indicators
                    
                    **DATA EXPLORATION TABLES**:
                    - Advanced filtering and sorting
                    - Inline editing capabilities
                    - Export functionality
                    - Pagination and performance optimization

                    ### STEP 4: SOPHISTICATED LAYOUT ARCHITECTURE
                    **Grid System Design:**
                    
                    **ASYMMETRIC LAYOUTS**:
                    - Non-uniform grid patterns for visual interest
                    - Varied component sizes based on importance
                    - Strategic use of white space
                    - Focal point creation through size variation
                    
                    **RESPONSIVE BREAKPOINTS**:
                    - Desktop: Complex multi-column layouts
                    - Tablet: Simplified 2-column with stacking
                    - Mobile: Single-column with prioritized content
                    - Touch-optimized interactions
                    
                    **DEPTH LAYERS**:
                    - Background: Base grid and spacing
                    - Content: Primary data visualizations
                    - Interactive: Hover states and controls
                    - Overlay: Modals and detailed views

                    ### STEP 5: PERPLEXITY-INSPIRED STYLING
                    **Visual Design Language:**
                    
                    **COLOR STRATEGY**:
                    - Monochromatic base with strategic accent colors
                    - Data-driven color coding (performance, status, categories)
                    - Subtle gradients and shadows for depth
                    - High contrast for accessibility
                    
                    **TYPOGRAPHY HIERARCHY**:
                    - Clear distinction between data and labels
                    - Consistent sizing scale (12px, 14px, 16px, 20px, 24px)
                    - Strategic use of font weights
                    - Optimal line height for readability
                    
                    **SPACING RHYTHM**:
                    - 8px base unit for consistent spacing
                    - Progressive spacing scale (8, 16, 24, 32, 48px)
                    - Generous white space for breathing room
                    - Aligned grid system

                    ### LAYOUT GENERATION REQUIREMENTS:
                    **MANDATORY SPECIFICATIONS:**
                    - **Intelligence**: Prioritize most important data prominently
                    - **Completeness**: Include ALL data points with smart hierarchy
                    - **Sophistication**: Use advanced layout patterns and interactions
                    - **Responsiveness**: Ensure optimal experience across all devices
                    - **Accessibility**: Maintain WCAG 2.1 AA compliance
                    - **Performance**: Optimize for fast loading and smooth interactions
                    - **Format**: Create exactly 3 layouts: layout-1, layout-2, layout-3
                    - **Branding**: Professional styling with consistent design language

                    ### LAYOUT DIFFERENTIATION STRATEGY:
                    **Layout 1: Executive Intelligence Hub**
                    - Hero metrics with trend indicators
                    - Real-time status dashboard
                    - Executive summary cards
                    - Strategic insight panels
                    
                    **Layout 2: Analytical Deep Dive**
                    - Interactive chart workbench
                    - Multi-dimensional data exploration
                    - Advanced filtering and segmentation
                    - Detailed data tables and exports
                    
                    **Layout 3: Performance Command Center**
                    - Time-series monitoring dashboard
                    - Comparative analysis views
                    - Anomaly detection alerts
                    - Predictive analytics panels

                    Create 3 sophisticated layouts that demonstrate mastery of modern analytics interface design, each showcasing different aspects of intelligent data presentation."""
                ),
                HumanMessage(
                    f"""Create 3 PERPLEXITY-STYLE ANALYTICS DASHBOARDS using advanced interface design:

                    **USER REQUEST:** {state['query']}
                    **COMPREHENSIVE DATASET:** {state['data']}

                    **ANALYTICS INTELLIGENCE REQUIREMENTS:**
                    1. **Smart Data Prioritization**: Identify and prominently feature the most business-critical metrics
                    2. **Contextual Insights**: Provide supporting data that explains performance and trends
                    3. **Interactive Exploration**: Enable users to drill down and explore data relationships
                    4. **Visual Storytelling**: Guide users through data narratives and insights
                    5. **Responsive Intelligence**: Adapt layout and emphasis based on screen size and context

                    **MODERN INTERFACE STANDARDS:**
                    - **Sophisticated Grid Systems**: Asymmetric layouts with varied component sizes
                    - **Advanced Typography**: Clear hierarchy with strategic font sizing and weights
                    - **Intelligent Color Usage**: Data-driven color coding with accessibility considerations
                    - **Micro-interactions**: Subtle animations and hover effects for enhanced UX
                    - **Progressive Disclosure**: Layer information depth through intuitive interactions

                    **LAYOUT SPECIFICATIONS:**
                    - **Layout 1 (Executive Intelligence Hub)**: Focus on high-level KPIs and strategic insights
                    - **Layout 2 (Analytical Deep Dive)**: Emphasize data exploration and detailed analysis
                    - **Layout 3 (Performance Command Center)**: Highlight real-time monitoring and alerts

                    **TECHNICAL REQUIREMENTS:**
                    - Use ALL available data with intelligent hierarchy
                    - Implement advanced CSS Grid and Flexbox layouts
                    - Create responsive designs with mobile-first approach
                    - Include interactive elements and data exploration features
                    - Maintain professional styling with consistent design language
                    - Ensure accessibility and performance optimization

                    **PERPLEXITY-INSPIRED FEATURES:**
                    - Clean, minimal aesthetic with strategic use of white space
                    - Intelligent information density without overwhelming users
                    - Contextual data relationships and insights
                    - Progressive disclosure of complex information
                    - Sophisticated yet intuitive navigation patterns

                    Focus on creating dashboards that feel like premium analytics platforms, with intelligent data presentation and sophisticated user experience design."""
                ),
            ]

            response = await structured_model.ainvoke(messages)

            state["layouts"] = response.layouts
            return state

        async def finalize_dashboard(
            state: AgentState,
        ) -> AgentState:
            """Finalize dashboard using Perplexity-style analytics approach."""
            structured_model = self.client.with_structured_output(Layout)

            messages = [
                SystemMessage(
                    """You are a senior product designer and full-stack developer specializing in PREMIUM ANALYTICS PLATFORMS like Perplexity Labs, Tableau, and modern data visualization tools. Your expertise is in creating production-ready, sophisticated dashboard experiences.

                    ## FINALIZATION METHODOLOGY: PERPLEXITY-STYLE ANALYTICS IMPLEMENTATION

                    ### 1. ADVANCED INTERFACE ARCHITECTURE
                    **Premium Dashboard Structure:**
                    
                    **HEADER INTELLIGENCE**:
                    - Brand identity with professional typography
                    - Real-time status indicators
                    - Global search and filtering capabilities
                    - User context and settings access
                    
                    **CONTENT ORCHESTRATION**:
                    - Intelligent grid system with varied component sizes
                    - Contextual sidebars with supporting information
                    - Progressive disclosure through expandable sections
                    - Coordinated views that respond to user interactions
                    
                    **NAVIGATION PATTERNS**:
                    - Breadcrumb navigation for complex data hierarchies
                    - Contextual actions and quick controls
                    - Smooth transitions between views
                    - Keyboard shortcuts for power users

                    ### 2. SOPHISTICATED STYLING IMPLEMENTATION
                    **Advanced CSS Architecture:**
                    
                    **DESIGN TOKENS & VARIABLES**:
                    ```css
                    /* Premium Color Palette */
                    --primary-50: #f0f9ff;
                    --primary-500: #3b82f6;
                    --primary-900: #1e3a8a;
                    --neutral-50: #fafafa;
                    --neutral-100: #f5f5f5;
                    --neutral-900: #0a0a0a;
                    
                    /* Data Visualization Colors */
                    --data-positive: #10b981;
                    --data-negative: #ef4444;
                    --data-warning: #f59e0b;
                    --data-info: #3b82f6;
                    
                    /* Spacing Scale */
                    --space-xs: 0.5rem;    /* 8px */
                    --space-sm: 0.75rem;   /* 12px */
                    --space-md: 1rem;      /* 16px */
                    --space-lg: 1.5rem;    /* 24px */
                    --space-xl: 2rem;      /* 32px */
                    --space-2xl: 3rem;     /* 48px */
                    
                    /* Typography Scale */
                    --text-xs: 0.75rem;    /* 12px */
                    --text-sm: 0.875rem;   /* 14px */
                    --text-base: 1rem;     /* 16px */
                    --text-lg: 1.125rem;   /* 18px */
                    --text-xl: 1.25rem;    /* 20px */
                    --text-2xl: 1.5rem;    /* 24px */
                    --text-3xl: 1.875rem;  /* 30px */
                    ```
                    
                    **ADVANCED LAYOUT PATTERNS**:
                    ```css
                    /* Intelligent Grid System */
                    .dashboard-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                        grid-auto-rows: minmax(200px, auto);
                        gap: var(--space-lg);
                        align-items: start;
                    }
                    
                    /* Asymmetric Layout */
                    .hero-metric { grid-column: span 2; grid-row: span 2; }
                    .secondary-metric { grid-column: span 1; grid-row: span 1; }
                    .chart-panel { grid-column: span 3; grid-row: span 2; }
                    
                    /* Responsive Breakpoints */
                    @media (max-width: 768px) {
                        .dashboard-grid {
                            grid-template-columns: 1fr;
                        }
                        .hero-metric,
                        .chart-panel {
                            grid-column: span 1;
                            grid-row: span 1;
                        }
                    }
                    ```

                    ### 3. PREMIUM COMPONENT IMPLEMENTATION
                    **High-Quality Component Design:**
                    
                    **METRIC CARDS with INTELLIGENCE**:
                    - Large primary value with semantic color coding
                    - Trend indicators with directional arrows
                    - Contextual comparison data (vs previous period)
                    - Micro-charts for visual context
                    - Interactive drill-down capabilities
                    
                    **CHART PANELS with SOPHISTICATION**:
                    - Professional data visualization with proper scales
                    - Interactive legends and data point tooltips
                    - Zoom and pan capabilities for detailed exploration
                    - Multiple chart types (line, bar, area, scatter)
                    - Export functionality for data sharing
                    
                    **DATA TABLES with ADVANCED FEATURES**:
                    - Smart column sizing and responsive behavior
                    - Advanced sorting and filtering controls
                    - Inline editing for data management
                    - Pagination with performance optimization
                    - Export options (CSV, PDF, Excel)
                    
                    **INSIGHT PANELS with AI-LIKE FEATURES**:
                    - Automated insight generation
                    - Anomaly detection and alerts
                    - Predictive analytics displays
                    - Recommendation systems
                    - Natural language summaries

                    ### 4. INTERACTIVE JAVASCRIPT IMPLEMENTATION
                    **Advanced Frontend Functionality:**
                    
                    **DATA BINDING & UPDATES**:
                    ```javascript
                    // Real-time data updates
                    class DashboardController {
                        constructor() {
                            this.data = {};
                            this.components = new Map();
                            this.filters = new Map();
                        }
                        
                        updateData(newData) {
                            this.data = { ...this.data, ...newData };
                            this.renderComponents();
                        }
                        
                        applyFilters(filters) {
                            this.filters = new Map([...this.filters, ...filters]);
                            this.renderComponents();
                        }
                    }
                    ```
                    
                    **INTERACTIVE FEATURES**:
                    - Cross-filtering between components
                    - Drill-down and drill-up navigation
                    - Time range selection with brush controls
                    - Dynamic data loading and caching
                    - Keyboard navigation support
                    
                    **PERFORMANCE OPTIMIZATION**:
                    - Virtual scrolling for large datasets
                    - Lazy loading of off-screen components
                    - Debounced search and filtering
                    - Efficient re-rendering strategies
                    - Memory management for long-running sessions

                    ### 5. ACCESSIBILITY & USABILITY
                    **Professional Standards:**
                    
                    **ACCESSIBILITY COMPLIANCE**:
                    - WCAG 2.1 AA compliance
                    - Screen reader optimization
                    - Keyboard navigation support
                    - High contrast mode support
                    - Focus management and skip links
                    
                    **USER EXPERIENCE OPTIMIZATION**:
                    - Loading states and progress indicators
                    - Error handling with helpful messages
                    - Responsive design for all devices
                    - Touch-friendly interactions
                    - Consistent interaction patterns

                    ### 6. PRODUCTION-READY IMPLEMENTATION
                    **Enterprise-Grade Code:**
                    
                    **CODE ORGANIZATION**:
                    - Modular component architecture
                    - Separation of concerns (HTML, CSS, JS)
                    - Consistent naming conventions
                    - Comprehensive error handling
                    - Performance monitoring hooks
                    
                    **DEPLOYMENT READINESS**:
                    - Self-contained iframe compatibility
                    - CDN-ready asset optimization
                    - Progressive enhancement
                    - Graceful degradation
                    - Cross-browser compatibility

                    ### OUTPUT REQUIREMENTS:
                    - **Premium Interface**: Sophisticated, professional dashboard design
                    - **Complete Implementation**: Full HTML, CSS, and JavaScript
                    - **Advanced Features**: Interactive elements and data exploration
                    - **Responsive Design**: Optimal experience across all devices
                    - **Production Quality**: Enterprise-ready code and implementation
                    - **Accessibility**: WCAG 2.1 AA compliance
                    - **Performance**: Optimized for fast loading and smooth interactions

                    Create a dashboard that rivals the best analytics platforms in terms of design sophistication, user experience, and technical implementation."""
                ),
                HumanMessage(
                    f"""Create the final PERPLEXITY-STYLE ANALYTICS DASHBOARD with premium implementation:

                    **SELECTED LAYOUT:** {state['selected_layout']}
                    **COMPONENT LIBRARY:** {state['ui_descriptor']}
                    **CSS DESIGN SYSTEM:** {state['design_system']}

                    **PREMIUM IMPLEMENTATION REQUIREMENTS:**
                    1. **Sophisticated Interface Design**: Create a dashboard that feels like a premium analytics platform
                    2. **Advanced Component Integration**: Use the component library to build complex, interactive elements
                    3. **Intelligent Data Presentation**: Present data with smart hierarchy and contextual insights
                    4. **Premium Styling**: Implement advanced CSS with sophisticated typography and spacing
                    5. **Interactive Features**: Add JavaScript functionality for data exploration and user interaction
                    6. **Responsive Excellence**: Ensure optimal experience across all devices and screen sizes

                    **PERPLEXITY-INSPIRED FEATURES:**
                    - **Clean Aesthetics**: Minimal design with strategic use of white space
                    - **Intelligent Information Architecture**: Smart data organization and progressive disclosure
                    - **Premium Typography**: Professional font hierarchy with excellent readability
                    - **Sophisticated Interactions**: Smooth animations and intuitive user flows
                    - **Data-Driven Insights**: Contextual information and intelligent data relationships

                    **TECHNICAL SPECIFICATIONS:**
                    - **Advanced CSS Grid**: Implement sophisticated, responsive grid systems
                    - **Component Mastery**: Use all available components with professional styling
                    - **Interactive JavaScript**: Create dynamic, data-driven functionality
                    - **Performance Optimization**: Ensure fast loading and smooth interactions
                    - **Accessibility Standards**: Maintain WCAG 2.1 AA compliance
                    - **Production Ready**: Enterprise-grade code suitable for deployment

                    **ANALYTICS PLATFORM FEATURES:**
                    - **Real-time Data Display**: Present data with live updates and status indicators
                    - **Advanced Filtering**: Implement sophisticated search and filter capabilities
                    - **Data Exploration**: Enable users to drill down and explore data relationships
                    - **Export Functionality**: Provide options for data sharing and export
                    - **Customization Options**: Allow users to personalize their dashboard experience

                    **FINAL OUTPUT:**
                    - Complete dashboard with premium design and functionality
                    - Comprehensive data integration with intelligent presentation
                    - Advanced interactive features for enhanced user experience
                    - Professional styling that rivals leading analytics platforms
                    - Production-ready code suitable for enterprise deployment
                    - Responsive design optimized for all devices and use cases

                    Focus on creating a dashboard that demonstrates mastery of modern analytics interface design, with the sophistication and polish of premium data visualization platforms."""
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
