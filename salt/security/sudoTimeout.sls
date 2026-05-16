# -----------------------------
# Manage /etc/sudoers.d/mscp
# -----------------------------

sudoers_mscp_managed:
  file.managed:
    - name: /etc/sudoers.d/mscp
    - user: root
    - group: wheel
    - mode: '0440'
    - contents: |
        Defaults log_allowed
        Defaults timestamp_timeout=0

sudoers_validate:
  cmd.run:
    - name: /usr/sbin/visudo -c
    - onchanges:
      - file: sudoers_mscp_managed
