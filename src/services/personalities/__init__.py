"""
Personality package initialization.
Imports all personality classes for easy access.
"""
from src.services.personalities.base import BasePersonality
from src.services.personalities.sustainability import SustainFocusPersonality
from src.services.personalities.equity import EquityMaxPersonality
from src.services.personalities.community import CommunityCentricPersonality
from src.services.personalities.innovation import InnovationEnginePersonality
from src.services.personalities.efficiency import EfficientAllocPersonality

# Dictionary mapping personality IDs to their respective classes
PERSONALITY_CLASSES = {
    "sustainability": SustainFocusPersonality,
    "equity": EquityMaxPersonality,
    "community": CommunityCentricPersonality,
    "innovation": InnovationEnginePersonality,
    "efficiency": EfficientAllocPersonality,
}

__all__ = [
    "BasePersonality",
    "SustainFocusPersonality",
    "EquityMaxPersonality",
    "CommunityCentricPersonality",
    "InnovationEnginePersonality",
    "EfficientAllocPersonality",
    "PERSONALITY_CLASSES",
]
