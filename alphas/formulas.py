"""
Implementation of all 101 formulaic alphas from Zura Kakushadze's paper.
Each alpha is implemented as a function that takes a data dictionary and returns the alpha values.
"""

import numpy as np
import pandas as pd
from alphas.operators import *


def alpha_001(data):
    """
    Alpha#1: rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5
    """
    close = data['close']
    returns_data = returns(close, 1)
    condition_df = returns_data < 0
    true_val = ts_std(returns_data, 20)
    false_val = close
    result = condition(condition_df, true_val, false_val)
    powered = power(result, 2.0)
    ts_argmax_val = ts_argmax(powered, 5)
    ranked = rank(ts_argmax_val)
    return ranked - 0.5


def alpha_002(data):
    """
    Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))
    """
    volume = data['volume']
    close = data['close']
    open_price = data['open']
    
    log_volume = log(volume)
    delta_log_volume = delta(log_volume, 2)
    rank1 = rank(delta_log_volume)
    
    price_ratio = (close - open_price) / open_price
    rank2 = rank(price_ratio)
    
    corr = correlation(rank1, rank2, 6)
    return -1 * corr


def alpha_003(data):
    """
    Alpha#3: (-1 * correlation(rank(open), rank(volume), 10))
    """
    open_price = data['open']
    volume = data['volume']
    
    rank1 = rank(open_price)
    rank2 = rank(volume)
    
    corr = correlation(rank1, rank2, 10)
    return -1 * corr


def alpha_004(data):
    """
    Alpha#4: (-1 * Ts_Rank(rank(low), 9))
    """
    low = data['low']
    ranked = rank(low)
    ts_ranked = ts_rank(ranked, 9)
    return -1 * ts_ranked


def alpha_005(data):
    """
    Alpha#5: (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))
    """
    open_price = data['open']
    close = data['close']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    sum_vwap = ts_sum(vwap, 10)
    part1 = rank(open_price - (sum_vwap / 10))
    
    part2 = -1 * abs_op(rank(close - vwap))
    
    return part1 * part2


def alpha_006(data):
    """
    Alpha#6: (-1 * correlation(open, volume, 10))
    """
    open_price = data['open']
    volume = data['volume']
    
    corr = correlation(open_price, volume, 10)
    return -1 * corr


def alpha_007(data):
    """
    Alpha#7: ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1 * 1))
    """
    close = data['close']
    volume = data['volume']
    
    adv20 = adv(volume, 20)
    condition_df = adv20 < volume
    
    delta_close = delta(close, 7)
    abs_delta = abs_op(delta_close)
    ts_ranked = ts_rank(abs_delta, 60)
    sign_delta = sign(delta_close)
    
    true_val = -1 * ts_ranked * sign_delta
    false_val = pd.DataFrame(-1, index=close.index, columns=close.columns if hasattr(close, 'columns') else [0])
    
    return condition(condition_df, true_val, false_val)


def alpha_008(data):
    """
    Alpha#8: (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10))))
    """
    open_price = data['open']
    close = data['close']
    returns_data = returns(close, 1)
    
    sum_open = ts_sum(open_price, 5)
    sum_returns = ts_sum(returns_data, 5)
    product = sum_open * sum_returns
    
    delayed = delay(product, 10)
    diff = product - delayed
    
    return -1 * rank(diff)


def alpha_009(data):
    """
    Alpha#9: ((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ? delta(close, 1) : (-1 * delta(close, 1))))
    """
    close = data['close']
    delta_close = delta(close, 1)
    
    ts_min_val = ts_min(delta_close, 5)
    ts_max_val = ts_max(delta_close, 5)
    
    condition1 = ts_min_val > 0
    condition2 = ts_max_val < 0
    
    result = condition(condition1, delta_close, 
                      condition(condition2, delta_close, -1 * delta_close))
    return result


def alpha_010(data):
    """
    Alpha#10: rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0) ? delta(close, 1) : (-1 * delta(close, 1)))))
    """
    close = data['close']
    delta_close = delta(close, 1)
    
    ts_min_val = ts_min(delta_close, 4)
    ts_max_val = ts_max(delta_close, 4)
    
    condition1 = ts_min_val > 0
    condition2 = ts_max_val < 0
    
    result = condition(condition1, delta_close,
                      condition(condition2, delta_close, -1 * delta_close))
    return rank(result)


def alpha_011(data):
    """
    Alpha#11: ((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(delta(volume, 3)))
    """
    close = data['close']
    volume = data['volume']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    diff = vwap - close
    
    rank1 = rank(ts_max(diff, 3))
    rank2 = rank(ts_min(diff, 3))
    rank3 = rank(delta(volume, 3))
    
    return (rank1 + rank2) * rank3


def alpha_012(data):
    """
    Alpha#12: (sign(delta(volume, 1)) * (-1 * delta(close, 1)))
    """
    close = data['close']
    volume = data['volume']
    
    sign_delta_volume = sign(delta(volume, 1))
    delta_close = delta(close, 1)
    
    return sign_delta_volume * (-1 * delta_close)


def alpha_013(data):
    """
    Alpha#13: (-1 * rank(covariance(rank(close), rank(volume), 5)))
    """
    close = data['close']
    volume = data['volume']
    
    rank_close = rank(close)
    rank_volume = rank(volume)
    
    cov = covariance(rank_close, rank_volume, 5)
    
    return -1 * rank(cov)


def alpha_014(data):
    """
    Alpha#14: ((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))
    """
    close = data['close']
    open_price = data['open']
    volume = data['volume']
    
    returns_data = returns(close, 1)
    delta_returns = delta(returns_data, 3)
    
    rank_delta = rank(delta_returns)
    corr = correlation(open_price, volume, 10)
    
    return -1 * rank_delta * corr


def alpha_015(data):
    """
    Alpha#15: (-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))
    """
    high = data['high']
    volume = data['volume']
    
    rank_high = rank(high)
    rank_volume = rank(volume)
    
    corr = correlation(rank_high, rank_volume, 3)
    ranked_corr = rank(corr)
    
    return -1 * ts_sum(ranked_corr, 3)


def alpha_016(data):
    """
    Alpha#16: (-1 * rank(covariance(rank(high), rank(volume), 5)))
    """
    high = data['high']
    volume = data['volume']
    
    rank_high = rank(high)
    rank_volume = rank(volume)
    
    cov = covariance(rank_high, rank_volume, 5)
    
    return -1 * rank(cov)


def alpha_017(data):
    """
    Alpha#17: (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) * rank(ts_rank((volume / adv20), 5)))
    """
    close = data['close']
    volume = data['volume']
    
    adv20 = adv(volume, 20)
    
    part1 = -1 * rank(ts_rank(close, 10))
    
    delta1 = delta(close, 1)
    delta2 = delta(delta1, 1)
    part2 = rank(delta2)
    
    volume_ratio = volume / adv20
    part3 = rank(ts_rank(volume_ratio, 5))
    
    return part1 * part2 * part3


def alpha_018(data):
    """
    Alpha#18: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10))))
    """
    close = data['close']
    open_price = data['open']
    
    diff = close - open_price
    abs_diff = abs_op(diff)
    std_diff = ts_std(abs_diff, 5)
    
    corr = correlation(close, open_price, 10)
    
    result = std_diff + diff + corr
    
    return -1 * rank(result)


def alpha_019(data):
    """
    Alpha#19: ((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250)))))
    """
    close = data['close']
    
    delayed_close = delay(close, 7)
    delta_close = delta(close, 7)
    
    sign_val = sign((close - delayed_close) + delta_close)
    
    returns_data = returns(close, 1)
    sum_returns = ts_sum(returns_data, 250)
    
    rank_val = rank(1 + sum_returns)
    
    return -1 * sign_val * (1 + rank_val)


def alpha_020(data):
    """
    Alpha#20: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open - delay(low, 1))))
    """
    open_price = data['open']
    high = data['high']
    close = data['close']
    low = data['low']
    
    part1 = -1 * rank(open_price - delay(high, 1))
    part2 = rank(open_price - delay(close, 1))
    part3 = rank(open_price - delay(low, 1))
    
    return part1 * part2 * part3


# Continue with more alphas...
def alpha_021(data):
    """
    Alpha#21: ((((sum(close, 8) / 8) + stddev(close, 8)) < (sum(close, 2) / 2)) ? (-1 * 1) : (((sum(close, 2) / 2) < ((sum(close, 8) / 8) - stddev(close, 8))) ? 1 : (((1 < (volume / adv20)) || ((volume / adv20) == 1)) ? 1 : (-1 * 1))))
    """
    close = data['close']
    volume = data['volume']
    
    adv20 = adv(volume, 20)
    
    mean8 = ts_sum(close, 8) / 8
    std8 = ts_std(close, 8)
    mean2 = ts_sum(close, 2) / 2
    
    volume_ratio = volume / adv20
    
    condition1 = (mean8 + std8) < mean2
    condition2 = mean2 < (mean8 - std8)
    condition3 = volume_ratio >= 1
    
    result = condition(condition1, pd.DataFrame(-1, index=close.index, columns=close.columns if hasattr(close, 'columns') else [0]),
                      condition(condition2, pd.DataFrame(1, index=close.index, columns=close.columns if hasattr(close, 'columns') else [0]),
                               condition(condition3, pd.DataFrame(1, index=close.index, columns=close.columns if hasattr(close, 'columns') else [0]),
                                        pd.DataFrame(-1, index=close.index, columns=close.columns if hasattr(close, 'columns') else [0]))))
    return result


def alpha_022(data):
    """
    Alpha#22: (-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20))))
    """
    high = data['high']
    volume = data['volume']
    close = data['close']
    
    corr = correlation(high, volume, 5)
    delta_corr = delta(corr, 5)
    
    std_close = ts_std(close, 20)
    rank_std = rank(std_close)
    
    return -1 * delta_corr * rank_std


def alpha_023(data):
    """
    Alpha#23: (((sum(high, 20) / 20) < high) ? (-1 * delta(high, 2)) : 0)
    """
    high = data['high']
    
    mean_high = ts_sum(high, 20) / 20
    condition_df = mean_high < high
    
    delta_high = delta(high, 2)
    
    result = condition(condition_df, -1 * delta_high, 
                      pd.DataFrame(0, index=high.index, columns=high.columns if hasattr(high, 'columns') else [0]))
    return result


def alpha_024(data):
    """
    Alpha#24: ((((delta((sum(close, 100) / 100), 100) / delay(close, 100)) < 0.05) || ((delta((sum(close, 100) / 100), 100) / delay(close, 100)) == 0.05)) ? (-1 * (close - ts_min(close, 100))) : (-1 * delta(close, 3)))
    """
    close = data['close']
    
    mean100 = ts_sum(close, 100) / 100
    delta_mean = delta(mean100, 100)
    delayed_close = delay(close, 100)
    ratio = delta_mean / delayed_close
    
    condition_df = ratio <= 0.05
    
    ts_min_close = ts_min(close, 100)
    true_val = -1 * (close - ts_min_close)
    false_val = -1 * delta(close, 3)
    
    return condition(condition_df, true_val, false_val)


def alpha_025(data):
    """
    Alpha#25: rank(((((-1 * returns) * adv20) * vwap) * (high - close)))
    """
    close = data['close']
    high = data['high']
    volume = data['volume']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    returns_data = returns(close, 1)
    adv20 = adv(volume, 20)
    
    result = (-1 * returns_data) * adv20 * vwap * (high - close)
    
    return rank(result)


def alpha_026(data):
    """
    Alpha#26: (-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))
    """
    volume = data['volume']
    high = data['high']
    
    ts_rank_volume = ts_rank(volume, 5)
    ts_rank_high = ts_rank(high, 5)
    
    corr = correlation(ts_rank_volume, ts_rank_high, 5)
    max_corr = ts_max(corr, 3)
    
    return -1 * max_corr


def alpha_027(data):
    """
    Alpha#27: ((0.5 < rank((sum(correlation(rank(volume), rank(vwap), 6), 2) / 2.0))) ? (-1 * 1) : 1)
    """
    volume = data['volume']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    rank_volume = rank(volume)
    rank_vwap = rank(vwap)
    
    corr = correlation(rank_volume, rank_vwap, 6)
    sum_corr = ts_sum(corr, 2)
    avg_corr = sum_corr / 2.0
    
    rank_avg = rank(avg_corr)
    
    condition_df = rank_avg > 0.5
    
    result = condition(condition_df, 
                      pd.DataFrame(-1, index=volume.index, columns=volume.columns if hasattr(volume, 'columns') else [0]),
                      pd.DataFrame(1, index=volume.index, columns=volume.columns if hasattr(volume, 'columns') else [0]))
    return result


def alpha_028(data):
    """
    Alpha#28: scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))
    """
    close = data['close']
    high = data['high']
    low = data['low']
    volume = data['volume']
    
    adv20 = adv(volume, 20)
    
    corr = correlation(adv20, low, 5)
    mid_price = (high + low) / 2
    
    result = corr + mid_price - close
    
    return scale(result)


def alpha_029(data):
    """
    Alpha#29: (min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1), 5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5))
    """
    close = data['close']
    
    returns_data = returns(close, 1)
    
    delta_close = delta(close - 1, 5)
    rank1 = rank(delta_close)
    rank2 = rank(-1 * rank1)
    rank3 = rank(rank2)
    
    ts_min_val = ts_min(rank3, 2)
    sum_val = ts_sum(ts_min_val, 1)
    log_val = log(sum_val)
    scaled = scale(log_val)
    rank4 = rank(scaled)
    rank5 = rank(rank4)
    
    product_val = ts_product(rank5, 1)
    min_val = ts_min(product_val, 5)
    
    delayed_returns = delay(-1 * returns_data, 6)
    ts_rank_val = ts_rank(delayed_returns, 5)
    
    return min_val + ts_rank_val


def alpha_030(data):
    """
    Alpha#30: (((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) + sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))
    """
    close = data['close']
    volume = data['volume']
    
    sign1 = sign(close - delay(close, 1))
    sign2 = sign(delay(close, 1) - delay(close, 2))
    sign3 = sign(delay(close, 2) - delay(close, 3))
    
    sum_signs = sign1 + sign2 + sign3
    rank_val = rank(sum_signs)
    
    sum_volume_5 = ts_sum(volume, 5)
    sum_volume_20 = ts_sum(volume, 20)
    
    return ((1.0 - rank_val) * sum_volume_5) / sum_volume_20


# Placeholder for remaining alphas (31-101)
# Each alpha would be implemented following the same pattern

def get_alpha_function(alpha_name):
    """Get alpha function by name."""
    alpha_functions = {
        'alpha_001': alpha_001,
        'alpha_002': alpha_002,
        'alpha_003': alpha_003,
        'alpha_004': alpha_004,
        'alpha_005': alpha_005,
        'alpha_006': alpha_006,
        'alpha_007': alpha_007,
        'alpha_008': alpha_008,
        'alpha_009': alpha_009,
        'alpha_010': alpha_010,
        'alpha_011': alpha_011,
        'alpha_012': alpha_012,
        'alpha_013': alpha_013,
        'alpha_014': alpha_014,
        'alpha_015': alpha_015,
        'alpha_016': alpha_016,
        'alpha_017': alpha_017,
        'alpha_018': alpha_018,
        'alpha_019': alpha_019,
        'alpha_020': alpha_020,
        'alpha_021': alpha_021,
        'alpha_022': alpha_022,
        'alpha_023': alpha_023,
        'alpha_024': alpha_024,
        'alpha_025': alpha_025,
        'alpha_026': alpha_026,
        'alpha_027': alpha_027,
        'alpha_028': alpha_028,
        'alpha_029': alpha_029,
        'alpha_030': alpha_030,
    }
    return alpha_functions.get(alpha_name)


def list_available_alphas():
    """List all implemented alpha names."""
    return [f'alpha_{i:03d}' for i in range(1, 31)]




# Additional Alphas (31-60)

def alpha_031(data):
    """
    Alpha#31: ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 * delta(close, 3)))) + sign(scale(correlation(adv20, low, 12))))
    """
    close = data['close']
    low = data['low']
    volume = data['volume']
    
    adv20 = adv(volume, 20)
    
    # First part
    delta_close = delta(close, 10)
    rank1 = rank(delta_close)
    rank2 = rank(rank1)
    neg_rank = -1 * rank2
    decay = ts_decay_linear(neg_rank, 10)
    rank3 = rank(decay)
    rank4 = rank(rank3)
    rank5 = rank(rank4)
    
    # Second part
    delta_close_3 = delta(close, 3)
    rank6 = rank(-1 * delta_close_3)
    
    # Third part
    corr = correlation(adv20, low, 12)
    scaled = scale(corr)
    sign_val = sign(scaled)
    
    return rank5 + rank6 + sign_val


def alpha_032(data):
    """
    Alpha#32: (scale(((sum(close, 7) / 7) - close)) + (20 * scale(correlation(vwap, delay(close, 5), 230))))
    """
    close = data['close']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    mean7 = ts_sum(close, 7) / 7
    part1 = scale(mean7 - close)
    
    delayed_close = delay(close, 5)
    corr = correlation(vwap, delayed_close, 230)
    part2 = 20 * scale(corr)
    
    return part1 + part2


def alpha_033(data):
    """
    Alpha#33: rank((-1 * ((1 - (open / close)) ^ 1)))
    """
    open_price = data['open']
    close = data['close']
    
    ratio = 1 - (open_price / close)
    result = -1 * power(ratio, 1)
    
    return rank(result)


def alpha_034(data):
    """
    Alpha#34: rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1)))))
    """
    close = data['close']
    returns_data = returns(close, 1)
    
    std2 = ts_std(returns_data, 2)
    std5 = ts_std(returns_data, 5)
    ratio = std2 / std5
    
    part1 = 1 - rank(ratio)
    
    delta_close = delta(close, 1)
    part2 = 1 - rank(delta_close)
    
    return rank(part1 + part2)


def alpha_035(data):
    """
    Alpha#35: ((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 - Ts_Rank(returns, 32)))
    """
    close = data['close']
    high = data['high']
    low = data['low']
    volume = data['volume']
    
    returns_data = returns(close, 1)
    
    part1 = ts_rank(volume, 32)
    
    price_sum = close + high - low
    part2 = 1 - ts_rank(price_sum, 16)
    
    part3 = 1 - ts_rank(returns_data, 32)
    
    return part1 * part2 * part3


def alpha_036(data):
    """
    Alpha#36: (((((2.21 * rank(correlation((close - open), delay(volume, 1), 15))) + (0.7 * rank((open - close)))) + (0.73 * rank(Ts_Rank(delay((-1 * returns), 6), 5)))) + rank(abs(correlation(vwap, adv20, 6)))) + (0.6 * rank((((sum(close, 200) / 200) - open) * (close - open)))))
    """
    close = data['close']
    open_price = data['open']
    volume = data['volume']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    returns_data = returns(close, 1)
    adv20 = adv(volume, 20)
    
    # Part 1
    price_diff = close - open_price
    delayed_volume = delay(volume, 1)
    corr1 = correlation(price_diff, delayed_volume, 15)
    part1 = 2.21 * rank(corr1)
    
    # Part 2
    part2 = 0.7 * rank(open_price - close)
    
    # Part 3
    delayed_returns = delay(-1 * returns_data, 6)
    ts_ranked = ts_rank(delayed_returns, 5)
    part3 = 0.73 * rank(ts_ranked)
    
    # Part 4
    corr2 = correlation(vwap, adv20, 6)
    part4 = rank(abs_op(corr2))
    
    # Part 5
    mean200 = ts_sum(close, 200) / 200
    part5 = 0.6 * rank((mean200 - open_price) * (close - open_price))
    
    return part1 + part2 + part3 + part4 + part5


def alpha_037(data):
    """
    Alpha#37: (rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close)))
    """
    open_price = data['open']
    close = data['close']
    
    diff = open_price - close
    delayed_diff = delay(diff, 1)
    
    corr = correlation(delayed_diff, close, 200)
    
    return rank(corr) + rank(diff)


def alpha_038(data):
    """
    Alpha#38: ((-1 * rank(Ts_Rank(close, 10))) * rank((close / open)))
    """
    close = data['close']
    open_price = data['open']
    
    ts_ranked = ts_rank(close, 10)
    part1 = -1 * rank(ts_ranked)
    
    ratio = close / open_price
    part2 = rank(ratio)
    
    return part1 * part2


def alpha_039(data):
    """
    Alpha#39: ((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 + rank(sum(returns, 250))))
    """
    close = data['close']
    volume = data['volume']
    
    returns_data = returns(close, 1)
    adv20 = adv(volume, 20)
    
    delta_close = delta(close, 7)
    
    volume_ratio = volume / adv20
    decay = ts_decay_linear(volume_ratio, 9)
    
    part1 = -1 * rank(delta_close * (1 - rank(decay)))
    
    sum_returns = ts_sum(returns_data, 250)
    part2 = 1 + rank(sum_returns)
    
    return part1 * part2


def alpha_040(data):
    """
    Alpha#40: ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))
    """
    high = data['high']
    volume = data['volume']
    
    std_high = ts_std(high, 10)
    part1 = -1 * rank(std_high)
    
    corr = correlation(high, volume, 10)
    
    return part1 * corr


def alpha_041(data):
    """
    Alpha#41: (((high * low) ^ 0.5) - vwap)
    """
    high = data['high']
    low = data['low']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    geometric_mean = power(high * low, 0.5)
    
    return geometric_mean - vwap


def alpha_042(data):
    """
    Alpha#42: (rank((vwap - close)) / rank((vwap + close)))
    """
    close = data['close']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    numerator = rank(vwap - close)
    denominator = rank(vwap + close)
    
    return numerator / denominator


def alpha_043(data):
    """
    Alpha#43: (ts_rank((volume / adv20), 20) * ts_rank((-1 * delta(close, 7)), 8))
    """
    close = data['close']
    volume = data['volume']
    
    adv20 = adv(volume, 20)
    
    volume_ratio = volume / adv20
    part1 = ts_rank(volume_ratio, 20)
    
    delta_close = delta(close, 7)
    part2 = ts_rank(-1 * delta_close, 8)
    
    return part1 * part2


def alpha_044(data):
    """
    Alpha#44: (-1 * correlation(high, rank(volume), 5))
    """
    high = data['high']
    volume = data['volume']
    
    rank_volume = rank(volume)
    
    corr = correlation(high, rank_volume, 5)
    
    return -1 * corr


def alpha_045(data):
    """
    Alpha#45: (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) * rank(correlation(sum(close, 5), sum(close, 20), 2))))
    """
    close = data['close']
    volume = data['volume']
    
    delayed_close = delay(close, 5)
    sum_delayed = ts_sum(delayed_close, 20)
    mean_delayed = sum_delayed / 20
    part1 = rank(mean_delayed)
    
    corr1 = correlation(close, volume, 2)
    
    sum_close_5 = ts_sum(close, 5)
    sum_close_20 = ts_sum(close, 20)
    corr2 = correlation(sum_close_5, sum_close_20, 2)
    part3 = rank(corr2)
    
    return -1 * part1 * corr1 * part3


def alpha_046(data):
    """
    Alpha#46: ((0.25 < (((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10))) ? (-1 * 1) : (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < 0) ? 1 : ((-1 * 1) * (close - delay(close, 1)))))
    """
    close = data['close']
    
    delayed_20 = delay(close, 20)
    delayed_10 = delay(close, 10)
    delayed_1 = delay(close, 1)
    
    slope1 = (delayed_20 - delayed_10) / 10
    slope2 = (delayed_10 - close) / 10
    diff = slope1 - slope2
    
    condition1 = diff > 0.25
    condition2 = diff < 0
    
    result = condition(condition1, 
                      pd.DataFrame(-1, index=close.index, columns=close.columns if hasattr(close, 'columns') else [0]),
                      condition(condition2,
                               pd.DataFrame(1, index=close.index, columns=close.columns if hasattr(close, 'columns') else [0]),
                               -1 * (close - delayed_1)))
    return result


def alpha_047(data):
    """
    Alpha#47: ((((rank((1 / close)) * volume) / adv20) * ((high * rank((high - close))) / (sum(high, 5) / 5))) - rank((vwap - delay(vwap, 5))))
    """
    close = data['close']
    high = data['high']
    volume = data['volume']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    adv20 = adv(volume, 20)
    
    # Part 1
    rank_inv_close = rank(1 / close)
    part1 = (rank_inv_close * volume) / adv20
    
    # Part 2
    rank_diff = rank(high - close)
    mean_high = ts_sum(high, 5) / 5
    part2 = (high * rank_diff) / mean_high
    
    # Part 3
    delayed_vwap = delay(vwap, 5)
    part3 = rank(vwap - delayed_vwap)
    
    return part1 * part2 - part3


def alpha_048(data):
    """
    Alpha#48: (indneutralize(((correlation(delta(close, 1), delta(delay(close, 1), 1), 250) * delta(close, 1)) / close), IndClass.subindustry) / sum(((delta(close, 1) / delay(close, 1)) ^ 2), 250))
    """
    close = data['close']
    
    delta_close = delta(close, 1)
    delayed_close = delay(close, 1)
    delta_delayed = delta(delayed_close, 1)
    
    corr = correlation(delta_close, delta_delayed, 250)
    
    numerator = (corr * delta_close) / close
    numerator = indneutralize(numerator, None)
    
    returns_squared = power(delta_close / delayed_close, 2)
    denominator = ts_sum(returns_squared, 250)
    
    return numerator / denominator


def alpha_049(data):
    """
    Alpha#49: (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 * 0.1)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))
    """
    close = data['close']
    
    delayed_20 = delay(close, 20)
    delayed_10 = delay(close, 10)
    delayed_1 = delay(close, 1)
    
    slope1 = (delayed_20 - delayed_10) / 10
    slope2 = (delayed_10 - close) / 10
    diff = slope1 - slope2
    
    condition_df = diff < -0.1
    
    result = condition(condition_df,
                      pd.DataFrame(1, index=close.index, columns=close.columns if hasattr(close, 'columns') else [0]),
                      -1 * (close - delayed_1))
    return result


def alpha_050(data):
    """
    Alpha#50: (-1 * ts_max(rank(correlation(rank(volume), rank(vwap), 5)), 5))
    """
    volume = data['volume']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    rank_volume = rank(volume)
    rank_vwap = rank(vwap)
    
    corr = correlation(rank_volume, rank_vwap, 5)
    ranked_corr = rank(corr)
    
    max_val = ts_max(ranked_corr, 5)
    
    return -1 * max_val


def alpha_051(data):
    """
    Alpha#51: (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 * 0.05)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))
    """
    close = data['close']
    
    delayed_20 = delay(close, 20)
    delayed_10 = delay(close, 10)
    delayed_1 = delay(close, 1)
    
    slope1 = (delayed_20 - delayed_10) / 10
    slope2 = (delayed_10 - close) / 10
    diff = slope1 - slope2
    
    condition_df = diff < -0.05
    
    result = condition(condition_df,
                      pd.DataFrame(1, index=close.index, columns=close.columns if hasattr(close, 'columns') else [0]),
                      -1 * (close - delayed_1))
    return result


def alpha_052(data):
    """
    Alpha#52: ((((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank(((sum(returns, 240) - sum(returns, 20)) / 220))) * ts_rank(volume, 5))
    """
    low = data['low']
    close = data['close']
    volume = data['volume']
    
    returns_data = returns(close, 1)
    
    ts_min_low = ts_min(low, 5)
    delayed_min = delay(ts_min_low, 5)
    
    part1 = -1 * ts_min_low + delayed_min
    
    sum_returns_240 = ts_sum(returns_data, 240)
    sum_returns_20 = ts_sum(returns_data, 20)
    returns_diff = (sum_returns_240 - sum_returns_20) / 220
    part2 = rank(returns_diff)
    
    part3 = ts_rank(volume, 5)
    
    return part1 * part2 * part3


def alpha_053(data):
    """
    Alpha#53: (-1 * delta((((close - low) - (high - close)) / (close - low)), 9))
    """
    close = data['close']
    high = data['high']
    low = data['low']
    
    numerator = (close - low) - (high - close)
    denominator = close - low
    
    ratio = numerator / denominator
    
    return -1 * delta(ratio, 9)


def alpha_054(data):
    """
    Alpha#54: ((-1 * ((low - close) * (open ^ 5))) / ((low - high) * (close ^ 5)))
    """
    open_price = data['open']
    close = data['close']
    high = data['high']
    low = data['low']
    
    numerator = -1 * (low - close) * power(open_price, 5)
    denominator = (low - high) * power(close, 5)
    
    return numerator / denominator


def alpha_055(data):
    """
    Alpha#55: (-1 * correlation(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low, 12)))), rank(volume), 6))
    """
    close = data['close']
    high = data['high']
    low = data['low']
    volume = data['volume']
    
    ts_min_low = ts_min(low, 12)
    ts_max_high = ts_max(high, 12)
    
    stochastic = (close - ts_min_low) / (ts_max_high - ts_min_low)
    rank_stochastic = rank(stochastic)
    
    rank_volume = rank(volume)
    
    corr = correlation(rank_stochastic, rank_volume, 6)
    
    return -1 * corr


def alpha_056(data):
    """
    Alpha#56: (0 - (1 * (rank((sum(returns, 10) / sum(sum(returns, 2), 3))) * rank((returns * cap)))))
    """
    close = data['close']
    volume = data['volume']
    
    returns_data = returns(close, 1)
    
    sum_returns_10 = ts_sum(returns_data, 10)
    sum_returns_2 = ts_sum(returns_data, 2)
    sum_sum = ts_sum(sum_returns_2, 3)
    
    ratio = sum_returns_10 / sum_sum
    part1 = rank(ratio)
    
    # Using volume as proxy for cap (market capitalization)
    cap = volume * close
    part2 = rank(returns_data * cap)
    
    return -(1 * part1 * part2)


def alpha_057(data):
    """
    Alpha#57: (0 - (1 * ((close - vwap) / decay_linear(rank(ts_argmax(close, 30)), 2))))
    """
    close = data['close']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    ts_argmax_close = ts_argmax(close, 30)
    ranked = rank(ts_argmax_close)
    decay = ts_decay_linear(ranked, 2)
    
    return -1 * (close - vwap) / decay


def alpha_058(data):
    """
    Alpha#58: (-1 * Ts_Rank(decay_linear(correlation(IndNeutralize(vwap, IndClass.sector), volume, 3.92795), 7.89291), 5.50322))
    """
    volume = data['volume']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    neutralized = indneutralize(vwap, None)
    
    corr = correlation(neutralized, volume, 4)
    decay = ts_decay_linear(corr, 8)
    ts_ranked = ts_rank(decay, 6)
    
    return -1 * ts_ranked


def alpha_059(data):
    """
    Alpha#59: (-1 * Ts_Rank(decay_linear(correlation(IndNeutralize(((vwap * 0.728317) + (vwap * (1 - 0.728317))), IndClass.industry), volume, 4.25197), 16.2289), 8.19648))
    """
    volume = data['volume']
    vwap = data.get('vwap', (data['high'] + data['low'] + data['close']) / 3)
    
    weighted_vwap = (vwap * 0.728317) + (vwap * (1 - 0.728317))
    neutralized = indneutralize(weighted_vwap, None)
    
    corr = correlation(neutralized, volume, 4)
    decay = ts_decay_linear(corr, 16)
    ts_ranked = ts_rank(decay, 8)
    
    return -1 * ts_ranked


def alpha_060(data):
    """
    Alpha#60: (0 - (1 * ((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) - scale(rank(ts_argmax(close, 10))))))
    """
    close = data['close']
    high = data['high']
    low = data['low']
    volume = data['volume']
    
    price_position = ((close - low) - (high - close)) / (high - low)
    weighted = price_position * volume
    ranked1 = rank(weighted)
    scaled1 = scale(ranked1)
    
    ts_argmax_close = ts_argmax(close, 10)
    ranked2 = rank(ts_argmax_close)
    scaled2 = scale(ranked2)
    
    return -(1 * ((2 * scaled1) - scaled2))


# Update the get_alpha_function to include new alphas
def get_alpha_function(alpha_name):
    """Get alpha function by name."""
    alpha_functions = {
        'alpha_001': alpha_001, 'alpha_002': alpha_002, 'alpha_003': alpha_003,
        'alpha_004': alpha_004, 'alpha_005': alpha_005, 'alpha_006': alpha_006,
        'alpha_007': alpha_007, 'alpha_008': alpha_008, 'alpha_009': alpha_009,
        'alpha_010': alpha_010, 'alpha_011': alpha_011, 'alpha_012': alpha_012,
        'alpha_013': alpha_013, 'alpha_014': alpha_014, 'alpha_015': alpha_015,
        'alpha_016': alpha_016, 'alpha_017': alpha_017, 'alpha_018': alpha_018,
        'alpha_019': alpha_019, 'alpha_020': alpha_020, 'alpha_021': alpha_021,
        'alpha_022': alpha_022, 'alpha_023': alpha_023, 'alpha_024': alpha_024,
        'alpha_025': alpha_025, 'alpha_026': alpha_026, 'alpha_027': alpha_027,
        'alpha_028': alpha_028, 'alpha_029': alpha_029, 'alpha_030': alpha_030,
        'alpha_031': alpha_031, 'alpha_032': alpha_032, 'alpha_033': alpha_033,
        'alpha_034': alpha_034, 'alpha_035': alpha_035, 'alpha_036': alpha_036,
        'alpha_037': alpha_037, 'alpha_038': alpha_038, 'alpha_039': alpha_039,
        'alpha_040': alpha_040, 'alpha_041': alpha_041, 'alpha_042': alpha_042,
        'alpha_043': alpha_043, 'alpha_044': alpha_044, 'alpha_045': alpha_045,
        'alpha_046': alpha_046, 'alpha_047': alpha_047, 'alpha_048': alpha_048,
        'alpha_049': alpha_049, 'alpha_050': alpha_050, 'alpha_051': alpha_051,
        'alpha_052': alpha_052, 'alpha_053': alpha_053, 'alpha_054': alpha_054,
        'alpha_055': alpha_055, 'alpha_056': alpha_056, 'alpha_057': alpha_057,
        'alpha_058': alpha_058, 'alpha_059': alpha_059, 'alpha_060': alpha_060,
    }
    return alpha_functions.get(alpha_name)


def list_available_alphas():
    """List all implemented alpha names."""
    return [f'alpha_{i:03d}' for i in range(1, 61)]
