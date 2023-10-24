import pandas as pd

## date times
# print(pd.Timestamp(1239.1238934, unit='D'))
# print(pd.Timestamp('2019-1-1'))
# print(pd.to_datetime('2019-1-1 12'))
# print(pd.to_datetime(['2018-1-1', '2019-1-2']))
# print(pd.date_range('2019-01', '2019-02'))

## time spans
# print(pd.Period('2019-01'))
# print(pd.Period('2019-05-01', freq='D'))
# print(pd.period_range('2019-01', '2019-02', freq='D'))

# p = pd.Period('2019-06-13')
# test = pd.Timestamp('2019-06-13 22:11')
# print(p.start_time < test < p.end_time)

print(pd.date_range('2019-01', '2019-02', freq='B'))
print(pd.date_range('2019-01', '2019-02', freq='W'))
print(pd.date_range('2019-01', '2019-02', freq='W-MON'))