{{ config(materialized='view') }}

select
    id
from {{ ref('stg_my_first_model') }}
