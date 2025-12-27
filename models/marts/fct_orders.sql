{{ config(materialized='table') }}

-- fct_orders
-- Grain: 1 row = 1 order (order_id)
-- Purpose: transactional facts for analytics (amounts, counts, statuses)

with orders as (
  select
    order_id,
    customer_id,
    order_date,
    amount,
    status
  from {{ ref('stg_orders') }}
),

customers as (
  select
    customer_id,
    country_code,
    is_active
  from {{ ref('dim_customers') }}
)

select
  o.order_id,
  o.customer_id,
  o.order_date,
  o.amount,
  o.status,

  -- useful slicing attributes (optional but practical)
  c.country_code,
  c.is_active

from orders o
inner join customers c
  on o.customer_id = c.customer_id

where o.order_id is not null
