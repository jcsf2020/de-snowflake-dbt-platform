{{ config(materialized='table') }}

select
    id
from {{ ref('int_my_first_model') }}
