{{ config(materialized='table') }}

-- fct_orders_daily
-- Grain: 1 row = 1 day (order_date)
-- Purpose: daily order volume + revenue KPIs (paid/refunded/cancelled)

with base as (
  select
    order_date,
    amount,
    status
  from {{ ref('fct_orders') }}
  where order_date is not null
),

agg as (
  select
    order_date,

    count(*) as total_orders,

    sum(case when status = 'paid' then 1 else 0 end) as paid_orders,
    sum(case when status = 'refunded' then 1 else 0 end) as refunded_orders,
    sum(case when status = 'cancelled' then 1 else 0 end) as cancelled_orders,

    sum(case when status = 'paid' then amount else 0 end) as revenue_paid,
    sum(case when status = 'refunded' then amount else 0 end) as amount_refunded,
    sum(case when status = 'cancelled' then amount else 0 end) as amount_cancelled

  from base
  group by 1
)

select *
from agg
order by order_date
