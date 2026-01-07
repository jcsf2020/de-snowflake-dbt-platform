{% snapshot customers_snapshot %}

{{
  config(
    target_schema='SNAPSHOTS',
    unique_key='customer_id',
    strategy='check',
    check_cols=['name', 'country', 'status']
  )
}}

select
  customer_id,
  name,
  country,
  status
from {{ ref('stg_customers') }}

{% endsnapshot %}
