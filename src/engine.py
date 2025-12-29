import pandas as pd
from dataclasses import dataclass
from typing import Dict, Optional, Callable

@dataclass
class MarketData:
    """
    Standardized container for market data.
    """
    closes: pd.DataFrame
    opens: pd.DataFrame
    highs: pd.DataFrame
    lows: pd.DataFrame
    volumes: pd.DataFrame
    vwap: pd.DataFrame
    returns: pd.DataFrame
    benchmark: Optional[pd.Series] = None

class AlphaEngine:
    """
    The engine responsible for executing alpha logic against a dataset.
    
    This class is Data Agnostic. It does not know where the data comes from (CSV, DB, API),
    only that it conforms to the MarketData structure.
    """
    
    def __init__(self, data: MarketData):
        self.data = data
        self.tickers = data.closes.columns.tolist()
        self.dates = data.closes.index.tolist()

    def run_alpha(self, alpha_func: Callable, **kwargs) -> pd.DataFrame:
        """
        Executes a given alpha function using the loaded data.
        
        Args:
            alpha_func: A function that takes (closes, opens, highs, lows, volumes, vwap, returns) 
                       and returns a DataFrame.
        """
        # We pass the data components to the alpha function
        # Using a dictionary unpacking or direct arguments depending on design
        # Here we assume alpha definitions accept the specific dataframes they need
        # or we pass a context object.
        # To make definitions clean (like the paper), we might want to bind the data to the operators context
        # OR pass the data container to the function.
        
        # Let's try passing the data object to the alpha function
        try:
            return alpha_func(self.data, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Error executing alpha: {e}")
