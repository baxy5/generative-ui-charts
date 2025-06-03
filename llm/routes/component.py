from fastapi import APIRouter

from models.component import ComponentRequestSchema
from services.component import generate_ui


router = APIRouter(prefix="/component", tags=["Component Generation"])


@router.post("/generate")
async def generate_component(request: ComponentRequestSchema):
    user_prompt = request.prompt
    response = generate_ui(user_prompt)
    return {"message": response}
