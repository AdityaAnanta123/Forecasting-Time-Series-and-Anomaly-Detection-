import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

from utils.config_loader import Config
from utils.logger import setup_logger


logger = setup_logger(__name__)
config = Config()

def fetch_yahoo_financa_data(symbol : str, period : str = "1y", interval : str = "id") -> pd.DataFrame:
    #Fetch data from yahoo finance API#
    logger.info("Fetching {symbol} data for period = {period}, interval = {interval}")
    try:
        df = yf.download(symbol, period = period, interval = interval, progress = False)
        df.reset_index(inplace = True)
        logger.info(f"Fetch {len(df)} rows for {symbol}")
        return df
    except Exception as e:
        logger.exception(f"Failed to fetch {symbol}: {e}")
        raise

def save_raw_data(df: pd.DataFrame, filename: str):
    #Save a raw data resulting from fetch data#
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    raw_dir = os.path.join(project_root, "data", "raw")
    os.makedirs(raw_dir, exist_ok= True)

    path = os.path.join(raw_dir, filename)
    df.to_csv(path, index= False)
    logger.info(f"Saved raw data to {path}")

