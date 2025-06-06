from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from agents.component_agent import ComponentRequestSchema, ComponentResponseSchema
from services.component_service import ComponentService

router = APIRouter()


@router.post(
    "/generate",
    response_model=ComponentResponseSchema,
    summary="Generate React component",
    description="Generate dynamic UI component for user's question from the medical data.",
)
async def generate_component(
    request: ComponentRequestSchema, service: Annotated[ComponentService, Depends()]
):
    try:
        component_response = await service.generate_ui_component(request)
        return component_response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate component: {e}"
        )
