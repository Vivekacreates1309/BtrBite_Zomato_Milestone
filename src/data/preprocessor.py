import pandas as pd
from typing import List, Dict, Any
from pathlib import Path
from ..models.restaurant import Restaurant

def _get_budget_tier(cost: int) -> str:
    if cost <= 500:
        return 'low'
    elif cost <= 1500:
        return 'medium'
    else:
        return 'high'

def _parse_cuisines(cuisine_str: Any) -> List[str]:
    if pd.isna(cuisine_str):
        return []
    return [c.strip() for c in str(cuisine_str).split(',') if c.strip()]

def _clean_rate(rate_str: Any) -> float:
    if pd.isna(rate_str) or rate_str == 'NEW' or rate_str == '-':
        return 0.0
    try:
        # e.g. "4.1/5" -> 4.1
        return float(str(rate_str).split('/')[0].strip())
    except Exception:
        return 0.0

def _clean_cost(cost_str: Any) -> int:
    if pd.isna(cost_str):
        return 0
    try:
        # e.g. "1,200" -> 1200
        return int(str(cost_str).replace(',', '').strip())
    except Exception:
        return 0

def preprocess_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and normalizes the Zomato dataset into the canonical schema.
    """
    print("Preprocessing dataset...")
    
    # Map from ManikaSaini/zomato-restaurant-recommendation dataset columns
    col_mapping = {
        'name': 'name',
        'location': 'location',
        'cuisines': 'cuisines',
        'approx_cost(for two people)': 'cost_for_two',
        'rate': 'rating',
        'votes': 'votes',
        'rest_type': 'rest_type'
    }
    
    # Rename columns if they exist
    rename_dict = {k: v for k, v in col_mapping.items() if k in df.columns}
    df = df.rename(columns=rename_dict)
    
    # Check if necessary canonical columns exist
    required_cols = ['name', 'location', 'cuisines', 'cost_for_two', 'rating']
    for col in required_cols:
        if col not in df.columns:
            # Fallback assignment
            df[col] = None

    # Synthetic ID if missing
    if 'id' not in df.columns:
        df['id'] = [str(i) for i in range(len(df))]
    else:
        df['id'] = df['id'].astype(str)
        
    if 'votes' not in df.columns:
        df['votes'] = 0
        
    # Drop rows missing critical data
    df = df.dropna(subset=['name', 'location', 'cost_for_two', 'rating'])
    
    # Coerce and clean types
    df['cost_for_two'] = df['cost_for_two'].apply(_clean_cost)
    df['rating'] = df['rating'].apply(_clean_rate)
    df['votes'] = pd.to_numeric(df['votes'], errors='coerce').fillna(0).astype(int)
    
    # Force rest_type to be a string (empty string if missing) to survive Parquet serialization
    if 'rest_type' in df.columns:
        df['rest_type'] = df['rest_type'].fillna('').astype(str)
    else:
        df['rest_type'] = ''
    
    # Parse cuisines
    df['cuisines'] = df['cuisines'].apply(_parse_cuisines)
    
    # Normalize text
    df['location'] = df['location'].astype(str).str.strip().str.title()
    df['name'] = df['name'].astype(str).str.strip()
    
    # Derive budget tier
    df['budget_tier'] = df['cost_for_two'].apply(_get_budget_tier)
    
    return df

def save_to_parquet(df: pd.DataFrame, output_path: str = "data/zomato_cleaned.parquet"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    print(f"Cached dataset to {output_path}")

def load_from_parquet(input_path: str = "data/zomato_cleaned.parquet") -> pd.DataFrame:
    return pd.read_parquet(input_path)
