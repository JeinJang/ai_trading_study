def returns(book, ticker):
  rtn = 1.0
  book['return'] = 1
  buy = 0.0
  sell = 0.0
  
  for i in book.index:
    if book.loc[i, 'trade'] == 'buy' + ticker and book.shift(1).loc[i, 'trade'] == '':
      # long 진입
      buy = book.loc[i, 'Adj Close']
      print('진입일: ', i, 'long 진입 가격: ', buy)
    elif book.loc[i, 'trade'] == 'buy' + ticker and book.shift(1).loc[i, 'trade'] == 'buy' + ticker:
      # 보유 중
      current = book.loc[i, 'Adj Close']
      rtn  = current / buy
      book.loc[i, 'return'] = rtn
    elif book.loc[i, 'trade'] == '' and book.shift(1).loc[i, 'trade'] == 'buy' + ticker:
      # long 청산
      sell = book.loc[i, 'Adj Close']
      rtn = sell / buy
      book.loc[i, 'return'] = rtn
      print("청산일 : ", i, "long 진입 가격 : ", buy, " | long 청산 가격 : ", sell, ' | return: ', round(rtn, 4))
      
    if book.loc[i, 'trade'] == '':
      buy = 0.0
      sell = 0.0
    
  acc_rtn = 1.0
  for i in book.index:
    if book.loc[i, 'trade'] == '' and book.shift(1).loc[i, 'trade'] == 'buy' + ticker:
    # long 청산 시
      rtn = book.loc[i, 'return']
      acc_rtn = acc_rtn * rtn
      book.loc[i, 'acc return'] = acc_rtn
    
  print('Accumulated return : ', round(acc_rtn, 4)) 
  return (round(acc_rtn, 4))