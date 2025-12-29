from alphas import AlphaEngine
import pandas as pd

def test_alpha_engine():
    print("Initializing AlphaEngine...")
    engine = AlphaEngine()
    
    print("Loading Data...")
    engine.load_data()
    print(f"Loaded data for {len(engine.tickers)} tickers and {len(engine.dates)} dates.")
    
    alphas_to_test = [1, 2, 3, 4, 5, 6, 9, 101]
    
    for alpha_id in alphas_to_test:
        print(f"Testing Alpha {alpha_id}...", end=" ")
        try:
            res = engine.get_alpha(alpha_id)
            if isinstance(res, pd.DataFrame):
                print(f"Success. Shape: {res.shape}")
                # Check for NaNs (some are expected due to lag/rolling)
                nan_count = res.isna().sum().sum()
                total_cells = res.size
                print(f"   NaN Ratio: {nan_count/total_cells:.2%}")
            else:
                print("Failed: Result is not a DataFrame")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_alpha_engine()
