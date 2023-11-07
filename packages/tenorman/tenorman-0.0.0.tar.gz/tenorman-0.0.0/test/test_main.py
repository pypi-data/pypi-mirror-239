import unittest
import pandas as pd

from helpers.data_service import TestReferenceDataService
from actions.get_data import get_data
from actions.optimiser import MeanVariance


class TestCalculateAverageDuration(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.data_svc = TestReferenceDataService()
        self.spot = self.data_svc.get_spot('_')
        self.points = self.data_svc.get_points('_')
        self.tenors = pd.read_csv('./test/test_data/tenors.csv', index_col=0, parse_dates=True)
        self.min_tenor = 1
        self.max_tenor = 6

    def test_get_data_spot(self):
        # Calculate the expected result manually based on the function's code
        expected_spot = self.spot

        # Call the function to get the actual result
        actual_spot, _ = get_data(ccy_pair='USDCHF', ccy_base='CHF', start_dt='20220101', pivot_usd=False, data_svc=self.data_svc)

        # Assert that the actual result matches the expected result
        self.assertTrue(expected_spot.equals(actual_spot))

    def test_get_data_points(self):
        # Calculate the expected result manually based on the function's code
        expected_spot = self.points

        # Call the function to get the actual result
        _, actual_points = get_data(ccy_pair='USDCHF', ccy_base='CHF', start_dt='20220101', pivot_usd=False, data_svc=self.data_svc)

        # Assert that the actual result matches the expected result
        self.assertTrue(expected_spot.equals(actual_points))

    def test_end_to_end(self):
        # Create an empty DataFrame
        expected_tenors = self.tenors

        # Call the function with an empty DataFrame
        df_spots, df_points = get_data('USDCHF', ccy_base='CHF')
        # Calculate optimal tenors
        mv = MeanVariance(min_tenor=1, max_tenor=6)
        actual_tenors = mv.compute_tenor(df_spots, df_points)

        # Assert that the result is an empty Series
        self.assertTrue(expected_tenors.equals(actual_tenors))


if __name__ == '__main__':
    unittest.main()