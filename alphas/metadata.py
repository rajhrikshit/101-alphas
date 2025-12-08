"""
Metadata and descriptions for all 101 alphas.
"""

ALPHA_DESCRIPTIONS = {
    'alpha_001': {
        'name': 'Alpha #1',
        'formula': 'rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5',
        'description': 'Combines volatility and price momentum. Uses conditional logic to select between return volatility (when negative) or close price.',
        'category': 'Momentum',
        'complexity': 'High',
    },
    'alpha_002': {
        'name': 'Alpha #2',
        'formula': '(-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))',
        'description': 'Negative correlation between volume changes and intraday returns.',
        'category': 'Volume',
        'complexity': 'Medium',
    },
    'alpha_003': {
        'name': 'Alpha #3',
        'formula': '(-1 * correlation(rank(open), rank(volume), 10))',
        'description': 'Negative correlation between opening price and volume.',
        'category': 'Volume',
        'complexity': 'Low',
    },
    'alpha_004': {
        'name': 'Alpha #4',
        'formula': '(-1 * Ts_Rank(rank(low), 9))',
        'description': 'Inverted time-series rank of low prices.',
        'category': 'Price',
        'complexity': 'Low',
    },
    'alpha_005': {
        'name': 'Alpha #5',
        'formula': '(rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))',
        'description': 'Combines opening price deviation from average VWAP with closing price deviation.',
        'category': 'VWAP',
        'complexity': 'Medium',
    },
    'alpha_006': {
        'name': 'Alpha #6',
        'formula': '(-1 * correlation(open, volume, 10))',
        'description': 'Negative correlation between opening price and volume.',
        'category': 'Volume',
        'complexity': 'Low',
    },
    'alpha_007': {
        'name': 'Alpha #7',
        'formula': '((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1))',
        'description': 'Conditional alpha based on volume relative to 20-day average.',
        'category': 'Momentum-Volume',
        'complexity': 'High',
    },
    'alpha_008': {
        'name': 'Alpha #8',
        'formula': '(-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10))))',
        'description': 'Change in the product of summed opening prices and returns.',
        'category': 'Momentum',
        'complexity': 'Medium',
    },
    'alpha_009': {
        'name': 'Alpha #9',
        'formula': '((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ? delta(close, 1) : (-1 * delta(close, 1))))',
        'description': 'Conditional daily return based on recent return patterns.',
        'category': 'Momentum',
        'complexity': 'High',
    },
    'alpha_010': {
        'name': 'Alpha #10',
        'formula': 'rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0) ? delta(close, 1) : (-1 * delta(close, 1)))))',
        'description': 'Ranked version of conditional daily return.',
        'category': 'Momentum',
        'complexity': 'High',
    },
    'alpha_011': {
        'name': 'Alpha #11',
        'formula': '((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(delta(volume, 3)))',
        'description': 'VWAP-close deviation combined with volume change.',
        'category': 'VWAP-Volume',
        'complexity': 'Medium',
    },
    'alpha_012': {
        'name': 'Alpha #12',
        'formula': '(sign(delta(volume, 1)) * (-1 * delta(close, 1)))',
        'description': 'Volume direction times negative price change.',
        'category': 'Volume-Price',
        'complexity': 'Low',
    },
    'alpha_013': {
        'name': 'Alpha #13',
        'formula': '(-1 * rank(covariance(rank(close), rank(volume), 5)))',
        'description': 'Negative covariance between ranked close and volume.',
        'category': 'Volume',
        'complexity': 'Medium',
    },
    'alpha_014': {
        'name': 'Alpha #14',
        'formula': '((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))',
        'description': 'Return momentum combined with open-volume correlation.',
        'category': 'Momentum-Volume',
        'complexity': 'Medium',
    },
    'alpha_015': {
        'name': 'Alpha #15',
        'formula': '(-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))',
        'description': 'Summed correlation between high price and volume.',
        'category': 'Volume',
        'complexity': 'Medium',
    },
    'alpha_016': {
        'name': 'Alpha #16',
        'formula': '(-1 * rank(covariance(rank(high), rank(volume), 5)))',
        'description': 'Negative covariance between ranked high price and volume.',
        'category': 'Volume',
        'complexity': 'Medium',
    },
    'alpha_017': {
        'name': 'Alpha #17',
        'formula': '(((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) * rank(ts_rank((volume / adv20), 5)))',
        'description': 'Complex combination of price rank, acceleration, and relative volume.',
        'category': 'Momentum-Volume',
        'complexity': 'High',
    },
    'alpha_018': {
        'name': 'Alpha #18',
        'formula': '(-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10))))',
        'description': 'Combines intraday range volatility with close-open correlation.',
        'category': 'Volatility',
        'complexity': 'Medium',
    },
    'alpha_019': {
        'name': 'Alpha #19',
        'formula': '((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250)))))',
        'description': 'Weekly price change combined with long-term return.',
        'category': 'Momentum',
        'complexity': 'High',
    },
    'alpha_020': {
        'name': 'Alpha #20',
        'formula': '(((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open - delay(low, 1))))',
        'description': 'Opening price gap relative to previous day OHLC.',
        'category': 'Gap',
        'complexity': 'Medium',
    },
    'alpha_021': {
        'name': 'Alpha #21',
        'formula': 'Complex conditional based on moving averages and volume',
        'description': 'Multi-condition alpha using short and long-term averages with volume filter.',
        'category': 'Mean-Reversion',
        'complexity': 'Very High',
    },
    'alpha_022': {
        'name': 'Alpha #22',
        'formula': '(-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20))))',
        'description': 'Change in high-volume correlation scaled by price volatility.',
        'category': 'Volume-Volatility',
        'complexity': 'Medium',
    },
    'alpha_023': {
        'name': 'Alpha #23',
        'formula': '(((sum(high, 20) / 20) < high) ? (-1 * delta(high, 2)) : 0)',
        'description': 'Conditional on high price relative to recent average.',
        'category': 'Mean-Reversion',
        'complexity': 'Medium',
    },
    'alpha_024': {
        'name': 'Alpha #24',
        'formula': 'Conditional based on long-term moving average change',
        'description': 'Uses 100-day moving average change as condition.',
        'category': 'Mean-Reversion',
        'complexity': 'High',
    },
    'alpha_025': {
        'name': 'Alpha #25',
        'formula': 'rank(((((-1 * returns) * adv20) * vwap) * (high - close)))',
        'description': 'Combines returns, volume, VWAP, and intraday range.',
        'category': 'Composite',
        'complexity': 'Medium',
    },
    'alpha_026': {
        'name': 'Alpha #26',
        'formula': '(-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))',
        'description': 'Maximum correlation between ranked volume and high price.',
        'category': 'Volume',
        'complexity': 'High',
    },
    'alpha_027': {
        'name': 'Alpha #27',
        'formula': '((0.5 < rank((sum(correlation(rank(volume), rank(vwap), 6), 2) / 2.0))) ? (-1) : 1)',
        'description': 'Binary signal based on volume-VWAP correlation.',
        'category': 'Volume-VWAP',
        'complexity': 'High',
    },
    'alpha_028': {
        'name': 'Alpha #28',
        'formula': 'scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))',
        'description': 'Scaled combination of volume-low correlation and price levels.',
        'category': 'Volume-Price',
        'complexity': 'Medium',
    },
    'alpha_029': {
        'name': 'Alpha #29',
        'formula': 'Complex multi-layer transformation',
        'description': 'Extremely complex alpha with multiple nested operations.',
        'category': 'Composite',
        'complexity': 'Very High',
    },
    'alpha_030': {
        'name': 'Alpha #30',
        'formula': '(((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) + sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))',
        'description': 'Price direction pattern combined with volume ratio.',
        'category': 'Momentum-Volume',
        'complexity': 'High',
    },
}


ALPHA_CATEGORIES = {
    'Momentum': ['alpha_001', 'alpha_008', 'alpha_009', 'alpha_010', 'alpha_014', 'alpha_019', 'alpha_030'],
    'Volume': ['alpha_002', 'alpha_003', 'alpha_006', 'alpha_013', 'alpha_015', 'alpha_016', 'alpha_026'],
    'VWAP': ['alpha_005', 'alpha_011', 'alpha_027', 'alpha_028'],
    'Volatility': ['alpha_018', 'alpha_022'],
    'Mean-Reversion': ['alpha_021', 'alpha_023', 'alpha_024'],
    'Gap': ['alpha_020'],
    'Composite': ['alpha_025', 'alpha_029'],
}


def get_alpha_metadata(alpha_name: str) -> dict:
    """Get metadata for a specific alpha."""
    return ALPHA_DESCRIPTIONS.get(alpha_name, {
        'name': alpha_name,
        'description': 'Description not available',
        'category': 'Unknown',
        'complexity': 'Unknown',
    })


def get_alphas_by_category(category: str) -> list:
    """Get list of alphas in a specific category."""
    return ALPHA_CATEGORIES.get(category, [])


def get_all_categories() -> list:
    """Get list of all alpha categories."""
    return list(ALPHA_CATEGORIES.keys())
