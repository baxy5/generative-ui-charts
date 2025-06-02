from fastapi import APIRouter
from services.rechart import generate_ui
from models.rechart import RechartRequestSchema

router = APIRouter(prefix="/rechart", tags=["Chart Generation"])

@router.post("/generate")
async def generate_rechart(request: RechartRequestSchema):
    user_prompt = request.prompt
    response = generate_ui(user_prompt)
    return {"message": response}
