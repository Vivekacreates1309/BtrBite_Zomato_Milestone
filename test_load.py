import os
from src.data.loader import fetch_zomato_dataset
from src.data.preprocessor import preprocess_dataset, save_to_parquet
from src.data.repository import RestaurantRepository

def main():
    parquet_path = "data/zomato_cleaned.parquet"
    
    # 1. Fetch from Hugging Face
    raw_df = fetch_zomato_dataset()
    print(f"Raw dataset shape: {raw_df.shape}")
    
    # 2. Preprocess
    cleaned_df = preprocess_dataset(raw_df)
    print(f"Cleaned dataset shape: {cleaned_df.shape}")
    
    # 3. Cache to Parquet
    save_to_parquet(cleaned_df, output_path=parquet_path)
    
    # 4. Load into Repository
    repo = RestaurantRepository(data_path=parquet_path)
    all_restaurants = repo.get_all()
    
    # 5. Print first 3
    print("\n--- Top 3 Restaurants from Repo ---")
    for r in all_restaurants[:3]:
        print(r.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
