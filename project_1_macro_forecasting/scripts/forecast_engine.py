# scripts/forecast_engine.py
from prophet import Prophet
import pandas as pd

def run_prophet_forecast(df):
    # df harus memiliki kolom 'ds' (tanggal) dan 'y' (nilai inflasi)
    model = Prophet(interval_width=0.95, yearly_seasonality=True)
    model.fit(df)
    
    future = model.make_future_dataframe(periods=12, freq='M')
    forecast = model.predict(future)
    
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
