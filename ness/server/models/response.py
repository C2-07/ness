from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional
from .staticModels import Status

class DiscordBotResponse(BaseModel):
    """Bot's response to a Discord message"""
    
    response_id: UUID = Field(default_factory=uuid4, description="Unique UUID for this response")
    
    # Link to Original Request
    request_id: UUID = Field(..., description="UUID of the original request")
    user_id: str = Field(..., description="Discord user ID")
    
    # Bot Response Info
    bot_response: str = Field(..., description="Bot's reply message")
    token_count: int = Field(..., description="Total tokens used for response")
    
    # Optional Debug Info
    model_used: Optional[str] = Field(None, description="LLM model used to generate the response")
    latency_ms: Optional[int] = Field(None, description="Time taken to generate the response in ms")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp of response generation")
    status: Status = Field(default=Status.SUCCESS, description="Processing status of the response")
    error_message: Optional[str] = Field(None, description="Error message if any error occurred")
    