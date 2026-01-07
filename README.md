# Snowflake + dbt Analytics Platform

End-to-end Data Engineering project using **dbt** and **Snowflake**, focused on analytics engineering best practices: layered modeling, data quality and documentation.

---

## Project Overview

This project demonstrates a modern analytics engineering workflow using dbt on top of Snowflake.
It covers the full lifecycle from raw data ingestion to analytics-ready dimensional models.

Key objectives:
- Apply analytics engineering best practices
- Build a clean dimensional model (facts & dimensions)
- Enforce data quality through automated tests
- Generate lineage-aware documentation with dbt Docs

---

## Data Model

The project implements a dimensional model optimized for analytics and BI use cases.

### Dimensions

- **dim_date**
  Calendar date dimension generated using a date spine, providing full daily coverage and common date attributes.

- **dim_customers**
  Customer dimension containing customer attributes such as country and active status.

### Facts

- **fct_orders**
  Order-level fact table (1 row per order) including order amount, status and customer relationship.

- **fct_orders_daily**
  Daily aggregated fact table with order counts and revenue metrics by status.

- **fct_orders_daily_by_date**
  Date-complete daily fact table built by joining `fct_orders_daily` with `dim_date`, ensuring zero-filled metrics for dates without orders.

---

## Analytics Engineering Practices

This project applies:

- Staging → Intermediate → Marts modeling layers
- Dimensional modeling (facts and dimensions)
- Data quality tests:
  - `not_null`
  - `unique`
  - `accepted_values`
  - `relationships`
- Incremental models and snapshots
- Reproducible builds with `dbt build`
- Documented lineage and metadata via dbt Docs

---

## Tech Stack

- dbt Core (v1.10)
- Snowflake
- SQL
- CSV seed data
- dbt tests and selectors
- dbt Docs (catalog and lineage)

---

## Project Structure

```text
models/
  staging/        Source cleaning and standardization
  intermediate/   Business logic transformations
  marts/          Analytics-ready tables (facts and dimensions)

seeds/            Versioned CSV seed data
snapshots/        Snapshot definitions
tests/            Data quality tests