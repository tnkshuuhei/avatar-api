"""
Personality package initialization.
Imports all personality classes for easy access.
"""
from src.services.personalities.base import BasePersonality
from src.services.personalities.sustain_focus import SustainFocusPersonality
from src.services.personalities.equity_max import EquityMaxPersonality
from src.services.personalities.community_centric import CommunityCentricPersonality
from src.services.personalities.innovation_engine import InnovationEnginePersonality
from src.services.personalities.efficient_alloc import EfficientAllocPersonality

# Dictionary mapping personality IDs to their respective classes
PERSONALITY_CLASSES = {
    "sustain-focus": SustainFocusPersonality,
    "equity-max": EquityMaxPersonality,
    "community-centric": CommunityCentricPersonality,
    "innovation-engine": InnovationEnginePersonality,
    "efficient-alloc": EfficientAllocPersonality,
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
