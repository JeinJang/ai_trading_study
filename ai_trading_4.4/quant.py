import pandas as pd
import numpy as np
import FinanceDataReader as fdr

## with open 이용해서 filtering하기
# import csv

# line_list = []

# with open('./data/krx/per_roa.csv') as csv_file:
#   csv_reader = csv.reader(csv_file, delimiter=',')
#   for row in csv_reader:
#     if '' in row:
#       pass
#     else:
#       line_list.append(row)

# df = pd.DataFrame(line_list[1:], columns=line_list[0])

## per, roa로 sort하는 함수(per은 낮을수록 좋고, roa는 높을수록 좋음)
def sort_val(s_val, asc = True, standard = 0):
  # s_val: 정렬할 series
  # asc: 오름차순 정렬 여부
  # standard: 기준값(기본값 0)
  
  s_val_mask = s_val.mask(s_val < standard, np.nan)
  s_val_mask_rank = s_val_mask.rank(ascending = asc, na_option = 'bottom')
  
  return s_val_mask_rank

df = pd.read_csv('./data/krx/per_roa.csv')
df = df[~df.isin([np.nan, np.inf, -np.inf]).any(axis=1)]

per = pd.to_numeric(df['PER'])
roa = pd.to_numeric(df['ROA'])

per_rank = sort_val(per, asc = True, standard = 0)
roa_rank = sort_val(roa, asc = False, standard = 0)

## 합산 랭킹
result_rank = per_rank + roa_rank
result_rank = sort_val(result_rank, asc = True)
result_rank = result_rank.where(result_rank <= 20, 0) # 상위 10개 종목 선정
result_rank = result_rank.mask(result_rank > 0, 1)

mf_df = df.loc[result_rank > 0, ['Code', 'Name', 'Marcap']].copy()
mf_df['Marcap'] = round(mf_df['Marcap'] / 100000000)
mf_stock_list = df.loc[result_rank > 0, 'Code']

mf_df['2023_수익률'] = ''
# for x in mf_stock_list:
#   df = fdr.DataReader(x, '2023-01-01', '2023-11-22')
#   cum_ret = df.loc[df.index[-1], 'Close'] / df.loc[df.index[0], 'Close'] - 1
#   mf_df.loc[mf_df['Code'] == x, '2023_수익률'] = cum_ret
#   df = None


for idx, code in enumerate(mf_df['Code'].values):
  code_name = mf_df.loc[mf_df['Code'] == code, 'Name'].values[0]
  print(code, code_name)
  df = fdr.DataReader(code, '2023-01-01', '2023-11-22')
  if idx == 0:
    mf_df_rtn = pd.DataFrame(index=df.index)
  df['daily_rtn'] = df['Close'].pct_change(periods=1)
  df['cum_rtn'] = (1 + df['daily_rtn']).cumprod()
  tmp = df.loc[:, ['cum_rtn']].rename(columns={'cum_rtn': code_name})
  
  mf_df_rtn = mf_df_rtn.join(tmp, how='left')
  df = None

print(mf_df_rtn)