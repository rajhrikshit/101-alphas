import pandas as pd
import numpy as np
from typing import List, Optional, Union, Dict, Literal

class MarketData:
    """
    A robust container for market data that guarantees alignment across fields.
    
    Design Philosophy:
    - Input: Long-format DataFrame (Database style) or aligned Dictionary.
    - Internal: Wide-format DataFrames (Matrix style) for vectorized performance.
    - Guarantee: All internal fields (open, close, etc.) share the EXACT same Index (Time) and Columns (Tickers).
    """
    
    REQUIRED_FIELDS = ['close', 'open', 'high', 'low', 'volume']
    
    def __init__(self, df: Union[pd.DataFrame, Dict[str, pd.DataFrame]], schema: Dict[str, str] = None):
        """
        Initialize from a Long-format DataFrame or a Dict of Wide DataFrames.
        
        Args:
            df: DataFrame with at least Date, Ticker, and OHLCV columns.
                OR Dict[str, pd.DataFrame] where keys are fields and values are Time x Ticker matrices.
            schema: Mapping of standard names to column names in df. 
                    Default: {'date': 'Date', 'ticker': 'Ticker', 'open': 'Open', ...}
        """
        self._schema = schema or {
            'date': 'Date',
            'ticker': 'Ticker',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume',
            'vwap': 'VWAP' # Optional
        }
        
        self._data: Dict[str, pd.DataFrame] = {}
        self.tickers: List[str] = []
        self.dates: List[pd.Timestamp] = []
        
        if isinstance(df, dict):
            self._init_from_dict(df)
        else:
            self._process_data(df)
            
        self._derive_missing_fields()
        
    def _init_from_dict(self, data_dict: Dict[str, pd.DataFrame]):
        """Initialize directly from aligned matrices (useful for subsets/baskets)."""
        if not data_dict:
            raise ValueError("Empty data dictionary provided")
            
        self._data = data_dict.copy()
        
        # Validate alignment
        ref_key = list(self._data.keys())[0]
        ref_df = self._data[ref_key]
        self.dates = ref_df.index.tolist()
        self.tickers = ref_df.columns.tolist()
        
        for k, v in self._data.items():
            if not v.index.equals(ref_df.index) or not v.columns.equals(ref_df.columns):
                # Try to align if indices match but are just ordered differently or subset
                if set(v.index) == set(ref_df.index) and set(v.columns) == set(ref_df.columns):
                     self._data[k] = v.reindex(index=ref_df.index, columns=ref_df.columns)
                else:
                    raise ValueError(f"Field {k} is not aligned with {ref_key}")

    def _process_data(self, df: pd.DataFrame):
        # Validate schema
        col_map = {v: k for k, v in self._schema.items()}
        df = df.rename(columns=col_map)
        
        # Ensure required columns exist
        missing = [f for f in ['date', 'ticker'] if f not in df.columns]
        if missing:
            raise ValueError(f"Input DataFrame missing required index columns: {missing}")

        # Standardize types
        df['date'] = pd.to_datetime(df['date'])
        
        # Set MultiIndex for easy unstacking
        # Handling duplicates: drop them or average them? Dropping for robustness.
        df = df.drop_duplicates(subset=['date', 'ticker'])
        df = df.set_index(['date', 'ticker']).sort_index()
        
        # Pivot all fields to Wide Format
        # This guarantees alignment because unstack operates on the same index
        available_fields = [c for c in df.columns if c in self.REQUIRED_FIELDS + ['vwap', 'returns']]
        
        if not available_fields:
            raise ValueError("Input data contains no recognizable market fields (open, close, etc).")

        for field in available_fields:
            # unstack(level=1) moves Ticker to columns
            self._data[field] = df[field].unstack(level=1)

        # Common attributes
        # We use the 'close' matrix as the reference for shape
        ref_matrix = self._data.get('close')
        if ref_matrix is None:
             ref_matrix = self._data[available_fields[0]]
        self.dates = ref_matrix.index.tolist()
        self.tickers = ref_matrix.columns.tolist()
        
        # Align all matrices to the reference (fill missing with NaN if unstack didn't do it)
        # unstack usually aligns, but let's be safe against sparse data
        for k, v in self._data.items():
            if not v.index.equals(ref_matrix.index) or not v.columns.equals(ref_matrix.columns):
                self._data[k] = v.reindex(index=ref_matrix.index, columns=ref_matrix.columns)
            
            # Forward fill then Backward fill to handle missing data holes
            # This is crucial for Alpha calculation stability
            self._data[k] = self._data[k].ffill().bfill()

    def _derive_missing_fields(self):
        # 1. Returns
        if 'returns' not in self._data and 'close' in self._data:
            self._data['returns'] = self._data['close'].pct_change()

        # 2. VWAP
        if 'vwap' not in self._data:
            # Approx VWAP = (H+L+C)/3
            if all(k in self._data for k in ['high', 'low', 'close']):
                self._data['vwap'] = (self._data['high'] + self._data['low'] + self._data['close']) / 3
            elif 'close' in self._data:
                 self._data['vwap'] = self._data['close'] # Fallback

    def __getattr__(self, name):
        """
        Dynamic accessor for data fields.
        Allows data.close, data.open, etc.
        """
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"MarketData has no field '{name}'")

    @property
    def fields(self) -> List[str]:
        return list(self._data.keys())

    def add_field(self, name: str, df: pd.DataFrame):
        """
        Add a derived field (like an Alpha or a factor) ensuring alignment.
        """
        if df.shape != (len(self.dates), len(self.tickers)):
            # Try to realign
            df = df.reindex(index=self.dates, columns=self.tickers)
        
        self._data[name] = df

    def subset(self, tickers: List[str]) -> 'MarketData':
        """
        Returns a new MarketData instance containing only the specified tickers.
        """
        valid_tickers = [t for t in tickers if t in self.tickers]
        if not valid_tickers:
            raise ValueError(f"No valid tickers found in subset request. Available: {self.tickers[:5]}...")
            
        new_data = {k: v[valid_tickers].copy() for k, v in self._data.items()}
        return MarketData(new_data)

    def create_basket(self, name: str = "BASKET", method: Literal['equal', 'price'] = 'equal', tickers: List[str] = None) -> 'MarketData':
        """
        Creates a synthetic MarketData instance containing a single ticker representing the basket.
        
        Args:
            name: Name of the synthetic ticker
            method: 'equal' (Equal Weighted) or 'price' (Price Weighted)
            tickers: Optional subset of tickers to include. If None, uses all.
        """
        source = self if tickers is None else self.subset(tickers)
        
        basket_data = {}
        
        if method == 'price':
            # Price Weighted: Sum of prices
            basket_data['close'] = source.close.sum(axis=1).to_frame(name)
            basket_data['open'] = source.open.sum(axis=1).to_frame(name)
            basket_data['high'] = source.high.sum(axis=1).to_frame(name)
            basket_data['low'] = source.low.sum(axis=1).to_frame(name)
            basket_data['volume'] = source.volume.sum(axis=1).to_frame(name)
            # Recalculate VWAP
            basket_data['vwap'] = (basket_data['high'] + basket_data['low'] + basket_data['close']) / 3
            
        elif method == 'equal':
            # Equal Weighted: Average Returns index
            # Index starts at 1.0
            daily_returns = source.returns.mean(axis=1).fillna(0)
            # Create a price series starting at 100
            index_curve = 100 * (1 + daily_returns).cumprod()
            
            basket_data['close'] = index_curve.to_frame(name)
            basket_data['volume'] = source.volume.sum(axis=1).to_frame(name)
            
            # Synthesize OHL based on constituents average intraday moves relative to previous close
            # This is an approximation
            avg_open_ret = (source.open / source.close.shift(1) - 1).mean(axis=1).fillna(0)
            avg_high_ret = (source.high / source.close.shift(1) - 1).mean(axis=1).fillna(0)
            avg_low_ret = (source.low / source.close.shift(1) - 1).mean(axis=1).fillna(0)
            
            prev_close = basket_data['close'].shift(1).fillna(100)
            
            basket_data['open'] = prev_close.multiply(1 + avg_open_ret, axis=0)
            basket_data['high'] = prev_close.multiply(1 + avg_high_ret, axis=0)
            basket_data['low'] = prev_close.multiply(1 + avg_low_ret, axis=0)
            
            # Fix initial day
            basket_data['open'].iloc[0] = basket_data['close'].iloc[0]
            basket_data['high'].iloc[0] = basket_data['close'].iloc[0]
            basket_data['low'].iloc[0] = basket_data['close'].iloc[0]
            
            basket_data['vwap'] = basket_data['close']

        return MarketData(basket_data)
