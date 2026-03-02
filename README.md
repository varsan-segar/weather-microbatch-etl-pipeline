# 🌦️ Weather Microbatch ETL Pipeline

An end-to-end **production-style microbatch ETL pipeline** that extracts weather data from the OpenWeather API, transforms it into analytics-ready format, and loads it into a PostgreSQL data warehouse using an idempotent, retry-safe design.

---

## 🚀 Project Overview

This project demonstrates real-world data engineering concepts including:

- API data ingestion  
- Microbatch processing (15-minute design)  
- Idempotent data loading  
- Dimension & fact table modeling  
- Exponential retry logic  
- Centralized logging  
- Transaction-safe database operations  
- Event-time vs ingestion-time modeling  

The system is built using Python and PostgreSQL and is structured to support orchestration with Airflow and containerization with Docker (planned enhancement).

---

## 🏗️ Architecture

            ┌─────────────────────┐
            │   OpenWeather API   │
            └──────────┬──────────┘
                       ↓
            ┌─────────────────────┐
            │     Extract Layer    │
            │  - Retry logic       │
            │  - Timeout handling  │
            └──────────┬──────────┘
                       ↓
            ┌─────────────────────┐
            │   Transform Layer    │
            │  - Kelvin → Celsius  │
            │  - Timestamp parsing │
            │  - Data normalization│
            └──────────┬──────────┘
                       ↓
            ┌─────────────────────┐
            │     Load Layer       │
            │  - FK resolution     │
            │  - Idempotent insert │
            │  - Conflict handling │
            └──────────┬──────────┘
                       ↓
            ┌─────────────────────┐
            │  PostgreSQL DW      │
            │  - city (dimension) │
            │  - weather (fact)   │
            └─────────────────────┘

---

## 📊 Data Model

### 🏙️ `city` (Dimension Table)

| Column | Type |
|--------|------|
| city_id | BIGINT (PK) |
| city_name | VARCHAR |
| latitude | DOUBLE PRECISION |
| longitude | DOUBLE PRECISION |

- Unique constraint on `city_name`
- Static metadata table

---

### 🌦️ `weather` (Fact Table)

| Column | Type |
|--------|------|
| weather_id | BIGINT (PK) |
| city_id | BIGINT (FK → city.city_id) |
| weather_description | VARCHAR |
| temperature_c | DOUBLE PRECISION |
| temperature_feels_like_c | DOUBLE PRECISION |
| humidity_percentage | INTEGER |
| pressure_hpa | INTEGER |
| wind_speed | DOUBLE PRECISION |
| recorded_at | TIMESTAMPTZ |
| ingested_at | TIMESTAMPTZ (DEFAULT CURRENT_TIMESTAMP) |

**Constraints**

- `UNIQUE (city_id, recorded_at)` ensures idempotency  
- Foreign key relationship enforces referential integrity  

---

## 🔁 Idempotency Design

The pipeline uses:

```sql
ON CONFLICT (city_id, recorded_at) DO NOTHING;
```

---

## 🗂️ Project Structure

```
weather-microbatch-etl-pipeline/
├── src/
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── load_cities.py
│   ├── logger_config.py
│   └── main.py
└── requirements.txt
```
---

## 🛠️ How to Run

### 1️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 2️⃣ Create .env File

```
API_KEY=your_openweather_api_key
HOST_NAME=your_host_name
DBNAME=your_dbname
PORT=your_port
USER=your_user_name
PASSWORD=your_password
```

### 3️⃣ Run the Pipeline

```
python src/main.py
```