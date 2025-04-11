import logging

from fastapi import APIRouter

from core.gemini_integration import GeminiIntegration
from models import (
    DiscordBotRequest, 
    DiscordBotResponse, 
    InternalBotRequest, 
    Status
)


logger = logging.getLogger(__name__)

# Name of The Book "ness"
ness = GeminiIntegration()
router = APIRouter()


@router.post("/ask", response_model=DiscordBotResponse, status_code=200)
async def ask(request: DiscordBotRequest) -> DiscordBotResponse:
    logger.info("Received request: %s", request)

    internal_req = InternalBotRequest(**request.model_dump())

    try:
        response = await ness.generate_response(
            user_message=internal_req.user_message)
        logger.info("Response generated: %s", response)

        return DiscordBotResponse(
            request_id=internal_req.request_id,
            user_id=internal_req.user_id,
            bot_response=response,
            token_count=ness.token_count,
            status=Status.SUCCESS,
        )

    except Exception as e:
        logger.error("Error generating response: %s", str(e))
        return DiscordBotResponse(
            request_id=internal_req.request_id,
            user_id=internal_req.user_id,
            bot_response="",
            token_count=0,
            status=Status.FAILED,
            error_message=str(e),
        )


@router.post("/do")
async def do(request):
    return {"detail": "Did something"}