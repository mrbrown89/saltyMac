# -----------------------------
# Disable Remote Apple Events
# -----------------------------

remote_apple_events_disabled:
  cmd.run:
    - name: /bin/launchctl disable system/com.apple.AEServer
    - unless: >
        /bin/launchctl print-disabled system |
        /usr/bin/grep -q '"com.apple.AEServer" => disabled'
    - shell: /bin/zsh
