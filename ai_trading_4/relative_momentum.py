import os
import pandas as pd
import numpy as np
import datetime
import FinanceDataReader as fdr


def data_preprocessing(sample, ticker, base_date):
  sample['CODE'] = ticker # 종목 코드 추가
  sample = sample[sample['Date'] >= base_date][['Date', 'CODE', 'Adj Close']].copy()
  
  # 기준 일자 이후 데이터 사용
  sample.reset_index(inplace=True, drop=True)
  # 기준 년월
  sample['STD_YM'] = sample['Date'].map(lambda x : x.strftime('%Y-%m'))
  sample['1M_RET'] = 0.0 # 수익률 컬럼
  ym_keys = list(sample['STD_YM'].unique())
  
  return sample, ym_keys


# 거래내역 컬럼
def create_trade_book(sample, sample_codes):
  book = pd.DataFrame()
  book = sample[sample_codes].copy()
  book['STD_YM'] = book.index.map(lambda x : x.strftime('%Y-%m'))
  # book['trade'] = ''
  for c in sample_codes:
    book['p ' + c] = ''
    book['r ' + c] = ''
  return book

# 상대 모멘텀 트레이딩
def tradings(book, s_codes):
  std_ym = ''
  buy_state = False
  
  for s in s_codes:
    print(s)
    for i in book.index:
      if book.loc[i, 'p ' + s] == '' and book.shift(1).loc[i, 'p ' + s] == 'ready ' + s:
        std_ym = book.loc[i, 'STD_YM']
        buy_state = True
        
      if book.loc[i, 'p ' + s] == '' and book.loc[i, 'STD_YM'] == std_ym  and buy_state == True:    
        book.loc[i, 'p ' + s] = 'buy ' + s
      
      if book.loc[i, 'p ' + s] == '':
        std_ym = None
        buy_state = False
  
  return book


def multi_returns(book, s_codes):
  # 손익 계산
  rtn = 1.0
  buy_dict = {}
  num = len(s_codes)
  sell_dict = {}
  
  for i in book.index:
    for s in s_codes:
      if book.loc[i, 'p ' + s] == 'buy ' + s and \
        book.shift(1).loc[i, 'p ' + s] == 'ready ' + s and \
          book.shift(2).loc[i, 'p ' + s] == '': 
        # long 진입
        buy_dict[s] = book.loc[i, s]
      elif book.loc[i, 'p ' + s] == '' and book.shift(1).loc[i, 'p ' + s] == 'buy ' + s: 
        # long 청산
        sell_dict[s] = book.loc[i, s]
        # 손익 계산
        rtn = (sell_dict[s] / buy_dict[s]) - 1
        book.loc[i, 'r ' + s] = rtn
        
        print('개별 청산일 : ', i, ' 종목 코드 : ', s, 'long 진입가격 : ', buy_dict[s], ' | long 청산가격 : ', sell_dict[s], ' | return : ', round(rtn * 100, 2), '%')
    
      if book.loc[i, 'p ' + s] == '': # 제로 포지션 || long 청산
        buy_dict[s] = 0.0
        sell_dict[s] = 0.0
        
  acc_rtn = 1.0
  
  for i in book.index:
    rtn = 0.0
    count = 0
    for s in s_codes:
      if book.loc[i, 'p ' + s] == '' and book.shift(1).loc[i, 'p ' + s] == 'buy ' + s:
        # 청산, 이 때 수익률 나옴
        count += 1
        rtn += book.loc[i, 'r ' + s]
    if (rtn != 0.0) and (count != 0):
      acc_rtn *= (rtn / count) + 1
      print('누적 청산일 : ', i, '청산 종목 수 : ', count, \
        '청산 수익률 : ', round((rtn / count), 4), '누적 수익률 : ', round(acc_rtn, 4))
    #수익률 계산
    book.loc[i, 'acc_rtn'] = acc_rtn
  
  print('누적 수익률 : ', round(acc_rtn, 4))
    



################################################################

# tickers = fdr.StockListing('S&P500')
# sample = ['MMM','AOS','ABT','ABBV','ACN','ADM','ADBE','ADP','AES','AFL','A','ABNB','APD','AKAM','ALK','ALB','ARE','ALGN','ALLE','LNT','ALL','GOOGL','GOOG','MO','AMZN','AMCR','AMD','AEE','AAL','AEP','AXP','AIG','AMT','AWK','AMP','AME','AMGN','APH','ADI','ANSS','AON','APA','AAPL','AMAT','APTV','ACGL','ANET','AJG','AIZ','T','ATO','ADSK','AZO','AVB','AVY','AXON','BKR','BALL','BAC','BBWI','BAX','BDX','WRB','BRKB','BBY','BIO','TECH','BIIB','BLK','BX','BK','BA','BKNG','BWA','BXP','BSX','BMY','AVGO','BR','BRO','BFB','BG','CHRW','CDNS','CZR','CPT','CPB','COF','CAH','KMX','CCL','CARR','CTLT','CAT','CBOE','CBRE','CDW','CE','COR','CNC','CNP','CDAY','CF','CRL','SCHW','CHTR','CVX','CMG','CB','CHD','CI','CINF','CTAS','CSCO','C','CFG','CLX','CME','CMS','KO','CTSH','CL','CMCSA','CMA','CAG','COP','ED','STZ','CEG','COO','CPRT','GLW','CTVA','CSGP','COST','CTRA','CCI','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DAL','XRAY','DVN','DXCM','FANG','DLR','DFS','DIS','DG','DLTR','D','DPZ','DOV','DOW','DTE','DUK','DD','EMN','ETN','EBAY','ECL','EIX','EW','EA','ELV','LLY','EMR','ENPH','ETR','EOG','EPAM','EQT','EFX','EQIX','EQR','ESS','EL','ETSY','EG','EVRG','ES','EXC','EXPE','EXPD','EXR','XOM','FFIV','FDS','FICO','FAST','FRT','FDX','FITB','FSLR','FE','FIS','FI','FLT','FMC','F','FTNT','FTV','FOXA','FOX','BEN','FCX','GRMN','IT','GEHC','GEN','GNRC','GD','GE','GIS','GM','GPC','GILD','GL','GPN','GS','HAL','HIG','HAS','HCA','PEAK','HSIC','HSY','HES','HPE','HLT','HOLX','HD','HON','HRL','HST','HWM','HPQ','HUBB','HUM','HBAN','HII','IBM','IEX','IDXX','ITW','ILMN','INCY','IR','PODD','INTC','ICE','IFF','IP','IPG','INTU','ISRG','IVZ','INVH','IQV','IRM','JBHT','JKHY','J','JNJ','JCI','JPM','JNPR','K','KVUE','KDP','KEY','KEYS','KMB','KIM','KMI','KLAC','KHC','KR','LHX','LH','LRCX','LW','LVS','LDOS','LEN','LIN','LYV','LKQ','LMT','L','LOW','LULU','LYB','MTB','MRO','MPC','MKTX','MAR','MMC','MLM','MAS','MA','MTCH','MKC','MCD','MCK','MDT','MRK','META','MET','MTD','MGM','MCHP','MU','MSFT','MAA','MRNA','MHK','MOH','TAP','MDLZ','MPWR','MNST','MCO','MS','MOS','MSI','MSCI','NDAQ','NTAP','NFLX','NEM','NWSA','NWS','NEE','NKE','NI','NDSN','NSC','NTRS','NOC','NCLH','NRG','NUE','NVDA','NVR','NXPI','ORLY','OXY','ODFL','OMC','ON','OKE','ORCL','OTIS','PCAR','PKG','PANW','PARA','PH','PAYX','PAYC','PYPL','PNR','PEP','PFE','PCG','PM','PSX','PNW','PXD','PNC','POOL','PPG','PPL','PFG','PG','PGR','PLD','PRU','PEG','PTC','PSA','PHM','QRVO','PWR','QCOM','DGX','RL','RJF','RTX','O','REG','REGN','RF','RSG','RMD','RVTY','RHI','ROK','ROL','ROP','ROST','RCL','SPGI','CRM','SBAC','SLB','STX','SEE','SRE','NOW','SHW','SPG','SWKS','SJM','SNA','SEDG','SO','LUV','SWK','SBUX','STT','STLD','STE','SYK','SYF','SNPS','SYY','TMUS','TROW','TTWO','TPR','TRGP','TGT','TEL','TDY','TFX','TER','TSLA','TXN','TXT','TMO','TJX','TSCO','TT','TDG','TRV','TRMB','TFC','TYL','TSN','USB','UDR','ULTA','UNP','UAL','UPS','URI','UNH','UHS','VLO','VTR','VLTO','VRSN','VRSK','VZ','VRTX','VFC','VTRS','VICI','V','VMC','WAB','WBA','WMT','WBD','WM','WAT','WEC','WFC','WELL','WST','WDC','WRK','WY','WHR','WMB','WTW','GWW','WYNN','XEL','XYL','YUM','ZBRA','ZBH','ZTS','ZION',]
sample = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-A', 'LLY', 'UNH']

month_last_df = pd.DataFrame(columns=['Date', 'CODE', '1M_RET'])
stock_df = pd.DataFrame(columns=['Date', 'CODE', 'Adj Close'])

base_date = '2016-01-02'
  
for ticker in sample:
  df = fdr.DataReader(ticker)
  df['CODE'] = ticker
  df['Date'] = df.index
  
  # 1단계: 데이터 가공
  price_df, ym_keys = data_preprocessing(df, ticker, base_date=base_date)
  
  # 붙이기
  stock_df = pd.concat([stock_df, price_df.loc[:, ['Date', 'CODE', 'Adj Close']]], sort = False)
  stock_df = stock_df.reset_index(drop=True)

  
  # 월별 상대 모멘텀 계산을 위한 1개월간 수익률 계산
  for ym in ym_keys:
    m_ret = price_df.loc[price_df[price_df['STD_YM'] == ym].index[-1], 'Adj Close'] \
      / price_df.loc[price_df[price_df['STD_YM'] == ym].index[0], 'Adj Close']
    price_df.loc[price_df['STD_YM'] == ym, ['1M_RET']] = m_ret
    
    new_row = price_df.loc[price_df[price_df['STD_YM'] == ym].index[-1], ['Date', 'CODE', '1M_RET']]
    new_row_df = pd.DataFrame([new_row.values], columns=['Date', 'CODE', '1M_RET'])
    month_last_df = pd.concat([month_last_df, new_row_df], sort=False)
    

# 2단계: 상대 모멘텀 수익률로 필터링
month_ret_df = month_last_df.pivot(index='Date', columns='CODE', values='1M_RET').copy()
# 투자 종목 선택할 rank
month_ret_df = month_ret_df.rank(axis=1, ascending=False, method="max", pct=True)

# 상위 40% 안에 드는 종목들만 신호 목록
month_ret_df = month_ret_df.where(month_ret_df < 0.4, np.nan)
month_ret_df.fillna(0, inplace=True)
month_ret_df[month_ret_df != 0] = 1

stock_codes = list(stock_df['CODE'].unique())

# 3단계: 신호 목록으로 트레이딩 + 포지셔닝
sig_dict = dict()
for date in month_ret_df.index:
  # 신호가 포착된 종목 코드 읽어오기
  ticker_list = list(month_ret_df.loc[date, month_ret_df.loc[date, :] >= 1.0].index)
  # 날짜별 종목 코드 저장
  sig_dict[date] = ticker_list

stock_c_matrix = stock_df.pivot(index='Date', columns='CODE', values='Adj Close').copy()
book = create_trade_book(stock_c_matrix, list(stock_df['CODE'].unique()))


print(book)

# 포지셔닝
for date, values in sig_dict.items():
  for stock in values:
    book.loc[date, 'p ' + stock] = 'ready ' + stock
    
# 3-2 트레이딩
book = tradings(book, stock_codes)

print(book.loc['2018-03-01':'2018-06-01', ['AAPL', 'p AAPL', 'r AAPL']])

# 4단계: 수익률 계산
multi_returns(book, stock_codes)