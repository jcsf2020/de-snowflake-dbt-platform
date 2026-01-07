{% macro count_rows(model) %}
  {% set relation = ref(model) %}
  {% set sql %}
    select count(*) as total_rows from {{ relation }}
  {% endset %}

  {% set res = run_query(sql) %}

  {% if execute %}
    {% set total = res.columns[0].values()[0] %}
    {{ log("total_rows=" ~ total, info=True) }}
  {% endif %}
{% endmacro %}
