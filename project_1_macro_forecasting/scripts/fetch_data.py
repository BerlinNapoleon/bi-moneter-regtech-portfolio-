# scripts/fetch_data.py
import yfinance as yf
import requests
import pandas as pd
from datetime import datetime

def fetch_exchange_rate():
    ticker = yf.Ticker('USDIDR=X')
    df = ticker.history(period='1y')[['Close']].reset_index()
    df.columns = ['date', 'usd_idr']
    return df

def fetch_worldbank_inflation():
    # Indicator: FP.CPI.TOTL.ZG (Inflation, consumer prices annual %)
    url = 'http://api.worldbank.org/v2/country/IDN/indicator/FP.CPI.TOTL.ZG?format=json&date=2000:2025'
    response = requests.get(url).json()
    records = []
    for entry in response[1]:
        if entry['value'] is not None:
            records.append({'year': entry['date'], 'inflation_rate': entry['value']})
    return pd.DataFrame(records)

if __name__ == '__main__':
    print('Fetching USD/IDR Data...')
    fx_df = fetch_exchange_rate()
    print(fx_df.tail())
