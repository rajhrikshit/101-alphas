# Quick Start Guide

Get up and running with the 101 Alphas Framework in minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/rajhrikshit/101-alphas.git
cd 101-alphas

# Install dependencies
pip install -r requirements.txt
```

## Launch the Dashboard

The easiest way to start is with the interactive dashboard:

```bash
streamlit run dashboard/app.py
```

This will open your browser to `http://localhost:8501` where you can:
1. Upload your own OHLCV data or generate sample data
2. Select alphas to calculate
3. Visualize and analyze results
4. Export calculated alpha values

## Using the Python API

### Basic Example

```python
from alphas import AlphaEngine
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv')

# Create engine
engine = AlphaEngine(data)

# Calculate a single alpha
alpha_1 = engine.calculate('alpha_001')
print(alpha_1.head())
```

### Calculate Multiple Alphas

```python
# Calculate specific alphas
alphas = engine.calculate_batch(['alpha_001', 'alpha_002', 'alpha_003'])
print(alphas.describe())

# Calculate all available alphas
all_alphas = engine.calculate_all()
```

### Browse Alphas by Category

```python
from alphas.metadata import get_alphas_by_category, get_all_categories

# See all categories
categories = get_all_categories()
print(categories)  # ['Momentum', 'Volume', 'VWAP', 'Volatility', ...]

# Get alphas in a category
momentum_alphas = get_alphas_by_category('Momentum')
results = engine.calculate_batch(momentum_alphas)
```

## Data Format

Your data must include these columns:
- `date`: Trading date (datetime format)
- `open`: Opening price
- `high`: Highest price
- `low`: Lowest price
- `close`: Closing price
- `volume`: Trading volume
- `symbol` (optional): Stock identifier for multi-asset data

### Single Stock Example

```csv
date,open,high,low,close,volume
2023-01-01,100.0,102.0,99.0,101.0,1000000
2023-01-02,101.0,103.0,100.0,102.0,1100000
2023-01-03,102.0,104.0,101.0,103.0,1050000
```

### Multiple Stocks Example

```csv
date,symbol,open,high,low,close,volume
2023-01-01,AAPL,150.0,152.0,149.0,151.0,1000000
2023-01-01,MSFT,250.0,252.0,248.0,251.0,800000
2023-01-02,AAPL,151.0,153.0,150.0,152.0,1100000
2023-01-02,MSFT,251.0,254.0,250.0,253.0,850000
```

## Understanding Alphas

### What are Alphas?

Alphas are mathematical formulas that combine market data (price, volume) to generate trading signals. The 101 alphas come from academic research and represent various trading strategies.

### Alpha Categories

1. **Momentum**: Trend-following signals based on price movement
2. **Volume**: Signals derived from trading volume patterns
3. **VWAP**: Using Volume-Weighted Average Price
4. **Volatility**: Based on price volatility measures
5. **Mean-Reversion**: Identifying overbought/oversold conditions
6. **Gap**: Analysis of opening gaps
7. **Composite**: Complex combinations of multiple factors

### Example: Understanding Alpha #1

```python
from alphas.metadata import get_alpha_metadata

info = get_alpha_metadata('alpha_001')
print(f"Name: {info['name']}")
print(f"Category: {info['category']}")
print(f"Description: {info['description']}")
print(f"Formula: {info['formula']}")
```

## Visualizing Results

### Time Series Plot

```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=alpha_1.index,
    y=alpha_1['alpha_001'],
    name='Alpha #1'
))
fig.show()
```

### Correlation Heatmap

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Calculate multiple alphas
alphas = engine.calculate_batch(['alpha_001', 'alpha_004', 'alpha_012'])

# Plot correlation
sns.heatmap(alphas.corr(), annot=True, cmap='coolwarm')
plt.show()
```

## Common Use Cases

### 1. Backtesting a Single Alpha

```python
# Calculate alpha
alpha_values = engine.calculate('alpha_001')

# Get returns
returns = data['close'].pct_change()

# Simple strategy: long when alpha > 0
strategy_returns = returns.where(alpha_values > 0, -returns)
cumulative_return = (1 + strategy_returns).cumprod()
```

### 2. Finding Best Alphas

```python
# Calculate all alphas
all_alphas = engine.calculate_all()

# Calculate correlation with forward returns
forward_returns = data['close'].pct_change(5).shift(-5)

correlations = {}
for alpha in all_alphas.columns:
    corr = all_alphas[alpha].corr(forward_returns)
    correlations[alpha] = abs(corr)

# Sort by absolute correlation
best_alphas = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
print("Top 10 alphas:")
for alpha, corr in best_alphas[:10]:
    print(f"{alpha}: {corr:.4f}")
```

### 3. Combining Multiple Alphas

```python
# Calculate several alphas
selected = ['alpha_001', 'alpha_004', 'alpha_012', 'alpha_018']
alphas = engine.calculate_batch(selected)

# Equal-weight combination
combined_alpha = alphas.mean(axis=1)

# Or use correlation-based weights
corr_matrix = alphas.corr()
# ... implement your weighting scheme
```

## Troubleshooting

### Issue: "Missing required columns"
**Solution**: Ensure your data has all required columns: open, high, low, close, volume

### Issue: "NaN values in results"
**Solution**: Most alphas need 60-250 days of historical data. Ensure you have enough data.

### Issue: "Alpha calculation fails"
**Solution**: Some alphas require specific data characteristics. Check for:
- No zero or negative prices
- No missing data gaps
- Sufficient history

## Next Steps

1. Read the [Alpha Descriptions](alpha_descriptions.md) to understand each formula
2. Check the [API Reference](api_reference.md) for detailed documentation
3. Explore [Examples](examples.md) for advanced usage patterns
4. Experiment with the dashboard to visualize different alphas

## Getting Help

- Check the documentation in the `docs/` directory
- Review the examples in `docs/examples.md`
- Run the tests: `python -m unittest tests.test_alphas`

## Performance Tips

1. Calculate alphas in batches rather than one at a time
2. Use smaller date ranges for initial experimentation
3. Start with simpler alphas before trying complex ones
4. Cache results if analyzing the same data multiple times

Happy alpha hunting! 🚀📈
