## 가격 데이터 불러오기 - S&P 500 ETF
## 볼린저 밴드
def bollinger_band(price_df, n, sigma):
  bb = price_df.copy()
  bb['center'] = price_df['Adj Close'].rolling(n).mean()
  bb['ub'] = bb['center'] + sigma * price_df['Adj Close'].rolling(n).std()
  bb['lb'] = bb['center'] - sigma * price_df['Adj Close'].rolling(n).std()
  
  return bb

# 거래내역 컬럼
def create_trade_book(sample):
  book = sample[['Adj Close']].copy()
  book['trade'] = ''
  return book
