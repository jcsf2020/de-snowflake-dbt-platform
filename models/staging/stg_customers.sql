{{ config(materialized='view') }}

select
  customer_id,
  name,
  country,
  status
from {{ ref('customers') }}
