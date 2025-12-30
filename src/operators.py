import pandas as pd
import numpy as np
from typing import Optional

"""
101 Alphas Operators
====================

This module implements the fundamental operators described in the 101 Alphas paper.
These operators are the building blocks for constructing complex alpha signals.

Key assumptions:
- Inputs are pandas DataFrames where Index=Date, Columns=Tickers.
- Operations are vectorized (work on the whole matrix at once).
"""

def rank(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cross-sectional rank.
    
    Maps values to their percentile rank across all stocks for a given day.
    Range: [0, 1]
    
    Formula: rank(x) = order(x) / n
    """
    return df.rank(axis=1, pct=True)

def delay(df: pd.DataFrame, period: int) -> pd.DataFrame:
    """
    Lag operator.
    
    Returns the value of x, 'period' days ago.
    """
    return df.shift(period)

def delta(df: pd.DataFrame, period: int) -> pd.DataFrame:
    """
    Difference operator.
    
    Formula: delta(x, d) = x_t - x_{t-d}
    """
    return df.diff(period)

def correlation(x: pd.DataFrame, y: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Rolling correlation over time.
    
    Calculates the correlation between x and y over the past 'window' days.
    """
    return x.rolling(window=window).corr(y)

def covariance(x: pd.DataFrame, y: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Rolling covariance over time.
    """
    return x.rolling(window=window).cov(y)

def scale(df: pd.DataFrame, k: float = 1.0) -> pd.DataFrame:
    """
    Rescales the input such that the sum of absolute values equals k.
    
    Formula: x / sum(|x|) * k
    Used to maintain constant leverage or capital allocation.
    """
    return df.div(df.abs().sum(axis=1), axis=0) * k

def signedpower(df: pd.DataFrame, a: float) -> pd.DataFrame:
    """
    Signed Power.
    
    Preserves the sign of the input while applying the power.
    Formula: sign(x) * |x|^a
    """
    return np.sign(df) * (np.abs(df) ** a)

def decay_linear(df: pd.DataFrame, period: int) -> pd.DataFrame:
    """
    Weighted moving average with linearly decaying weights.
    
    Weight d days ago = period - d + 1 (normalized).
    Example period=3: Weights are 3, 2, 1 (for t, t-1, t-2).
    """
    weights = np.arange(1, period + 1)
    sum_weights = np.sum(weights)
    
    # Efficient implementation using rolling apply with dot product
    # Note: construct weights such that the most recent observation (at index period-1 in the window) gets the highest weight
    # np.dot(x, w) where x is the window.
    # If window is [x_{t-2}, x_{t-1}, x_t], we want w = [1, 2, 3]
    
    return df.rolling(period).apply(lambda x: np.dot(x, weights) / sum_weights, raw=True)

def ts_sum(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series sum over the past 'window' days."""
    return df.rolling(window).sum()

def ts_mean(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series mean over the past 'window' days."""
    return df.rolling(window).mean()

def ts_min(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series minimum over the past 'window' days."""
    return df.rolling(window).min()

def ts_max(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series maximum over the past 'window' days."""
    return df.rolling(window).max()

def ts_argmax(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Time-series argmax.
    
    Returns the index (day offset) of the maximum value in the window.
    Based on standard interpretations, this usually returns how many days ago the max occurred,
    or a scaled value.
    
    Here, we return the 0-based index within the window (0 to window-1), 
    scaled to be comparable if needed.
    """
    return df.rolling(window).apply(np.argmax, raw=True)

def ts_argmin(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series argmin."""
    return df.rolling(window).apply(np.argmin, raw=True)
    
def stddev(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Moving standard deviation."""
    return df.rolling(window).std()

ts_std = stddev


def ts_rank(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Time-series rank.
    
    Rank of the current value against its own history over 'window' days.
    """
    return df.rolling(window).rank(pct=True)

def log(df: pd.DataFrame) -> pd.DataFrame:
    """Natural logarithm."""
    return np.log(df)

def sign(df: pd.DataFrame) -> pd.DataFrame:
    """Sign function (-1, 0, 1)."""
    return np.sign(df)

def indneutralize(df: pd.DataFrame, industry_groups: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Industry neutralization.
    
    Projecting out the industry mean.
    Since industry data is not currently available, this is a pass-through (identity).
    """
    # TODO: Implement actual neutralization when sector data is available.
    return df
