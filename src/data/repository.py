from typing import List
import pandas as pd
from .preprocessor import load_from_parquet
from ..models.restaurant import Restaurant

class RestaurantRepository:
    """
    In-memory query interface over the preprocessed dataset.
    """
    def __init__(self, data_path: str = "data/zomato_cleaned.parquet"):
        self.data_path = data_path
        self._restaurants: List[Restaurant] = []
        self._load_data()

    def _load_data(self):
        try:
            df = load_from_parquet(self.data_path)
            # Convert DataFrame rows directly into Pydantic models
            self._restaurants = [Restaurant(**row) for row in df.to_dict(orient='records')]
            print(f"Repository loaded {len(self._restaurants)} restaurants into memory.")
        except Exception as e:
            print(f"Error loading repository data: {e}")
            self._restaurants = []

    def get_all(self) -> List[Restaurant]:
        return self._restaurants
