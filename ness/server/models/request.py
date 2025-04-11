from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from .staticModels import Status


class DiscordBotRequest(BaseModel):
    """Incoming message from a Discord user (processed by bot)"""

    # User Info
    user_id: str = Field(..., description="Discord user ID")
    username: str = Field(..., description="Discord username")

    # Discord Message Metadata
    guild_id: str = Field(..., description="Guild (server) ID")
    channel_id: str = Field(..., description="Channel ID")
    message_id: str = Field(..., description="Message ID")
    user_message: str = Field(..., description="Raw message content from user")
    timestamp: datetime = Field(..., description="Message timestamp")

    # Processing Metadata
    status: Status = Field(
        default=Status.PENDING, description="Request processing status"
    )
    prompt_type: str = Field(..., description="Type of prompt to use")


class InternalBotRequest(DiscordBotRequest):
    """Internal representation of a Discord bot request"""

    request_id: UUID = Field(
        default_factory=uuid4, description="Unique UUID for this request"
    )
    class Config:
        extra = "ignore"  # ignore extra fields not defined in the model
