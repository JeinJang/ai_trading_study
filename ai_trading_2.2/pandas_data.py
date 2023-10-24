import pandas as pd
import numpy as np#

## 데이터 불러오기
# df = pd.read_csv('./data/TSLA.csv')
# print(df.head())

# tsla_df = pd.read_csv('./data/TSLA.csv', index_col='Date', parse_dates=['Date'])
# print(tsla_df.head())
# print(type(tsla_df.index))
# print(type(tsla_df.index[0]))

## 결측치와 이상치
# s1 = pd.Series([1, np.nan, 3, 4, 5])
# s2 = pd.Series([1, 2, np.nan, 4, 5])
# s3 = pd.Series([1, 2, 3, np.nan, 5])
# df = pd.DataFrame({
#   'S1': s1,
#   'S2': s2,
#   'S3': s3
# })

# print(df.head())
# print(df['S1'].isna())
# print(df.isna()) ## NaN 값 포함 여부 묻는 거
# print(df.isna().sum())
# print(df.isin([np.nan]))
# print(df.isnull())

# python은 na와 null을 구분하지 않아서 isna와 isnull이 똑값이 동작
# print(df.fillna(method='pad'))

# df.dropna()
# df.dropna(axis='rows')
# print(df.dropna(axis=1))

# print(tsla_df.isin([np.nan, np.inf, -np.inf]).any())

## 슬라이싱, 인덱싱, 서브셋 데이터 추출
# print(tsla_df[['Open', 'High']])
# print(tsla_df[0:3])
# print(tsla_df['2023-01-01': '2023-01-20'])

# loc 인덱스 값 기준으로 행 데이터 추출
# iloc 정수형 값으로 데이터 추출

# print(type(tsla_df.loc['2022-09-19']))
# print(tsla_df.iloc[0])
# print(tsla_df.loc['2022-09-19' : '2022-11-01', ['Open', 'High', 'Low', 'Close']])
# print(tsla_df.loc['2023-04'])

### 시계열 분석에 유용한 pandas 함수
## shift
# tsla_df['close_lag1'] = tsla_df['Close'].shift()

# ## pct_change
# tsla_df['pct_change'] = tsla_df['Close'].pct_change()

# ## diff
# tsla_df['close_diff'] = tsla_df['Close'].diff()

# ## rolling 함수
# tsla_df['MA_5'] = tsla_df['Close'].rolling(window=5).mean()
# print(tsla_df.head(15))
