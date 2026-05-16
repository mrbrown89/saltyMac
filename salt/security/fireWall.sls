# -----------------------------
# Firewall Settings aka Application Layer Firewall (ALF) in Apple speak
# -----------------------------

enable_firewall:
  cmd.run:
    - name: /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
    - unless: /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate | grep -i "enabled"
    - shell: /bin/zsh

enable_stealth_mode:
  cmd.run:
    - name: /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on
    - unless: /usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode | grep -i "on"
    - shell: /bin/zsh

