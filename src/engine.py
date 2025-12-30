import pandas as pd
from typing import Callable, Optional, List, Literal, Union
from src.market_data import MarketData

class AlphaEngine:
    """
    The engine responsible for executing alpha logic against a dataset.
    """
    
    def __init__(self, data: MarketData):
        self.data = data

    def run_alpha(self, alpha_func: Callable, **kwargs) -> pd.DataFrame:
        """
        Executes a given alpha function using the current MarketData container.
        """
        try:
            # Pass the MarketData object directly.
            # The alpha function will access .close, .open etc. which are guaranteed to be aligned.
            result = alpha_func(self.data, **kwargs)
            
            # Ensure the result is aligned with the ecosystem
            if isinstance(result, pd.DataFrame):
                 # Align just in case the alpha did something weird, though operations *should* preserve index
                 if not result.index.equals(self.data.close.index):
                     result = result.reindex(self.data.close.index)
                 if not result.columns.equals(self.data.close.columns):
                     result = result.reindex(columns=self.data.close.columns)
            
            return result
        except Exception as e:
            raise RuntimeError(f"Error executing alpha: {e}")

    def run_on_subset(self, tickers: List[str], alpha_func: Callable, **kwargs) -> pd.DataFrame:
        """
        Run alpha on a specific subset of tickers.
        """
        subset_data = self.data.subset(tickers)
        engine = AlphaEngine(subset_data)
        return engine.run_alpha(alpha_func, **kwargs)

    def run_on_basket(self, alpha_func: Callable, tickers: List[str] = None, method: Literal['equal', 'price'] = 'equal', **kwargs) -> pd.DataFrame:
        """
        Run alpha on a synthetic basket created from the tickers.
        """
        basket_data = self.data.create_basket(name="BASKET", method=method, tickers=tickers)
        engine = AlphaEngine(basket_data)
        return engine.run_alpha(alpha_func, **kwargs)
