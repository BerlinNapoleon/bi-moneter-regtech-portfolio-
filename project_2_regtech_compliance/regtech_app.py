# regtech_app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title='RegTech Bank Compliance Portal', layout='wide')

st.title('🛡️ Portal Kepatuhan Regulasi & SLA Pengawasan Perbankan')

# Generate Dummy but realistic Data
@st.cache_data(ttl=3600)
def generate_compliance_data():
    np.random.seed(42)
    bank_names = [f"Bank {chr(65+i)} Indonesia" for i in range(15)]
    data = {
        'Nama Bank': bank_names,
        'Kategori': np.random.choice(['KBMI 1', 'KBMI 2', 'KBMI 3', 'KBMI 4'], 15),
        'CAR (%)': np.round(np.random.uniform(10.5, 25.0, 15), 2),
        'NPL (%)': np.round(np.random.uniform(0.5, 5.5, 15), 2),
        'LDR (%)': np.round(np.random.uniform(70.0, 95.0, 15), 2),
        'Status Pelaporan': np.random.choice(['Tepat Waktu', 'Terlambat (<3 Hari)', 'Terlambat (>3 Hari)'], 15, p=[0.7, 0.2, 0.1]),
    }
    df = pd.DataFrame(data)
    # CAR minimum rule is around 8% + buffer. Let's flag CAR < 12% as warning.
    # NPL maximum is 5%
    df['Status Kesehatan'] = df.apply(lambda row: 'Perlu Perhatian Khusus' if row['NPL (%)'] > 5.0 or row['CAR (%)'] < 12.0 else 'Sehat', axis=1)
    return df

df_banks = generate_compliance_data()

# Calculate Metrics
total_banks = len(df_banks)
on_time = len(df_banks[df_banks['Status Pelaporan'] == 'Tepat Waktu'])
on_time_pct = (on_time / total_banks) * 100
late_sla = len(df_banks[df_banks['Status Pelaporan'] == 'Terlambat (>3 Hari)'])
health_risk = len(df_banks[df_banks['Status Kesehatan'] == 'Perlu Perhatian Khusus'])

# Summary Cards
c1, c2, c3, c4 = st.columns(4)
c1.metric('Total Bank Terdaftar', f'{total_banks} Bank')
c2.metric('Kepatuhan Tepat Waktu', f'{on_time_pct:.1f}%', '+1.2%')
c3.metric('Laporan Terlambat (SLA Risk)', f'{late_sla} Bank', delta_color='inverse' if late_sla > 0 else 'normal')
c4.metric('Bank Perlu Perhatian Khusus', f'{health_risk} Bank', delta_color='inverse' if health_risk > 0 else 'normal')

st.markdown("---")

col_table, col_chart = st.columns([6, 4])

with col_table:
    st.subheader('📋 Matriks Status Pelaporan & Kesehatan Bank')
    
    # Conditional formatting function for the dataframe
    def color_status(val):
        color = 'white'
        if isinstance(val, str):
            if val == 'Tepat Waktu' or val == 'Sehat': color = 'green'
            elif 'Terlambat' in val or val == 'Perlu Perhatian Khusus': color = 'red'
        elif isinstance(val, float):
            pass # We will handle numeric styling below
        return f'color: {color}'

    # Custom styling
    styled_df = df_banks.style\
        .applymap(color_status, subset=['Status Pelaporan', 'Status Kesehatan'])\
        .background_gradient(subset=['NPL (%)'], cmap='Reds', vmin=0, vmax=5.5)\
        .background_gradient(subset=['CAR (%)'], cmap='Greens_r', vmin=10, vmax=25)
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

with col_chart:
    st.subheader('📊 Distribusi Kepatuhan NPL vs CAR')
    fig = px.scatter(
        df_banks, 
        x="CAR (%)", 
        y="NPL (%)", 
        color="Kategori", 
        hover_name="Nama Bank",
        symbol="Status Kesehatan",
        size_max=15,
    )
    
    # Adding warning lines
    fig.add_hline(y=5.0, line_dash="dash", line_color="red", annotation_text="Batas NPL (5%)")
    fig.add_vline(x=12.0, line_dash="dash", line_color="orange", annotation_text="Batas Aman CAR (12%)")
    
    fig.update_layout(template='plotly_white', margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

st.info("💡 **Analisis RegTech:** Bank yang berada di area kiri atas (CAR rendah, NPL tinggi) memerlukan intervensi *supervisory action* dari otoritas untuk mencegah risiko sistemik.")
