# Alpha Descriptions

This document provides detailed descriptions of all implemented alphas from the "101 Formulaic Alphas" paper.

## Overview

The 101 alphas are quantitative trading signals that combine various market data features (price, volume, etc.) using mathematical operators to predict future returns or identify trading opportunities.

## Categories

### Momentum Alphas
Capture price momentum and trend-following signals.
- Alpha #1, #8, #9, #10, #14, #19, #30

### Volume Alphas
Focus on trading volume patterns and relationships.
- Alpha #2, #3, #6, #13, #15, #16, #26

### VWAP Alphas
Utilize Volume-Weighted Average Price.
- Alpha #5, #11, #27, #28

### Volatility Alphas
Measure and exploit volatility patterns.
- Alpha #18, #22

### Mean-Reversion Alphas
Identify overbought/oversold conditions.
- Alpha #21, #23, #24

### Gap Alphas
Analyze opening gaps relative to previous prices.
- Alpha #20

### Composite Alphas
Combine multiple factors.
- Alpha #25, #29

## Alpha Details

### Alpha #1
**Formula:** `rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5`

**Description:** Combines volatility and price momentum using conditional logic. When returns are negative, uses 20-day return volatility; otherwise uses close price. Takes the squared value, finds the time-series argmax over 5 days, ranks it, and centers around zero.

**Use Case:** Identifies stocks with strong recent momentum patterns, accounting for volatility during down periods.

### Alpha #2
**Formula:** `(-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))`

**Description:** Negative correlation between changes in log volume and intraday returns over 6 days.

**Use Case:** Detects inverse relationships between volume changes and price movement within the day.

### Alpha #3
**Formula:** `(-1 * correlation(rank(open), rank(volume), 10))`

**Description:** Negative 10-day correlation between opening price rank and volume rank.

**Use Case:** Identifies stocks where high opening prices correspond to low volume (or vice versa).

### Alpha #4
**Formula:** `(-1 * Ts_Rank(rank(low), 9))`

**Description:** Inverted 9-day time-series rank of ranked low prices.

**Use Case:** Finds stocks with recently declining low prices.

### Alpha #5
**Formula:** `(rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))`

**Description:** Opening price deviation from 10-day average VWAP multiplied by absolute closing price deviation from VWAP.

**Use Case:** Identifies price-VWAP relationships that may signal reversals.

## Operator Reference

### Time-Series Operators
- `ts_sum(x, d)`: Sum over past d days
- `ts_mean(x, d)`: Average over past d days
- `ts_std(x, d)`: Standard deviation over past d days
- `ts_rank(x, d)`: Percentile rank over past d days
- `ts_max(x, d)`: Maximum over past d days
- `ts_min(x, d)`: Minimum over past d days
- `ts_argmax(x, d)`: Days since maximum in past d days
- `ts_argmin(x, d)`: Days since minimum in past d days

### Cross-Sectional Operators
- `rank(x)`: Cross-sectional percentile rank
- `scale(x, a)`: Scale to sum to a

### Other Operators
- `delta(x, d)`: x today minus x d days ago
- `delay(x, d)`: Value from d days ago
- `correlation(x, y, d)`: d-day correlation between x and y
- `covariance(x, y, d)`: d-day covariance between x and y

### Mathematical Functions
- `sign(x)`: Sign of x (-1, 0, or 1)
- `abs(x)`: Absolute value
- `log(x)`: Natural logarithm
- `power(x, e)`: x raised to power e

## Usage Tips

1. **Data Quality**: Ensure your data is clean and properly formatted
2. **Look-back Period**: Most alphas require 60-250 days of history
3. **Multi-Asset**: Alphas work best on cross-sections of multiple stocks
4. **Combination**: Consider combining multiple alphas for better signals
5. **Transaction Costs**: Account for costs when implementing alphas

## References

Kakushadze, Z. (2016). "101 Formulaic Alphas". Wilmott Magazine, 2016(84), 72-81.
