# -----------------------------
# Disable SMB signing for better SMB performance
# -----------------------------

ensureNsmbConfExists:
  file.managed:
    - name: /etc/nsmb.conf
    - user: root
    - group: wheel
    - mode: '0644'
    - replace: False

disableSMBSigning:
  file.blockreplace:
    - name: /etc/nsmb.conf
    - marker_start: "# START SALT MANAGED BLOCK"
    - marker_end: "# END SALT MANAGED BLOCK"
    - content: |
        [default]
        signing_required=no
    - append_if_not_found: True
    - require:
      - file: ensureNsmbConfExists
