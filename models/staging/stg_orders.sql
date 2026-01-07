{{ config(materialized='view') }}

-- stg_orders
-- Purpose: clean + type-cast raw orders seed for downstream models
-- Grain: 1 row = 1 order (order_id)

with src as (
  select
    try_to_number(order_id)          as order_id,
    try_to_number(customer_id)       as customer_id,
    try_to_date(order_date)          as order_date,
    try_to_decimal(to_varchar(amount_eur), 10, 2)    as amount,
    lower(trim(status))              as status
  from {{ source('demo_de','orders') }}
)

select
  order_id,
  customer_id,
  order_date,
  amount,
  status
from src
where order_id is not null
