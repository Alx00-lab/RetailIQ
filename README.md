# RetailIQ — End-to-End Data Engineering & Analytics Pipeline

> An end-to-end data project built on the Brazilian E-Commerce dataset (Olist), covering data ingestion, transformation, star schema modeling, and business intelligence reporting.

---

## Overview

RetailIQ is a portfolio project that simulates a real-world analytics engineering workflow. Raw transactional data is extracted from CSV files, cleaned and validated through a modular Python ETL pipeline, loaded into a SQL Server data warehouse following a star schema, and finally visualized in Power BI with DAX-powered business metrics.

The goal is to answer business questions around customer behavior, product performance, delivery efficiency, and revenue trends — across ~100K orders and ~32K products spanning 2016–2018.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data source | [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle) |
| Transformation | Python, pandas |
| Database connectivity | SQLAlchemy, pyodbc |
| Data warehouse | Microsoft SQL Server |
| BI & reporting | Power BI, DAX |
| Version control | Git, GitHub |

---

## Architecture

```
Raw CSVs (brazilian-ecommerce/)
        │
        ▼
ETL Pipeline (Python)
  ├── pipeline.py   — load, audit, clean, validate, feature engineering
  └── loader.py     — dimension preparation + SQL Server load
        │
        ▼
SQL Server — RetailIQ_db
  ├── dim_customers
  ├── dim_products
  ├── dim_orders
  ├── dim_date
  └── fact_order_items   ← star schema fact table
        │
        ▼
Power BI Dashboard
  └── DAX measures — revenue, delivery KPIs, cohort analysis
```

---

## Project Structure

```
RetailIQ/
│
├── brazilian-ecommerce/          # Raw source CSVs (not tracked in git)
│
├── ETL/
│   ├── pipeline.py               # Main ETL orchestrator
│   └── loader.py                 # Dimension preparation & DB loading
│
├── SQL Query/                    # Analytical SQL queries
│
├── Diagrams/                     # Schema diagrams & architecture visuals
│
├── requirements.txt
└── README.md
```

---

## Data Model

Star schema centered on `fact_order_items`, with four dimension tables.

```
dim_customers ◄──────────────────────────┐
  customer_unique_id (PK)                │
  customer_city, state, zip              │
                                         │
dim_products ◄──────────────────┐        │
  product_id (PK)               │        │
  category, dimensions, weight  │        │
                                │        │
dim_date ◄───────────────────┐  │        │
  DateKey (PK)               │  │        │
  Year, Month, Quarter       │  │        │
                             │  │        │
                    fact_order_items      │
                      order_id ──────────┘ → dim_orders
                      order_item_id           customer_unique_id (FK)
                      product_id (FK) ────────►
                      DateKey (FK) ───────────►
                      price, freight_value
                      seller_id
```

---

## ETL Pipeline

### pipeline.py — 7-stage orchestration

| Stage | Function | Description |
|---|---|---|
| 1 | `load_data()` | Reads all source CSVs into a dictionary of DataFrames |
| 2 | `audit_df()` | Reports shape, nulls, dtypes, and duplicates per table |
| 3 | `clean_products()` | Fills missing categories, merges English translation |
| 4 | `clean_orders()` | Parses timestamps, flags missing delivery dates |
| 5 | `validate_orders()` | Catches delivered orders with no delivery date |
| 6 | `create_features()` | Derives total order value and delivery days |
| 7 | `add_customers()` | Enriches fact data with customer_unique_id |

### loader.py — dimension loading

- Prepares each dimension: selects columns, deduplicates PKs, derives DateKey
- Guards against double-loads — skips tables that already contain data
- Loads in FK-safe order: customers → products → date → orders → fact_order_items

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- Microsoft SQL Server (local or remote)
- ODBC Driver 17 for SQL Server
- Power BI Desktop

### Installation

```bash
git clone https://github.com/your-username/RetailIQ.git
cd RetailIQ
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### Database setup

Run the SQL script in `SQL Query/` against your SQL Server instance to create the schema and populate `dim_date`.

Update the connection in `ETL/loader.py`:

```python
engine = get_engine(server="YOUR_SERVER", database="RetailIQ_db")
```

### Run the pipeline

```bash
python ETL/pipeline.py
```

---

## Dataset Overview

| Table | Rows | Description |
|---|---|---|
| orders | 99,441 | Order-level records with timestamps and status |
| order_items | 112,650 | Line items — products, prices, freight |
| products | 32,951 | Product catalogue with dimensions and category |
| customers | 99,441 | Customer location and unique identifier |
| category_translation | 71 | Portuguese → English category mapping |

Key data quality findings from audit:
- 2,965 orders missing delivery date (flagged, not dropped)
- 610 products with missing category (filled as 'Other', then translated)
- 8 orders marked delivered with no recorded delivery date (validated and reported)

---

## Status

| Phase | Status |
|---|---|
| ETL pipeline | Complete |
| SQL Server schema | Complete |
| Dimension loading | Complete |
| Analytical SQL queries | In progress |
| Power BI data model | In progress |
| DAX measures | In progress |
| Dashboard & reporting | In progress |

---

## Roadmap

- [ ] Analytical SQL queries (revenue by state, top products, delivery performance)
- [ ] Power BI data model connected to SQL Server
- [ ] DAX measures (MTD revenue, delivery SLA %, customer retention)
- [ ] Interactive Power BI dashboard
- [ ] Query performance optimization (indexes)

---

## Author

**Alexander** — Data Engineering Portfolio Project

[GitHub](https://github.com/your-username) · [LinkedIn](https://linkedin.com/in/your-profile)

---

## Data Source

Olist Brazilian E-Commerce Public Dataset, available on [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), released under CC BY-NC-SA 4.0.