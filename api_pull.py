import pandas as pd
from pandas import DataFrame
import requests
import simplejson as json
from datetime import datetime, date


def get_data(ticker):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'

    params = {'api_key':'VEGV3MZYOH1TFOX8', 'qopts.columns':'date,close'}
    params['ticker'] = ticker
    
    today = date.today()
    start_date = today.replace(year=today.year if today.month > 1 else today.year - 1, month=today.month - 1 if today.month >1 else 12)
    print(today,start_date)
    resp = requests.get(url+'&symbol='+str(ticker)+'&outputsize=compact&apikey=VEGV3MZYOH1TFOX8')
    try:
        json = resp.json()
        df = pd.DataFrame.from_dict(json['Time Series (Daily)'],orient='index')
        df ['date'] = pd.to_datetime(df.index)
        datatable = df ['date']
        df['4. close'].astype('float')
        df.index = pd.to_datetime(df.date)
        return df['4. close'][len(df)-23:]#df[(df['date']>=start_date) & (df['date']<=today)]['4. close']
    except Exception as e:
        df = []
        return df

