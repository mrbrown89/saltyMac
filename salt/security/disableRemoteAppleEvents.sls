# -----------------------------
# Disable Remote Apple Events
# -----------------------------

{% if not grains.get("salty_ci", False) %}

remote_apple_events_disabled:
  cmd.run:
    - name: /bin/launchctl disable system/com.apple.AEServer
    - unless: >
        /bin/launchctl print-disabled system |
        /usr/bin/grep -q '"com.apple.AEServer" => disabled'
    - shell: /bin/zsh

{% else %}

skip_remote_apple_events_in_ci:
  test.nop:
    - name: "Skipping Remote Apple Events hardening on GitHub Actions runner"

{% endif %}
