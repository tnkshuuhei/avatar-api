"""
CommunityCentric personality: Specialist in community-based approaches.
Imports model spec from file.
"""
from src.services.personalities.base import BasePersonality


class CommunityCentricPersonality(BasePersonality):
    """CommunityCentric personality class with dynamic model spec loading."""

    id = "community"
    name = "CommunityCentric"
    tags = [
        "Community Engagement Frameworks",
        "Participatory Decision Models",
        "Social Capital Building",
        "Local Knowledge Integration",
    ]