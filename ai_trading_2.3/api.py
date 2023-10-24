import FinanceDataReader as fdr
import matplotlib.pyplot as plt

# df_krx = fdr.StockListing('KRX')
# print(len(df_krx))
# print(df_krx.head())

# df_spx = fdr.StockListing('S&P500')
# print(df_spx)

## 가격 데이터 불러오기
df = fdr.DataReader('TSLA')
# print(df.head(10))
df['Close'].plot()
plt.show()