"""
Alpha calculation engine that orchestrates data processing and alpha computation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
from alphas.formulas import get_alpha_function, list_available_alphas


class AlphaEngine:
    """
    Main engine for calculating alphas from market data.
    
    This engine handles data validation, preprocessing, and alpha calculation.
    It supports single or batch calculation of alphas on provided datasets.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the alpha engine with market data.
        
        Args:
            data: DataFrame containing OHLCV data with columns:
                  - date: Trading date
                  - open: Opening price
                  - high: Highest price
                  - low: Lowest price
                  - close: Closing price
                  - volume: Trading volume
                  - symbol (optional): Stock/instrument identifier
        """
        self.raw_data = data.copy()
        self.data = self._preprocess_data(data)
        self.data_dict = self._prepare_data_dict()
        
    def _preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess and validate input data.
        
        Args:
            data: Raw market data
            
        Returns:
            Preprocessed data
        """
        df = data.copy()
        
        # Ensure date column exists and is datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
        
        # Validate required columns
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Handle multi-asset data
        if 'symbol' in df.columns:
            # Set multi-index for symbol and date
            if 'date' in df.columns:
                df = df.set_index(['date', 'symbol'])
        elif 'date' in df.columns:
            df = df.set_index('date')
        
        # Calculate VWAP if not present
        if 'vwap' not in df.columns:
            df['vwap'] = (df['high'] + df['low'] + df['close']) / 3
        
        # Remove any NaN or infinite values
        df = df.replace([np.inf, -np.inf], np.nan)
        
        return df
    
    def _prepare_data_dict(self) -> Dict[str, pd.DataFrame]:
        """
        Prepare data dictionary for alpha calculations.
        
        Returns:
            Dictionary with separate DataFrames for each price field
        """
        data_dict = {}
        
        for col in ['open', 'high', 'low', 'close', 'volume', 'vwap']:
            if col in self.data.columns:
                data_dict[col] = self.data[[col]].copy()
        
        return data_dict
    
    def calculate(self, alpha_name: str) -> pd.DataFrame:
        """
        Calculate a single alpha.
        
        Args:
            alpha_name: Name of the alpha (e.g., 'alpha_001')
            
        Returns:
            DataFrame containing calculated alpha values
        """
        alpha_func = get_alpha_function(alpha_name)
        
        if alpha_func is None:
            raise ValueError(f"Alpha '{alpha_name}' not found or not implemented")
        
        try:
            result = alpha_func(self.data_dict)
            
            # Ensure result is a DataFrame
            if isinstance(result, pd.Series):
                result = result.to_frame(name=alpha_name)
            elif isinstance(result, pd.DataFrame) and alpha_name not in result.columns:
                result.columns = [alpha_name]
            
            return result
        except Exception as e:
            raise RuntimeError(f"Error calculating {alpha_name}: {str(e)}")
    
    def calculate_batch(self, alpha_names: List[str]) -> pd.DataFrame:
        """
        Calculate multiple alphas at once.
        
        Args:
            alpha_names: List of alpha names to calculate
            
        Returns:
            DataFrame with columns for each alpha
        """
        results = {}
        
        for alpha_name in alpha_names:
            try:
                alpha_result = self.calculate(alpha_name)
                results[alpha_name] = alpha_result.iloc[:, 0] if len(alpha_result.columns) == 1 else alpha_result
            except Exception as e:
                print(f"Warning: Failed to calculate {alpha_name}: {str(e)}")
                continue
        
        if not results:
            raise RuntimeError("Failed to calculate any alphas")
        
        return pd.DataFrame(results)
    
    def calculate_all(self) -> pd.DataFrame:
        """
        Calculate all available alphas.
        
        Returns:
            DataFrame with columns for each alpha
        """
        available_alphas = list_available_alphas()
        return self.calculate_batch(available_alphas)
    
    def get_available_alphas(self) -> List[str]:
        """
        Get list of all available alpha names.
        
        Returns:
            List of alpha names
        """
        return list_available_alphas()
    
    def get_data_summary(self) -> Dict:
        """
        Get summary statistics of the loaded data.
        
        Returns:
            Dictionary with data summary
        """
        return {
            'num_records': len(self.data),
            'start_date': self.data.index.min() if 'date' in str(self.data.index.names) else None,
            'end_date': self.data.index.max() if 'date' in str(self.data.index.names) else None,
            'columns': list(self.data.columns),
            'has_multi_assets': 'symbol' in str(self.data.index.names),
        }
