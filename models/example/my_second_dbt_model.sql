
-- Use the `ref` function to select from other models

select *
from {{ ref('stg_my_first_model') }}
where id = 1
