{% set brew = pillar.get('brew', {}) %}
{% set brew_bin = '/opt/homebrew/bin/brew' %}
{% set console_user = grains['console_user'] %}

# -------------------------------------------------
# Homebrew taps
# -------------------------------------------------

{% for tap in brew.get('taps', []) %}

brew_tap_{{ tap | replace('/', '_') }}:
  cmd.run:
    - name: {{ brew_bin }} tap {{ tap }}
    - unless: {{ brew_bin }} tap | grep -q "^{{ tap }}$"
    - runas: {{ console_user }}

{% endfor %}

# -------------------------------------------------
# Homebrew formulae
# -------------------------------------------------

brew_formulae:
  pkg.installed:
    - pkgs:
{% for formula in brew.get('formulae', []) %}
      - {{ formula }}
{% endfor %}
    - brew_bin: {{ brew_bin }}
    - require:
{% for tap in brew.get('taps', []) %}
      - cmd: brew_tap_{{ tap | replace('/', '_') }}
{% endfor %}

# -------------------------------------------------
# Homebrew casks
# -------------------------------------------------

{% for cask in brew.get('casks', []) %}

brew_cask_{{ cask | replace('-', '_') }}:
  cmd.run:
    - name: {{ brew_bin }} install --cask {{ cask }}
    - unless: {{ brew_bin }} list --cask {{ cask }}
    - runas: {{ grains['console_user'] }}
    - require:
{% for tap in brew.get('taps', []) %}
      - cmd: brew_tap_{{ tap | replace('/', '_') }}
{% endfor %}

{% endfor %}
