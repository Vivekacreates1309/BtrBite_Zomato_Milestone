from pydantic import BaseModel, Field
from typing import List, Optional

class Restaurant(BaseModel):
    id: str = Field(description="Stable identifier")
    name: str
    location: str = Field(description="City or locality")
    cuisines: List[str] = Field(default_factory=list, description="List of cuisines, e.g. ['Italian', 'Continental']")
    cost_for_two: int = Field(description="Numeric cost indicator")
    rating: float = Field(description="Numeric rating, e.g. 4.2")
    votes: int = Field(default=0, description="Popularity signal")
    rest_type: Optional[str] = Field(default=None, description="Casual dining, cafe, etc.")
    budget_tier: str = Field(description="'low', 'medium', or 'high' based on cost_for_two")
