from typing import List
from pathlib import Path
import pandas as pd
from .preprocessor import load_from_parquet, preprocess_dataset, save_to_parquet
from ..models.restaurant import Restaurant

class RestaurantRepository:
    """
    In-memory query interface over the preprocessed dataset.
    Auto-downloads from HuggingFace if the local parquet cache is missing.
    """
    def __init__(self, data_path: str = "data/zomato_cleaned.parquet"):
        self.data_path = data_path
        self._restaurants: List[Restaurant] = []
        self._ensure_data_exists()
        self._load_data()

    def _ensure_data_exists(self):
        """Download and preprocess the dataset if the parquet file is missing."""
        if Path(self.data_path).exists():
            return
        print(f"Parquet file not found at {self.data_path}. Downloading from HuggingFace...")
        try:
            from datasets import load_dataset
            ds = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
            raw_df = ds.to_pandas()
            cleaned_df = preprocess_dataset(raw_df)
            save_to_parquet(cleaned_df, self.data_path)
            print("Dataset downloaded and cached successfully.")
        except Exception as e:
            print(f"Failed to download dataset: {e}")

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
