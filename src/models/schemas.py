"""
Pydantic models for API request and response validation.
"""
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
    personality_id: Optional[str] = Field(
        None, description="The ID of the personality that generated the answer"
    )


class HealthCheck(BaseModel):
    status: str = "ok"
    version: str


class PersonalityTag(BaseModel):
    name: str = Field(..., description="The name of the tag")


class PersonalityInfo(BaseModel):
    id: str = Field(..., description="The unique identifier for the personality")
    name: str = Field(..., description="The display name of the personality")
    tags: List[str] = Field(
        default_factory=list,
        description="Tags describing the personality's focus areas",
    )
    description: Optional[str] = Field(
        None, description="A detailed description of the personality"
    )
