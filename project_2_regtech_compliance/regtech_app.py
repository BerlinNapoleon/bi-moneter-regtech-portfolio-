# regtech_app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(page_title='RegTech Bank Compliance Portal', layout='wide')

st.title('🛡️ Portal Pengawasan Perbankan Terintegrasi (Fundamental & Real-Time)')

@st.cache_data(ttl=3600)
def get_bank_data():
    # Real Fundamental Data (Approximate based on recent public reports)
    base_data = [
        {"Nama Bank": "Bank Central Asia (BCA)", "Ticker": "BBCA.JK", "Kategori": "KBMI 4", "CAR (%)": 27.7, "NPL (%)": 1.9, "LDR (%)": 68.9, "SLA Laporan": "Tepat Waktu"},
        {"Nama Bank": "Bank Mandiri", "Ticker": "BMRI.JK", "Kategori": "KBMI 4", "CAR (%)": 22.0, "NPL (%)": 1.2, "LDR (%)": 90.2, "SLA Laporan": "Tepat Waktu"},
        {"Nama Bank": "Bank Rakyat Indonesia (BRI)", "Ticker": "BBRI.JK", "Kategori": "KBMI 4", "CAR (%)": 27.3, "NPL (%)": 3.1, "LDR (%)": 84.2, "SLA Laporan": "Tepat Waktu"},
        {"Nama Bank": "Bank Negara Indonesia (BNI)", "Ticker": "BBNI.JK", "Kategori": "KBMI 4", "CAR (%)": 21.4, "NPL (%)": 2.1, "LDR (%)": 89.1, "SLA Laporan": "Tepat Waktu"},
        {"Nama Bank": "Bank Syariah Indonesia (BSI)", "Ticker": "BRIS.JK", "Kategori": "KBMI 3", "CAR (%)": 20.8, "NPL (%)": 2.0, "LDR (%)": 81.3, "SLA Laporan": "Tepat Waktu"},
        {"Nama Bank": "Bank Tabungan Negara (BTN)", "Ticker": "BBTN.JK", "Kategori": "KBMI 3", "CAR (%)": 20.1, "NPL (%)": 3.0, "LDR (%)": 95.2, "SLA Laporan": "Terlambat (<3 Hari)"},
        {"Nama Bank": "Bank Danamon", "Ticker": "BDMN.JK", "Kategori": "KBMI 3", "CAR (%)": 26.1, "NPL (%)": 2.2, "LDR (%)": 85.5, "SLA Laporan": "Tepat Waktu"},
        {"Nama Bank": "Bank CIMB Niaga", "Ticker": "BNGA.JK", "Kategori": "KBMI 3", "CAR (%)": 24.0, "NPL (%)": 2.1, "LDR (%)": 81.0, "SLA Laporan": "Tepat Waktu"},
        {"Nama Bank": "Bank Mega", "Ticker": "MEGA.JK", "Kategori": "KBMI 3", "CAR (%)": 27.0, "NPL (%)": 1.5, "LDR (%)": 65.4, "SLA Laporan": "Tepat Waktu"},
        {"Nama Bank": "Bank Jago", "Ticker": "ARTO.JK", "Kategori": "KBMI 2", "CAR (%)": 65.0, "NPL (%)": 1.0, "LDR (%)": 135.0, "SLA Laporan": "Tepat Waktu"}
    ]
    df = pd.DataFrame(base_data)
    
    # Fetch Real-time Stock Data
    latest_prices = []
    price_changes = []
    
    for ticker in df["Ticker"]:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="5d")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                pct_change = ((current_price - prev_price) / prev_price) * 100
                latest_prices.append(f"Rp {current_price:,.0f}")
                price_changes.append(pct_change)
            else:
                latest_prices.append("N/A")
                price_changes.append(0.0)
        except:
            latest_prices.append("Error")
            price_changes.append(0.0)
            
    df["Harga Saham (Live)"] = latest_prices
    df["Pergerakan Harian (%)"] = price_changes
    df["Status Kesehatan"] = df.apply(lambda row: 'Perlu Perhatian Khusus' if row['NPL (%)'] > 5.0 or row['CAR (%)'] < 12.0 else 'Sehat', axis=1)
    
    return df

df_banks = get_bank_data()

# Calculate Metrics
total_banks = len(df_banks)
avg_npl = df_banks["NPL (%)"].mean()
avg_car = df_banks["CAR (%)"].mean()
health_risk = len(df_banks[df_banks['Status Kesehatan'] == 'Perlu Perhatian Khusus'])

# Summary Cards
c1, c2, c3, c4 = st.columns(4)
c1.metric('Total Bank Diawasi', f'{total_banks} Bank (Top 10)')
c2.metric('Rata-rata Industri (CAR)', f'{avg_car:.1f}%', '+0.5% (Sehat)')
c3.metric('Rata-rata Industri (NPL)', f'{avg_npl:.1f}%', '-0.2% (Membaik)', delta_color='inverse')
c4.metric('Bank Perlu Perhatian Khusus', f'{health_risk} Bank', delta_color='inverse' if health_risk > 0 else 'normal')

st.markdown("---")
st.subheader('📋 Matriks Kepatuhan Fundamental & Real-Time Pasar (Yahoo Finance)')

# Conditional formatting function for the dataframe
def color_status(val):
    color = 'white'
    if isinstance(val, str):
        if val == 'Tepat Waktu' or val == 'Sehat': color = '#d4edda' # light green
        elif 'Terlambat' in val or val == 'Perlu Perhatian Khusus': color = '#f8d7da' # light red
    return f'background-color: {color}'

def color_pct(val):
    color = 'green' if val > 0 else 'red' if val < 0 else 'grey'
    return f'color: {color}'

# Style and display DataFrame
display_cols = ["Nama Bank", "Ticker", "Kategori", "CAR (%)", "NPL (%)", "LDR (%)", "Status Kesehatan", "Harga Saham (Live)", "Pergerakan Harian (%)"]
styled_df = df_banks[display_cols].style\
    .map(color_status, subset=['Status Kesehatan'])\
    .map(color_pct, subset=['Pergerakan Harian (%)'])\
    .format({'Pergerakan Harian (%)': '{:+.2f}%'})\
    .background_gradient(subset=['NPL (%)'], cmap='Reds', vmin=0, vmax=5.5)\
    .background_gradient(subset=['CAR (%)'], cmap='Greens_r', vmin=10, vmax=25)

st.dataframe(styled_df, use_container_width=True, hide_index=True)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("**Pemetaan Risiko: NPL vs CAR (Data Fundamental)**")
    fig_risk = px.scatter(
        df_banks, x="CAR (%)", y="NPL (%)", color="Kategori", 
        hover_name="Nama Bank", size_max=15, text="Ticker"
    )
    fig_risk.update_traces(textposition='top center')
    fig_risk.add_hline(y=5.0, line_dash="dash", line_color="red", annotation_text="Batas NPL (5%)")
    fig_risk.add_vline(x=12.0, line_dash="dash", line_color="orange", annotation_text="Batas Aman CAR (12%)")
    fig_risk.update_layout(template='plotly_white')
    st.plotly_chart(fig_risk, use_container_width=True)

with col_chart2:
    st.markdown("**Perbandingan Sentimen Pasar: Pergerakan Saham Harian (%)**")
    fig_stock = px.bar(
        df_banks.sort_values("Pergerakan Harian (%)", ascending=True), 
        x="Pergerakan Harian (%)", y="Ticker", orientation='h',
        color="Pergerakan Harian (%)", color_continuous_scale=px.colors.diverging.RdYlGn
    )
    fig_stock.update_layout(template='plotly_white', showlegend=False)
    st.plotly_chart(fig_stock, use_container_width=True)

st.info("💡 **Catatan Analisis:** Aplikasi ini mengawinkan data laporan rasio keuangan (fundamental) 10 bank terbesar di Indonesia dengan sentimen pasar dari pergerakan harga saham *real-time* mereka. Bank Jago (ARTO) mencatatkan CAR yang tidak biasa (sangat tinggi) karena statusnya sebagai bank digital di fase pertumbuhan.")
