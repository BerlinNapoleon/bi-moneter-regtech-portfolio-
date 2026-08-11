# 📊 Portfolio: Data Science & Business Intelligence (Moneter & RegTech)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![API](https://img.shields.io/badge/API_Driven-00599C?style=for-the-badge&logo=json&logoColor=white)

Selamat datang di repositori portofolio Business Intelligence (BI) dan Data Science saya. Repositori ini berisi dua aplikasi analitik interaktif yang berfokus pada sektor **Ekonomi Makro (Moneter)** dan **Kepatuhan Perbankan (RegTech)**. 

Seluruh aplikasi dibangun menggunakan Python murni dan disajikan dalam bentuk dashboard interaktif menggunakan **Streamlit**.

---

## 🚀 Live Demo Dashboards

Anda dapat langsung mencoba dan berinteraksi dengan dashboard secara *live* melalui tautan berikut:

1. 🌍 **[Project 1: Dashboard Makroekonomi & Proyeksi Inflasi](https://bi-macro-dashboard.streamlit.app/)**
2. 🏦 **[Project 2: Portal RegTech & Pengawasan Perbankan](https://regtechberlin.streamlit.app/)**

---

## 📂 Ringkasan Proyek

### 1. Project 1: Dashboard Makroekonomi Indonesia
Aplikasi pemantauan indikator moneter untuk mempermudah analisis kebijakan ekonomi, mengintegrasikan data pasar global dengan data historis dalam negeri.
* **Fitur Utama:**
  * Metrik Real-Time untuk pergerakan nilai tukar **USD/IDR** dan Harga Minyak Dunia (**WTI Crude Oil**).
  * Data Inflasi historis dan terbaru Indonesia.
  * Grafik interaktif (*time-series*) yang memungkinkan pengguna melihat tren jangka panjang.
* **Sumber Data (API-Driven):**
  * `yfinance`: Menarik pergerakan harga komoditas dan valuta asing (Forex) secara langsung.
  * `World Bank API`: Menarik data makro (Inflasi/CPI) Indonesia secara dinamis tanpa intervensi manual.

### 2. Project 2: Portal RegTech (Regulatory Technology)
Dashboard simulasi pengawasan perbankan yang mengawinkan data laporan keuangan riil dari **Top 10 Bank di Indonesia** dengan sentimen pergerakan pasar saham mereka secara *real-time*.
* **Fitur Utama:**
  * **Matriks Kepatuhan:** Memantau indikator fundamental kesehatan bank (NPL dan CAR) berdasarkan batas regulasi Bank Indonesia / OJK (misal: NPL maks 5%, CAR batas aman 12%).
  * **Analisis Fundamental vs Sentimen:** Membandingkan posisi risiko (Scatter Plot NPL vs CAR) dengan pergerakan harian harga saham (Bar Chart).
  * *Conditional Formatting* cerdas untuk memberi peringatan (merah/hijau) secara otomatis pada bank yang melanggar batas (SLA) kepatuhan.
* **Sumber Data:**
  * Laporan Keuangan Publik Kuartalan (CAR, NPL, LDR).
  * `yfinance` (Ticker: BBCA.JK, BMRI.JK, dll) untuk Live Stock Movement.

---

## 🏗️ Arsitektur Data (Mengapa Tanpa Database?)

Anda mungkin menyadari bahwa proyek ini **tidak menggunakan SQL / NoSQL Database eksternal** secara tradisional. Arsitektur ini sengaja dirancang secara spesifik untuk kebutuhan portofolio berbasis *Cloud* dengan pendekatan **In-Memory & API-Driven Architecture**:

1. **Lightweight & Real-Time:** Data diambil langsung dari penyedia (API Yahoo Finance & World Bank) saat aplikasi dimuat.
2. **In-Memory Caching:** Untuk mengatasi *API Rate Limiting* dan memastikan performa secepat kilat, aplikasi menggunakan `@st.cache_data`. Data disimpan di dalam RAM server selama jangka waktu tertentu (misal 1 jam) sehingga 1.000 user yang mengakses dalam rentang waktu tersebut tidak akan membebani API penyedia.
3. **Production Context:** Dalam lingkungan industri/perbankan sesungguhnya (Enterprise), aliran data (ETL/ELT pipeline) pada dasbor ini akan dialihkan untuk membaca dari *Data Warehouse* (seperti BigQuery atau PostgreSQL) yang di-update setiap malam melalui *Cron Jobs*.

---

## 💻 Cara Menjalankan Secara Lokal (Local Setup)

Jika Anda ingin menjalankan atau memodifikasi kode ini di komputer Anda sendiri, ikuti langkah berikut:

1. **Clone Repositori ini:**
   ```bash
   git clone https://github.com/BerlinNapoleon/bi-moneter-regtech-portfolio-.git
   cd bi-moneter-regtech-portfolio-
   ```

2. **Install Dependensi:**
   Pastikan Anda telah menginstal Python (>=3.8). Install semua *library* yang dibutuhkan:
   ```bash
   pip install -r project_2_regtech_compliance/requirements.txt
   ```

3. **Jalankan Aplikasi:**
   *Untuk menjalankan Project 1 (Makroekonomi):*
   ```bash
   streamlit run project_1_macro_forecasting/app.py
   ```
   *Untuk menjalankan Project 2 (RegTech):*
   ```bash
   streamlit run project_2_regtech_compliance/regtech_app.py
   ```

---
*Dibuat untuk mendemonstrasikan integrasi antara Ilmu Ekonomi/Perbankan, Data Analitik, dan Rekayasa Perangkat Lunak.*