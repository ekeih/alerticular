{% set alerts_firing = alerts | selectattr("status", "equalto", "firing") | list %}
{% set alerts_resolved = alerts | selectattr("status", "equalto", "resolved") | list %}

{% if alerts_resolved | length > 0 %}
  {% for alert in alerts_resolved %}
:white_check_mark: {{ alert.labels.alertname }}
    {% if alert.annotations.message is defined %}
      _{{ alert.annotations.message }}_
    {% endif %}
  {% endfor %}
{% endif %}

{% if alerts_firing | length > 0 %}
  {% for alert in alerts_firing %}
:fire: {{ alert.labels.alertname }}
    {% if alert.annotations.message is defined %}
      _{{ alert.annotations.message }}_
    {% endif %}
  {% endfor %}
{% endif %}
