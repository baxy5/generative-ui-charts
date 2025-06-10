from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from agents.test import UiComponentRequestSchema, UiComponentResponseSchema
from services.test import UiComponentService


router = APIRouter()


@router.post(
    "/generate",
    response_model=UiComponentResponseSchema,
    summary="Generate UI Component",
    description="Generate a React component based on the provided prompt. Returns the component name and code.",
)
async def generate_ui_component(
    request: UiComponentRequestSchema, service: Annotated[UiComponentService, Depends()]
):
    try:
        return await service.generate_ui_component(request)
    except HTTPException as e:
        # Re-raise HTTP exceptions from the service layer
        raise e
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {str(e)}"
        )
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate component: {str(e)}",
        )
