# API Reference

## AlphaEngine

The main class for calculating alphas.

### Constructor

```python
AlphaEngine(data: pd.DataFrame)
```

**Parameters:**
- `data`: DataFrame with OHLCV data

**Required columns:**
- `date`: Trading date (datetime)
- `open`: Opening price (float)
- `high`: Highest price (float)
- `low`: Lowest price (float)
- `close`: Closing price (float)
- `volume`: Trading volume (float)
- `symbol` (optional): Stock identifier (string)

### Methods

#### calculate
```python
calculate(alpha_name: str) -> pd.DataFrame
```
Calculate a single alpha.

**Parameters:**
- `alpha_name`: Name of alpha (e.g., 'alpha_001')

**Returns:**
- DataFrame with alpha values

**Example:**
```python
engine = AlphaEngine(data)
alpha_1 = engine.calculate('alpha_001')
```

#### calculate_batch
```python
calculate_batch(alpha_names: List[str]) -> pd.DataFrame
```
Calculate multiple alphas.

**Parameters:**
- `alpha_names`: List of alpha names

**Returns:**
- DataFrame with columns for each alpha

**Example:**
```python
alphas = engine.calculate_batch(['alpha_001', 'alpha_002', 'alpha_003'])
```

#### calculate_all
```python
calculate_all() -> pd.DataFrame
```
Calculate all available alphas.

**Returns:**
- DataFrame with all alphas

#### get_available_alphas
```python
get_available_alphas() -> List[str]
```
Get list of available alpha names.

#### get_data_summary
```python
get_data_summary() -> Dict
```
Get summary of loaded data.

## Operators

All operators are available in `alphas.operators` module.

### Time-Series Operators

#### ts_sum
```python
ts_sum(df: pd.DataFrame, window: int) -> pd.DataFrame
```
Rolling sum over window days.

#### ts_mean
```python
ts_mean(df: pd.DataFrame, window: int) -> pd.DataFrame
```
Rolling mean over window days.

#### ts_rank
```python
ts_rank(df: pd.DataFrame, window: int) -> pd.DataFrame
```
Rolling percentile rank.

### Cross-Sectional Operators

#### rank
```python
rank(df: pd.DataFrame) -> pd.DataFrame
```
Cross-sectional percentile rank.

#### scale
```python
scale(df: pd.DataFrame, a: float = 1.0) -> pd.DataFrame
```
Scale to sum to a.

### Other Operators

#### delta
```python
delta(df: pd.DataFrame, period: int = 1) -> pd.DataFrame
```
Difference over period days.

#### correlation
```python
correlation(x: pd.DataFrame, y: pd.DataFrame, window: int) -> pd.DataFrame
```
Rolling correlation.

## Metadata Functions

### get_alpha_metadata
```python
get_alpha_metadata(alpha_name: str) -> dict
```
Get metadata for an alpha.

**Returns:**
```python
{
    'name': 'Alpha #1',
    'formula': '...',
    'description': '...',
    'category': 'Momentum',
    'complexity': 'High'
}
```

### get_alphas_by_category
```python
get_alphas_by_category(category: str) -> list
```
Get alphas in a category.

### get_all_categories
```python
get_all_categories() -> list
```
Get all category names.

## Complete Example

```python
import pandas as pd
from alphas import AlphaEngine
from alphas.metadata import get_alpha_metadata, get_all_categories

# Load data
data = pd.read_csv('market_data.csv')

# Initialize engine
engine = AlphaEngine(data)

# Get available alphas
print(f"Available alphas: {engine.get_available_alphas()}")

# Calculate single alpha
alpha_1 = engine.calculate('alpha_001')
print(alpha_1.head())

# Calculate by category
from alphas.metadata import get_alphas_by_category
momentum_alphas = get_alphas_by_category('Momentum')
momentum_results = engine.calculate_batch(momentum_alphas)

# Get alpha information
for alpha in momentum_alphas:
    info = get_alpha_metadata(alpha)
    print(f"{info['name']}: {info['description']}")

# Calculate all alphas
all_results = engine.calculate_all()
print(all_results.describe())
```
