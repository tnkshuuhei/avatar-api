"""
Personality manager to handle access to different AI personalities.
Acts as a facade for the personality system.
"""
from typing import Dict, Any, List, Optional, Type
from langchain.prompts import PromptTemplate

from src.services.personalities import BasePersonality, PERSONALITY_CLASSES


def get_personality_prompt(personality_id: str) -> PromptTemplate:
    """
    Get the prompt template for a specific personality.

    Args:
        personality_id: The ID of the personality

    Returns:
        A PromptTemplate configured for the personality
    """
    personality_class = _get_personality_class(personality_id)
    return personality_class.get_prompt_template()


def get_default_prompt() -> PromptTemplate:
    """Get a default prompt template"""
    return BasePersonality.get_prompt_template()


def get_personality_info(personality_id: str) -> Dict[str, Any]:
    """
    Get information about a specific personality.

    Args:
        personality_id: The ID of the personality

    Returns:
        Dictionary with personality information
    """
    personality_class = _get_personality_class(personality_id)
    return personality_class.get_info()


def list_personalities() -> List[Dict[str, Any]]:
    """
    List all available personalities.

    Returns:
        List of personality information dictionaries
    """
    return [cls.get_info() for cls in PERSONALITY_CLASSES.values()]


def get_model_name(personality_id: str) -> str:
    """
    Get the recommended model name for a personality.

    Args:
        personality_id: The ID of the personality

    Returns:
        Model name string
    """
    personality_class = _get_personality_class(personality_id)
    return personality_class.model_name


def get_temperature(personality_id: str) -> float:
    """
    Get the recommended temperature setting for a personality.

    Args:
        personality_id: The ID of the personality

    Returns:
        Temperature value
    """
    personality_class = _get_personality_class(personality_id)
    return personality_class.temperature


def _get_personality_class(personality_id: str) -> Type[BasePersonality]:
    """
    Get the personality class for a given ID.

    Args:
        personality_id: The ID of the personality

    Returns:
        Personality class
    """
    return PERSONALITY_CLASSES.get(personality_id, BasePersonality)
