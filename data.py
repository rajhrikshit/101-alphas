from datetime import datetime, timedelta
import duckdb
import pandas as pd
import numpy as np
import os

# Use a local path for the workspace environment
DB_PATH = '/workspace/sp500.db'
# Fallback/Original path from user
ORIGINAL_DB_PATH = '/Users/hrikshit/duckdb/markets/na/sp500.db'

def generate_synthetic_data(start_date, end_date):
    """Generates synthetic stock data for testing."""
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK.B', 'JPM', 'JNJ']
    
    data = []
    for ticker in tickers:
        # Random walk for price
        prices = 100 + np.cumsum(np.random.randn(len(dates)))
        # Ensure positive
        prices = np.maximum(prices, 1.0)
        
        for i, date in enumerate(dates):
            close = prices[i]
            open_p = close * (1 + np.random.randn() * 0.01)
            high = max(open_p, close) * (1 + abs(np.random.randn()) * 0.005)
            low = min(open_p, close) * (1 - abs(np.random.randn()) * 0.005)
            vol = np.random.randint(100000, 10000000)
            
            data.append({
                'Date': date,
                'Ticker': ticker,
                'Open': open_p,
                'High': high,
                'Low': low,
                'Close': close,
                'Volume': vol,
                # Include fields that might be expected
                'Dividends': 0.0,
                'Stock Splits': 0.0
            })
            
    return pd.DataFrame(data)

def ensure_db_exists():
    """Checks if DB exists, if not creates it with synthetic data."""
    if os.path.exists(DB_PATH):
        return

    print(f"Database not found at {DB_PATH}. Creating synthetic data...")
    # Generate data from 2010 to today
    df = generate_synthetic_data('2018-01-01', datetime.today().strftime('%Y-%m-%d'))
    
    with duckdb.connect(DB_PATH) as con:
        con.execute("CREATE TABLE history AS SELECT * FROM df")
    print("Synthetic database created.")

def load_sp500(table_name='history', start_date='2020-01-01', end_date=None):
    if end_date is None:
        end_date = datetime.today().date()
        
    # Check if we are in the original environment or cloud
    db_path = ORIGINAL_DB_PATH if os.path.exists(ORIGINAL_DB_PATH) else DB_PATH
    
    if db_path == DB_PATH:
        ensure_db_exists()
        
    try:
        with duckdb.connect(db_path) as con:
            # Check if table exists
            tables = con.execute("SHOW TABLES").fetchall()
            if (table_name,) not in tables:
                # If using synthetic DB, we only created 'history'
                 if table_name != 'history':
                     print(f"Table {table_name} not found. Using 'history'.")
                     table_name = 'history'

            qry = f"select * from {table_name} where Date between '{start_date}' and '{end_date}'"
            history = con.execute(qry).df()
            return history
    except Exception as e:
        print(f"Error loading data: {e}")
        # Fallback to generating dataframe directly if DB fails
        return generate_synthetic_data(start_date, str(end_date))
