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

            system_message = """You are an expert web developer specializing in creating interactive dashboards and components that will be embedded in iframes. Your task is to generate complete, self-contained web components with HTML, CSS, and JavaScript.

            ## CRITICAL REQUIREMENTS:

            ### 2. HTML REQUIREMENTS:
            - Generate ONLY the content that goes inside the <body> tag
            - Use semantic HTML5 elements (section, article, header, etc.)
            - Include proper ARIA labels for accessibility
            - Use data attributes for JavaScript targeting (data-component, data-value, etc.)
            - Create responsive layouts using CSS Grid or Flexbox
            - Include loading states and error handling elements

            ### 3. CSS REQUIREMENTS:
            - Write modern, responsive CSS
            - Use CSS Grid and Flexbox for layouts
            - Include hover effects and smooth transitions
            - Support both light and dark themes
            - Use CSS custom properties (variables) for consistency
            - Make components responsive (mobile-first approach)
            - Include print styles if relevant
            - Scope styles to avoid conflicts (use specific class names)

            ### 4. JAVASCRIPT REQUIREMENTS:
            - Write vanilla JavaScript (no external libraries unless specified)
            - Include proper error handling with try-catch blocks
            - Implement responsive behavior
            - Add interactive features (click, hover, animations)
            - Include data update functionality
            - Implement proper event listeners with cleanup
            - Add iframe communication capabilities
            - Include performance optimizations (debouncing, throttling)
            - Make code modular and well-commented

            ### 5. COMPONENT TYPES TO SUPPORT:

            **DASHBOARD**: Multi-widget layouts with metrics, charts, and KPIs
            **METRICS**: Key performance indicators with visual emphasis
            **CHART**: Data visualizations (bar, line, pie, scatter plots)
            **TABLE**: Interactive data tables with sorting, filtering, pagination
            **FORM**: Interactive forms with validation and submission
            **TIMELINE**: Event timelines and progress indicators
            **MAP**: Location-based visualizations
            **CALENDAR**: Date/time based components

            ### 6. STYLING GUIDELINES:
            - Use a consistent color palette
            - Implement proper typography hierarchy
            - Include loading animations and micro-interactions
            - Support accessibility (WCAG 2.1 AA compliance)
            - Use modern CSS features (Grid, Flexbox, Custom Properties)
            - Include responsive breakpoints: mobile (320px+), tablet (768px+), desktop (1024px+)

            ### 7. DATA HANDLING:
            - Accept data through a global `window.componentData` object
            - Implement data validation and error handling
            - Support real-time data updates
            - Handle empty states and loading states
            - Include data formatting utilities

            ### 8. PERFORMANCE:
            - Optimize for fast rendering
            - Use efficient DOM manipulation
            - Implement virtual scrolling for large datasets
            - Include lazy loading for images and heavy content
            - Minimize reflows and repaints

            ### 9. SECURITY:
            - Sanitize any user input
            - Avoid inline event handlers
            - Use proper escaping for dynamic content
            - Implement CSP-compatible code

            Remember: The generated component will be loaded in a sandboxed iframe, so it must be completely self-contained and secure."""

            human_message = f"""Generate a professional web component based on the following requirements:
                                User's prompt: {state['question']}
                                
                                Provided data: {state['data']}
                                
                                ## SPECIFIC REQUIREMENTS:

                                ### Data Presentation:
                                - Highlight the most important metrics prominently
                                - Use appropriate chart types for the data relationships
                                - Include comparative elements (previous period, benchmarks, targets)
                                - Show data trends and patterns clearly

                                ### User Experience:
                                - Implement smooth transitions and hover effects
                                - Add tooltips for detailed information
                                - Include interactive filtering/sorting where applicable
                                - Provide clear visual hierarchy

                                ### Technical Implementation:
                                - Ensure component auto-resizes based on content
                                - Implement proper error handling for missing data
                                - Include loading states during data updates
                                - Make component keyboard accessible

                                ### Visual Design:
                                - Use professional typography and spacing
                                - Implement consistent visual patterns
                                - Include appropriate icons and visual elements
                                - Ensure readability across different screen sizes

                                ## EXAMPLE DATA STRUCTURE HANDLING:
                                If the data contains:
                                - **Metrics**: Display as KPI cards with trend indicators
                                - **Time Series**: Create line/area charts with zoom capabilities
                                - **Categories**: Use bar charts, pie charts, or treemaps
                                - **Comparisons**: Implement side-by-side comparisons or overlays
                                - **Geographic**: Consider map visualizations if location data exists
                                - **Hierarchical**: Use nested layouts or drill-down capabilities

                                Make the component visually appealing, highly functional, and optimized for the iframe embedding approach.
                                """

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
        self, question: str, data: str
    ) -> AgentResponseSchema:
        """Generate page_title, HTML, CSS and JS code."""

        initial_state: AgentState = {
            "question": question,
            "data": data,
        }

        config = RunnableConfig(configurable={"thread_id": "1"})

        result = await self.graph.ainvoke(initial_state, config=config)

        if "result" in result and result["result"] is not None:
            return result["result"]
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to generate components for Iframe."
            )
