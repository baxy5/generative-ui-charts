import json
from typing import Annotated, Any, List, Optional, TypedDict
from fastapi import Depends, HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from langgraph.graph.graph import CompiledGraph
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables.config import RunnableConfig
from core.common import get_gpt_client


class ComponentRequestSchema(BaseModel):
    prompt: str


class ComponentResponseSchema(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the component.")
    component: Optional[str] = Field(default=None, description="Component code.")


class Component(BaseModel):
    """Component description"""

    type: str
    description: str
    htmlTags: List[str]
    style: str


class AgentState(TypedDict):
    """State used by the agent through the workflow"""

    question: str
    data: str
    components: List[Component]
    analyzedData: str
    builtComponent: str
    final_response: Optional[ComponentResponseSchema]


DEFAULT_COMPONENTS = [
    Component(
        type="Card",
        description="This is a card component for displaying important details.",
        htmlTags=["h1", "h2", "p", "span", "ul", "li"],
        style="w-full max-w-[281px] h-36 flex flex-col items-start p-4 gap-1 bg-white border border-[#99C1C1] backdrop-blur-[100px] rounded-2xl box-border",
    ),
    Component(
        type="MetricBox",
        description="A box component for displaying key medical metrics with percentage changes. Useful for showing vital signs, lab results, or treatment progress with trend indicators.",
        htmlTags=["div", "span", "p", "h3", "svg"],
        style="w-full max-w-[300px] p-4 bg-card-light rounded-lg border border-gray-200 shadow-sm flex flex-col gap-2",
    ),
    Component(
        type="AlertBox",
        description="A prominent alert component for displaying critical medical information, warnings, or important notices. Ideal for abnormal results, medication alerts, or emergency information.",
        htmlTags=["div", "p", "span", "svg", "button"],
        style="w-full p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3",
    ),
    Component(
        type="TimelineCard",
        description="A timeline component for displaying medical history, treatment progress, or test results chronologically. Perfect for showing patient history or treatment milestones.",
        htmlTags=["div", "ul", "li", "span", "p", "time"],
        style="w-full max-w-[400px] p-4 bg-card-medium rounded-lg border border-gray-200",
    ),
    Component(
        type="ComparisonBox",
        description="A component for comparing two sets of medical data side by side. Useful for showing before/after results, normal vs abnormal values, or different time periods.",
        htmlTags=["div", "table", "tr", "td", "th", "span"],
        style="w-full max-w-[500px] p-4 bg-card-dark rounded-lg border border-gray-200",
    ),
    Component(
        type="StatusIndicator",
        description="A compact component for displaying patient status, test results, or treatment progress with visual indicators. Great for quick status overviews in dashboards.",
        htmlTags=["div", "span", "p", "svg"],
        style="w-full max-w-[200px] p-3 bg-card-light rounded-lg border border-gray-200 flex items-center gap-2",
    ),
]


class ComponentAgent:
    """Agent for generating UI components."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]):
        self.client = client
        self.checkpoint_saver = InMemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self) -> CompiledGraph:
        """Build the langgraph workflow for component generation"""

        # Initialize the graph
        graph = StateGraph(AgentState)

        async def analyze_data(state: AgentState):
            """1. Node of Component Agent Graph

            Extracting data for the user question.
            """
            messages = [
                SystemMessage(
                    f"""You are an AI assistant specialized in data analysis. Your task is to analyze 
                    the provided data based on the user's question and extract all the information that answers it.
                    Return only the extracted information, without any extra text or explanations.
                    Analyze the provided data and question carefully.
                    Provide a clear rationale for your choices.
                    """
                ),
                HumanMessage(
                    f"""
                             Question: {state["question"]}
                             
                             The provided data: {state["data"]}
                             """
                ),
            ]
            response = await self.client.ainvoke(messages)

            try:
                state["analyzedData"] = response.content
                return state
            except Exception as e:
                # TODO: Fallback invoke with more precise instructions
                raise HTTPException(
                    status_code=500, detail="Failed to analyze data and generate plan."
                )

        async def component_plan(state: AgentState):
            """2. Node of Component Agent Graph

            Fill the data with one of the prebuilt component.
            """
            messages = [
                SystemMessage(
                    f"""You are an AI assistant specialized creating UI 
                        component from the user's question and the provided analyzed data.
                        You have to choose from the predefined UI components which can be filled with the data.
                        """
                ),
                HumanMessage(
                    f"""Analyzed data which you have to use to fill the component(s): {state["analyzedData"]}
                        
                        Predefined UI components: {state['components']}"""
                ),
            ]
            response = await self.client.ainvoke(messages)

            try:
                state["builtComponent"] = response.content
                return state
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to combine prebuilt component with data.",
                )

        async def generate(state: AgentState) -> ComponentResponseSchema:
            """3. Node of Component Agent Graph

            Generate final response component.
            """
            structured_output_model = self.client.with_structured_output(
                ComponentResponseSchema
            )
            messages = [
                SystemMessage(
                    f"""You are a specialized front end developer. Your task is to create one React component 
                                      from the already built components. You have to provided a name and the component code as a response.
                                      The React code's must have an "export default [componentName]" at the end.
                                      """
                ),
                HumanMessage(
                    f"Create a React component which can be rendered, from these components: {state['builtComponent']}"
                ),
            ]
            response = await structured_output_model.ainvoke(messages)

            try:
                state["final_response"] = response
                return state
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to finalize component generation. {response}",
                )

        # Add nodes to the graph
        graph.add_node("analyze_data", analyze_data)
        graph.add_node("component_plan", component_plan)
        graph.add_node("generate", generate)

        # Define edges between nodes
        graph.set_entry_point("analyze_data")
        graph.add_edge("analyze_data", "component_plan")
        graph.add_edge("component_plan", "generate")
        graph.add_edge("generate", END)

        return graph.compile(checkpointer=self.checkpoint_saver)

    async def generate_ui_component(
        self, question: str, data: Any | dict
    ) -> ComponentResponseSchema:
        """Generate UI component based on the user's question and the data."""

        initial_state: AgentState = {
            "question": question,
            "data": json.dumps(data),
            "components": DEFAULT_COMPONENTS,
        }
        config = RunnableConfig(configurable={"thread_id": "1"})

        result = await self.graph.ainvoke(initial_state, config=config)

        if "final_response" in result and result["final_response"] is not None:
            return result["final_response"]

        return ComponentResponseSchema(
            name="", component="Failed to generate component."
        )
