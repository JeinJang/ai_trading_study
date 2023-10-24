import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('./data/AMZN.csv', index_col='Date', parse_dates=['Date'])

price_df = df.loc[:, ['Adj Close']].copy()
price_df['daily_rtn'] = price_df['Adj Close'].pct_change()
price_df['st_rtn'] = (1 + price_df['daily_rtn']).cumprod()

# 연평균 복리 수익률 CAGR
# 기하 평균 수익률 분석(제곱으로 값을 구하는 방식)

CAGR = price_df.loc['2023-08-02', 'st_rtn'] ** (252./len(price_df.index)) - 1

# 최대 낙폭 MDD
historical_max = price_df['Adj Close'].cummax()
daily_drawdown = price_df['Adj Close'] / historical_max - 1
historical_dd = daily_drawdown.cummin()
MDD = historical_dd.min()

# 변동성 Vol
VOL = np.std(price_df['daily_rtn']) * np.sqrt(252.)

# 샤프 지수
Sharpe = np.mean(price_df['daily_rtn']) / np.std(price_df['daily_rtn']) * np.sqrt(252.)

print('CAGR: ', round(CAGR * 100, 2), '%')
print('Sharpe: ', round(Sharpe, 2))
print('VOL: ', round(VOL * 100, 2), '%')
print('MDD: ', round(-1 * MDD * 100, 2), '%')