import sys
import pandas as pd
import numpy as np
from datetime import datetime as dt
import ccy as ccyf
from helpers.data_service import BbgReferenceDataService, BbgApiReferenceDataService
from helpers.forward_helper import pivot_pts, calc_pts_factor, calc_pivot_spt_pts
from logger import LOGGER


def get_data_ccy(ccy_pair='USDCHF', data_svc=BbgReferenceDataService()):
	"""
	For a given currency pair get the
	:param ccy_pair: currency pair to collect
	:param data_svc: data service
	:return: spot, points, outright and pts scale factor
	"""
	ccy = ccyf.currency_pair(ccy_pair[0:3] + 'USD').mkt().code
	fac = calc_pts_factor(ccy)
	df_spot = data_svc.get_spot(ccy)
	df_points = data_svc.get_points(ccy)
	df_outright = pd.DataFrame(index=df_spot.index, columns=df_points.columns)
	for col in df_outright:
		df_outright.loc[:, col] = df_points[col] / calc_pts_factor(ccy) + df_spot[df_spot.columns[0]]
	return df_spot, df_points, df_outright, fac


def get_data(ccy_pair='USDCHF', ccy_base='CHF', start_dt='20220101', pivot_usd=False, data_svc=BbgReferenceDataService()):
	"""
	Wrapper function to collect required data and ensure data is pivoted correctly
	:param ccy_pair: Market convention currency pair
	:param ccy_base: Client base currency
	:param pivot_usd: Bool to pivot to via two currencies against USD
	:param start_dt: Start date for data collection
	:param data_svc: Data service
	:return: dataframe of spots and corresponding points
	"""
	data_svc.start_dt = start_dt
	ccy_pair_f = ccyf.currency_pair(ccy_pair)
	if ccy_pair_f.code != ccy_pair:
		LOGGER.warning('Currency pair not given in market convention')
		sys.exit()

	if pivot_usd:
		# Get ccy1 vs. USD
		ccy1 = ccyf.currency_pair(ccy_pair[0:3] + 'USD').mkt().code
		df_spot1, df_points1, df_outright1, fac1 = get_data_ccy(ccy_pair=ccy1, data_svc=data_svc)

		# Get ccy2 vs. USD
		ccy2 = ccyf.currency_pair(ccy_pair[0:3] + 'USD').mkt().code
		df_spot2, df_points2, df_outright2, fac2 = get_data_ccy(ccy_pair=ccy2, data_svc=data_svc)

		# Calculate new spot and outright by pivoting
		df_spot, df_outright = calc_pivot_spt_pts(df_spot1, df_spot2, df_outright1, df_outright2, fac1, fac2, ccy1,
		                                          ccy2, ccy_pair)

	else:
		df_spot = data_svc.get_spot(ccy_pair)
		df_points = data_svc.get_points(ccy_pair.replace('USD', ''))

	# If the ccy base is not the correct order flip
	if ccy_base != ccy_pair_f.ccy2.code:
		df_spot, df_points = pivot_pts(df_spot, df_points, fac=calc_pts_factor(ccy_pair))

	return df_spot, df_points


def get_broken_pts(ccy_pair='USDCHF', ccy_base='CHF', start_dt='20220101', pivot_usd=False, data_svc=BbgReferenceDataService()):
	dt_range = pd.date_range(start='1998-12-31', end='2024-08-30', freq='BM')
	df = pd.DataFrame(index=dt_range)
	ccy1 = ccy_pair[0:3]
	ccy2 = ccy_pair[3:]
	# Create ticker spot
	df['ticker spot'] = [f'{ccy1}/{ccy2} SPOT@{df.index[x].strftime("%m%d%y")} BGNL curncy' for x in range(0, len(df))]
	df['ticker spot'][df.index >= dt.now()] = np.nan

	import pdblp
	con = pdblp.BCon(timeout=3000)
	con.start()

	test = con.ref_hist([f'{ccy1}{ccy2} BGNL Curncy'], flds='settle_dt', dates=[ix.strftime('%Y%m%d') for ix in df.index])
	test['date'] = pd.to_datetime(test['date'], format='%Y%m%d')
	test = test.set_index('date')
	df['settle_dt'] = test['value']

	df_px_mid = con.ref(list(df['ticker spot'].dropna().values), flds='px_mid')
	df_px_mid = df_px_mid.set_index('ticker')

	df = df.set_index('ticker spot')
	df['px_mid'] = df_px_mid['value']
	df['ticker spot'] = df.index
	df = df.set_index(test.index)

	# Get the forward tickers
	tenor_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	tenor_df = pd.DataFrame(index=df.index, columns=tenor_lst)
	for ix in df[df.index <= dt.now()].index:
		print(ix)
		for tenor in tenor_lst:
			dt1 = df.shift(-tenor).loc[ix, 'settle_dt'].strftime('%m%d%y')
			dt2 = ix.strftime('%m%d%y')
			ticker = '{}/{} {}x{} BGNL curncy'.format(ccy1, ccy2, dt1, dt2)
			tenor_df.loc[ix, tenor] = ticker
	tenor_df = tenor_df.dropna()
	df_open_outright = pd.DataFrame(index=tenor_df.index, columns=tenor_lst)
	for tenor in tenor_lst:
		df_open_outright_tmp = con.ref(list(tenor_df[tenor].values), flds='px_mid')
		df_open_outright_tmp = df_open_outright_tmp.set_index('ticker')
		df_open_outright = df_open_outright.set_index(tenor_df[tenor])
		df_open_outright[tenor] = df_open_outright_tmp['value']

	df_open_outright = df_open_outright.set_index(tenor_df.index)
	df_open_pts = df_open_outright.copy().set_index(tenor_df.index)
	for col in df_open_pts.columns:
		df_open_pts[col] = df_open_pts[col] - df['px_mid']
	df_open_pts = df_open_pts * 10000

	df_close_pts = df_open_outright.copy().shift(axis=1)
	df_close_pts[1] = df['px_mid']

	for col in df_close_pts.columns:
		df_close_pts[col] = df_close_pts[col] - df['px_mid']
	df_close_pts = df_close_pts * 10000

	df_pl = (df_open_pts - df_close_pts) / 10000
	for col in df_pl.columns:
		df_pl[col] = df_pl[col] / df['px_mid']

"""
dt_range = pd.date_range(start='1998-12-31', end='2024-08-30', freq='BM')
df = pd.DataFrame(index=dt_range)

# Create ticker spot
df['ticker spot'] = ['{}/{} SPOT@{} {} curncy'.format(ccy1, ccy2, df.index[x].strftime('%m%d%y'), pricer) for x in range(0, len(df))]
df['ticker spot'][df.index >= datetime.now()] = np.nan

df_settle_dt = con.ref(list(df['ticker spot'].dropna().values), flds='settle_dt')

# Slow
df['settle_dt'] = np.nan
ticker = '{}{} {} Curncy'.format(ccy1, ccy2, pricer)
for ix in df.index:
	df.loc[ix, 'settle_dt'] = con.ref(ticker, flds='settle_dt', ovrds=[('REFERENCE_DATE', ix.strftime('%Y%m%d'))]).loc[0, 'value']

# Faster
test = con.ref_hist(['{}{} {} Curncy'.format(ccy1, ccy2, pricer)], flds='settle_dt', dates=[ix.strftime('%Y%m%d') for ix in df.index])

df_settle_dt = con.ref(list(df['ticker spot'].dropna().values), flds='settle_dt')
df_settle_dt['settle_dt'] = pd.to_datetime(df_settle_dt['value'])
df_settle_dt = df_settle_dt.set_index('ticker')

df = df.set_index('ticker spot')

df['settle_dt'] = df_settle_dt['settle_dt']

df_px_mid = blp.bdp(df.index, flds=['px_mid'])
df_px_mid = con.ref(list(df.index.dropna().values), flds='px_mid')
df_px_mid = df_px_mid.set_index('ticker')
df['px_mid'] = df_px_mid['value']

df['ticker spot'] = df.index
df = df.set_index('date')


df_mid = con.ref_hist(['{}{} {} Curncy'.format(ccy1, ccy2, pricer)], flds=['PX_MID'], dates=['20220831', '20220930'])
dates = ["20160625", "20200626"]
x = con.ref_hist("AUDUSD CMPN Curncy", "PX_LAST", dates)

df_data = con.ref_hist(['{}{} {} Curncy'.format(ccy1, ccy2, pricer)], flds=['settle_dt'], dates=df.index)
df_data = df_data.set_index('date')
df_data = df_data.pivot(columns='field', values='value')

# df_data = con.ref_hist(['{}{} {} Curncy'.format(ccy1, ccy2, pricer)], flds=['PX_MID'], dates=[x.strftime('%Y%m%d') for x in df.index])
df_data = con.ref_hist(['{}{} {} Curncy'.format(ccy1, ccy2, pricer)], flds=['PX_MID'], dates=['20220831'])

df[df_data.columns] = df_data

# Get the forward tickers
tenor_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
tenor_df = pd.DataFrame(index=df.index, columns=tenor_lst)
for ix in df_data[df_data.index <= datetime.now()].index:
	for tenor in tenor_lst:
		dt1 = df.shift(-tenor).loc[ix, 'settle_dt'].strftime('%m%d%y')
		dt2 = ix.strftime('%m%d%y')
		ticker = '{}/{} {}x{} {} curncy'.format(ccy1, ccy2, dt1, dt2, pricer)
		tenor_df.loc[ix, tenor] = ticker


# Cross currency basis
# Difference between forward points and interest rate differentials for each tenor


ccy = 'USDCHF'
xxy_tickers_lst = ['SFXOQQ1 BGN Curncy', 'SFBS1 BGN Curncy', 'USDCHF BGN Curncy', 'SFSW1V3 BGN Curncy', 
'USSA1 BGN Curncy', 'CHF12M BGN Index', 'US0003M BGN Index']

df_xxy = con.bdh(xxy_tickers_lst, flds='PX_LAST', start_date=start_date, end_date='')
df_xxy = df_xxy.droplevel('field', axis=1)

df_xxy['xxy'] = (df_xxy['{} BGN Curncy'.format(ccy)] / (df_xxy['{} BGN Curncy'.format(ccy)] - df_xxy['CHF12M BGN Index']/10000) * (1 + df_xxy['USSA1 BGN Curncy']/100) - 1)
df_xxy['xxy'] = df_xxy['xxy']*100 - df_xxy['SFSW1V3 BGN Curncy']

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df_xxy['SFSW1V3 BGN Curncy']*100)
ax.plot(df_xxy['SFBS1 BGN Curncy'])
ax.plot(df_xxy['SFXOQQ1 BGN Curncy'])


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df_xxy['xxy']*100)
ax.plot(df_xxy['SFBS1 BGN Curncy'])
ax.plot(df_xxy['SFXOQQ1 BGN Curncy'])


ccy = 'EURUSD'
xxy_tickers_lst = ['EUXOQQ1 BGN Curncy', 'EUBS1 BGN Curncy', 'EURUSD BGN Curncy', 'EUSW1V3 BGN Curncy', 
'USSA1 BGN Curncy', 'USSW1 BGN Curncy', 'EUR12M BGN Index', 'US0003M BGN Index', 'USOSFR1 BGN Curncy', 'USOSFRC BGN Curncy', 'TSFR3M Index', 
'USSFVF1 BGN Curncy', 'ESTRON BGN Index', 'EONIA BGN Index', 'EESWE1 BGNL Curncy', 'SOFRRATE BGN Index', 
'EUR003M BGN Index']

df_xxy = con.bdh(xxy_tickers_lst, flds='PX_LAST', start_date=start_date, end_date='')
df_xxy = df_xxy.droplevel('field', axis=1)

# Calculate theoretical swap
# EURUSD Spot / (EURUSD Spot + 1Y EURUSD forward pts) + (1 + 1Y USD Swap) - 1
df_xxy['theoretical_swap'] = (df_xxy['{} BGN Curncy'.format(ccy)] / (df_xxy['{} BGN Curncy'.format(ccy)] + df_xxy['EUR12M BGN Index']/10000) * (1 + df_xxy['USSA1 BGN Curncy']/100) - 1)
# Compare to actual swap
df_xxy['xxy'] = df_xxy['theoretical_swap']*100 - df_xxy['EUSW1V3 BGN Curncy']

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df_xxy['USSA1 BGN Curncy'], label='USSA1 BGN Curncy')
ax.plot(df_xxy['USOSFRC BGN Curncy'], label='USOSFRC BGN Curncy')
ax.plot(df_xxy['USOSFR1 BGN Curncy'], label='USOSFR1 BGN Curncy')
ax.legend()

d = 31
d_ct = 360
pt_scale = 10000

spot = 1.0800
fwd = 1.081546
pts = spot - fwd
print(pts * pt_scale)
ir1 = 5.6369
ir2 = 3.5336

implied_spot = (spot + pts / d) * (1 + ir1/100 * d/day_count) / (1 + ir2/100 * d / d_ct)

implied_pts = (spot * (1 + ir2/100 * d/d_ct) / (1 + ir1/100 * d/d_ct) - spot) * pt_scale



fwd_theo = spot * ((1 + (ir1 * d/b)) / (1 + (ir2 * d/b)))

fwd_pts = fwd - spot 

fwd_pts_q = 15.60

eur_swap_theoretical = (spot/fwd) * (1 + ir1) - 1
eur_swap_theoretical = (fwd/spot) * (1 + ir1) - 1

ir2 - eur_swap_theoretical

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df_xxy['EUBS1 BGN Curncy'], label='EUBS1 BGN Curncy')
ax.plot(df_xxy['USSA1 BGN Curncy'], label='USSA1 BGN Curncy')
ax.plot(df_xxy['US0003M BGN Index'], label='US0003M BGN Index')
ax.plot(df_xxy['SOFRRATE Index'], label='SOFRRATE Index')
ax.plot(df_xxy['TSFR3M Index'], label='TSFR3M Index')

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df_xxy['EUR003M BGN Index'], label='EUR003M BGN Index')
ax.plot(df_xxy['US0003M BGN Index'], label='US0003M BGN Index')
ax.plot(df_xxy['EONIA BGN Index'], label='EONIA BGN Index')
ax.plot(df_xxy['EESWE1 BGNL Curncy'], label='EESWE1 BGNL Curncy')
# ax.plot(df_xxy['SOFRRATE BGN Index'], label='SOFRRATE BGN Index')

ax.legend()
ax.grid()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df_xxy['theoretical_swap']*100, label='theoretical_swap')
ax.plot(df_xxy['EUSW1V3 BGN Curncy'], label='EUSW1V3 BGN Curncy')
ax.legend()


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(df_xxy['xxy']*100)
ax.plot(df_xxy['EUBS1 BGN Curncy'])
ax.plot(df_xxy['EUXOQQ1 BGN Curncy'])

date = '2011-12-29'
print(df_xxy.loc[date])


df_xxy = con.bdh(['USSA1 Curncy'], flds='PX_MID', start_date=start_date, end_date='')



	slope = df_points['{}{}M {} curncy'.format(ccy2, str(12), pricer)] - df_points['{}{}M {} curncy'.format(ccy2, str(1),
																											pricer)]
	df_outright = pd.DataFrame(index=df_spot.index, columns=tenor_lst)
	for col in df_outright.columns:
		df_outright.loc[:, col] = (df_spot['{} {} curncy'.format(ccy, pricer)] + df_points[points_tickers_lst[col - 1]] / 10000)

	df_cash = pd.DataFrame(index=df_spot.index, columns=tenor_lst)
	for tenor in df_cash.columns:
		if tenor == 1:
			df_cash[tenor] = (df_outright[tenor] - df_spot['{} {} curncy'.format(ccy, pricer)].shift(-1)) / df_spot['{} {} curncy'.format(ccy, pricer)]
		else:
			df_cash[tenor] = (df_outright[tenor] - df_outright[tenor - 1].shift(-1)) / df_spot['{} {} curncy'.format(ccy, pricer)]
	df_cash['Spot'] = (df_spot - df_spot.shift(-1)) / df_spot

	df_port_impact = pd.DataFrame(index=df_spot.index, columns=tenor_lst)

	for tenor in df_port_impact.columns:
		df_port_impact[tenor] = df_cash[tenor] - df_cash['Spot']

	df_carry = pd.DataFrame(index=df_spot.index, columns=tenor_lst)
	for tenor in df_carry.columns:
		if tenor == 1:
			df_carry[tenor] = df_points['{}{}M {} curncy'.format(ccy2, tenor, pricer)]
		else:
			df_carry[tenor] = df_points['{}{}M {} curncy'.format(ccy2, tenor, pricer)] - df_points['{}{}M {} curncy'.format(ccy2, tenor-1, pricer)]


	df_duration = pd.DataFrame(index=df_spot.index, columns=tenor_lst)
	for tenor in df_duration.columns:
		df_duration[tenor] = df_points['{}{}M {} curncy'.format(ccy2, tenor, pricer)] - df_points['{}{}M {} curncy'.format(ccy2, tenor, pricer)].shift(-1)


	df_port_impact.cumsum().plot()
	df_port_impact.max(axis=1).cumsum().plot()
	df_port_impact.min(axis=1).cumsum().plot()


###############################
# Test pivots
###############################
import matplotlib

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

# data_svc = BbgApiReferenceDataService()
ccy_pair = 'EURJPY'
ccy_base = 'JPY'
pivot_usd = True

data_svc = BbgReferenceDataService()
ccy_pair_f = ccyf.currency_pair(ccy_pair)
if ccy_pair_f.code != ccy_pair:
	LOGGER.warning('Currency pair not given in market convention')
	sys.exit()

df_spot_o = data_svc.get_spots(ccy_pair)
df_points_o = data_svc.get_points(ccy_pair)
# df_points_o = data_svc.get_points(ccy_pair.replace('USD', ''))
if ccy_base != ccy_pair_f.ccy2.code:
	df_spot, df_points = pivot_points(df_spot_o, df_points_o, fac=calculate_points_factor(ccy_pair))

if pivot_usd:
	ccy1 = ccyf.currency_pair(ccy_pair[0:3] + 'USD').mkt().code
	fac1 = calculate_points_factor(ccy1)
	df_spot1 = data_svc.get_spots(ccy1)
	df_points1 = data_svc.get_points(ccy1)
	df_outright1 = pd.DataFrame(index=df_spot1.index, columns=df_points1.columns)
	for col in df_outright1:
		df_outright1.loc[:, col] = df_points1[col] / calculate_points_factor(ccy1) + df_spot1[df_spot1.columns[0]]

	ccy2 = ccyf.currency_pair(ccy_pair[3:] + 'USD').mkt().code
	fac2 = calculate_points_factor(ccy2)
	df_spot2 = data_svc.get_spots(ccy2)
	df_points2 = data_svc.get_points(ccy2)
	df_outright2 = pd.DataFrame(index=df_spot2.index, columns=df_points2.columns)
	for col in df_outright2:
		df_outright2.loc[:, col] = df_points2[col] / calculate_points_factor(ccy2) + df_spot2[df_spot2.columns[0]]

	df_spot = pd.DataFrame(index=df_spot1.index, columns=['{} BGNL curncy'.format(ccy_pair)])
	df_outright = pd.DataFrame(index=df_outright1.index,
	                           columns=['{}{}M BGNL curncy'.format(ccy_pair, x) for x in range(1, 13)])
	df_points = df_outright.copy()
	if ccy1[0:3] + ccy2[0:3] != ccy_pair:
		df_spot['{} BGNL curncy'.format(ccy_pair)] = df_spot1['{} BGNL curncy'.format(ccy1)] * df_spot2[
			'{} BGNL curncy'.format(ccy2)]
		for col in df_outright.columns:
			df_outright[col] = df_outright1[col.replace(ccy_pair, ccy1)] * df_outright2[col.replace(ccy_pair, ccy2)]
			df_points[col] = (df_outright[col] - df_spot['{} BGNL curncy'.format(ccy_pair)]) * min(fac1, fac2)
	else:
		df_spot['{} BGNL curncy'.format(ccy_pair)] = df_spot1['{} BGNL curncy'.format(ccy1)] / df_spot2[
			'{} BGNL curncy'.format(ccy2)]
		for col in df_outright.columns:
			df_outright[col] = df_outright1[col.replace(ccy_pair, ccy1)] / df_outright2[col.replace(ccy_pair, ccy2)]
			df_points[col] = (df_outright[col] - df_spot['{} BGNL curncy'.format(ccy_pair)]) * min(fac1, fac2)

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax1.set_title('{} BGNL BBG vs Pivot Spot'.format(ccy_pair))
ax1.plot(df_spot_o['{} BGNL curncy'.format(ccy_pair)], label='BBG Spot')
ax1.plot(df_spot['{} BGNL curncy'.format(ccy_pair)], label='USD Pivot Spot')
ax1.legend()
ax1.grid()
ax2 = fig.add_subplot(2, 1, 2)
ax2.plot(df_spot_o['{} BGNL curncy'.format(ccy_pair)] - df_spot['{} BGNL curncy'.format(ccy_pair)], label='Diff')
ax2.legend()
ax2.grid()

tenor = 3
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax1.set_title('{} BGNL BBG vs Pivot Points'.format(ccy_pair))
ax1.plot(df_points_o['{}12M BGNL curncy'.format(ccy_pair, tenor)], label='BBG Points')
ax1.plot(df_points['{}12M BGNL curncy'.format(ccy_pair, tenor)], label='USD Pivot Points')
ax1.legend()
ax1.grid()
ax2 = fig.add_subplot(2, 1, 2)
ax2.plot(
	df_points_o['{}12M BGNL curncy'.format(ccy_pair, tenor)] - df_points['{}12M BGNL curncy'.format(ccy_pair, tenor)],
	label='Diff')
ax2.legend()
ax2.grid()
"""
