import pandas as pd
import numpy as np
import datetime
import FinanceDataReader as fdr
import matplotlib.pylab as plt
from abs_momentum_return import returns

## 절대 모멘텀
ticker = 'AMZN'
df = fdr.DataReader(ticker)
price_df = df.loc[:, ['Adj Close']].copy()

price_df['STD_YM'] = price_df.index.map(lambda x : x.strftime('%Y-%m'))

month_list = price_df['STD_YM'].unique()
month_last_df = pd.DataFrame()
for m in month_list:
    month_data = price_df.loc[price_df[price_df['STD_YM'] == m].index[-1]]
    month_last_df = pd.concat([month_last_df, month_data.to_frame().T])

month_last_df.index.name = 'Date'

# data 가공
month_last_df['BF_1M_Adj_Close'] = month_last_df.shift(1)['Adj Close']
month_last_df['BF_12M_Adj_Close'] = month_last_df.shift(12)['Adj Close']
month_last_df.fillna(0, inplace=True)

# position 기록
book = price_df.copy()
book['trade'] = ''

#trading
for x in month_last_df.index:
  signal = ''
  # 절대 모멘텀
  momentum_index = month_last_df.loc[x, 'BF_1M_Adj_Close'] / month_last_df.loc[x, 'BF_12M_Adj_Close'] - 1
  # 절대 모덴텀 지표 true false
  flag =  True if ((momentum_index > 0.0) and (momentum_index != np.inf)) and (momentum_index != -np.inf) else False and True
  if flag:
    signal = 'buy' + ticker
  print('날짜: ', x, '모멘텀 인덱스: ', momentum_index, 'flag: ', flag, 'signal: ', signal)
  book.loc[x:, 'trade'] = signal

returns(book, ticker)