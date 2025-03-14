"""
EquityMax personality: Specialist in equity and fairness considerations.
"""

from src.services.personalities.base import BasePersonality


class EquityMaxPersonality(BasePersonality):
    """EquityMax personality class."""

    id = "equity"
    name = "EquityMax"
    tags = [
        "Population Impact Analysis",
        "Geographic Equity Weighting",
        "Underserved Population Targeting",
        "Community Input Interpreter",
    ]
