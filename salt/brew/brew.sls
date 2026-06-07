{% set brew = pillar.get('brew', {}) %}
{% set brew_bin = '/opt/homebrew/bin/brew' %}
{% set console_user = grains.get('console_user', 'root') %}

# -------------------------------------------------
# Homebrew taps
# -------------------------------------------------

{% for tap in brew.get('taps', []) %}

brew_tap_{{ tap | replace('/', '_') }}:
  cmd.run:
    - name: >
        su - {{ console_user }} -c '
        eval "$({{ brew_bin }} shellenv)";
        {{ brew_bin }} tap {{ tap }}
        '
    - unless: >
        su - {{ console_user }} -c '
        eval "$({{ brew_bin }} shellenv)";
        {{ brew_bin }} tap | grep -qx "{{ tap }}"
        '

{% endfor %}

# -------------------------------------------------
# Homebrew formulae
# -------------------------------------------------

brew_formulae:
  cmd.run:
    - name: >
        su - {{ console_user }} -c '
        eval "$({{ brew_bin }} shellenv)";
        {{ brew_bin }} install {{ brew.get("formulae", []) | join(" ") }}
        '
    - unless: >
        su - {{ console_user }} -c '
        eval "$({{ brew_bin }} shellenv)";
        {{ brew_bin }} list --formula | grep -E "({{ brew.get("formulae", []) | join("|") }})"
        '

# -------------------------------------------------
# Homebrew casks
# -------------------------------------------------

{% for cask in brew.get('casks', []) %}

brew_cask_{{ cask | replace('-', '_') }}:
  cmd.run:
    - name: >
        su - {{ console_user }} -c '
        eval "$({{ brew_bin }} shellenv)";
        {{ brew_bin }} install --cask {{ cask }}
        '
    - unless: >
        su - {{ console_user }} -c '
        eval "$({{ brew_bin }} shellenv)";
        {{ brew_bin }} list --cask | grep -qx "{{ cask }}"
        '

{% endfor %}
