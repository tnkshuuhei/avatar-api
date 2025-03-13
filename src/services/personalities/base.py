"""
Base personality class that all specific personalities will inherit from.
"""
from typing import List, Dict, Any
from langchain.prompts import PromptTemplate


class BasePersonality:
    """Base class for AI personalities."""

    id: str = "base"
    name: str = "Base Personality"
    tags: List[str] = []

    @classmethod
    def get_system_prompt(cls) -> str:
        """Get the system prompt template for this personality."""
        return """<instructions>
You are an AI assistant that answers questions based on specific document knowledge.
</instructions>

<context>
{context}
</context>

<guidelines>
1. Respond in the same language as the question
2. Use the information provided in the context to answer questions
3. If the answer is not contained in the context, acknowledge the limitations of your knowledge
4. Provide clear, concise answers
5. Use a professional but friendly tone
</guidelines>

<question>{question}</question>
"""

    @classmethod
    def get_prompt_template(cls) -> PromptTemplate:
        """Get the prompt template configured for this personality."""
        return PromptTemplate(
            template=cls.get_system_prompt(), input_variables=["context", "question"]
        )

    @classmethod
    def get_info(cls) -> Dict[str, Any]:
        """Get basic information about this personality."""
        return {
            "id": cls.id,
            "name": cls.name,
            "tags": cls.tags,
        }
