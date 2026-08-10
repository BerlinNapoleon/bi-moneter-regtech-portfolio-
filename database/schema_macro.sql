-- Skema Tabel Makroekonomi
CREATE TABLE IF NOT EXISTS macro_indicators (
    id SERIAL PRIMARY KEY,
    record_date DATE NOT NULL UNIQUE,
    inflation_rate NUMERIC(5,2),
    bi_rate NUMERIC(5,2),
    usd_idr NUMERIC(10,2),
    crude_oil_usd NUMERIC(8,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skema Tabel Hasil Forecasting
CREATE TABLE IF NOT EXISTS inflation_forecasts (
    id SERIAL PRIMARY KEY,
    forecast_date DATE NOT NULL,
    predicted_inflation NUMERIC(5,2),
    lower_bound NUMERIC(5,2),
    upper_bound NUMERIC(5,2),
    model_used VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
