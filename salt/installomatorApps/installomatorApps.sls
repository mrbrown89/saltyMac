include:
  - installomator.installomator

{% for app_id, app in pillar.get('installomator_apps', {}).items() %}

installomator_{{ app_id }}:
  installomator.managed:
    - label: {{ app.label }}
    - appName: {{ app.name }}
    - bundleId: {{ app.bundle_id }}
    - args:
{% for arg in app.get('args', []) %}
      - {{ arg }}
{% endfor %}
{% if app.get('search_paths') %}
    - searchPaths: {{ app.search_paths | tojson }}
{% endif %}
    - require:
      - file: installomator-script

{% endfor %}
