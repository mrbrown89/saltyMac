# -----------------------------
# Enable system auditing
# -----------------------------

auditd_enabled:
  cmd.run:
    - name: /bin/launchctl enable system/com.apple.auditd
    - unless: /bin/launchctl print-disabled system | /usr/bin/grep -q '"com.apple.auditd" => enabled'
    - shell: /bin/zsh

auditd_init:
  cmd.run:
    - name: /usr/sbin/audit -i
    - onchanges:
      - cmd: auditd_enabled
    - shell: /bin/zsh
