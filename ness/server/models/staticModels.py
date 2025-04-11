from enum import Enum

__all__ = [
    "Status",
    "PromptType"
]

class Status(str, Enum):
    PENDING: str = "pending"
    IN_PROGRESS: str = "in_progress"
    COMPLETED: str = "completed"
    FAILED: str = "failed"
    CANCELLED: str = "cancelled"
    SUCCESS: str = "success"
    ERROR: str = "error"


class PromptType(str, Enum):
    SUMMARIZE: str = "summarize"
    EXPLAIN: str = "explain"
    ANALYZE: str = "analyze"
    DISCUSS: str = "discuss"
    DEBATE: str = "debate"
    GENERATE: str = "generate"
    REWRITE: str = "rewrite"
    CLARIFY: str = "clarify"
    