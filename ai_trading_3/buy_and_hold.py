import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('./data/AMZN.csv', index_col='Date', parse_dates=['Date'])
# df[df.isin([np.nan, np.inf, -np.inf]).any(axis=1)]

## 종가 기준 일간 그래프 보는 법
# from_date = '1997-01-03'
# to_date = '2003-01-03'
# price_df = df.loc[from_date:to_date, ['Adj Close']].copy()
# price_df.plot(figsize=(16,9))

# plt.show()

## 일별 수익률
# price_df = df.loc[:, ['Adj Close']].copy()
# price_df['daily_rtn'] = price_df['Adj Close'].pct_change()
# price_df['st_rtn'] = (1 + price_df['daily_rtn']).cumprod()

# price_df['st_rtn'].plot()


price_df = df.loc[:, ['Adj Close']].copy()
price_df['daily_rtn'] = price_df['Adj Close'].pct_change()
price_df['st_rtn'] = (1 + price_df['daily_rtn']).cumprod()

base_date = '2011-01-03'
tmp_df = price_df.loc[base_date:, ['st_rtn']] / price_df.loc[base_date, ['st_rtn']]
last_date = tmp_df.index[-1]
print('누적 수익: ', tmp_df.loc[last_date, 'st_rtn'])
tmp_df.plot(figsize=(16, 9))
plt.show()