import pandas as pd
import aiohttp
import asyncio
import numpy as np
import FinanceDataReader as fdr
import ssl

# 경고문 안 뜨게 하기
import warnings
warnings.filterwarnings("ignore")

# 전역 카운터
completed_tasks = 0

def on_task_done():
  global completed_tasks
  completed_tasks += 1
  print(f"Completed tasks: {completed_tasks}", end='\r')

# SSL 컨텍스트 생성
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def fetch(session, url):
  async with session.get(url) as response:
    return await response.text()

async def get_roa(session, code):
  URL = f"https://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode=A{code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=104&stkGb=701"
  r = await fetch(session, URL)
  if r.find('ROA') == -1:
    return np.nan
  df = pd.read_html(r)[0]
  df = df.iloc[:, [0, -1]]
  roa = df[df.iloc[:, 0] == 'ROA계산에 참여한 계정 펼치기']
  if not roa.empty:
    roa = roa.iloc[0, -1]
  else:
    roa = np.nan
  return roa

async def get_per(session, code):
  URL = f"https://finance.naver.com/item/main.nhn?code={code}"
  r = await fetch(session, URL)
  df = pd.read_html(r)[3]
  df = df.iloc[:, [0, -2]]
  per = df[df.iloc[:, 0] == 'PER(배)']
  if not per.empty:
    per = per.iloc[0, 1]
  else:
    per = np.nan
  return per

async def get_financials(session, code):
  roa = await get_roa(session, code)
  per = await get_per(session, code)
    
  await asyncio.sleep(1)
  on_task_done()
  return code, roa, per

async def main():
  krx_df = fdr.StockListing('KRX')
  krx_df_copy = krx_df.loc[:, ['Code', 'Name', 'Close', 'Changes', 'ChagesRatio', 'Volume', 'Marcap']]

  tasks = []
  connector = aiohttp.TCPConnector(limit=5, ssl=ssl_context)
  timeout = aiohttp.ClientTimeout(total=3600)
  async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
    for i in krx_df_copy.index:
      code = krx_df_copy.loc[i, 'Code']
      tasks.append(asyncio.ensure_future(get_financials(session, code)))

    financial_results = await asyncio.gather(*tasks)

    for result in financial_results:
      code, roa, per = result
      i = krx_df_copy.index[krx_df_copy['Code'] == code][0]
      print(i + 1, code, krx_df_copy.loc[i, 'Name'], '\nroa : ', roa, 'per : ', per)
      krx_df_copy.loc[i, 'ROA'] = roa
      krx_df_copy.loc[i, 'PER'] = per

  # Save the DataFrame to a CSV file
  krx_df_copy.to_csv('./data/krx/per_roa.csv', index=False)

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())