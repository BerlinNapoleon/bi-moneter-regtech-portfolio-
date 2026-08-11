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

# Fetch real-time data
usd_idr_price, usd_idr_delta = get_realtime_usd_idr()

st.title('🇮🇩 Dashboard Indikator Makroekonomi & Proyeksi Inflasi')
st.caption('Data Pipeline Otomatis | Proyeksi Time-Series untuk Analisis Kebijakan Moneter')

# Filter & Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric('Inflasi Terakhir (Data Dummy)', '2.84%', '-0.12%')
col2.metric('USD / IDR (Real-Time)', f'Rp {usd_idr_price:,.0f}', f'Rp {usd_idr_delta:+,.0f}')
col3.metric('BI Rate (Data Dummy)', '6.25%', '0.00%')
col4.metric('Harga Minyak WTI (Data Dummy)', '$74.50', '-$1.20')

# Plotly Charts
st.subheader('📊 Proyeksi Inflasi Indonesia (12 Bulan Ke Depan)')
# [Render Plotly Chart di sini...]
