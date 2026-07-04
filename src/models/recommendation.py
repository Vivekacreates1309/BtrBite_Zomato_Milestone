from pydantic import BaseModel, Field
from typing import List
from .restaurant import Restaurant

class LLMRecommendationItem(BaseModel):
    id: str = Field(description="The restaurant ID")
    explanation: str = Field(description="Why this restaurant is recommended based on the user's preferences")
    rank: int = Field(description="Rank of the restaurant among the candidates")

class LLMRecommendationResponse(BaseModel):
    recommendations: List[LLMRecommendationItem]

class RecommendationResponse(Restaurant):
    explanation: str = Field(description="AI generated explanation for this recommendation")
    rank: int = Field(description="Rank assigned by the AI")
