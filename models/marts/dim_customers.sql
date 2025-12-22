{{ config(materialized='table') }}

select
  customer_id,
  name,
  country
from {{ ref('int_customers') }}
