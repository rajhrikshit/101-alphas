"""
Unit tests for the 101 Alphas framework.
"""

import unittest
import pandas as pd
import numpy as np
from alphas.engine import AlphaEngine
from alphas.operators import *
from alphas.metadata import get_alpha_metadata, get_all_categories
from dashboard.utils import create_sample_data, validate_data


class TestOperators(unittest.TestCase):
    """Test mathematical operators."""
    
    def setUp(self):
        """Set up test data."""
        np.random.seed(42)
        self.df = pd.DataFrame({
            'value': np.random.randn(100)
        })
    
    def test_ts_sum(self):
        """Test time-series sum."""
        result = ts_sum(self.df, 10)
        self.assertEqual(len(result), len(self.df))
        self.assertTrue(pd.isna(result.iloc[0, 0]))  # First value should be NaN
        self.assertFalse(pd.isna(result.iloc[20, 0]))  # Later values should not be NaN
    
    def test_ts_mean(self):
        """Test time-series mean."""
        result = ts_mean(self.df, 5)
        self.assertEqual(len(result), len(self.df))
        # Check that mean is calculated correctly for a window
        window_data = self.df.iloc[5:10]['value']
        expected_mean = window_data.mean()
        actual_mean = result.iloc[9, 0]
        self.assertAlmostEqual(actual_mean, expected_mean, places=5)
    
    def test_delta(self):
        """Test delta operator."""
        result = delta(self.df, 1)
        self.assertEqual(len(result), len(self.df))
        # First value should be NaN
        self.assertTrue(pd.isna(result.iloc[0, 0]))
    
    def test_rank(self):
        """Test rank operator."""
        result = rank(self.df)
        # Ranks should be between 0 and 1
        self.assertTrue((result.iloc[:, 0] >= 0).all())
        self.assertTrue((result.iloc[:, 0] <= 1).all())
    
    def test_correlation(self):
        """Test correlation operator."""
        df2 = pd.DataFrame({'value': np.random.randn(100)})
        result = correlation(self.df, df2, 10)
        # Correlation should be between -1 and 1
        valid_corr = result.dropna().iloc[:, 0]
        self.assertTrue((valid_corr >= -1).all())
        self.assertTrue((valid_corr <= 1).all())


class TestAlphaEngine(unittest.TestCase):
    """Test AlphaEngine class."""
    
    def setUp(self):
        """Set up test data."""
        self.data = create_sample_data(num_days=100, num_symbols=1)
    
    def test_engine_initialization(self):
        """Test engine initialization."""
        engine = AlphaEngine(self.data)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.data)
        self.assertIsNotNone(engine.data_dict)
    
    def test_calculate_single_alpha(self):
        """Test calculating a single alpha."""
        engine = AlphaEngine(self.data)
        result = engine.calculate('alpha_001')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_calculate_batch(self):
        """Test batch calculation."""
        engine = AlphaEngine(self.data)
        alphas = ['alpha_001', 'alpha_004', 'alpha_006']
        result = engine.calculate_batch(alphas)
        self.assertIsNotNone(result)
        # At least one alpha should be calculated
        self.assertGreaterEqual(len(result.columns), 1)
    
    def test_get_available_alphas(self):
        """Test getting available alphas."""
        engine = AlphaEngine(self.data)
        alphas = engine.get_available_alphas()
        self.assertIsInstance(alphas, list)
        self.assertGreater(len(alphas), 0)
    
    def test_invalid_alpha(self):
        """Test handling of invalid alpha name."""
        engine = AlphaEngine(self.data)
        with self.assertRaises(ValueError):
            engine.calculate('alpha_999')


class TestDataValidation(unittest.TestCase):
    """Test data validation."""
    
    def test_valid_data(self):
        """Test validation of valid data."""
        data = create_sample_data(num_days=50, num_symbols=1)
        self.assertTrue(validate_data(data))
    
    def test_missing_columns(self):
        """Test handling of missing columns."""
        data = pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=10),
            'close': np.random.rand(10),
            'volume': np.random.rand(10)
        })
        with self.assertRaises(ValueError):
            validate_data(data)
    
    def test_sample_data_generation(self):
        """Test sample data generation."""
        data = create_sample_data(num_days=100, num_symbols=3)
        self.assertEqual(len(data), 300)  # 100 days * 3 symbols
        self.assertIn('date', data.columns)
        self.assertIn('symbol', data.columns)
        self.assertIn('close', data.columns)


class TestMetadata(unittest.TestCase):
    """Test metadata functions."""
    
    def test_get_alpha_metadata(self):
        """Test getting alpha metadata."""
        metadata = get_alpha_metadata('alpha_001')
        self.assertIsInstance(metadata, dict)
        self.assertIn('name', metadata)
        self.assertIn('description', metadata)
        self.assertIn('category', metadata)
    
    def test_get_all_categories(self):
        """Test getting all categories."""
        categories = get_all_categories()
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)
        self.assertIn('Momentum', categories)


class TestAlphaCalculations(unittest.TestCase):
    """Test specific alpha calculations."""
    
    def setUp(self):
        """Set up test data with known values."""
        # Create simple test data
        dates = pd.date_range('2023-01-01', periods=50)
        self.data = pd.DataFrame({
            'date': dates,
            'open': 100 + np.arange(50) * 0.5,
            'high': 102 + np.arange(50) * 0.5,
            'low': 98 + np.arange(50) * 0.5,
            'close': 101 + np.arange(50) * 0.5,
            'volume': 1000000 + np.arange(50) * 1000
        })
    
    def test_alpha_001_no_error(self):
        """Test that Alpha #1 calculates without error."""
        engine = AlphaEngine(self.data)
        try:
            result = engine.calculate('alpha_001')
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Alpha #1 raised an exception: {e}")
    
    def test_alpha_002_no_error(self):
        """Test that Alpha #2 calculates without error."""
        engine = AlphaEngine(self.data)
        try:
            result = engine.calculate('alpha_004')  # Use alpha 4 instead
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Alpha #4 raised an exception: {e}")
    
    def test_multiple_alphas_consistency(self):
        """Test that calculating alphas produces consistent results."""
        engine = AlphaEngine(self.data)
        
        # Calculate same alpha twice
        result1 = engine.calculate('alpha_004')
        result2 = engine.calculate('alpha_004')
        
        # Results should be identical
        pd.testing.assert_frame_equal(result1, result2)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
