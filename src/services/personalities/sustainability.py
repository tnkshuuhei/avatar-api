"""
SustainFocus personality: Specialist in sustainability and long-term thinking.
"""
from src.services.personalities.base import BasePersonality


class SustainFocusPersonality(BasePersonality):
    """SustainFocus personality class."""

    id = "sustainability"
    name = "SustainFocus"
    tags = [
        "Sustainability Metrics",
        "Long-term Impact Projection",
        "Governance Structure Analysis",
        "Community Participation Scorer",
    ]