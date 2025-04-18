"""Contains Models"""

from enum import Enum
from typing import Any
from uuid import uuid4, UUID
from pydantic import BaseModel, PrivateAttr

__all__ = ["Priority"]


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(BaseModel):
    _id: UUID = PrivateAttr(default_factory=uuid4)
    function_name: str
    arguments: Any | None
    priority: Priority = Priority.MEDIUM

    @property
    def id(self) -> UUID:
        return self._id