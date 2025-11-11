import os
import pandas as pd
from utils.logger import setup_logger

logger = setup_logger(__name__)

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add Time-Series Feature (lag, rolling mean, return)
    """

    logger.info("Generating Features")

    df["Return"] = df["Close"].pct_change()
    df["RollingMean_5"] = df["Close"].rolling(window=5).mean()
    df["RollingStd_5"] = df["Close"].rolling(window=5).std()
    df["Lag_1"] = df["Close"].shift(1)

    df = df.dropna().reset_index(drop=True)
    logger.info(f"Feature set shape : {df.shape}")
    return df

def save_feature_data(df: pd.DataFrame, filename: str):
    """
    Save Feature Data to processed/ directory
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    feat_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(feat_dir, exist_ok=True)

    path = os.path.join(feat_dir, filename)
    df.to_csv(path, index=False)
    logger.info(f"Saved feature data to {path}")