from sqlalchemy import text
from database.db_connection import engine, get_db
from utils.logger import setup_logger

logger = setup_logger()

def create_time_series_table():
    #Create table if the table not exists.#
    query = """
    CREATE TABLE IF NOT EXISTS time_series_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10),
    date DATE,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT
    );
    """

    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()
    logger.info("✅ Table 'time_series_data' checked/created successfully.")

def insert_data(df, symbol):
    #Insert dataframe data to table time_series_data#
    with engine.connect() as conn:
        for _, row in df.iterrows():
            conn.execute(
                text(
                    """
                    INSERT INTO time_series_data (
                    symbol, 
                    date, 
                    open,
                    high,
                    low,
                    close,
                    volume)
                    VALUES (
                    :symbol,
                    :date,
                    :open,
                    :high,
                    :low,
                    :close,
                    :volume)
                    ON CONFLICT (
                    symbol, date)
                    DO NOTHING;
                    """
                ),
                {
                    "symbol": symbol,
                    "date": row["Date"],
                    "open": row["Open"],
                    "high": row["High"],
                    "low": row["Low"],
                    "close": row["Close"],
                    "volume": int(row["Volume"])
                }
            )
        conn.commit()
    logger.info(f"✅ Inserted {len(df)} records for {symbol}")

def fetch_latest_data (symbol, limit = 10):
    #Fetch latest data from database#
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT * FROM time_series_data
                WHERE symbol = :symbol
                ORDER BY data DESC
                LIMIT :limit;
                """
            ),
            {"symbol": symbol, "limit": limit}
        )
        rows = result.fetchall()
    logger.info(f"Fetched {len(rows)} records for {symbol}")
    return rows