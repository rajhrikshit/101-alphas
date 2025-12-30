from src.data_loader import load_market_data
from src.engine import AlphaEngine
from src.definitions import alpha_101, alpha_001
import pandas as pd

def check():
    print("Loading data...")
    data = load_market_data()
    print(f"Data loaded: {len(data.tickers)} tickers, {len(data.dates)} dates.")
    
    engine = AlphaEngine(data)
    
    # 1. Standard Run
    print("\n[Standard] Running Alpha 101 on all tickers...")
    res = engine.run_alpha(alpha_101)
    print(f"Result shape: {res.shape}")
    print(res.iloc[-5:, :3]) # Show last 5 days, first 3 tickers

    # 2. Subset Run
    target_tickers = data.tickers[:3]
    print(f"\n[Subset] Running Alpha 101 on {target_tickers}...")
    res_subset = engine.run_on_subset(target_tickers, alpha_101)
    print(f"Result shape: {res_subset.shape}")
    
    # 3. Basket Run (Equal Weighted)
    print("\n[Basket] Running Alpha 101 on Equal Weighted Basket...")
    res_basket = engine.run_on_basket(alpha_101, method='equal')
    print(f"Result shape: {res_basket.shape}")
    print(res_basket.tail())

    print("\nVerification complete.")

if __name__ == "__main__":
    check()
