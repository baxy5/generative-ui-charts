from fastapi import APIRouter

from services.appic import generate_ui
from models.appic import AppicRequestSchema


router = APIRouter(prefix="/appic", tags=["Appic"])


@router.post("/generate")
async def generate_appic(request: AppicRequestSchema):
    user_prompt = request.prompt
    response = generate_ui(user_prompt)
    return {"message": response}
