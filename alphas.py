import pandas as pd
import numpy as np
from data import load_sp500

class AlphaEngine:
    def __init__(self):
        self.closes = None
        self.opens = None
        self.highs = None
        self.lows = None
        self.volumes = None
        self.returns = None
        self.vwap = None
        self.benchmark = None
        self.tickers = []
        self.dates = []

    def load_data(self):
        """Loads data using data.py and prepares it for alpha calculation."""
        df = load_sp500()
        
        if df.empty:
            raise ValueError("No data loaded from load_sp500")

        # Ensure Date is datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Pivot data to (Date x Ticker) matrices
        self.closes = df.pivot(index='Date', columns='Ticker', values='Close')
        self.opens = df.pivot(index='Date', columns='Ticker', values='Open')
        self.highs = df.pivot(index='Date', columns='Ticker', values='High')
        self.lows = df.pivot(index='Date', columns='Ticker', values='Low')
        self.volumes = df.pivot(index='Date', columns='Ticker', values='Volume')
        
        # Forward fill missing data then backward fill
        self.closes = self.closes.ffill().bfill()
        self.opens = self.opens.ffill().bfill()
        self.highs = self.highs.ffill().bfill()
        self.lows = self.lows.ffill().bfill()
        self.volumes = self.volumes.ffill().bfill()
        
        self.returns = self.closes.pct_change()
        
        # Approximate VWAP if not present (Open+High+Low+Close)/4 or (H+L+C)/3
        self.vwap = (self.highs + self.lows + self.closes) / 3
        
        self.tickers = self.closes.columns.tolist()
        self.dates = self.closes.index.tolist()
        
        # Create SPX (Benchmark) - Simple Average for now
        self.benchmark = self.closes.mean(axis=1)

    # --- Helper Functions (Operators) ---
    # Most operators work on the DataFrame (cross-sectional or time-series)

    def rank(self, df):
        """Cross-sectional rank (0 to 1)."""
        return df.rank(axis=1, pct=True)

    def delay(self, df, period):
        """Lag operator."""
        return df.shift(period)

    def correlation(self, x, y, window):
        """Rolling correlation."""
        return x.rolling(window=window).corr(y)

    def covariance(self, x, y, window):
        """Rolling covariance."""
        return x.rolling(window=window).cov(y)

    def scale(self, df, k=1):
        """Rescale such that sum(abs(x)) = k (usually 1 or a constant).
        The paper definition might vary, often it's x / sum(abs(x))."""
        return df.div(df.abs().sum(axis=1), axis=0) * k

    def delta(self, df, period):
        """x - x.shift(period)"""
        return df.diff(period)

    def signedpower(self, df, a):
        """sign(x) * |x|^a"""
        return np.sign(df) * (np.abs(df) ** a)

    def decay_linear(self, df, period):
        """Weighted moving average with linear decay weights."""
        weights = np.arange(1, period + 1)
        sum_weights = np.sum(weights)
        
        def weighted_avg(x):
            if len(x) < period: return np.nan
            return np.dot(x, weights) / sum_weights

        # Rolling apply is slow, try to vectorize or use pandas ewm as approximation?
        # Exact implementation using rolling apply:
        # return df.rolling(period).apply(weighted_avg, raw=True)
        # Optimization:
        return df.rolling(period).apply(lambda x: np.dot(x, weights)/sum_weights, raw=True)

    def ts_min(self, df, window):
        return df.rolling(window).min()

    def ts_max(self, df, window):
        return df.rolling(window).max()

    def ts_argmax(self, df, window):
        """Index of max value in rolling window (0 to window-1).
        Paper typically uses 1-based or 0-based index from the end?
        Let's assume returns the day index (0 is today, window-1 is 'window' days ago).
        Standard pandas 'idxmax' returns the label.
        We need the integer offset."""
        return df.rolling(window).apply(np.argmax, raw=True)

    def ts_argmin(self, df, window):
        return df.rolling(window).apply(np.argmin, raw=True)
        
    def stddev(self, df, window):
        return df.rolling(window).std()

    def ts_rank(self, df, window):
        """Rank over time."""
        return df.rolling(window).rank(pct=True) # Check if pct is needed, usually yes.

    # --- Alpha Implementations ---
    # Notes:
    # - IndNeutralize is skipped (no industry data).
    # - Cap is skipped (assume small caps already filtered or handled).
    
    def get_alpha(self, number):
        method_name = f"alpha_{number:03d}"
        if hasattr(self, method_name):
            return getattr(self, method_name)()
        else:
            raise NotImplementedError(f"Alpha {number} not implemented.")

    def alpha_001(self):
        # Alpha#1: (rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5)
        
        # Condition
        cond = self.returns < 0
        inner = cond * self.stddev(self.returns, 20) + (~cond) * self.closes
        
        # Signed Power
        sp = self.signedpower(inner, 2.0)
        
        # Ts_ArgMax
        ts_amax = self.ts_argmax(sp, 5)
        
        # Rank
        return self.rank(ts_amax) - 0.5

    def alpha_002(self):
        # Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))
        
        # delta(log(volume), 2)
        p1 = self.delta(np.log(self.volumes), 2)
        rank_p1 = self.rank(p1)
        
        # (close - open) / open  => returns based on open? 
        p2 = (self.closes - self.opens) / self.opens
        rank_p2 = self.rank(p2)
        
        corr = self.correlation(rank_p1, rank_p2, 6)
        return -1.0 * corr

    def alpha_003(self):
        # Alpha#3: (-1 * correlation(rank(open), rank(volume), 10))
        return -1.0 * self.correlation(self.rank(self.opens), self.rank(self.volumes), 10)

    def alpha_004(self):
        # Alpha#4: (-1 * Ts_Rank(rank(low), 9))
        return -1.0 * self.ts_rank(self.rank(self.lows), 9)

    def alpha_005(self):
        # Alpha#5: (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))
        
        # sum(vwap, 10) / 10 is moving average of vwap
        ma_vwap = self.vwap.rolling(10).mean()
        
        term1 = self.rank(self.opens - ma_vwap)
        term2 = -1.0 * np.abs(self.rank(self.closes - self.vwap))
        
        return term1 * term2

    def alpha_006(self):
        # Alpha#6: (-1 * correlation(open, volume, 10))
        return -1.0 * self.correlation(self.opens, self.volumes, 10)
    
    def alpha_009(self):
        # Alpha#9: ((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ? delta(close, 1) : (-1 * delta(close, 1))))
        
        delta_close = self.delta(self.closes, 1)
        min_delta = self.ts_min(delta_close, 5)
        max_delta = self.ts_max(delta_close, 5)
        
        cond1 = min_delta > 0
        cond2 = max_delta < 0
        
        # Logic: 
        # If min_delta > 0 (all positive changes), result = delta_close (Trend follow)
        # Else If max_delta < 0 (all negative changes), result = delta_close (Trend follow down)
        # Else (mixed), result = -1 * delta_close (Mean reversion)
        
        # Implementation using where
        res = np.where(cond1, delta_close, np.where(cond2, delta_close, -1.0 * delta_close))
        return pd.DataFrame(res, index=self.closes.index, columns=self.closes.columns)

    def alpha_101(self):
        # Alpha#101: ((close - open) / ((high - low) + .001))
        # Note: 101 Alphas paper usually ends at 101.
        return (self.closes - self.opens) / ((self.highs - self.lows) + 0.001)

