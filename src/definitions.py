import pandas as pd
import numpy as np
from src.operators import (
    rank, delay, delta, correlation, covariance, scale, 
    signedpower, decay_linear, ts_min, ts_max, ts_argmax, 
    ts_argmin, stddev, ts_rank, log, sign
)
from src.engine import MarketData

"""
Alpha Definitions
=================

Each alpha is defined as a standalone function taking a MarketData object.
We also provide a registry with metadata (Latex, Description) for the UI.
"""

def alpha_001(data: MarketData) -> pd.DataFrame:
    """
    Alpha#1: (rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5)
    """
    inner = data.returns.copy()
    inner[inner < 0] = stddev(data.returns, 20)
    inner[inner >= 0] = data.closes
    
    sp = signedpower(inner, 2.0)
    ts_amax = ts_argmax(sp, 5)
    return rank(ts_amax) - 0.5

def alpha_002(data: MarketData) -> pd.DataFrame:
    """
    Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))
    """
    # Part A: delta(log(volume), 2)
    s1 = delta(log(data.volumes), 2)
    rank_s1 = rank(s1)
    
    # Part B: (close - open) / open
    s2 = (data.closes - data.opens) / data.opens
    rank_s2 = rank(s2)
    
    return -1.0 * correlation(rank_s1, rank_s2, 6)

def alpha_003(data: MarketData) -> pd.DataFrame:
    """
    Alpha#3: (-1 * correlation(rank(open), rank(volume), 10))
    """
    return -1.0 * correlation(rank(data.opens), rank(data.volumes), 10)

def alpha_004(data: MarketData) -> pd.DataFrame:
    """
    Alpha#4: (-1 * Ts_Rank(rank(low), 9))
    """
    return -1.0 * ts_rank(rank(data.lows), 9)

def alpha_005(data: MarketData) -> pd.DataFrame:
    """
    Alpha#5: (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))
    """
    # sum(vwap, 10) / 10 is simply a 10-day moving average
    ma_vwap = data.vwap.rolling(10).mean()
    
    term1 = rank(data.opens - ma_vwap)
    term2 = -1.0 * np.abs(rank(data.closes - data.vwap))
    
    return term1 * term2

def alpha_006(data: MarketData) -> pd.DataFrame:
    """
    Alpha#6: (-1 * correlation(open, volume, 10))
    """
    return -1.0 * correlation(data.opens, data.volumes, 10)

def alpha_009(data: MarketData) -> pd.DataFrame:
    """
    Alpha#9: ((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ? delta(close, 1) : (-1 * delta(close, 1))))
    """
    delta_close = delta(data.closes, 1)
    min_delta = ts_min(delta_close, 5)
    max_delta = ts_max(delta_close, 5)
    
    cond1 = min_delta > 0
    cond2 = max_delta < 0
    
    res = np.where(cond1, delta_close, np.where(cond2, delta_close, -1.0 * delta_close))
    return pd.DataFrame(res, index=data.closes.index, columns=data.closes.columns)

def alpha_101(data: MarketData) -> pd.DataFrame:
    """
    Alpha#101: ((close - open) / ((high - low) + .001))
    """
    return (data.closes - data.opens) / ((data.highs - data.lows) + 0.001)

# Registry for UI
ALPHA_REGISTRY = {
    1: {
        "func": alpha_001,
        "latex": r"Rank(Ts\_ArgMax(SignedPower(((returns < 0) ? StdDev(returns, 20) : close), 2), 5)) - 0.5",
        "description": "Exploits mean reversion in short-term extreme price moves (via SignedPower)."
    },
    2: {
        "func": alpha_002,
        "latex": r"-1 \times Correlation(Rank(Delta(Log(volume), 2)), Rank(\frac{close - open}{open}), 6)",
        "description": "Relates volume changes to price returns."
    },
    3: {
        "func": alpha_003,
        "latex": r"-1 \times Correlation(Rank(open), Rank(volume), 10)",
        "description": "Correlation between Open Price ranks and Volume ranks."
    },
    4: {
        "func": alpha_004,
        "latex": r"-1 \times Ts\_Rank(Rank(low), 9)",
        "description": "Reversion based on the rank of Low prices."
    },
    5: {
        "func": alpha_005,
        "latex": r"Rank(open - \text{MA}_{10}(vwap)) \times (-1 \times |Rank(close - vwap)|)",
        "description": "Interacts deviation from VWAP trend with daily VWAP deviation."
    },
    6: {
        "func": alpha_006,
        "latex": r"-1 \times Correlation(open, volume, 10)",
        "description": "Price-Volume correlation signal."
    },
    9: {
        "func": alpha_009,
        "latex": r"\text{If } min(\Delta close, 5) > 0 \text{ then } \Delta close \text{ else if } max(\Delta close, 5) < 0 \text{ then } \Delta close \text{ else } -\Delta close",
        "description": "Momentum if trend is consistent (all up or all down), otherwise Mean Reversion."
    },
    101: {
        "func": alpha_101,
        "latex": r"\frac{close - open}{(high - low) + 0.001}",
        "description": "Normalized range location (Close relative to Open, scaled by High-Low range)."
    }
}
