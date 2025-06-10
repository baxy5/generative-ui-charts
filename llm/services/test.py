from typing import Annotated
from fastapi import Depends, HTTPException
from agents.test import (
    UiComponentAgent,
    UiComponentRequestSchema,
    UiComponentResponseSchema,
)


class UiComponentService:
    """Service for interacting with the UiComponent Agent."""

    def __init__(self, agent: Annotated[UiComponentAgent, Depends()]):
        self.agent = agent

    async def generate_ui_component(
        self, request: UiComponentRequestSchema
    ) -> UiComponentResponseSchema:
        """Generate a UI component based on the user's request."""
        try:
            component_response = await self.agent.generate_ui_component(
                question=request.prompt
            )
            return component_response
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error while generating component: {e}"
            )
