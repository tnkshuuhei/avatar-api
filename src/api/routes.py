from fastapi import APIRouter, Depends, HTTPException
from src.models.schemas import Question, Answer, HealthCheck
from src.services.ai_agent import AIAgent
import time

router = APIRouter()

# Create a single instance of AIAgent to be reused
ai_agent = AIAgent()


@router.get("/")
async def root():
    return {"message": "Hello World!"}


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint to verify the API is running."""
    return HealthCheck(version="1.0.0")


@router.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    """
    Process a question and return an answer from the AI agent.

    This endpoint receives a question from the frontend and passes it to the AI agent
    that was trained on PDF documents. It returns the answer along with optional
    metadata like confidence score and sources.
    """
    try:
        # Measure response time for performance monitoring
        start_time = time.time()

        # Get answer from AI agent
        answer_text, sources = ai_agent.ask(question.text, question.context)

        # Calculate response time
        response_time = time.time() - start_time
        print(f"Response time: {response_time:.2f} seconds")

        # Return the answer
        return Answer(text=answer_text, sources=sources)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing question: {str(e)}"
        )


@router.post("/reset")
async def reset_conversation():
    """Reset the conversation history for the AI agent."""
    try:
        ai_agent.reset_conversation()
        return {"status": "success", "message": "Conversation reset successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error resetting conversation: {str(e)}"
        )
