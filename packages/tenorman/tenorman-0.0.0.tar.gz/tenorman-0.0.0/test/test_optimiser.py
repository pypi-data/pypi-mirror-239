import unittest
import pandas as pd

# Import the function to be tested
from actions.optimiser import MeanVariance


class TestMeanVariance(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.df_weights = pd.DataFrame({
            'A': [1, 0, 0.9],
            'B': [0, 1, 0],
            'C': [0, 0, 0],
            'D': [0, 0, 0.1]
        })

    def test_calculate_average_duration(self):
        # Calculate the expected result manually based on the function's code
        expected_result = pd.Series([1, 2, 1], name='average_duration', dtype=int)

        # Call the function to get the actual result
        actual_result = calc_avg_dur(self.df_weights, min_ten=1, max_ten=4)

        # Assert that the actual result matches the expected result
        self.assertTrue(expected_result.equals(actual_result))

    def test_calculate_average_duration_with_empty_dataframe(self):
        # Create an empty DataFrame
        empty_df = pd.DataFrame()

        # Call the function with an empty DataFrame
        result = calc_avg_dur(empty_df, min_ten=1, max_ten=4)

        # Assert that the result is an empty Series
        self.assertTrue(result.empty)

if __name__ == '__main__':
    unittest.main()