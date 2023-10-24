import FinanceDataReader as fdr
import matplotlib.pylab as plt
from regression_to_mean import bollinger_band, create_trade_book

def tradings(sample, book): # buy 상태가 아니게 되면 팔아
  for i in sample.index:
    if sample.loc[i, 'Adj Close'] > sample.loc[i, 'ub']:
      book.loc[i, 'trade'] = ''
    elif sample.loc[i, 'lb'] > sample.loc[i, 'Adj Close']:
      if book.shift(1).loc[i, 'trade'] == 'buy':
        book.loc[i, 'trade'] = 'buy'
      else:
        book.loc[i, 'trade'] = 'buy'
    elif sample.loc[i, 'ub'] >= sample.loc[i, 'Adj Close'] and sample.loc[i, 'Adj Close'] >= sample.loc[i, 'lb']:
      if book.shift(1).loc[i, 'trade'] == 'buy':
        book.loc[i, 'trade'] = 'buy' # 매수 상태 유지
      else:
        book.loc[i, 'trade'] = ''
        
  return book

# 수익률 계산
def get_returns(book):
  rtn = 1.0
  book['return'] = 1
  buy = 0.0
  sell = 0.0
  
  for i in book.index:
    # long position
    if book.loc[i, 'trade'] == 'buy' and book.shift(1).loc[i, 'trade'] == '':
      buy = book.loc[i, 'Adj Close']
      print("진입일 : ", i, "long 진입 가격 : ", buy)
    # long 청산
    elif book.loc[i, 'trade'] == '' and book.shift(1).loc[i, 'trade'] == 'buy':
      sell = book.loc[i, 'Adj Close']
      rtn = (sell - buy) / buy + 1
      book.loc[i, 'return'] = rtn
      print("청산일 : ", i, "long 진입 가격 : ", buy, " | long 청산 가격 : ", sell, ' | return: ', round(rtn, 4))
    
    if book.loc[i, 'trade'] == '':
      buy = 0.0
      sell = 0.0
  
  acc_rtn = 1.0
  for i in book.index:
    rtn = book.loc[i, 'return']
    acc_rtn = acc_rtn * rtn
    book.loc[i, 'acc return'] = acc_rtn
  
  print('Accumulated return : ', round(acc_rtn, 4))
  
  return (round(acc_rtn, 4))
        
n = 20
sigma = 2        

df = fdr.DataReader('148020')
# 코스피 한정
df.rename(columns={'Close':'Adj Close'}, inplace=True)
price_df = df.loc[:, ['Adj Close']].copy()
bollinger = bollinger_band(price_df, n, sigma)

base_date = '2010-12-10'
sample = bollinger.loc[base_date:]
book = create_trade_book(sample)

book = tradings(sample, book)
print(get_returns(book))

book['acc return'].plot()
plt.show()

print(df)