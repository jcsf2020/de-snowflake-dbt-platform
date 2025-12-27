{{ config(materialized='table') }}

-- dim_customers
-- Grain: 1 row = 1 customer (customer_id)
-- Purpose: customer attributes used to slice facts (who/what)

with src as (
  select
    customer_id,
    name    as customer_name,
    country as country_code,
    status,
    case when status = 'active' then true else false end as is_active
  from {{ ref('stg_customers') }}
)

select
  customer_id,
  customer_name,
  country_code,
  status,
  is_active
from src
