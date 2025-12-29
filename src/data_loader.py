import duckdb
import pandas as pd
import numpy as np
import os
from datetime import datetime
from src.market_data import MarketData

# Fallback paths
DB_PATH = '/workspace/sp500.db'
ORIGINAL_DB_PATH = '/Users/hrikshit/duckdb/markets/na/sp500.db'

def generate_synthetic_df(start_date, end_date):
    """Generates synthetic stock data in Long format."""
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK.B', 'JPM', 'JNJ']
    
    data = []
    for ticker in tickers:
        prices = 100 + np.cumsum(np.random.randn(len(dates)))
        prices = np.maximum(prices, 1.0)
        
        for i, date in enumerate(dates):
            close = prices[i]
            open_p = close * (1 + np.random.randn() * 0.01)
            high = max(open_p, close) * (1 + abs(np.random.randn()) * 0.005)
            low = min(open_p, close) * (1 - abs(np.random.randn()) * 0.005)
            vol = int(np.random.randint(100000, 10000000))
            
            data.append({
                'Date': date,
                'Ticker': ticker,
                'Open': open_p,
                'High': high,
                'Low': low,
                'Close': close,
                'Volume': vol
            })
            
    return pd.DataFrame(data)

def ensure_db_exists(path):
    if os.path.exists(path):
        return
    print(f"Database not found at {path}. Creating synthetic data...")
    df = generate_synthetic_df('2018-01-01', datetime.today().strftime('%Y-%m-%d'))
    with duckdb.connect(path) as con:
        con.execute("CREATE TABLE history AS SELECT * FROM df")

def load_market_data(start_date='2020-01-01', end_date=None) -> MarketData:
    """
    Loads raw data from DuckDB (or synthetic) and returns a robust MarketData object.
    """
    if end_date is None:
        end_date = datetime.today().date()
        
    db_path = ORIGINAL_DB_PATH if os.path.exists(ORIGINAL_DB_PATH) else DB_PATH
    if db_path == DB_PATH:
        ensure_db_exists(DB_PATH)
        
    try:
        with duckdb.connect(db_path) as con:
            tables = con.execute("SHOW TABLES").fetchall()
            table_name = 'history'
            if (table_name,) not in tables:
                 if tables: table_name = tables[0][0]

            qry = f"select * from {table_name} where Date between '{start_date}' and '{end_date}'"
            df = con.execute(qry).df()
    except Exception as e:
        print(f"Error loading DB: {e}. Using synthetic.")
        df = generate_synthetic_df(start_date, str(end_date))

    if df.empty:
        raise ValueError("Loaded data is empty.")

    # Create MarketData object (Handles pivoting, alignment, validation)
    return MarketData(df)
