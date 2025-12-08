# Usage Instructions for 101 Alphas Framework

## Quick Start in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Launch the Dashboard
```bash
streamlit run dashboard/app.py
```

### Step 3: Explore Alphas
The dashboard will open in your browser at `http://localhost:8501`

## Dashboard Features

### 1. Data Input
- **Upload File**: Upload CSV or Excel files with OHLCV data
- **Use Sample Data**: Generate synthetic data for testing (adjustable parameters)

### 2. Alpha Selection
- **By Category**: Select all alphas in a category (Momentum, Volume, VWAP, etc.)
- **Individual**: Hand-pick specific alphas
- **All Alphas**: Calculate all 60 implemented alphas at once

### 3. Visualizations
- **Overview Tab**: Summary statistics, mean values, standard deviations
- **Time Series Tab**: Interactive line plots showing alpha values over time
- **Heatmap Tab**: Correlation analysis between alphas
- **Data Table Tab**: Raw alpha values with export capability

### 4. Alpha Information
Each alpha includes:
- Formula description
- Mathematical expression
- Category classification
- Complexity rating
- Use case explanation

## Python API Usage

### Basic Example
```python
from alphas import AlphaEngine
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv')

# Initialize engine
engine = AlphaEngine(data)

# Calculate alpha
result = engine.calculate('alpha_001')
print(result.head())
```

### Batch Calculation
```python
# Calculate multiple alphas
alphas = ['alpha_001', 'alpha_004', 'alpha_012']
results = engine.calculate_batch(alphas)

# View statistics
print(results.describe())
```

### Category-Based Analysis
```python
from alphas.metadata import get_alphas_by_category

# Get momentum alphas
momentum_alphas = get_alphas_by_category('Momentum')

# Calculate all momentum alphas
results = engine.calculate_batch(momentum_alphas)
```

## Data Format Requirements

Your CSV/Excel file must contain:
- `date`: Trading date (any datetime format)
- `open`: Opening price
- `high`: Highest price
- `low`: Lowest price  
- `close`: Closing price
- `volume`: Trading volume
- `symbol` (optional): Stock identifier for multi-asset data

### Example Data Format
```csv
date,symbol,open,high,low,close,volume
2023-01-01,AAPL,150.0,152.0,149.0,151.0,1000000
2023-01-02,AAPL,151.0,153.0,150.0,152.0,1100000
2023-01-03,AAPL,152.0,154.0,151.0,153.0,1050000
```

## Implemented Alphas

### By Category
1. **Momentum** (7 alphas): Trend-following signals
   - alpha_001, alpha_008, alpha_009, alpha_010, alpha_014, alpha_019, alpha_030

2. **Volume** (7 alphas): Trading volume patterns
   - alpha_002, alpha_003, alpha_006, alpha_013, alpha_015, alpha_016, alpha_026

3. **VWAP** (4 alphas): Volume-weighted average price
   - alpha_005, alpha_011, alpha_027, alpha_028

4. **Volatility** (2 alphas): Price volatility measures
   - alpha_018, alpha_022

5. **Mean-Reversion** (3 alphas): Overbought/oversold signals
   - alpha_021, alpha_023, alpha_024

6. **Gap** (1 alpha): Opening gap analysis
   - alpha_020

7. **Composite** (2 alphas): Multi-factor combinations
   - alpha_025, alpha_029

Plus 34 additional alphas (alpha_031 through alpha_060)

## Performance Tips

1. **Start Small**: Begin with 100-200 days of data for testing
2. **Batch Processing**: Calculate multiple alphas at once for efficiency
3. **Memory**: Single-stock analysis uses less memory than multi-stock
4. **Historical Data**: Most alphas need 60-250 days for proper calculation

## Troubleshooting

### Common Issues

**Q: Dashboard won't start**
```bash
# Verify installation
pip install streamlit
streamlit --version

# Try explicitly
python -m streamlit run dashboard/app.py
```

**Q: Alpha calculation returns NaN**
- Ensure sufficient historical data (250+ days recommended)
- Check for missing values in your data
- Verify all required columns are present

**Q: Import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Q: "Length mismatch" errors**
- Some complex alphas may not work with single-stock data
- Try with multi-stock dataset or use simpler alphas

## Advanced Usage

### Custom Analysis
```python
# Calculate all alphas
all_results = engine.calculate_all()

# Find best performing alphas
correlations = {}
for col in all_results.columns:
    # Your performance metric here
    correlations[col] = all_results[col].mean()

# Sort and display
sorted_alphas = sorted(correlations.items(), 
                      key=lambda x: abs(x[1]), 
                      reverse=True)
print("Top 10 alphas:", sorted_alphas[:10])
```

### Export Results
```python
# Calculate and save
results = engine.calculate_batch(['alpha_001', 'alpha_004'])
results.to_csv('alpha_results.csv')
```

## Testing

Run the test suite:
```bash
python -m unittest tests.test_alphas -v
```

Expected output: 18 tests passing

## Getting Help

1. Check [Quick Start Guide](docs/quickstart.md)
2. Read [API Reference](docs/api_reference.md)
3. Review [Examples](docs/examples.md)
4. See [Alpha Descriptions](docs/alpha_descriptions.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding new alphas (61-101)
- Improving operators
- Enhancing the dashboard
- Reporting issues

## License

MIT License - See [LICENSE](LICENSE) file

---

**Happy Alpha Hunting! 🚀📈**

For questions or issues, please open a GitHub issue.
