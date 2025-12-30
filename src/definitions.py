import pandas as pd
import numpy as np
from src.operators import (
    rank, delay, delta, correlation, covariance, scale, 
    signedpower, decay_linear, ts_min, ts_max, ts_argmax, 
    ts_argmin, stddev, ts_rank, log, sign, ts_sum, ts_mean, 
    ts_std, indneutralize
)
from src.market_data import MarketData

"""
Alpha Definitions
=================

Implementation of WorldQuant's 101 Alphas.
Reference: "101 Formulaic Alphas" by Zura Kakushadze.

Accessors like data.closes are replaced with data.close (singular, matching standard schema).
The MarketData object handles the mapping.
"""

def adv(data: MarketData, d: int) -> pd.DataFrame:
    """Average Daily Volume"""
    return ts_mean(data.volume, d)

def alpha_001(data: MarketData) -> pd.DataFrame:
    """
    Alpha#1: (rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5)
    """
    inner = data.returns.copy()
    inner[inner < 0] = stddev(data.returns, 20)
    inner[inner >= 0] = data.close
    
    sp = signedpower(inner, 2.0)
    ts_amax = ts_argmax(sp, 5)
    return rank(ts_amax) - 0.5

def alpha_002(data: MarketData) -> pd.DataFrame:
    """
    Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))
    """
    s1 = delta(log(data.volume), 2)
    rank_s1 = rank(s1)
    
    s2 = (data.close - data.open) / data.open
    rank_s2 = rank(s2)
    
    return -1.0 * correlation(rank_s1, rank_s2, 6)

def alpha_003(data: MarketData) -> pd.DataFrame:
    """
    Alpha#3: (-1 * correlation(rank(open), rank(volume), 10))
    """
    return -1.0 * correlation(rank(data.open), rank(data.volume), 10)

def alpha_004(data: MarketData) -> pd.DataFrame:
    """
    Alpha#4: (-1 * Ts_Rank(rank(low), 9))
    """
    return -1.0 * ts_rank(rank(data.low), 9)

def alpha_005(data: MarketData) -> pd.DataFrame:
    """
    Alpha#5: (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))
    """
    ma_vwap = ts_mean(data.vwap, 10)
    
    term1 = rank(data.open - ma_vwap)
    term2 = -1.0 * np.abs(rank(data.close - data.vwap))
    
    return term1 * term2

def alpha_006(data: MarketData) -> pd.DataFrame:
    """
    Alpha#6: (-1 * correlation(open, volume, 10))
    """
    return -1.0 * correlation(data.open, data.volume, 10)

def alpha_007(data: MarketData) -> pd.DataFrame:
    """
    Alpha#7: ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1 * 1))
    """
    adv20 = adv(data, 20)
    cond = adv20 < data.volume
    
    delta_close_7 = delta(data.close, 7)
    term_true = -1.0 * ts_rank(np.abs(delta_close_7), 60) * sign(delta_close_7)
    
    return np.where(cond, term_true, -1.0)

def alpha_008(data: MarketData) -> pd.DataFrame:
    """
    Alpha#8: (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10))))
    """
    sum_open_5 = ts_sum(data.open, 5)
    sum_ret_5 = ts_sum(data.returns, 5)
    prod = sum_open_5 * sum_ret_5
    
    return -1.0 * rank(prod - delay(prod, 10))

def alpha_009(data: MarketData) -> pd.DataFrame:
    """
    Alpha#9: ((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ? delta(close, 1) : (-1 * delta(close, 1))))
    """
    delta_close = delta(data.close, 1)
    min_delta = ts_min(delta_close, 5)
    max_delta = ts_max(delta_close, 5)
    
    cond1 = min_delta > 0
    cond2 = max_delta < 0
    
    res = np.where(cond1, delta_close, np.where(cond2, delta_close, -1.0 * delta_close))
    return pd.DataFrame(res, index=data.close.index, columns=data.close.columns)

def alpha_010(data: MarketData) -> pd.DataFrame:
    """
    Alpha#10: rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0) ? delta(close, 1) : (-1 * delta(close, 1)))))
    """
    delta_close = delta(data.close, 1)
    min_delta = ts_min(delta_close, 4)
    max_delta = ts_max(delta_close, 4)
    
    cond1 = min_delta > 0
    cond2 = max_delta < 0
    
    inner = np.where(cond1, delta_close, np.where(cond2, delta_close, -1.0 * delta_close))
    return rank(pd.DataFrame(inner, index=data.close.index, columns=data.close.columns))

def alpha_011(data: MarketData) -> pd.DataFrame:
    """
    Alpha#11: ((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(delta(volume, 3)))
    """
    diff = data.vwap - data.close
    term1 = rank(ts_max(diff, 3))
    term2 = rank(ts_min(diff, 3))
    term3 = rank(delta(data.volume, 3))
    
    return (term1 + term2) * term3

def alpha_012(data: MarketData) -> pd.DataFrame:
    """
    Alpha#12: (sign(delta(volume, 1)) * (-1 * delta(close, 1)))
    """
    return sign(delta(data.volume, 1)) * (-1.0 * delta(data.close, 1))

def alpha_013(data: MarketData) -> pd.DataFrame:
    """
    Alpha#13: (-1 * rank(covariance(rank(close), rank(volume), 5)))
    """
    return -1.0 * rank(covariance(rank(data.close), rank(data.volume), 5))

def alpha_014(data: MarketData) -> pd.DataFrame:
    """
    Alpha#14: ((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))
    """
    term1 = -1.0 * rank(delta(data.returns, 3))
    term2 = correlation(data.open, data.volume, 10)
    return term1 * term2

def alpha_015(data: MarketData) -> pd.DataFrame:
    """
    Alpha#15: (-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))
    """
    # Note: sum here is ts_sum
    corr = correlation(rank(data.high), rank(data.volume), 3)
    return -1.0 * ts_sum(rank(corr), 3)

def alpha_016(data: MarketData) -> pd.DataFrame:
    """
    Alpha#16: (-1 * rank(covariance(rank(high), rank(volume), 5)))
    """
    return -1.0 * rank(covariance(rank(data.high), rank(data.volume), 5))

def alpha_017(data: MarketData) -> pd.DataFrame:
    """
    Alpha#17: (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) * rank(ts_rank((volume / adv20), 5)))
    """
    adv20 = adv(data, 20)
    term1 = -1.0 * rank(ts_rank(data.close, 10))
    term2 = rank(delta(delta(data.close, 1), 1))
    term3 = rank(ts_rank(data.volume / adv20, 5))
    return term1 * term2 * term3

def alpha_018(data: MarketData) -> pd.DataFrame:
    """
    Alpha#18: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10))))
    """
    term1 = stddev(np.abs(data.close - data.open), 5)
    term2 = data.close - data.open
    term3 = correlation(data.close, data.open, 10)
    return -1.0 * rank(term1 + term2 + term3)

def alpha_019(data: MarketData) -> pd.DataFrame:
    """
    Alpha#19: ((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250)))))
    """
    term1 = -1.0 * sign((data.close - delay(data.close, 7)) + delta(data.close, 7))
    term2 = 1.0 + rank(1.0 + ts_sum(data.returns, 250))
    return term1 * term2

def alpha_020(data: MarketData) -> pd.DataFrame:
    """
    Alpha#20: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open - delay(low, 1))))
    """
    term1 = -1.0 * rank(data.open - delay(data.high, 1))
    term2 = rank(data.open - delay(data.close, 1))
    term3 = rank(data.open - delay(data.low, 1))
    return term1 * term2 * term3

def alpha_101(data: MarketData) -> pd.DataFrame:
    """
    Alpha#101: ((close - open) / ((high - low) + .001))
    """
    return (data.close - data.open) / ((data.high - data.low) + 0.001)

# Registry for automatic discovery
ALPHA_REGISTRY = {
    1: {"func": alpha_001},
    2: {"func": alpha_002},
    3: {"func": alpha_003},
    4: {"func": alpha_004},
    5: {"func": alpha_005},
    6: {"func": alpha_006},
    7: {"func": alpha_007},
    8: {"func": alpha_008},
    9: {"func": alpha_009},
    10: {"func": alpha_010},
    11: {"func": alpha_011},
    12: {"func": alpha_012},
    13: {"func": alpha_013},
    14: {"func": alpha_014},
    15: {"func": alpha_015},
    16: {"func": alpha_016},
    17: {"func": alpha_017},
    18: {"func": alpha_018},
    19: {"func": alpha_019},
    20: {"func": alpha_020},
    101: {"func": alpha_101}
}
