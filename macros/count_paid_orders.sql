{% macro count_paid_orders() %}
  {% set relation = ref('fct_orders') %}
  {% set sql %}
    select count(*) as paid_orders
    from {{ relation }}
    where status = 'paid'
  {% endset %}

  {% set res = run_query(sql) %}

  {% if execute %}
    {% set total = res.columns[0].values()[0] %}
    {{ log("paid_orders=" ~ total, info=True) }}
  {% endif %}
{% endmacro %}
