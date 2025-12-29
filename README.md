# 101 Alphas Implementation

This project implements a subset of the 101 Alphas (Kakushadze, 2016) and provides a Streamlit UI to visualize them.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r pyproject.toml # or manually pip install streamlit duckdb pandas numpy scipy plotly
    ```
    (Note: Dependencies were added to `pyproject.toml` and installed in the environment)

2.  **Data**:
    The system expects a DuckDB database at `/workspace/sp500.db`.
    -   If not found, `data.py` will automatically create a synthetic dataset for testing purposes.
    -   The synthetic data includes 10 tickers (AAPL, MSFT, etc.) with OHLCV data.

## Running the App

Run the Streamlit frontend:

```bash
streamlit run app.py
```

## Structure

-   `alphas.py`: Contains the `AlphaEngine` class and alpha definitions (Alphas 1-6, 9, 101).
-   `data.py`: Handles data loading (DuckDB) and synthetic data generation.
-   `app.py`: Streamlit dashboard.
-   `check_setup.py`: Script to verify the backend without the UI.

## Notes & Assumptions

-   **Data Source**: We assume the input is a set of stocks (S&P 500 components).
-   **SPX Benchmark**: The S&P 500 index (SPX) is approximated as the mean of the available components (Equal Weighted) since market cap data might be missing.
-   **Missing Fields**: VWAP is approximated as `(High + Low + Close) / 3` if not present in the database.
-   **Implementation**: A subset of alphas are implemented to demonstrate the architecture. Adding more is straightforward in `alphas.py`.
