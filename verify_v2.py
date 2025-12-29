from src.data_loader import load_market_data
from src.engine import AlphaEngine
from src.definitions import alpha_101

def check():
    print("Loading data...")
    data = load_market_data()
    print(f"Data loaded: {data.close.shape}")
    
    engine = AlphaEngine(data)
    print("Running Alpha 101...")
    res = engine.run_alpha(alpha_101)
    print(f"Result shape: {res.shape}")
    print("Verification complete.")

if __name__ == "__main__":
    check()
