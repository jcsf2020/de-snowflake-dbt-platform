Senão o GitHub **não cria as caixas com botão Copy**.

---

# SOLUÇÃO — README FINAL (APROVADO)

Abaixo está o **README corrigido**, **100% funcional**, **copiar → colar → guardar**.
Não mexas em nada.

---

## 🔒 README FINAL — COPIAR TUDO

```md
# Snowflake + dbt Analytics Platform

End-to-end Analytics Engineering project using **dbt** and **Snowflake**, showcasing modern data engineering best practices: layered modeling, data quality enforcement, historical tracking (SCD Type 2), documentation, and orchestration.

---

## Project Overview

This project demonstrates a production-style analytics engineering workflow built on top of Snowflake using dbt.
It covers the full lifecycle from source data to analytics-ready dimensional models, following patterns commonly used in modern data teams.

Key objectives of this project:

- Apply analytics engineering best practices
- Build a clean and scalable dimensional model (facts & dimensions)
- Enforce data quality through automated testing
- Track historical changes using dbt snapshots (SCD Type 2)
- Generate lineage-aware documentation with dbt Docs
- Orchestrate pipeline execution using Prefect

This repository is intended as a **portfolio project** to demonstrate real-world data engineering and analytics engineering skills.

---

## Data Model

The project implements a dimensional model optimized for analytics and BI use cases.

### Dimensions

- **dim_date**
  Calendar date dimension generated using a date spine, providing complete daily coverage and common date attributes.

- **dim_customers**
  Current-state customer dimension containing attributes such as country and active status.

- **dim_customers_scd2**
  Slowly Changing Dimension (Type 2) built from snapshot history, preserving full customer attribute history over time.

### Facts

- **fct_orders**
  Order-level fact table (one row per order) including order amount, status, and customer relationship.

- **fct_orders_daily**
  Daily aggregated fact table with order counts and revenue metrics by order status.

- **fct_orders_daily_by_date**
  Date-complete daily fact table created by joining `fct_orders_daily` with `dim_date`, ensuring zero-filled metrics for dates without orders.

---

## Analytics Engineering Practices

This project applies the following analytics engineering patterns:

- Layered modeling: **staging → intermediate → marts**
- Dimensional modeling (facts and dimensions)
- Data quality tests:
  - `not_null`
  - `unique`
  - `accepted_values`
  - `relationships`
- Incremental models for efficient processing
- dbt snapshots for historical tracking (SCD Type 2)
- Reproducible builds using `dbt build`
- Fully documented lineage and metadata using dbt Docs

---

## Orchestration

Pipeline execution is orchestrated using **Prefect**.

The orchestration layer is responsible for coordinating execution order, retries, and observability.
It does **not** perform data transformations.

Execution flow:

1. `dbt deps`
2. `dbt build`

> dbt handles transformations and testing.
> Snowflake executes the SQL.
> Prefect orchestrates the workflow.

---

## Tech Stack

- dbt Core (v1.10)
- Snowflake
- Prefect (local orchestration)
- SQL
- CSV seed data
- dbt tests and macros
- dbt Docs (catalog and lineage)

---

## Project Structure

~~~text
models/
  staging/        Source cleaning and standardization
  intermediate/   Business logic transformations
  marts/          Analytics-ready tables (facts and dimensions)

seeds/            Versioned CSV seed data
snapshots/        Snapshot definitions
macros/           Reusable SQL macros
orchestration/    Prefect flow definitions

~~~

## Observability & Run Metrics

This project includes a lightweight observability layer on top of dbt runs.

After each execution, dbt artifacts are parsed to extract operational metrics:

- Source: `target/run_results.json` and `target/manifest.json`
- Metrics extracted:
  - Success / fail / warn counts
  - Execution time per model and test
  - Top slowest nodes
  - Breakdown by resource type (models, tests, seeds, snapshots)

### Implementation

A Python script processes dbt artifacts and generates:

- `metrics_latest.json` — aggregated run metrics
- `metrics_latest.csv` — row-level execution metrics

Location:
~~~text
orchestration/metrics_from_run_results.py
orchestration/logs/
~~~
```
