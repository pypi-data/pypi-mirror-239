import unittest
import pandas as pd

from helpers.forward_helper import calc_avg_dur, get_tenor_cols, apply_laddering


class TestCalculateAverageDuration(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.df_weights = pd.DataFrame({
            'CHF1M BGNL curncy': [1, 0, 0.9],
            'CHF2M BGNL curncy': [0, 0.4, 0],
            'CHF3M BGNL curncy': [0, 0, 0],
            'CHF4M BGNL curncy': [0, 0.6, 0],
            'CHF5M BGNL curncy': [0, 0, 0],
            'CHF6M BGNL curncy': [0, 0, 0.1]
        })

    def test_calc_avg_dur(self):
        # Calculate the expected result manually based on the function's code
        expected_result = pd.Series([1, 3, 1], name='average_duration', dtype=int)

        # Call the function to get the actual result
        actual_result = calc_avg_dur(self.df_weights, min_ten=1, max_ten=6)

        # Assert that the actual result matches the expected result
        self.assertTrue(expected_result.equals(actual_result))

    def test_calc_avg_dur_with_empty_dataframe(self):
        # Create an empty DataFrame
        empty_df = pd.DataFrame()

        # Call the function with an empty DataFrame
        result = calc_avg_dur(empty_df, min_ten=1, max_ten=4)

        # Assert that the result is an empty Series
        self.assertTrue(result.empty)

    def test_get_tenor_cols_with_valid_range(self):
        # Test the function with a valid range of tenors (1 to 3)
        min_tenor = 1
        max_tenor = 3

        expected_result = ['CHF1M BGNL curncy', 'CHF2M BGNL curncy', 'CHF3M BGNL curncy']
        actual_result = get_tenor_cols(self.df_weights, min_tenor, max_tenor)

        self.assertEqual(expected_result, actual_result)

    def test_get_tenor_cols_with_invalid_range(self):
        # Test the function with an invalid range of tenors (4 to 5)
        min_tenor = 7
        max_tenor = 8

        expected_result = []
        actual_result = get_tenor_cols(self.df_weights, min_tenor, max_tenor)

        self.assertEqual(expected_result, actual_result)

    def test_get_tenor_cols_with_empty_dataframe(self):
        # Test the function with an empty DataFrame
        empty_df = pd.DataFrame()

        min_tenor = 1
        max_tenor = 3

        expected_result = []
        actual_result = get_tenor_cols(empty_df, min_tenor, max_tenor)

        self.assertEqual(expected_result, actual_result)

    def test_apply_laddering(self):
        # Test the function with sample data and parameters
        min_tenor = 1
        max_tenor = 6
        window = 63  # You can adjust this value as needed

        expected_result = pd.DataFrame({
            'CHF1M BGNL curncy': [1/3, 0, 1/3],
            'CHF2M BGNL curncy': [1/3, 1/3, 1/3],
            'CHF3M BGNL curncy': [1/3, 1/3, 1/3],
            'CHF4M BGNL curncy': [0, 1/3, 0],
            'CHF5M BGNL curncy': [0, 0, 0],
            'CHF6M BGNL curncy': [0, 0, 0],
        }, dtype=float)

        actual_result = apply_laddering(self.df_weights, min_tenor, max_tenor, window)

        self.assertTrue(expected_result.equals(actual_result))

    def test_apply_laddering_with_warning(self):
        # Test the function with a window value that triggers a warning
        min_tenor = 1
        max_tenor = 3
        window = 62  # This will trigger the warning

        # You may want to capture the warning message using the 'warnings' module
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")  # Ensure warnings are always triggered
            apply_laddering(self.df_weights, min_tenor, max_tenor, window)

            # Check if a warning was issued
            self.assertEqual(len(w), 1)
            self.assertTrue("Warning weights do not sum to 1" in str(w[0].message))


if __name__ == '__main__':
    unittest.main()