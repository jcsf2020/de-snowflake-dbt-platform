# Snowflake + dbt Analytics Platform

End-to-end Analytics Engineering project using **dbt** and **Snowflake**, showcasing modern data engineering best practices: layered modeling, data quality enforcement, historical tracking (SCD Type 2), documentation, and observability.

---

## Project Overview

This project demonstrates a production-style analytics engineering workflow built on top of Snowflake using dbt.

It covers the full lifecycle from raw data to analytics-ready dimensional models, following patterns commonly used in modern data teams and remote-first environments.

**Primary goals:**
- Apply analytics engineering best practices
- Build scalable dimensional models (facts & dimensions)
- Enforce data quality through automated testing
- Track historical changes using SCD Type 2 snapshots
- Expose execution metrics and pipeline observability

This repository is designed as a **portfolio-grade project**, aligned with real-world data engineering expectations.

---

## Data Model

The project implements a dimensional model optimized for analytics and BI use cases.

### Dimensions
- **dim_date**
  Calendar date dimension generated via a date spine.

- **dim_customers**
  Current-state customer dimension.

- **dim_customers_scd2**
  Slowly Changing Dimension (Type 2) preserving full customer history.

### Facts
- **fct_orders**
  Order-level fact table.

- **fct_orders_daily**
  Daily aggregated metrics.

- **fct_orders_daily_by_date**
  Date-complete daily metrics (zero-filled for missing days).

---

## Analytics Engineering Practices

- Layered modeling: **staging → intermediate → marts**
- Dimensional modeling
- Incremental models
- dbt snapshots (SCD Type 2)
- Data quality tests:
  - `not_null`
  - `unique`
  - `accepted_values`
  - `relationships`
- Reproducible builds with `dbt build`
- Fully documented lineage via dbt Docs

---

## Orchestration

Pipeline execution is orchestrated using **Prefect**.

Prefect is responsible for:
- Execution order
- Observability
- Retries

Transformations remain entirely inside dbt.

**Execution flow:**
1. `dbt deps`
2. `dbt build`

---

## Observability & Run Metrics

This project includes a lightweight observability layer on top of dbt runs.

After each execution, dbt artifacts are parsed to extract operational metrics.

**Sources:**
- `target/run_results.json`
- `target/manifest.json`

**Metrics produced:**
- Success / failure counts
- Execution time per node
- Resource-type breakdown (model, test, seed, snapshot)
- Top slowest nodes

---

## Metrics Output

Generated after each run:

- `orchestration/logs/metrics_latest.json`
- `orchestration/logs/metrics_latest.csv`

These files allow inspection of pipeline performance and bottlenecks.

---

## Project Structure

~~~text
models/
  staging/        Source standardization
  intermediate/   Business logic
  marts/          Analytics-ready models

seeds/            Versioned CSV seed data
snapshots/        Snapshot definitions (SCD2)
macros/           Reusable dbt macros
orchestration/    Orchestration & observability logic
~~~

---

## How to Run

```bash
dbt deps
dbt build
python orchestration/metrics_from_run_results.py
```
