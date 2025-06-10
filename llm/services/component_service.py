from typing import Annotated
from fastapi import Depends, HTTPException
from core.common import get_data
from agents.component_agent import (
    ComponentAgent,
    ComponentRequestSchema,
    ComponentResponseSchema,
)


class ComponentService:
    """Service for interacting with the component Agent."""

    def __init__(self, agent: Annotated[ComponentAgent, Depends()]):
        self.data_path = "mock-data/response_1748851964185.json"
        self.agent = agent

    async def generate_ui_component(
        self, request: ComponentRequestSchema
    ) -> ComponentResponseSchema:
        try:
            data = get_data(self.data_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading data: {e}")

        try:
            component_response = await self.agent.generate_ui_component(
                question=request.prompt, data=data
            )
            return component_response
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error while generating component: {e}"
            )
