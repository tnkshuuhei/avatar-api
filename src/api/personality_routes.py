"""
API routes for personality-specific endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional

from src.models.schemas import Question, Answer, PersonalityInfo
from src.services.ai_agent import AIAgent
from src.services.personality_manager import list_personalities, get_personality_info

# Create router
router = APIRouter(prefix="/personalities", tags=["personalities"])

# Dictionary to store AI agent instances for each personality and user
personality_agents: Dict[str, Dict[str, AIAgent]] = {}


def get_agent_for_user(personality_id: str, user_id: str = "default") -> AIAgent:
    """
    Get or create an AI agent for a specific personality and user.

    Args:
        personality_id: The personality ID
        user_id: The user ID

    Returns:
        An AIAgent instance
    """
    # Initialize the dictionary for this personality if it doesn't exist
    if personality_id not in personality_agents:
        personality_agents[personality_id] = {}

    # Create a new agent for this user if one doesn't exist
    if user_id not in personality_agents[personality_id]:
        personality_agents[personality_id][user_id] = AIAgent(
            personality_id=personality_id
        )

    return personality_agents[personality_id][user_id]


@router.get("/", response_model=List[PersonalityInfo])
async def get_all_personalities():
    """
    Get a list of all available AI personalities.

    Returns:
        List of personality information
    """
    return list_personalities()


@router.get("/{personality_id}", response_model=PersonalityInfo)
async def get_personality(personality_id: str):
    """
    Get information about a specific AI personality.

    Args:
        personality_id: The ID of the personality to retrieve

    Returns:
        Personality information
    """
    personality = get_personality_info(personality_id)
    if not personality:
        raise HTTPException(
            status_code=404, detail=f"Personality '{personality_id}' not found"
        )

    personality["id"] = personality_id
    return personality


@router.post("/{personality_id}/ask", response_model=Answer)
async def ask_personality_question(personality_id: str, question: Question):
    """
    Ask a question to a specific AI personality.

    Args:
        personality_id: The ID of the personality to ask
        question: The question data

    Returns:
        The AI's answer
    """
    try:
        # Get or create an agent for this personality and user
        agent = get_agent_for_user(
            personality_id=personality_id, user_id=question.user_id or "default"
        )

        # Get the answer
        answer_text, sources = agent.ask(question.text)

        # Return the formatted answer
        return Answer(text=answer_text, sources=sources, personality_id=personality_id)
    except Exception as e:
        # Handle errors
        error_msg = str(e)
        if "overloaded" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail="The AI service is currently overloaded. Please try again in a few minutes.",
            )
        raise HTTPException(
            status_code=500, detail=f"Error processing question: {error_msg}"
        )


@router.post("/{personality_id}/reset")
async def reset_personality_conversation(
    personality_id: str, user_id: Optional[str] = None
):
    """
    Reset the conversation history for a specific personality.

    Args:
        personality_id: The ID of the personality
        user_id: Optional user ID (defaults to 'default')

    Returns:
        Success message
    """
    user_id = user_id or "default"

    # Check if there's an agent for this personality and user
    if (
        personality_id in personality_agents
        and user_id in personality_agents[personality_id]
    ):
        # Reset the conversation
        personality_agents[personality_id][user_id].reset_conversation()

    return {"status": "success", "message": "Conversation reset successfully"}
