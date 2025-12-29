# 101 Alphas Research Platform

A modular, robust, and educational platform for quantitative research based on the "101 Formulaic Alphas" paper (Kakushadze, 2016).

## Key Features

-   **Data Agnostic Architecture**: The system ingests standard "Long Format" data (Database/CSV style) and internally converts it to strictly aligned "Wide Format" matrices. This prevents common indexing errors and alignment bugs found in ad-hoc research scripts.
-   **Robust Engine**: The `MarketData` container guarantees that all fields (`Open`, `Close`, `Volume`, etc.) share the exact same Time x Ticker index.
-   **Educational Frontend**: A Streamlit UI that displays the Mathematical Formula (LaTeX), the Python Code, and the Visual Output side-by-step.
-   **Modular Operators**: Core primitives (`rank`, `delay`, `signedpower`) are isolated in `src/operators.py`, making the code self-documenting.

## Quick Start

### 1. Installation

The project uses `pyproject.toml` for dependencies.

```bash
pip install -r pyproject.toml
# OR if using uv (recommended)
uv pip install -r pyproject.toml
```

### 2. Run the App

```bash
streamlit run app.py
```

## Architecture

-   **`src/market_data.py`**: The core container. It takes raw data, pivots it, aligns indices, and provides safe accessors (e.g., `data.close`).
-   **`src/operators.py`**: Vectorized implementations of the alpha primitives.
-   **`src/definitions.py`**: The Alphas themselves, defined as functions of `MarketData`.
-   **`src/data_loader.py`**: Adapter for loading data from DuckDB (or generating synthetic test data).

## Extending

To add a new Alpha:
1.  Open `src/definitions.py`.
2.  Define a function `alpha_XXX(data: MarketData)`.
3.  Register it in `ALPHA_REGISTRY` with its LaTeX formula and description.

## Robustness Notes

-   **Alignment**: The `MarketData` class reindexes all inputs to a shared `(Date, Ticker)` grid upon initialization.
-   **Missing Data**: Forward-filling and Backward-filling are applied by default to handle sparse data, ensuring Alphas don't break on isolated NaNs.
