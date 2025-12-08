"""
Utility functions for the dashboard.
"""

import pandas as pd
import numpy as np
from typing import Union
import io


def load_data(file) -> pd.DataFrame:
    """
    Load data from uploaded file.
    
    Args:
        file: Uploaded file object (CSV or Excel)
        
    Returns:
        DataFrame with loaded data
    """
    try:
        # Get file extension
        filename = file.name.lower()
        
        if filename.endswith('.csv'):
            data = pd.read_csv(file)
        elif filename.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel.")
        
        # Validate data
        validate_data(data)
        
        return data
    
    except Exception as e:
        raise RuntimeError(f"Error loading data: {str(e)}")


def validate_data(data: pd.DataFrame) -> bool:
    """
    Validate that data has required columns.
    
    Args:
        data: DataFrame to validate
        
    Returns:
        True if valid
        
    Raises:
        ValueError if validation fails
    """
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    
    # Check for required columns (case-insensitive)
    data_columns_lower = [col.lower() for col in data.columns]
    missing = [col for col in required_columns if col not in data_columns_lower]
    
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Normalize column names to lowercase
    data.columns = [col.lower() for col in data.columns]
    
    # Check for numeric columns
    for col in required_columns:
        if col in data.columns and not pd.api.types.is_numeric_dtype(data[col]):
            raise ValueError(f"Column '{col}' must be numeric")
    
    return True


def create_sample_data(num_days: int = 252, num_symbols: int = 3) -> pd.DataFrame:
    """
    Create synthetic sample data for demonstration.
    
    Args:
        num_days: Number of trading days
        num_symbols: Number of symbols/stocks
        
    Returns:
        DataFrame with sample OHLCV data
    """
    np.random.seed(42)
    
    data_list = []
    
    symbols = [f'STOCK{i+1}' for i in range(num_symbols)]
    dates = pd.date_range(end=pd.Timestamp.now(), periods=num_days, freq='D')
    
    for symbol in symbols:
        # Generate price data with random walk
        initial_price = np.random.uniform(50, 200)
        returns = np.random.normal(0.0005, 0.02, num_days)
        close_prices = initial_price * np.exp(np.cumsum(returns))
        
        # Generate OHLC from close
        high_prices = close_prices * (1 + np.abs(np.random.normal(0, 0.01, num_days)))
        low_prices = close_prices * (1 - np.abs(np.random.normal(0, 0.01, num_days)))
        open_prices = np.roll(close_prices, 1)
        open_prices[0] = close_prices[0]
        
        # Ensure OHLC logic is valid
        for i in range(num_days):
            high_prices[i] = max(high_prices[i], open_prices[i], close_prices[i])
            low_prices[i] = min(low_prices[i], open_prices[i], close_prices[i])
        
        # Generate volume
        base_volume = np.random.uniform(1000000, 5000000)
        volumes = base_volume * (1 + np.random.normal(0, 0.3, num_days))
        volumes = np.abs(volumes)
        
        # Create DataFrame for this symbol
        symbol_data = pd.DataFrame({
            'date': dates,
            'symbol': symbol,
            'open': open_prices,
            'high': high_prices,
            'low': low_prices,
            'close': close_prices,
            'volume': volumes
        })
        
        data_list.append(symbol_data)
    
    # Combine all symbols
    data = pd.concat(data_list, ignore_index=True)
    data = data.sort_values(['date', 'symbol']).reset_index(drop=True)
    
    return data


def format_number(num: float, decimals: int = 2) -> str:
    """
    Format number for display.
    
    Args:
        num: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted string
    """
    if pd.isna(num):
        return 'N/A'
    
    if abs(num) >= 1e6:
        return f'{num/1e6:.{decimals}f}M'
    elif abs(num) >= 1e3:
        return f'{num/1e3:.{decimals}f}K'
    else:
        return f'{num:.{decimals}f}'


def calculate_performance_metrics(alpha_values: pd.Series) -> dict:
    """
    Calculate performance metrics for an alpha.
    
    Args:
        alpha_values: Series of alpha values
        
    Returns:
        Dictionary of metrics
    """
    return {
        'mean': alpha_values.mean(),
        'std': alpha_values.std(),
        'sharpe': alpha_values.mean() / alpha_values.std() if alpha_values.std() != 0 else 0,
        'min': alpha_values.min(),
        'max': alpha_values.max(),
        'skew': alpha_values.skew(),
        'kurtosis': alpha_values.kurtosis()
    }


def create_comparison_table(alpha_results: pd.DataFrame) -> pd.DataFrame:
    """
    Create comparison table for multiple alphas.
    
    Args:
        alpha_results: DataFrame with alpha values
        
    Returns:
        DataFrame with comparison metrics
    """
    metrics = {}
    
    for col in alpha_results.columns:
        metrics[col] = calculate_performance_metrics(alpha_results[col])
    
    comparison_df = pd.DataFrame(metrics).T
    comparison_df = comparison_df.round(4)
    
    return comparison_df
