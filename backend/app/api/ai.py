from fastapi import APIRouter

from app.schemas.ai import (
    AIRequest,
    AIResponse,
)
from app.services.ai_service import AIService

router = APIRouter()


@router.post(
    "/chat",
    response_model=AIResponse,
)
async def chat(
    request: AIRequest,
):

    service = AIService()

    result = await service.chat(
        request.question
    )

    return AIResponse(
        response=result["response"],
        sources=result["sources"],
    )