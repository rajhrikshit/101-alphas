"""
Time-series and cross-sectional operators used in alpha formulas.
These operators form the building blocks for all 101 alpha formulas.
"""

import numpy as np
import pandas as pd
from typing import Union, Optional


def ts_sum(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series sum over the past 'window' days."""
    return df.rolling(window=window, min_periods=window).sum()


def ts_mean(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series mean over the past 'window' days."""
    return df.rolling(window=window, min_periods=window).mean()


def ts_std(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series standard deviation over the past 'window' days."""
    return df.rolling(window=window, min_periods=window).std()


def ts_rank(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series rank over the past 'window' days."""
    return df.rolling(window=window, min_periods=window).apply(
        lambda x: pd.Series(x).rank(pct=True).iloc[-1]
    )


def ts_product(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series product over the past 'window' days."""
    return df.rolling(window=window, min_periods=window).apply(np.prod)


def ts_min(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series minimum over the past 'window' days."""
    return df.rolling(window=window, min_periods=window).min()


def ts_max(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series maximum over the past 'window' days."""
    return df.rolling(window=window, min_periods=window).max()


def ts_argmax(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series arg max over the past 'window' days."""
    return df.rolling(window=window, min_periods=window).apply(
        lambda x: x.argmax() + 1
    )


def ts_argmin(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series arg min over the past 'window' days."""
    return df.rolling(window=window, min_periods=window).apply(
        lambda x: x.argmin() + 1
    )


def delta(df: pd.DataFrame, period: int = 1) -> pd.DataFrame:
    """Calculate difference between current value and value 'period' days ago."""
    return df.diff(period)


def delay(df: pd.DataFrame, period: int = 1) -> pd.DataFrame:
    """Return value from 'period' days ago."""
    return df.shift(period)


def rank(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-sectional rank (percentile) across instruments."""
    if isinstance(df, pd.Series):
        return df.rank(pct=True)
    return df.rank(pct=True, axis=1)


def scale(df: pd.DataFrame, a: float = 1.0) -> pd.DataFrame:
    """Scale values to sum to 'a' (cross-sectional)."""
    if isinstance(df, pd.Series):
        total = df.abs().sum()
        return df / total * a if total != 0 else df
    return df.div(df.abs().sum(axis=1), axis=0) * a


def ts_correlation(x: pd.DataFrame, y: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series correlation between x and y over 'window' days."""
    return x.rolling(window=window, min_periods=window).corr(y)


def ts_covariance(x: pd.DataFrame, y: pd.DataFrame, window: int) -> pd.DataFrame:
    """Time-series covariance between x and y over 'window' days."""
    return x.rolling(window=window, min_periods=window).cov(y)


def correlation(x: pd.DataFrame, y: pd.DataFrame, window: int) -> pd.DataFrame:
    """Alias for ts_correlation."""
    return ts_correlation(x, y, window)


def covariance(x: pd.DataFrame, y: pd.DataFrame, window: int) -> pd.DataFrame:
    """Alias for ts_covariance."""
    return ts_covariance(x, y, window)


def sign(df: pd.DataFrame) -> pd.DataFrame:
    """Return sign of values: 1 for positive, -1 for negative, 0 for zero."""
    return np.sign(df)


def abs_op(df: pd.DataFrame) -> pd.DataFrame:
    """Return absolute values."""
    return np.abs(df)


def log(df: pd.DataFrame) -> pd.DataFrame:
    """Return natural logarithm, handling non-positive values."""
    return np.log(df.clip(lower=1e-10))


def power(df: pd.DataFrame, exp: float) -> pd.DataFrame:
    """Raise values to power 'exp'."""
    return df ** exp


def condition(condition_df: pd.DataFrame, true_df: pd.DataFrame, false_df: pd.DataFrame) -> pd.DataFrame:
    """Return true_df where condition is True, otherwise false_df."""
    return true_df.where(condition_df, false_df)


def ts_decay_linear(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Weighted moving average with linearly decaying weights.
    Most recent value has weight 'window', previous has 'window-1', etc.
    """
    weights = np.arange(1, window + 1)
    weights = weights / weights.sum()
    
    def weighted_mean(x):
        if len(x) < window:
            return np.nan
        return np.sum(x * weights)
    
    return df.rolling(window=window, min_periods=window).apply(weighted_mean)


def indneutralize(df: pd.DataFrame, industry: pd.DataFrame) -> pd.DataFrame:
    """
    Industry neutralize: subtract industry mean from each value.
    For simplified implementation without industry data, returns original.
    """
    # Simplified version: demean within each time period
    if isinstance(df, pd.Series):
        return df - df.mean()
    return df.sub(df.mean(axis=1), axis=0)


def returns(df: pd.DataFrame, period: int = 1) -> pd.DataFrame:
    """Calculate returns over 'period' days."""
    return df.pct_change(period)


def ts_regression_slope(y: pd.DataFrame, x: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Time-series linear regression slope of y on x over 'window' days.
    """
    def calc_slope(arr_y, arr_x):
        if len(arr_y) < window or len(arr_x) < window:
            return np.nan
        # Simple linear regression
        x_mean = np.mean(arr_x)
        y_mean = np.mean(arr_y)
        numerator = np.sum((arr_x - x_mean) * (arr_y - y_mean))
        denominator = np.sum((arr_x - x_mean) ** 2)
        if denominator == 0:
            return np.nan
        return numerator / denominator
    
    result = pd.DataFrame(index=y.index, columns=y.columns if hasattr(y, 'columns') else [0])
    for i in range(window - 1, len(y)):
        y_window = y.iloc[i - window + 1:i + 1]
        x_window = x.iloc[i - window + 1:i + 1]
        result.iloc[i] = calc_slope(y_window.values.flatten(), x_window.values.flatten())
    
    return result


def ts_regression_residual(y: pd.DataFrame, x: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Time-series linear regression residual of y on x over 'window' days.
    """
    slope = ts_regression_slope(y, x, window)
    intercept = ts_mean(y, window) - slope * ts_mean(x, window)
    predicted = slope * x + intercept
    return y - predicted


def highday(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Number of days since highest value in the past 'window' days."""
    return ts_argmax(df, window)


def lowday(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Number of days since lowest value in the past 'window' days."""
    return ts_argmin(df, window)


def sumif(condition_df: pd.DataFrame, value_df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Sum of values where condition is true over 'window' days."""
    masked = value_df.where(condition_df, 0)
    return ts_sum(masked, window)


def sma(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Simple moving average (alias for ts_mean)."""
    return ts_mean(df, window)


def wma(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Weighted moving average (alias for ts_decay_linear)."""
    return ts_decay_linear(df, window)


def sequence(n: int) -> pd.Series:
    """Generate sequence from 1 to n."""
    return pd.Series(range(1, n + 1))


# Convenience functions for common operations
def adv(volume: pd.DataFrame, window: int) -> pd.DataFrame:
    """Average daily volume over 'window' days."""
    return ts_mean(volume, window)
