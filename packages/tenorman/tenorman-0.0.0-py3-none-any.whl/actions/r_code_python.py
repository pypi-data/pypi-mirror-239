import pandas as pd
import numpy as np
import cvxpy as cp
from actions.get_data import get_data
from helpers.general_helper import generic_align
from matplotlib import pyplot as plt
from helpers.forward_helper import apply_laddering
# import matplotlib
# matplotlib.use('TkAgg')
import re

# Define variables
ccy_pair = "USDCHF"
fct = 10000
PER = "CHF"

bmrk = 3
max_ten = 6
min_ten = 1

T_cost = [0.0001 * i for i in range(max_ten, 0, -1)]

df_spot, df_points = get_data(ccy_pair=ccy_pair, ccy_base=PER)

tenor_lst = [int(re.findall(r'\d+', x)[0]) for x in df_points.columns if int(re.findall(r'\d+', x)[0]) >= min_ten and int(re.findall(r'\d+', x)[0]) <= max_ten]
ten_cols = [x for x in df_points.columns if int(re.findall(r'\d+', x)[0]) in tenor_lst]

# Limit points to tenors
df_points = df_points[[x for x in df_points.columns if x in ten_cols]]

df_tenors = df_points.shift(21) - df_points.shift(1, axis=1).fillna(0)

# Calculate the yield part of the equation
df_yields = (df_tenors / fct)
for col in df_yields.columns:
	df_yields[col] = df_yields[col] / df_spot['USDCHF BGNL curncy'].shift(21)
df_yields_smooth = df_yields.rolling(5).median()


###########################
# Rolling
#####################
window = 62
# Calculate spot returns
spot_ret = np.log(df_spot).diff().dropna()

# Align spots and smooth yields. Drop NAs
spot_ret, df_yields_smooth = generic_align([spot_ret, df_yields_smooth], index=True, columns=False, drop_na='all', sort_col=False)



# Optimiser
df_weights = pd.DataFrame(index=df_yields_smooth.index, columns=df_yields_smooth.columns)
w = cp.Variable(len(df_yields_smooth.columns))
for x in range(window+1, len(df_yields_smooth)):
	yields_smooth_tmp = df_yields_smooth.iloc[x - window:x+1]
	expected_returns = yields_smooth_tmp.mean() - np.divide(T_cost, 12)

	cov_mat = yields_smooth_tmp.cov()*21

	# https://www.kaggle.com/code/marketneutral/cvxpy-portfolio-optimization-example
	ret = expected_returns.values.T@w
	risk = cp.quad_form(w, cov_mat)
	prob = cp.Problem(cp.Maximize(ret - 0.5*risk), [cp.sum(w) == 1, w >= 0])
	prob.solve()
	df_weights.iloc[x] = w.value


# Average duration
df_weights_ladder = apply_laddering(df_weights, min_ten, max_ten, window)

df_weights_ladder_m = df_weights_ladder.resample('BM').last()
df_yields_m = df_yields.resample('BM').last().fillna(method='ffill')

# Calculate PnL
pl_tm = (df_weights_ladder_m.shift(1) * df_yields_m).sum(axis=1)
#pl_tm_0 = (df_weights_m.shift(1) * df_yields_m).sum(axis=1)

# Calculate benchmark weights
df_bmark_weights = pd.DataFrame(index=df_weights_ladder_m.index, columns=df_weights_ladder_m.columns)
count = 5
for x in range(len(df_bmark_weights)):
	if count == -1:
		count = 5
	df_bmark_weights.iloc[x, count] = 1
	count -= 1

pl_bm = (df_bmark_weights.shift(1) * df_yields_m).sum(axis=1)

# Calculate approximate PnL Excess
excess = pl_tm - pl_bm

# plot
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.set_title('{}: Tenor Management {}-{}M vs. 6M Benchmark'.format(ccy_pair, min_ten, max_ten))
ax1.plot(excess.cumsum(), label='Excess')
ax1.legend()
ax1.grid()
ax2 = fig.add_subplot(212, sharex=ax1)
ax2.plot(pl_tm.cumsum(), label='Tenor Management')
ax2.plot(pl_bm.cumsum(), label='6M Benchmark')
ax2.legend()
ax2.grid()

###########################
# R test
# Check inputs / outputs between R and Py
#########################
# Spots
df_spot_R = pd.read_csv('reference/spots_R.csv', index_col=0, parse_dates=True)

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(df_spot_R['CHF BGNL Curncy'], label='R')
ax1.plot(df_spot['USDCHF BGNL curncy'], label='Py')
ax1.legend()
ax2 = fig.add_subplot(212, sharex=ax1)
ax2.plot(df_spot_R['CHF BGNL Curncy'] - df_spot['USDCHF BGNL curncy'], label='diff')
plt.show()

#  yields
df_yields_R = pd.read_csv('reference/yields_R.csv', index_col=0, parse_dates=True)
df_yields_R.columns = df_yields.columns

for col in df_yields_R.columns:
	fig = plt.figure()
	ax1 = fig.add_subplot(211)
	ax1.plot(df_yields_R[col], label='R')
	ax1.plot(df_yields_smooth[col], label='Py')
	ax1.legend()
	ax2 = fig.add_subplot(212, sharex=ax1)
	ax2.plot(df_yields_R[col] - df_yields_smooth[col], label='diff')
	plt.show()


# smooth yields
df_yields_smooth_R = pd.read_csv('reference/yields_smooth_R.csv', index_col=0, parse_dates=True)
df_yields_smooth_R.columns = df_yields_smooth.columns

for col in df_yields_smooth_R.columns:
	fig = plt.figure()
	ax1 = fig.add_subplot(211)
	ax1.plot(df_yields_smooth_R[col], label='R')
	ax1.plot(df_yields_smooth[col], label='Py')
	ax1.legend()
	ax2 = fig.add_subplot(212, sharex=ax1)
	ax2.plot(df_yields_smooth_R[col] - df_yields_smooth[col], label='diff')
	plt.show()


df_weights_R = pd.read_csv('reference/tenor_strategy_weights_R.csv', index_col=0, parse_dates=True)
df_weights_R.columns = df_weights.columns

for col in df_weights_R.columns:
	fig = plt.figure()
	ax1 = fig.add_subplot(211)
	ax1.plot(df_weights_R[col], label='R')
	ax1.plot(df_weights[col], label='Py')
	ax1.legend()
	ax2 = fig.add_subplot(212, sharex=ax1)
	ax2.plot(df_weights_R[col] - df_weights[col], label='diff')
	plt.show()

df_weights_m_R = pd.read_csv('reference/Target_tenor_m.csv', index_col=0, parse_dates=True)
df_weights_m_R.columns = df_weights.columns

for col in df_weights_m_R.columns:
	fig = plt.figure()
	ax1 = fig.add_subplot(211)
	ax1.plot(df_weights_m_R[col], label='R')
	ax1.plot(df_weights_ladder_m[col], label='Py')
	ax1.legend()
	ax2 = fig.add_subplot(212, sharex=ax1)
	ax2.plot(df_weights_m_R[col] - df_weights_ladder_m[col], label='diff')
	plt.show()


df_yields_m_R = pd.read_csv('reference/yields_m_R.csv', index_col=0, parse_dates=True)
df_yields_m_R.columns = df_yields_m.columns

for col in df_yields_m_R.columns:
	fig = plt.figure()
	ax1 = fig.add_subplot(211)
	ax1.plot(df_yields_m_R[col], label='R')
	ax1.plot(df_yields_m[col], label='Py')
	ax1.legend()
	ax2 = fig.add_subplot(212, sharex=ax1)
	ax2.plot(df_yields_m_R[col] - df_yields_m[col], label='diff')
	plt.show()


###########################
# Umb test
#########################

df = pd.read_csv('reference/umb_opt_check.csv', index_col=0, parse_dates=True)

expected_returns = df.mean()

cov_mat = np.matmul(df.transpose(), df) / len(df)

# https://www.kaggle.com/code/marketneutral/cvxpy-portfolio-optimization-example
w = cp.Variable(len(df.columns))
ret = expected_returns.values.T@w
risk = cp.quad_form(w, cov_mat)

prob = cp.Problem(cp.Maximize(ret - (3/2)*risk), [cp.sum(w) == 1, w >= 0])
prob.solve()


###########################
# Test first 60 day loop compare to R
###########################

start_dt = '1999-02-05'
end_dt = '1999-04-30'

spot_ret = np.log(df_spot[start_dt:end_dt]).diff().dropna()
std_dev = spot_ret.std()

term_spread = df_yields_smooth[start_dt:end_dt]

expected_returns = term_spread.mean() - np.divide(T_cost, 12)
cov_mat = term_spread.cov(min_periods=1)

# https://www.kaggle.com/code/marketneutral/cvxpy-portfolio-optimization-example
w = cp.Variable(len(term_spread.columns))
ret = expected_returns.values.T@w
risk = cp.quad_form(w, cov_mat)
prob = cp.Problem(cp.Maximize(ret - 0.5*risk), [cp.sum(w) == 1, w >= 0])
prob.solve()