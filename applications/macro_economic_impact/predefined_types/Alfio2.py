from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any

class Alfio2(BaseModel):
    market_sentiment: str | None = Field(default=None, description='The general market sentiment for the day, e.g., Positive, Negative, Neutral.')
    market_sentiment_explanation: float | None = Field(default=None, description='Explain the main reason for the market sentiment judgment you just expressed.')
    relevant_factors: list[str] | None = Field(default=None, description='List the most relevant factors (e.g., economic indicators, geopolitical events) that influenced your market sentiment assessment.')
    relevant_news_selection: float | None = Field(default=None, description='List the specific news headlines that had a significant impact on your market sentiment evaluation.')