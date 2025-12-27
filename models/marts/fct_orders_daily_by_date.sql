{{ config(materialized='table') }}

-- fct_orders_daily_by_date
-- Grain: 1 row = 1 day (date_day)
-- Purpose: daily metrics with a complete calendar (includes days with 0 orders)

with d as (
  select date_day
  from {{ ref('dim_date') }}
),

o as (
  select
    order_date,
    count(*) as total_orders,
    sum(case when status = 'paid' then 1 else 0 end) as paid_orders,
    sum(case when status = 'refunded' then 1 else 0 end) as refunded_orders,
    sum(case when status = 'cancelled' then 1 else 0 end) as cancelled_orders,
    sum(case when status = 'paid' then amount else 0 end) as revenue_paid
  from {{ ref('fct_orders') }}
  group by 1
)

select
  d.date_day as order_date,
  coalesce(o.total_orders, 0) as total_orders,
  coalesce(o.paid_orders, 0) as paid_orders,
  coalesce(o.refunded_orders, 0) as refunded_orders,
  coalesce(o.cancelled_orders, 0) as cancelled_orders,
  coalesce(o.revenue_paid, 0) as revenue_paid
from d
left join o
  on d.date_day = o.order_date
