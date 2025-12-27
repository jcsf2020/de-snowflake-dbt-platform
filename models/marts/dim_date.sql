{{ config(materialized='table') }}

-- dim_date
-- Grain: 1 row = 1 day (date_day)
-- Purpose: calendar dimension to join facts and enable time-based analytics

with date_spine as (
  {{ dbt_utils.date_spine(
      datepart="day",
      start_date="to_date('2024-01-01')",
      end_date="to_date('2024-12-31')"
  ) }}
),

final as (
  select
    cast(date_day as date)                                         as date_day,
    year(date_day)                                                 as year,
    month(date_day)                                                as month,
    to_char(date_day, 'MMMM')                                      as month_name,
    day(date_day)                                                  as day,
    dayofweekiso(date_day)                                         as day_of_week_iso,
    to_char(date_day, 'DY')                                        as day_name_short,
    weekiso(date_day)                                              as week_of_year_iso,
    case when dayofweekiso(date_day) in (6, 7) then true else false end as is_weekend
  from date_spine
)

select * from final
