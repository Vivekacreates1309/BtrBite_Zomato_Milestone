from pydantic import BaseModel, Field
from typing import Optional

class UserPreferences(BaseModel):
    location: str = Field(description="Required location/city")
    budget: str = Field(description="'low', 'medium', or 'high'")
    cuisine: Optional[str] = Field(default=None, description="Optional primary cuisine")
    min_rating: float = Field(default=0.0, description="Minimum acceptable rating, e.g. 3.5")
    additional: Optional[str] = Field(default=None, description="Free-text additional preferences")
