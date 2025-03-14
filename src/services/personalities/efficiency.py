"""
EfficientAlloc personality: Specialist in efficiency and return on investment.
Incorporates model spec loaded from file.
"""
from src.services.personalities.base import BasePersonality


class EfficientAllocPersonality(BasePersonality):
    """EfficientAlloc personality class with dynamic model spec loading."""

    id = "efficiency"
    name = "EfficientAlloc"
    tags = [
        "ROI Calculator",
        "Resource Optimization",
        "Scalability Predictor",
        "Cost-Benefit Analyzer",
    ]
