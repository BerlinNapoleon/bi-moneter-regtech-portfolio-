# app.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
import os

st.set_page_config(page_title='Macroeconomic & Inflation Forecasting Dashboard', layout='wide')

@st.cache_data(ttl=3600) # Cache data for 1 hour to avoid API rate limits
def get_realtime_usd_idr():
    try:
        ticker = yf.Ticker('USDIDR=X')
        # Get the latest closing price
        data = ticker.history(period='5d')
        latest_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2]
        delta = latest_price - prev_price
        return latest_price, delta
    except Exception as e:
        return 17750, 0 # Fallback default

@st.cache_data(ttl=3600)
def get_realtime_wti():
    try:
        ticker = yf.Ticker('CL=F')
        data = ticker.history(period='5d')
        latest_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2]
        delta = latest_price - prev_price
        return latest_price, delta
    except Exception as e:
        return 74.50, 0

@st.cache_data(ttl=86400) # Cache for 1 day
def get_latest_inflation():
    import requests
    try:
        url = 'https://api.worldbank.org/v2/country/IDN/indicator/FP.CPI.TOTL.ZG?format=json&date=2024:2025'
        response = requests.get(url).json()
        
        # Get the two most recent available years
        data = [entry for entry in response[1] if entry['value'] is not None]
        latest_val = data[0]['value']
        prev_val = data[1]['value']
        delta = latest_val - prev_val
        return latest_val, delta
    except Exception as e:
        return 2.84, 0

# Fetch real-time data
usd_idr_price, usd_idr_delta = get_realtime_usd_idr()
wti_price, wti_delta = get_realtime_wti()
inflation_val, inflation_delta = get_latest_inflation()

st.title('🇮🇩 Dashboard Indikator Makroekonomi & Proyeksi Inflasi')
st.caption('Data Pipeline Otomatis | Proyeksi Time-Series untuk Analisis Kebijakan Moneter')

# Filter & Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric('Inflasi Indonesia (World Bank)', f'{inflation_val:.2f}%', f'{inflation_delta:+.2f}%')
col2.metric('USD / IDR (Real-Time)', f'Rp {usd_idr_price:,.0f}', f'Rp {usd_idr_delta:+,.0f}')
col3.metric('BI Rate (BI - Static)', '6.00%', '0.00%')
col4.metric('Harga Minyak WTI (Real-Time)', f'${wti_price:.2f}', f'${wti_delta:+.2f}')

# Plotly Charts
st.subheader('📊 Historis Inflasi & Proyeksi Sederhana')

@st.cache_data(ttl=86400)
def get_historical_inflation():
    import requests
    url = 'https://api.worldbank.org/v2/country/IDN/indicator/FP.CPI.TOTL.ZG?format=json&date=2015:2025'
    response = requests.get(url).json()
    records = []
    for entry in response[1]:
        if entry['value'] is not None:
            records.append({'Tahun': entry['date'], 'Inflasi (%)': entry['value']})
    df = pd.DataFrame(records)
    df = df.sort_values('Tahun')
    return df

inflation_df = get_historical_inflation()

# Buat chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=inflation_df['Tahun'], y=inflation_df['Inflasi (%)'], mode='lines+markers', name='Inflasi Aktual', line=dict(color='blue', width=2)))

fig.update_layout(
    title='Tingkat Inflasi Tahunan Indonesia (2015 - Sekarang)',
    xaxis_title='Tahun',
    yaxis_title='Inflasi (%)',
    template='plotly_white',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)
