"""
InnovationEngine personality: Specialist in innovative approaches and creative solutions.
"""
from src.services.personalities.base import BasePersonality


class InnovationEnginePersonality(BasePersonality):
    """InnovationEngine personality class."""

    id = "innovation"
    name = "InnovationEngine"
    tags = [
        "Breakthrough Solution Design",
        "Technology Integration",
        "Adaptive Systems Thinking",
        "Future Trends Analysis",
    ]
