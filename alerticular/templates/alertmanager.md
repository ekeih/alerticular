**Status: {{ status }}**
{% for alert in alerts -%}

- {{ alert.labels.alertname }}
  {% if alert.annotations.message is defined %}
  {{ alert.annotations.message }}
  {%- endif -%}

{%- endfor %}
