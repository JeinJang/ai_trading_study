import pandas as pd

index = pd.date_range(start='2019-01-01', end='2022-01-01', freq='B')
series = pd.Series(range(len(index)), index=index)
print(series.resample(rule='MS').sum())