import cvxpy as cp
from helpers.general_helper import generic_align
from helpers.forward_helper import apply_laddering, get_tenor_cols
from abc import ABCMeta, abstractmethod
from typing import TypeVar
import numpy as np
import pandas as pd
from logger import LOGGER
from datetime import datetime

PandasDataframe = TypeVar('pandas.core.frame.DataFrame')

LOGGER.info('###############################################')
LOGGER.info(f'Running Optimiser: {str(datetime.now())}')


class BaseOptimiser:
	__metaclass__ = ABCMeta

	@abstractmethod
	def compute_tenor(self, df_spot: pd.DataFrame, df_points: pd.DataFrame) -> pd.DataFrame:
		pass


class MeanVariance(BaseOptimiser):

	def __init__(self, max_tenor=None, min_tenor=None, look_back=None, fct=None, t_cost=None):
		"""
		Calculate the optimal tenor using mean variance framework
		:param max_ten:
		:param min_ten:
		"""
		self.max_tenor = 12 if max_tenor is None else max_tenor
		self.min_tenor = 1 if min_tenor is None else min_tenor
		self.look_back = 62 if look_back is None else look_back
		self.fct = 10000 if fct is None else fct
		self.t_cost = [0.0001 * i for i in range(self.max_tenor, 0, -1)] if t_cost is None else t_cost

	def compute_tenor(self, df_spot: pd.DataFrame, df_points: pd.DataFrame) -> pd.DataFrame:
		"""
		Simple exponentially weighted crossover momentum strategy
		:param df_spot: DataFrame with single column of spot values
		:param df_points: DataFrame with max_ten - min_ten tenor columns for above spot
		:return: dataframe of tenors with optimal weight as 1
		"""
		LOGGER.info('Running Mean Variance Optimisation')

		ten_cols = get_tenor_cols(df_points, self.min_tenor, self.max_tenor)
		df_points = df_points[[x for x in df_points.columns if x in ten_cols]]
		df_tenors = df_points.shift(21) - df_points.shift(1, axis=1).fillna(0)

		# Calculate the yield part of the equation
		df_yields = (df_tenors / self.fct)
		for col in df_yields.columns:
			df_yields[col] = df_yields[col] / df_spot[df_spot.columns[0]].shift(21)
		#df_yields_smooth = df_yields.rolling(self.look_back).median()

		# Calculate spot returns
		spot_ret = np.log(df_spot).diff().dropna()

		# Align spots and smooth yields. Drop NAs
		spot_ret, df_yields = generic_align([spot_ret, df_yields], index=True, columns=False,
												   drop_na='all', sort_col=False)

		# Optimiser
		df_weights = pd.DataFrame(index=df_yields.index, columns=df_yields.columns)
		w = cp.Variable(len(df_yields.columns))
		for x in range(self.look_back+1, len(df_yields)):
			df_yields_temp = df_yields.iloc[x - self.look_back:x + 1]
			expected_returns = df_yields_temp.median()
			cov_mat = df_yields_temp.cov() * 21
			ret = expected_returns.values.T @ w
			risk = cp.quad_form(w, cov_mat)
			prob = cp.Problem(cp.Maximize(ret - 0.5 * risk), [cp.sum(w) == 1, w >= 0])
			prob.solve()
			df_weights.iloc[x] = w.value

		# Apply Laddering
		df_weights_ladder = apply_laddering(df_weights, self.min_tenor, self.max_tenor, self.look_back)

		# Resample to monthly last business
		df_weights_ladder_m = df_weights_ladder.resample('BM').last()

		# Output weights to csv
		df_weights_ladder_m.to_csv('c:\\temp\\df_tenor_tmp.csv')

		return df_weights_ladder_m
