# SNOWFLAKE-DBT-LIMIT-REMOVAL-P1 — Repository Evidence Diagnostic

## Date
2026-06-06T10:04:00Z

## Git state
## proof/snowflake-dbt-limit-removal-p1
?? snowflake-dbt-limit-removal-diagnostic-2026-06-06.md

## Branch
proof/snowflake-dbt-limit-removal-p1

## Last commits
4a8989c Remove tutorial dbt models from lineage (#4)
cbb7326 docs: finalize README with CI, observability and production notes
77a46aa docs: document CI and code quality workflow
ea9eb54 ci: add GitHub Actions workflow for python syntax checks
6c03f66 feat: enrich dbt run metrics with resource type and execution time
a84a720 docs: fix README markdown code block closure
0a31b33 docs: fix README markdown blocks for proper rendering
3e63318 feat: add dbt run metrics export (run_results + manifest) (#3)

## Tracked dbt/project files
README.md
dbt_project.yml
macros/.gitkeep
macros/count_orders_by_status.sql
macros/count_paid_orders.sql
macros/count_rows.sql
models/intermediate/int_customers.sql
models/intermediate/schema.yml
models/marts/dim_customers.sql
models/marts/dim_customers_scd2.sql
models/marts/dim_date.sql
models/marts/fct_orders.sql
models/marts/fct_orders_daily.sql
models/marts/fct_orders_daily_by_date.sql
models/marts/schema.yml
models/sources/sources.yml
models/staging/schema.yml
models/staging/stg_customers.sql
models/staging/stg_orders.sql
orchestration/metrics_from_run_results.py
orchestration/prefect_flow.py
packages.yml
requirements.txt
seeds/.gitkeep
seeds/customers.csv
seeds/orders.csv
seeds/schema.yml
snapshots/.gitkeep
snapshots/customers_snapshot.sql
tests/.gitkeep

## Scaffold/tutorial indicators in tracked files

## Local target artifacts
-rw-r--r--@ 1 joaofonseca  staff   327B Jun  1 11:15 target/catalog.json
-rw-r--r--@ 1 joaofonseca  staff   786K Jun  1 14:34 target/manifest.json
-rw-r--r--@ 1 joaofonseca  staff    64K Jan 12 00:00 target/run_results.json

## dbt project config
1:name: 'de_snowflake_dbt'
3:profile: 'de_snowflake_dbt'
5:model-paths: ["models"]
7:test-paths: ["tests"]
9:macro-paths: ["macros"]
10:snapshot-paths: ["snapshots"]

## Safety
- Did not read .env.
- Did not print environment variables.
- Did not run dbt against Snowflake.
- Did not run Snowflake CLI.

## dbt parse
2026-06-06T10:04:42Z
[0m10:04:44  Running with dbt=1.10.17
[0m10:04:45  Registered adapter: snowflake=1.10.2
[0m10:04:45  Performance info: /Users/joaofonseca/projects/de-snowflake-dbt-platform/de_snowflake_dbt/target/perf_info.json
DBT_PARSE_EXIT=0

## Local dbt artifact metadata
2026-06-06T10:05:31Z
- target/manifest.json: exists=True size_bytes=804927
- target/run_results.json: exists=True size_bytes=65844
- target/catalog.json: exists=True size_bytes=327

### manifest summary
- dbt_schema_version: https://schemas.getdbt.com/dbt/manifest/v12.json
- project_name: de_snowflake_dbt
- adapter_type: snowflake
- nodes_total: 76
- sources_total: 1
- macros_total: 609
- nodes_by_type: {'model': 9, 'snapshot': 1, 'seed': 2, 'test': 64}

### run_results summary
- dbt_schema_version: https://schemas.getdbt.com/dbt/run-results/v6.json
- generated_at: 2026-01-12T00:00:49.561017Z
- results_total: 84
- statuses: {'success': 84}

## Safety
- Read local dbt artifact metadata only.
- Did not print rows/data.
- Did not read .env.
- Did not print environment variables.
- Did not connect to Snowflake.
