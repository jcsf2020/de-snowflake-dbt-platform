{{ config(
    materialized = 'incremental',
    unique_key = 'customer_id',
    incremental_strategy = 'merge'
) }}
select customer_id,
    name,
    country,
    status,
    dbt_valid_from,
    dbt_valid_to
from {{ ref('customers_snapshot') }}
where dbt_valid_to is null
