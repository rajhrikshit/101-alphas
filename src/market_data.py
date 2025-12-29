import pandas as pd
import numpy as np
from typing import List, Optional, Union, Dict

class MarketData:
    """
    A robust container for market data that guarantees alignment across fields.
    
    Design Philosophy:
    - Input: Long-format DataFrame (Database style) or aligned Dictionary.
    - Internal: Wide-format DataFrames (Matrix style) for vectorized performance.
    - Guarantee: All internal fields (open, close, etc.) share the EXACT same Index (Time) and Columns (Tickers).
    """
    
    REQUIRED_FIELDS = ['close', 'open', 'high', 'low', 'volume']
    
    def __init__(self, df: pd.DataFrame, schema: Dict[str, str] = None):
        """
        Initialize from a Long-format DataFrame.
        
        Args:
            df: DataFrame with at least Date, Ticker, and OHLCV columns.
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
        
        self._process_data(df)
        self._derive_missing_fields()
        
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

