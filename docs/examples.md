# Examples and Tutorials

## Basic Usage

### Example 1: Single Stock Analysis

```python
import pandas as pd
from alphas import AlphaEngine

# Load single stock data
data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=252),
    'open': [100 + i * 0.1 for i in range(252)],
    'high': [101 + i * 0.1 for i in range(252)],
    'low': [99 + i * 0.1 for i in range(252)],
    'close': [100.5 + i * 0.1 for i in range(252)],
    'volume': [1000000 + i * 1000 for i in range(252)]
})

# Create engine
engine = AlphaEngine(data)

# Calculate alpha
alpha_1 = engine.calculate('alpha_001')
print(alpha_1.tail())
```

### Example 2: Multiple Stocks

```python
import pandas as pd
from alphas import AlphaEngine

# Load multi-stock data
data = pd.read_csv('multi_stock_data.csv')
# Must have columns: date, symbol, open, high, low, close, volume

engine = AlphaEngine(data)

# Calculate alphas
alphas = engine.calculate_batch(['alpha_001', 'alpha_002', 'alpha_003'])

# View results per symbol
print(alphas.head())
```

### Example 3: Category-Based Analysis

```python
from alphas import AlphaEngine
from alphas.metadata import get_alphas_by_category, get_all_categories

# Load data
data = pd.read_csv('market_data.csv')
engine = AlphaEngine(data)

# Analyze by category
for category in get_all_categories():
    print(f"\n{category} Alphas:")
    category_alphas = get_alphas_by_category(category)
    results = engine.calculate_batch(category_alphas)
    
    # Show summary
    print(results.describe())
```

## Advanced Usage

### Example 4: Alpha Correlation Analysis

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from alphas import AlphaEngine

# Load data and calculate alphas
data = pd.read_csv('market_data.csv')
engine = AlphaEngine(data)
results = engine.calculate_all()

# Calculate correlation matrix
corr_matrix = results.corr()

# Plot heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, cmap='coolwarm', center=0, vmin=-1, vmax=1)
plt.title('Alpha Correlation Matrix')
plt.tight_layout()
plt.savefig('alpha_correlation.png')
```

### Example 5: Alpha Performance Comparison

```python
import pandas as pd
import plotly.graph_objects as go
from alphas import AlphaEngine

# Load data
data = pd.read_csv('market_data.csv')
engine = AlphaEngine(data)

# Select alphas to compare
alphas_to_compare = ['alpha_001', 'alpha_002', 'alpha_003']
results = engine.calculate_batch(alphas_to_compare)

# Create comparison plot
fig = go.Figure()
for alpha in alphas_to_compare:
    fig.add_trace(go.Scatter(
        x=results.index,
        y=results[alpha],
        name=alpha,
        mode='lines'
    ))

fig.update_layout(
    title='Alpha Comparison Over Time',
    xaxis_title='Date',
    yaxis_title='Alpha Value'
)
fig.show()
```

### Example 6: Custom Data Loading

```python
import pandas as pd
from alphas import AlphaEngine

# Load from different sources
def load_from_database():
    # Your database logic here
    pass

def load_from_api():
    # Your API logic here
    pass

# Load and format data
raw_data = load_from_database()

# Ensure correct format
formatted_data = raw_data.rename(columns={
    'timestamp': 'date',
    'ticker': 'symbol',
    'o': 'open',
    'h': 'high',
    'l': 'low',
    'c': 'close',
    'v': 'volume'
})

# Calculate alphas
engine = AlphaEngine(formatted_data)
results = engine.calculate_batch(['alpha_001', 'alpha_002'])
```

### Example 7: Backtesting with Alphas

```python
import pandas as pd
import numpy as np
from alphas import AlphaEngine

# Load historical data
data = pd.read_csv('historical_data.csv')
engine = AlphaEngine(data)

# Calculate alpha
alpha_values = engine.calculate('alpha_001')

# Simple backtest: long top quintile, short bottom quintile
returns = data.set_index('date')['close'].pct_change()

# Combine alpha with returns
backtest_data = pd.DataFrame({
    'alpha': alpha_values.iloc[:, 0],
    'returns': returns
})

# Calculate quintiles
backtest_data['quintile'] = pd.qcut(backtest_data['alpha'], 5, labels=False)

# Calculate strategy returns
long_returns = backtest_data[backtest_data['quintile'] == 4]['returns']
short_returns = backtest_data[backtest_data['quintile'] == 0]['returns']

strategy_returns = long_returns.mean() - short_returns.mean()
print(f"Strategy Return: {strategy_returns:.4f}")
```

### Example 8: Batch Processing Large Datasets

```python
import pandas as pd
from alphas import AlphaEngine
import concurrent.futures

def process_symbol(symbol, data):
    """Process alphas for a single symbol."""
    symbol_data = data[data['symbol'] == symbol]
    engine = AlphaEngine(symbol_data)
    return engine.calculate_batch(['alpha_001', 'alpha_002', 'alpha_003'])

# Load large dataset
data = pd.read_csv('large_dataset.csv')
symbols = data['symbol'].unique()

# Process in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(process_symbol, symbol, data): symbol 
               for symbol in symbols}
    
    results = {}
    for future in concurrent.futures.as_completed(futures):
        symbol = futures[future]
        try:
            results[symbol] = future.result()
        except Exception as e:
            print(f"Error processing {symbol}: {e}")

# Combine results
all_results = pd.concat(results, names=['symbol', 'date'])
print(all_results.head())
```

## Dashboard Usage

### Starting the Dashboard

```bash
streamlit run dashboard/app.py
```

### Dashboard Features

1. **Data Upload**: Upload CSV or Excel files
2. **Sample Data**: Generate synthetic data for testing
3. **Alpha Selection**: Choose alphas by category or individually
4. **Visualization**: View time series, correlations, and distributions
5. **Export**: Download results as CSV

### Dashboard Tips

- Use sample data to explore features before uploading real data
- Select fewer alphas initially for faster computation
- Use the correlation heatmap to find redundant alphas
- Export results for further analysis in other tools
