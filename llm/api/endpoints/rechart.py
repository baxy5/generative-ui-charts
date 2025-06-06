from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from agents.rechart_agent import RechartRequestSchema, RechartResponseSchema
from services.rechart_service import RechartService

router = APIRouter()


@router.post(
    "/generate",
    response_model=RechartResponseSchema,
    summary="Generate Rechart graph component.",
    description="Generate dynamic Rechart component for user's question from the medical data.",
)
async def generate_rechart(
    request: RechartRequestSchema, service: Annotated[RechartService, Depends()]
) -> RechartResponseSchema:
    try:
        response = await service.generate_rechart(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate rechart component. {e}"
        )
