# 101 Alphas Framework

An interactive framework for implementing and visualizing the 101 formulaic alphas from Zura Kakushadze's paper "101 Formulaic Alphas".

## Overview

This framework provides:
- **Complete Implementation**: All 101 alpha formulas from the research paper
- **Interactive Dashboard**: Streamlit-based UI for intuitive exploration and visualization
- **Dynamic Data Support**: Works with any dataset containing required fields (OHLCV data)
- **Modular Architecture**: Easy to extend and customize

## Features

- ✅ All 101 alpha formulas implemented with mathematical operators
- ✅ Interactive web-based dashboard
- ✅ Real-time alpha calculation and visualization
- ✅ Data upload support (CSV, Excel)
- ✅ Alpha comparison and analysis tools
- ✅ Filtering and search capabilities
- ✅ Comprehensive documentation for each alpha

## Installation

```bash
# Clone the repository
git clone https://github.com/rajhrikshit/101-alphas.git
cd 101-alphas

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# Launch the dashboard
streamlit run dashboard/app.py
```

Then open your browser to `http://localhost:8501`

## Usage

### Using the Dashboard

1. **Upload Data**: Upload your OHLCV dataset (CSV or Excel format)
2. **Select Alphas**: Browse and select alphas to calculate
3. **Visualize**: View alpha values, distributions, and correlations
4. **Compare**: Compare multiple alphas side-by-side
5. **Export**: Download calculated alpha values

### Programmatic Usage

```python
from alphas import AlphaEngine
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv')

# Initialize engine
engine = AlphaEngine(data)

# Calculate specific alpha
alpha_1 = engine.calculate('alpha_001')

# Calculate multiple alphas
results = engine.calculate_batch(['alpha_001', 'alpha_002', 'alpha_003'])
```

## Data Format

The framework expects data with the following columns:
- `date`: Trading date
- `open`: Opening price
- `high`: Highest price
- `low`: Lowest price
- `close`: Closing price
- `volume`: Trading volume
- `symbol` (optional): Stock/instrument identifier for multi-asset datasets

## Project Structure

```
101-alphas/
├── alphas/              # Alpha calculation engine
│   ├── __init__.py
│   ├── engine.py        # Main calculation engine
│   ├── formulas.py      # All 101 alpha formulas
│   ├── operators.py     # Mathematical operators (ts_rank, ts_mean, etc.)
│   └── metadata.py      # Alpha descriptions and metadata
├── dashboard/           # Interactive dashboard
│   ├── app.py          # Main Streamlit application
│   ├── components/     # Dashboard components
│   └── utils.py        # Dashboard utilities
├── data/               # Sample datasets
├── tests/              # Unit tests
├── docs/               # Documentation
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Alpha Formulas

The framework implements all 101 alphas from the paper. Each alpha is a formulaic expression that combines:
- **Time-series operators**: ts_rank, ts_mean, ts_std, ts_sum, etc.
- **Cross-sectional operators**: rank, scale
- **Mathematical functions**: abs, log, sign, delta, etc.
- **Logical operators**: condition, correlation, covariance

## Documentation

- [Alpha Descriptions](docs/alpha_descriptions.md): Detailed explanation of each alpha
- [API Reference](docs/api_reference.md): Complete API documentation
- [Examples](docs/examples.md): Usage examples and tutorials

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## References

Kakushadze, Z. (2016). "101 Formulaic Alphas". Wilmott Magazine, 2016(84), 72-81.

## Citation

If you use this framework in your research, please cite:

```bibtex
@article{kakushadze2016101,
  title={101 Formulaic Alphas},
  author={Kakushadze, Zura},
  journal={Wilmott Magazine},
  volume={2016},
  number={84},
  pages={72--81},
  year={2016}
}
```
