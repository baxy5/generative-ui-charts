from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from agents.iframe_component_agent import (
    IframeComponentRequestSchema,
    IframeComponentResponseSchema,
)
from services.iframe_component_service import IframeComponentService


router = APIRouter()


@router.post(
    "/generate",
    response_model=IframeComponentResponseSchema,
    description="Generate URL and Id for Iframe",
)
async def generate_iframe_component(
    request: IframeComponentRequestSchema,
    service: Annotated[IframeComponentService, Depends()],
):
    try:
        return await service.generate_iframe_component(request)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate URL and Id: {e}"
        )
