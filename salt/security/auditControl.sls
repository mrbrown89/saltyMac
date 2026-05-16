# -----------------------------
# Ensure audit_control exists and enforce ownership + permissions
# -----------------------------
audit_control_file:
  file.managed:
    - name: /etc/security/audit_control
    - replace: false
    - user: root
    - group: wheel
    - mode: '0440'

# Remove extended ACLs if present
audit_control_strip_acl:
  cmd.run:
    - name: /bin/chmod -N /etc/security/audit_control
    - onlyif: >
        /bin/ls -le /etc/security/audit_control |
        /usr/bin/awk 'NR > 1 { found=1 } END { exit found ? 0 : 1 }'
    - require:
      - file: audit_control_file
    - shell: /bin/zsh
