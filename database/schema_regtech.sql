-- Tabel Lembaga Perbankan
CREATE TABLE IF NOT EXISTS banks (
    bank_id VARCHAR(10) PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    category VARCHAR(20) CHECK (category IN ('KBMI 1', 'KBMI 2', 'KBMI 3', 'KBMI 4')),
    contact_email VARCHAR(100)
);

-- Tabel Master Regulasi & SLA
CREATE TABLE IF NOT EXISTS regulatory_rules (
    rule_id VARCHAR(10) PRIMARY KEY,
    rule_name VARCHAR(150) NOT NULL,
    frequency VARCHAR(20),
    sla_days_after_period INT
);

-- Tabel Pelaporan Regulasi
CREATE TABLE IF NOT EXISTS compliance_submissions (
    submission_id SERIAL PRIMARY KEY,
    bank_id VARCHAR(10) REFERENCES banks(bank_id),
    rule_id VARCHAR(10) REFERENCES regulatory_rules(rule_id),
    period_date DATE NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('COMPLIANT', 'NON_COMPLIANT', 'LATE_SUBMISSION', 'PENDING')),
    validation_notes TEXT,
    file_path TEXT
);
