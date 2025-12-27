# Snowflake + dbt Analytics Platform

End-to-end Data Engineering project using **dbt** and **Snowflake**, focused on analytics engineering best practices: layered modeling, data quality tests and documentation.

---

## Project Overview

## Data Model

This project implements a dimensional model optimized for analytics.

### Dimensions
- **dim_date**  
  Calendar dimension generated using a date spine, providing full date coverage and attributes such as year, month, day and weekday.

- **dim_customers**  
  Customer dimension enriched with country and active status.

### Facts
- **fct_orders**  
  Order-level fact table (1 row per order) including order amount, status and customer attributes.

- **fct_orders_daily**  
  Daily aggregated fact table with order counts and revenue metrics split by order status.

- **fct_orders_daily_by_date**  
  Date-complete daily fact table built by joining `fct_orders_daily` with `dim_date`, ensuring zero-filled metrics for dates without orders.


This project demonstrates a **modern analytics stack** with:

- Staging → Intermediate → Marts data modeling
- Dimensional model (dimensions + facts)
- Data quality tests (not_null, unique, accepted_values)
- Reproducible builds and documented lineage

Designed for **portfolio, technical interviews and real-world analytics scenarios**.

---

## Tech Stack

- dbt Core (v1.10)
- Snowflake
- SQL
- CSV seeds
- dbt tests & selectors
- dbt Docs (catalog + lineage)

---

## Project Structure

models/
  staging/        Source cleaning and standardization  
  intermediate/   Business logic transformations  
  marts/          Analytics-ready tables (dimensions and facts)  

seeds/            Versioned CSV seed data  
tests/            Data quality tests  
snapshots/        Snapshot structure  

---

## How to Run

dbt run  
dbt test  
dbt build  

Generate docs:

dbt docs generate  
dbt docs serve --port 8080  

---

## Author

Joao Fonseca
