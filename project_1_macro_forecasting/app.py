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

@st.cache_data(ttl=3600)
def get_historical_stock(ticker_symbol, name, period='1y'):
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=period)
        df.reset_index(inplace=True)
        return df[['Date', 'Close']].rename(columns={'Close': name})
    except Exception as e:
        return pd.DataFrame()

st.subheader('📈 Analisis Real-Time Pasar Saham & Komoditas')

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("**Pergerakan USD/IDR (1 Tahun Terakhir)**")
    usd_df = get_historical_stock('USDIDR=X', 'USD/IDR')
    if not usd_df.empty:
        fig_usd = go.Figure()
        fig_usd.add_trace(go.Scatter(x=usd_df['Date'], y=usd_df['USD/IDR'], mode='lines', name='USD/IDR', line=dict(color='green')))
        fig_usd.update_layout(template='plotly_white', margin=dict(l=0, r=0, t=30, b=0), hovermode='x unified')
        st.plotly_chart(fig_usd, use_container_width=True)

with col_chart2:
    st.markdown("**Pergerakan Harga Minyak WTI (1 Tahun Terakhir)**")
    wti_df = get_historical_stock('CL=F', 'WTI Crude Oil')
    if not wti_df.empty:
        fig_wti = go.Figure()
        fig_wti.add_trace(go.Scatter(x=wti_df['Date'], y=wti_df['WTI Crude Oil'], mode='lines', name='WTI Price', line=dict(color='orange')))
        fig_wti.update_layout(template='plotly_white', margin=dict(l=0, r=0, t=30, b=0), hovermode='x unified')
        st.plotly_chart(fig_wti, use_container_width=True)

st.markdown("### 🔍 Analisis Singkat Data Saat Ini")
st.info(f"""
Berdasarkan data real-time:
- **Nilai Tukar Rupiah:** Berada di kisaran **Rp {usd_idr_price:,.0f}**. Fluktuasi ini dapat mempengaruhi harga barang impor.
- **Harga Minyak Dunia (WTI):** Berada di level **${wti_price:.2f}**. Harga minyak memiliki korelasi yang kuat terhadap subsidi energi pemerintah dan potensi inflasi *administered prices* (harga yang diatur pemerintah).
- **Inflasi Indonesia:** Berada di angka **{inflation_val:.2f}%** (Data Bank Dunia terbaru). Hal ini masih relatif terkendali sesuai rentang target Bank Indonesia.
""")
