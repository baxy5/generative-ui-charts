from typing import Annotated
from fastapi import APIRouter, Depends
from agents.dashboard_agent import DashboardRequestSchema, DashboardResponseSchema
from services.dashboard_service import DashboardService


router = APIRouter()


@router.post("/generate-layouts")
async def generate_layouts(
    request: DashboardRequestSchema, service: Annotated[DashboardService, Depends()]
) -> DashboardResponseSchema:
    request.phase = "generate_layouts"
    return await service.generate_dashboard(request)


@router.post("/generate-final")
async def generate_final_dashboard(
    request: DashboardRequestSchema, service: Annotated[DashboardService, Depends()]
) -> DashboardResponseSchema:
    request.phase = "finalize_dashboard"
    return await service.generate_dashboard(request)
