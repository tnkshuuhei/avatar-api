from pydantic import BaseModel, Field
from typing import Optional, List


class Question(BaseModel):
    text: str = Field(..., description="The question text from the user")
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    session_id: Optional[str] = Field(
        None, description="Optional session identifier for conversation tracking"
    )
    context: Optional[List[str]] = Field(
        None, description="Optional previous conversation context"
    )


class Answer(BaseModel):
    text: str = Field(..., description="The answer text from the AI agent")
    confidence: Optional[float] = Field(
        None, description="Optional confidence score of the answer"
    )
    sources: Optional[List[str]] = Field(
        None, description="Optional sources used to generate the answer"
    )


class HealthCheck(BaseModel):
    status: str = "ok"
    version: str
