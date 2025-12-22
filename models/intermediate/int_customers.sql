{{ config(materialized='view') }}

select
  customer_id,
  name,
  country,
  status
from {{ ref('stg_customers') }}
where status = 'active'
