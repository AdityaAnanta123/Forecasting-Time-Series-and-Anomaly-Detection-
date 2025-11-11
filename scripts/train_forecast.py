from src.data_pipeline.fetch_data import fetch_yahoo_financa_data, save_raw_data
from src.data_pipeline.preprocess import clean_data, save_processed_data
from src.data_pipeline.feature_engineer import add_features, save_feature_data

from src.utils.config_loader import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)
config = Config()

def main():
    logger.info("Starting time series forecasting pipeline")

    symbols = config.get("data_source", "symbols", default=["AAPL"])
    period = config.get("data_source", "period", default=["6mo"])
    interval = config.get("data_source", "interval", default=["id"])

    for symbol in symbols:
        logger.info(f". processing {symbol}")

        #Take a raw data from data/raw/
        df_raw = fetch_yahoo_financa_data(symbol, period, interval)
        save_raw_data(df_raw, f"{symbol}_raw.csv")

        #Preprocessing
        df_clean = clean_data(df_raw)
        save_processed_data(df_clean, f"{symbol}_clean.csv")

        #Feature Engineer
        df_feat = add_features(df_clean)
        save_feature_data(df_feat, f"{symbol}_feature.csv")

    logger.info("Data Pipeline completed succesfully")

if __name__ == "__main__":
    main()