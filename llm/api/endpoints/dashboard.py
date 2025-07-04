from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.dashboard.dashboard_final_service import DashboardFinalService
from services.dashboard.dashboard_layout_service import DashboardLayoutService
from schemas.dashboard_schema import (
    FinalRequestSchema,
    FinalResponseSchema,
    LayoutRequestSchema,
    LayoutResponseSchema,
)


router = APIRouter()


@router.post("/generate-layouts")
async def generate_layouts(
    request: LayoutRequestSchema, service: Annotated[DashboardLayoutService, Depends()]
) -> LayoutResponseSchema:
    request.phase = "layout"

    try:
        return await service.generate_layouts(request)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Layout api -> Failed to generate dashboard: {e}",
        )


@router.post("/generate-final")
async def generate_final_dashboard(
    request: FinalRequestSchema, service: Annotated[DashboardFinalService, Depends()]
) -> FinalResponseSchema:
    request.phase = "final"

    try:
        return await service.generate_final(request)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Final api -> Failed to generate dashboard: {e}"
        )
