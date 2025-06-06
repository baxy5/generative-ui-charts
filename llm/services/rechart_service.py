from typing import Annotated
from fastapi import Depends, HTTPException
from agents.rechart_agent import (
    RechartAgent,
    RechartRequestSchema,
    RechartResponseSchema,
)
from core.common import get_data


class RechartService:
    """Service for interacting with the Rechart agent."""

    def __init__(self, agent: Annotated[RechartAgent, Depends()]):
        self.data_path = "mock-data/response_1748851964185.json"
        self.agent = agent

    async def generate_rechart(
        self, request: RechartRequestSchema
    ) -> RechartResponseSchema:
        try:
            data = get_data(self.data_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load data: {e}")

        try:
            rechart_response = await self.agent.generate_ui_rechart(
                request=request, data=data
            )
            return rechart_response
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error while generating Rechart component."
            )
