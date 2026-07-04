from datasets import load_dataset
import pandas as pd

def fetch_zomato_dataset() -> pd.DataFrame:
    """
    Fetches the Zomato dataset from Hugging Face and returns it as a pandas DataFrame.
    Dataset: ManikaSaini/zomato-restaurant-recommendation
    """
    print("Loading dataset from Hugging Face: ManikaSaini/zomato-restaurant-recommendation")
    dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
    
    # Typically we use the 'train' split if available.
    if 'train' in dataset:
        df = dataset['train'].to_pandas()
    else:
        # Fallback to whatever the first split is
        split = list(dataset.keys())[0]
        df = dataset[split].to_pandas()
        
    return df
