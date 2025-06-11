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
            messages = [
                SystemMessage(
                    """You are a specialized React developer skilled at creating UI components.
                       Your task is to create a React component based on the provided data and UI component descriptor.
                       
                       IMPORTANT RESTRICTION: The component MUST ONLY include ONE import statement:
                        - ONLY use: "import React from 'react';"
                        - DO NOT import any other libraries, components, hooks, or utilities
                        - DO NOT use any external dependencies
                        - All functionality must be self-contained within the component
                        
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
        graph.add_node("component_descriptor", component_descriptor)
        graph.add_node("final_component_generation", final_component_generation)

        # Define edges between nodes
        graph.set_entry_point("extract_data")
        graph.add_edge("extract_data", "component_descriptor")
        graph.add_edge("component_descriptor", "final_component_generation")
        graph.add_edge("final_component_generation", END)

        return graph.compile(checkpointer=self.checkpoint_saver)

    async def generate_ui_component(
        self, question: str, data: str, component_descriptors: json
    ) -> UiComponentResponseSchema:
        """Generate UI component based on the user's question and the data."""

        initial_state: AgentState = {
            "question": question,
            "provided_data": data,
            "component_descriptors": component_descriptors,
        }
        config = RunnableConfig(configurable={"thread_id": "1"})

        result = await self.graph.ainvoke(initial_state, config=config)

        if "final_component" in result and result["final_component"] is not None:
            return result["final_component"]

        return UiComponentResponseSchema(
            name="Failed", component="Failed to generate component."
        )
