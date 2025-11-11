import os
import pandas as pd
from utils.logger import setup_logger

logger = setup_logger(__name__)

def clean_data( df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleaning data include :
    - Remove Duplicate
    - Handling Missing Values
    - Checking datetime is right
    """
    logger.info("Starting data cleaning")

    #Drop Duplicate
    df = df.drop_duplicates(subset = ["Date"])
    df = df.sort_values("Date")

    #Handling Missing Values
    df = df.fillna(method = "ffill").fillna(method = "bfill")

    #Validation to main column
    if "Close" not in df.columns:
        raise ValueError("Missing Close column in dataFrame")
    
    logger.info(f"Cleaned dataset : {len(df)} rows remaining")
    return df

def save_processed_data(df: pd.DataFrame, filename: str):
    """
    Save preprocessing result to processed/ directory
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))
    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    path = os.path.join(processed_dir, filename)
    df.to_csv(path, index=False)
    logger.info(f"Save preprocessed data to {path}")
    